"""
iM Worker Pass - Prototype Backend (FastAPI) + Blockchain Web3

기능:
1. 발급 (W3C DID 기반 전자서명 + 블록체인 레지스트리에 keccak256 해시 등록)
2. 검증 (전자서명 위변조 검사 -> 블록체인 온체인 철회 여부 실시간 조회 -> 제출 대상 검사)
3. 관리자 (체류자격 취소 시 블록체인 revoke 트랜잭션 발생 및 온체인 즉시 거부)
"""

import base64
import json
import os
import uuid
import hashlib
import secrets
from datetime import timedelta
from datetime import datetime, timezone
from io import BytesIO

import qrcode
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from crypto_utils import sign_payload, verify_signature
from models import CredentialIssueRequest, PresentationRequest, VerifyRequest
from blockchain_client import get_blockchain_client, CredentialStatus

load_dotenv()

ISSUER_SECRET = os.environ.get("ISSUER_SECRET", "dev-only-change-me")

app = FastAPI(
    title="iM Worker Pass - Prototype API (Web3 & Blockchain)",
    version="0.2.0",
    description="외국인 근로자 분산신원인증(DID) 및 스마트 컨트랙트 상태 레지스트리 API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the reviewer HTML from the same FastAPI process for the local demo.
_frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# 로컬/시연용 인메모리 저장소 (Supabase 미설정 시에도 즉시 무중단 구동)
_local_db = {}
_presentation_sessions = {}

def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def _init_dummy_data():
    bc = get_blockchain_client()
    dummy_workers = [
        {
            "credential_id": "cred-vn-001",
            "worker_name": "NGUYEN VAN A",
            "nationality": "베트남",
            "account_bank": "iM뱅크",
            "account_number": "512-123456-01",
            "status": "valid",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "credential_id": "cred-id-002",
            "worker_name": "SITI RAHAYU",
            "nationality": "인도네시아",
            "account_bank": "iM뱅크",
            "account_number": "512-987654-02",
            "status": "valid",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]
    for w in dummy_workers:
        _local_db[w["credential_id"]] = w
        try:
            bc_res = bc.issue(w["credential_id"])
            w["tx_hash"] = bc_res["tx_hash"]
            w["explorer_url"] = bc_res["explorer_url"]
        except Exception:
            pass

_init_dummy_data()

def _get_supabase_safe():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if url and key and "xxxxxxxxxxxx" not in url:
        try:
            from supabase_client import get_supabase
            return get_supabase()
        except Exception:
            return None
    return None


@app.get("/health")
def health():
    bc = get_blockchain_client()
    return {
        "ok": True,
        "blockchain": {
            "mode": "live_testnet" if bc.is_live_network else "simulator",
            "explorer_base_url": bc.explorer_base_url
        }
    }


# ---------------------------------------------------------------------------
# S1~S4 : 자격증 발급 — 개인정보는 지갑에, 블록체인에는 고유 ID 해시와 상태(Valid)만 기록
# ---------------------------------------------------------------------------
@app.post("/credentials")
def issue_credential(req: CredentialIssueRequest):
    # A안: 이름과 계좌번호가 일치하는 근로자가 이미 존재하는지 중복 검사
    sb = _get_supabase_safe()
    if sb:
        try:
            res = (
                sb.table("credentials")
                .select("*")
                .eq("worker_name", req.worker_name)
                .eq("account_number", req.account_number)
                .limit(1)
                .execute()
            )
            if res.data:
                existing = dict(res.data[0])
                existing["is_existing"] = True
                existing["message"] = "이미 발급된 근로자입니다. 기존 자격증이 조회되었습니다."
                return existing
        except Exception:
            pass

    for existing in _local_db.values():
        if existing.get("worker_name") == req.worker_name and existing.get("account_number") == req.account_number:
            res_data = dict(existing)
            res_data["is_existing"] = True
            res_data["message"] = "이미 발급된 근로자입니다. 기존 자격증이 조회되었습니다."
            return res_data

    cid = str(uuid.uuid4())
    bc = get_blockchain_client()

    # 1. 블록체인 스마트 컨트랙트에 등록 (keccak256 해시값만 전송)
    bc_res = bc.issue(cid)

    row = {
        "credential_id": cid,
        "worker_name": req.worker_name,
        "nationality": req.nationality,
        "account_bank": req.account_bank,
        "account_number": req.account_number,
        "status": "valid",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "credential_hash": bc_res["credential_hash"],
        "tx_hash": bc_res["tx_hash"],
        "explorer_url": bc_res["explorer_url"],
        "is_existing": False,
        "message": "신규 자격증 발급 및 블록체인 등록 완료"
    }

    # Supabase 또는 로컬 DB 저장
    if sb:
        try:
            sb.table("credentials").insert(row).execute()
        except Exception as e:
            print(f"[Supabase sync error]: {e}")
    
    _local_db[cid] = row
    return row


@app.get("/credentials")
def list_credentials():
    sb = _get_supabase_safe()
    if sb:
        try:
            res = sb.table("credentials").select("*").order("created_at", desc=True).execute()
            if res.data:
                return res.data
        except Exception as e:
            print(f"[Supabase fetch error]: {e}")

    return list(_local_db.values())


# ---------------------------------------------------------------------------
# S5 : 근로자 지갑에서 "제출용 QR" 생성
# ---------------------------------------------------------------------------
@app.post("/presentations")
def create_presentation(req: PresentationRequest):
    cid = req.credential_id
    cred = None

    sb = _get_supabase_safe()
    if sb:
        try:
            res = sb.table("credentials").select("*").eq("credential_id", cid).limit(1).execute()
            if res.data:
                cred = res.data[0]
        except Exception:
            pass

    if not cred:
        cred = _local_db.get(cid)

    if not cred:
        raise HTTPException(status_code=404, detail="해당 credential_id를 찾을 수 없습니다.")

    # 서명 대상 필드 (이 중 하나라도 위변조되면 검증 실패)
    signed_fields = {
        "credential_id": cred["credential_id"],
        "worker_name": cred["worker_name"],
        "nationality": cred["nationality"],
        "account_bank": cred["account_bank"],
        "account_number": cred["account_number"],
        "target_id": req.target_id,
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
    signature = sign_payload(signed_fields, ISSUER_SECRET)
    payload = {**signed_fields, "signature": signature}

    return {
        "payload": payload,
        "qr_image_base64": _make_qr_base64(payload)
    }


def _make_qr_base64(payload: dict) -> str:
    img = qrcode.make(json.dumps(payload, ensure_ascii=False))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


# ---------------------------------------------------------------------------
# S5 secure demo flow: QR contains only a random one-time token.
# Legacy /presentations remains for backwards-compatible tests.
# ---------------------------------------------------------------------------
@app.post("/presentations/secure")
def create_secure_presentation(req: PresentationRequest):
    cred = _local_db.get(req.credential_id)
    if not cred:
        raise HTTPException(status_code=404, detail="credential not found")
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=60)
    _presentation_sessions[_token_hash(token)] = {
        "credential_id": req.credential_id,
        "target_id": req.target_id,
        "expires_at": expires_at,
        "status": "created",
    }
    payload = {"v": 1, "t": token}
    return {"qr_payload": payload, "qr_image_base64": _make_qr_base64(payload), "expires_at": expires_at.isoformat()}


@app.post("/presentations/secure/consume")
def consume_secure_presentation(req: VerifyRequest):
    raw = req.payload
    token = raw.get("t") if isinstance(raw, dict) else None
    if not isinstance(token, str):
        raise HTTPException(status_code=400, detail="token payload required")
    session = _presentation_sessions.get(_token_hash(token))
    if not session:
        raise HTTPException(status_code=404, detail="session not found")
    if session["expires_at"] <= datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="session expired")
    if session["status"] != "created":
        raise HTTPException(status_code=409, detail="session already consumed")
    if session["target_id"] != req.verifier_id:
        raise HTTPException(status_code=403, detail="target mismatch")
    session["status"] = "consumed"
    cred = _local_db.get(session["credential_id"])
    if not cred:
        raise HTTPException(status_code=404, detail="credential not found")
    status = get_blockchain_client().get_status(session["credential_id"])
    if not status["is_valid"]:
        return {"result":"fail","reason":"REVOKED","onchain_proof":status}
    return {"result":"pass","worker_name":cred["worker_name"],"nationality":cred["nationality"],"account_bank":cred["account_bank"],"account_number":cred["account_number"],"onchain_proof":status}


@app.post("/insurance/enroll")
def insurance_enroll(req: dict):
    """QR-free insurer demo: verify the selected credential on-chain, then record enrollment."""
    cid = req.get("credential_id")
    if not isinstance(cid, str):
        raise HTTPException(status_code=400, detail="credential_id required")
    cred = _local_db.get(cid)
    if not cred:
        raise HTTPException(status_code=404, detail="credential not found")
    status = get_blockchain_client().get_status(cid)
    if not status["is_valid"]:
        raise HTTPException(status_code=409, detail="credential revoked")
    return {"result":"pass","insurer_id":"insurer_1","worker_name":cred["worker_name"],"additional_documents":0,"additional_identity_checks":0,"qr_used":0,"onchain_proof":status}


# ---------------------------------------------------------------------------
# S6~S9 : 검증 — 회사/병원/보험사 스캔 시 블록체인 스마트 컨트랙트 실시간 검사
#
# 순서:
#   1) 서명 검사   -> 위변조 차단 (계좌번호 변조 등)
#   2) 블록체인 온체인 상태 검사 -> 철회 차단 (법무부 체류자격 취소)
#   3) 대상 검사   -> 오배송 차단 (다른 회사에 QR 제출)
# ---------------------------------------------------------------------------
@app.post("/verify")
def verify(req: VerifyRequest):
    payload = dict(req.payload)
    signature = payload.pop("signature", None)
    cid = payload.get("credential_id")

    # 1) 서명 무결성 검사 (1글자 위변조 시 즉시 차단)
    if not verify_signature(payload, signature, ISSUER_SECRET):
        return {
            "result": "fail",
            "reason": "SIGNATURE_INVALID",
            "message": "검사 실패: 데이터가 위변조되었거나 전자서명이 유효하지 않습니다.",
        }

    # 2) 블록체인 스마트 컨트랙트 온체인 상태 검사 (S10)
    bc = get_blockchain_client()
    bc_status = bc.get_status(cid)

    # 체인 상에서 Revoked이거나 유효하지 않은 경우
    if not bc_status["is_valid"]:
        return {
            "result": "fail",
            "reason": "REVOKED",
            "message": "검사 실패: 체류자격이 블록체인 원장에서 철회(Revoked)되었습니다.",
            "onchain_proof": bc_status
        }

    # DB 상태 추가 더블체크
    cred = _local_db.get(cid)
    if cred and cred.get("status") != "valid":
        return {
            "result": "fail",
            "reason": "REVOKED",
            "message": "검사 실패: 체류자격/자격 상태가 철회되었습니다.",
            "onchain_proof": bc_status
        }

    # 3) 제출 대상(target_id) 검사 (오배송 시연)
    if payload.get("target_id") != req.verifier_id:
        return {
            "result": "fail",
            "reason": "TARGET_MISMATCH",
            "message": f"검사 실패: 제출 대상 불일치 (제출대상: {payload.get('target_id')}, 스캐너: {req.verifier_id})",
        }

    return {
        "result": "pass",
        "message": "검사 통과 (블록체인 분산 원장 검증 완료)",
        "worker_name": payload.get("worker_name"),
        "nationality": payload.get("nationality"),
        "account_bank": payload.get("account_bank"),
        "account_number": payload.get("account_number"),
        "onchain_verified": True,
        "onchain_proof": bc_status
    }


# ---------------------------------------------------------------------------
# S9 : 관리자용 — 체류자격 철회 및 복구 시 실제 블록체인 트랜잭션 발생
# ---------------------------------------------------------------------------
@app.post("/admin/credentials/{credential_id}/revoke")
def revoke(credential_id: str):
    bc = get_blockchain_client()
    bc_res = bc.revoke(credential_id)

    if credential_id in _local_db:
        _local_db[credential_id]["status"] = "revoked"
        _local_db[credential_id]["last_tx_hash"] = bc_res["tx_hash"]
        _local_db[credential_id]["explorer_url"] = bc_res["explorer_url"]

    sb = _get_supabase_safe()
    if sb:
        try:
            sb.table("credentials").update({"status": "revoked"}).eq("credential_id", credential_id).execute()
        except Exception:
            pass

    return {
        "credential_id": credential_id,
        "status": "revoked",
        "tx_hash": bc_res["tx_hash"],
        "explorer_url": bc_res["explorer_url"],
        "message": "블록체인에 체류자격 철회 트랜잭션이 기록되었습니다."
    }


@app.post("/admin/credentials/{credential_id}/restore")
def restore(credential_id: str):
    bc = get_blockchain_client()
    bc_res = bc.restore(credential_id)

    if credential_id in _local_db:
        _local_db[credential_id]["status"] = "valid"
        _local_db[credential_id]["last_tx_hash"] = bc_res["tx_hash"]
        _local_db[credential_id]["explorer_url"] = bc_res["explorer_url"]

    sb = _get_supabase_safe()
    if sb:
        try:
            sb.table("credentials").update({"status": "valid"}).eq("credential_id", credential_id).execute()
        except Exception:
            pass

    return {
        "credential_id": credential_id,
        "status": "valid",
        "tx_hash": bc_res["tx_hash"],
        "explorer_url": bc_res["explorer_url"],
        "message": "블록체인에 체류자격 복구 트랜잭션이 기록되었습니다."
    }


if os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
