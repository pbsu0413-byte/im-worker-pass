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
from models import (
    AttendanceScanRequest,
    BankVerifyRequest,
    CredentialIssueRequest,
    InsuranceDecisionRequest,
    InsuranceSubmitRequest,
    PresentationRequest,
    VerifyRequest,
    WalletRegisterRequest,
)
import wallet as wallet_svc
import attendance as att
from blockchain_client import get_blockchain_client, CredentialStatus
from agency_api import PURPOSE_AGENCIES, coverage as agency_coverage, run_lookups

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
# 자리 3(보험)에서 가입한 사실을 기록한다.
# 카드를 지갑에 발급하지 않고, 자리 2(병원) 제출 시 여기를 조회해 보험 상태를 만든다.
_insurance_db = {}

def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def _init_dummy_data():
    """
    시연 편의를 위해 두 명은 서버 시작 시 미리 지갑을 만들어 둔다.
    나머지 인물은 wallet.html에서 은행 확인 → 지갑 발급 흐름으로 직접 만든다.
    값은 기관 시드에서 조회해 채운다 (하드코딩하지 않는다).
    """
    bc = get_blockchain_client()
    for cid, name in [("cred-vn-001", "NGUYEN VAN A"), ("cred-id-002", "SITI RAHAYU")]:
        values, log = run_lookups({"worker_name": name}, purpose="employer")
        row = {
            "credential_id": cid,
            "worker_name": name,
            "status": "valid",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "agency_lookups": log,
            "verified_by": "iM-BANK-001",
            "id_document": "여권 + 외국인등록증 대조",
        }
        row.update(values)
        row.pop("account_verified", None)
        _local_db[cid] = row
        try:
            # 실제 체인에 붙으면 재시작 때마다 같은 더미를 다시 등록하려다
            # "Credential already exists"로 revert 된다. 미등록일 때만 등록한다.
            status = bc.get_status(cid)
            row["credential_hash"] = status["credential_hash"]
            if status["status_code"] == int(CredentialStatus.NONE):
                res = bc.issue(cid)
                row["tx_hash"] = res["tx_hash"]
                row["explorer_url"] = res["explorer_url"]
                row["chain_mode"] = res.get("mode")
            else:
                row["status"] = status["status_name"]
                row["tx_hash"] = None
                row["explorer_url"] = None
                row["chain_mode"] = status["mode"]
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
# ---------------------------------------------------------------------------
# 이직(사업장 변경) 서류 대사표
#
# E-9 사업장 변경은 "고용센터 사업장변경 신청 → 구직·알선 → 새 사업장 고용허가서
# → 출입국 근무처변경허가" 순으로 진행된다. 이 중 발급기관이 서명할 수 있고
# 상태가 바뀌는 항목만 크리덴셜로 검증하고, 나머지는 원본 제출로 남긴다.
#
#   verified : 온체인 크리덴셜로 검증 완료 (수기 확인 불필요)
#   attached : 지갑에 파일로 동봉 — 검증 대상이 아니므로 담당자가 눈으로 확인
#   required : 크리덴셜로 대체 불가 — 실물 지참 또는 별도 발급 필요
# ---------------------------------------------------------------------------
_DEADLINE_DAYS = 30  # 근로계약 종료 후 1개월 이내 사업장 변경 신청


def _fmt(v, dash="—"):
    return v if v else dash


def _days_left(date_str: str | None, days: int):
    """근로계약 종료일 + days 까지 남은 일수. 계산 불가하면 None."""
    if not date_str:
        return None
    try:
        end = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None
    return (end + timedelta(days=days) - datetime.now(timezone.utc).date()).days


# 체류자격마다 이직 규정이 다르다. 이 표가 대사표의 분기 근거다.
# 규정은 제도 개정이 잦으므로 발표 자료에 수치를 박기 전 원문을 재확인할 것.
_VISA_RULES = {
    "E-9": {
        "label": "비전문취업 (고용허가제)",
        "change_rule": "사업장 변경 3회 제한 · 계약 종료 후 1개월 내 신청 · 구직기간 3개월",
        "count_limited": True,
        "deadline_days": 30,
        "search_days": 90,
    },
    "H-2": {
        "label": "방문취업 (동포 특례고용)",
        "change_rule": "특례고용 — 사업장 변경 횟수 제한 없음 · 근무개시 15일 내 신고",
        "count_limited": False,
        "deadline_days": None,
        "search_days": None,
    },
    "E-7-4": {
        "label": "숙련기능인력 (점수제)",
        "change_rule": "근무처 변경 사전허가 대상 · 최소 근무기간 또는 사용자 귀책 요건 충족 필요",
        "count_limited": False,
        "deadline_days": None,
        "search_days": None,
    },
    "F-6": {
        "label": "결혼이민",
        "change_rule": "취업활동 제한 없음 · 사업장 변경 신고 불필요",
        "count_limited": False,
        "deadline_days": None,
        "search_days": None,
    },
}


def _visa_rule(cred: dict):
    return _VISA_RULES.get(cred.get("visa_type") or "E-9", _VISA_RULES["E-9"])


def _build_job_change_dossier(cred: dict) -> dict:
    rule = _visa_rule(cred)
    notice = []

    verified = [
        {
            "name": "체류자격",
            "value": (
                f"{_fmt(cred.get('visa_type'), 'E-9')} {rule['label']} · "
                f"만료 {_fmt(cred.get('visa_valid_until'))}"
                + (f" · 상태 {cred['visa_status']}" if cred.get("visa_status") not in (None, "유효") else "")
            ),
            "issuer": "출입국·외국인청",
        },
        {
            "name": "이직 규정",
            "value": rule["change_rule"],
            "issuer": "체류자격별 적용 규정",
        },
    ]

    # 사업장 변경 횟수는 E-9에만 있는 개념이다.
    used, limit = cred.get("job_change_used"), cred.get("job_change_limit") or 3
    excluded = cred.get("job_change_excluded") or 0
    if rule["count_limited"]:
        verified.append({
            "name": "사업장 변경 이력",
            "value": (
                f"{used}/{limit}회 사용" + (f" (사용자 귀책 {excluded}건 미산입)" if excluded else "")
                if used is not None else "변경 이력 없음"
            ),
            "issuer": "고용노동부 고용센터",
        })
        if used is not None and used >= limit:
            notice.append("사업장 변경 횟수 한도 소진 — 사용자 귀책 사유 확인 필요")

    verified.append({
        "name": "고용·경력",
        "value": (
            f"{cred['employer_name']} · {_fmt(cred.get('industry'))} · "
            f"{_fmt(cred.get('employment_from'))}~{_fmt(cred.get('employment_to'))} · "
            f"{_fmt(cred.get('job_category'))}"
            if cred.get("employer_name")
            else "고용 기록 없음 (신규 입국 또는 취업 제한 없는 자격)"
        ),
        "issuer": "고용노동부 고용센터",
    })
    verified.append({
        "name": "급여계좌",
        "value": f"{_fmt(cred.get('account_bank'))} {_fmt(cred.get('account_number'))}",
        "issuer": "iM뱅크 실명확인",
    })

    # 건강진단 — 유효기간까지 본다
    hc, until = cred.get("health_check_date"), cred.get("health_check_valid_until")
    if hc:
        expired = bool(until and until < datetime.now(timezone.utc).date().isoformat())
        verified.append({
            "name": "건강진단",
            "value": (f"{hc} 실시 · {until or '유효기간 미상'}까지"
                      + (" · 기한 경과" if expired else " 유효") + " (진단 내용 비공개)"),
            "issuer": "지정 의료기관",
        })
        if expired:
            notice.append(f"건강진단 기한 경과({until}) — 입사 전 재검진 필요")
    else:
        notice.append("건강진단 기록 없음 — 입사 전 검진 필요")

    # 한국어 — 자격마다 요구되는 시험이 다르다
    if cred.get("eps_topik_score"):
        verified.append({
            "name": "한국어 (EPS-TOPIK)",
            "value": f"{cred['eps_topik_score']} · {_fmt(cred.get('eps_topik_date'))} 응시 (E-9 입국 요건)",
            "issuer": "한국산업인력공단",
        })
    if cred.get("topik_level") or cred.get("kiip_level"):
        parts = []
        if cred.get("topik_level"):
            parts.append(f"{cred['topik_level']} ({_fmt(cred.get('topik_date'))})")
        if cred.get("kiip_level"):
            parts.append(f"{cred.get('kiip_program', '사회통합프로그램')} {cred['kiip_level']}")
        verified.append({
            "name": "한국어 (TOPIK·KIIP)",
            "value": " · ".join(parts),
            "issuer": "국립국제교육원",
        })

    if cred.get("job_training_name"):
        verified.append({
            "name": "취업교육",
            "value": f"{cred['job_training_name']} {cred.get('job_training_hours', '')}시간 · {_fmt(cred.get('job_training_date'))} 이수",
            "issuer": "한국산업인력공단",
        })
    if cred.get("certificate_name"):
        verified.append({
            "name": "국가기술자격",
            "value": f"{cred['certificate_name']} ({_fmt(cred.get('certificate_grade'))}) · {_fmt(cred.get('certificate_date'))} 취득",
            "issuer": "Q-Net 한국산업인력공단",
        })
    if cred.get("safety_training_name"):
        verified.append({
            "name": "안전보건교육",
            "value": (f"{cred['safety_training_name']}"
                      + (f" {cred['safety_training_hours']}" if cred.get("safety_training_hours") else "")
                      + f" · {_fmt(cred.get('safety_training_date'))} 이수"),
            "issuer": "안전보건공단",
        })
    elif (cred.get("industry") or "") == "건설업":
        notice.append("건설업 기초안전보건교육 미이수 — 현장 투입 전 4시간 이수 필요")

    # 이 화면은 채용 사업장이 스캔하는 화면이다. 근로자가 이 회사에 내거나
    # 이 회사가 확인해야 하는 것만 서류로 세운다.
    attached = [{"name": "증명사진", "note": "인사기록카드용 · 검증 대상 아님"}]
    required = [
        {"name": "여권 · 외국인등록증", "note": "채용 시 실물 대조 (체류자격 확인 의무)"},
        {"name": "표준근로계약서", "note": "본 사업장과 새로 체결 · 서명본"},
    ]
    procedure = [
        {"name": "고용센터 사업장변경 신청", "note": "근로자 본인 · E-9 해당"} if rule["count_limited"]
        else {"name": "근무처 변경 신고·허가", "note": f"{cred.get('visa_type')} 절차에 따름"},
        {"name": "출입국 근무처변경 허가·신고", "note": "근로자 본인 · 통합신청서(별지 제34호)"},
        {"name": "고용허가서 발급", "note": "본 사업장이 고용센터에서 발급"} if rule["count_limited"]
        else {"name": "고용 신고", "note": "본 사업장 처리"},
        {"name": "4대보험 취득신고 · 고용변동 신고", "note": "입사 후 본 사업장 처리"},
    ]

    # 기한 계산은 E-9에만 적용된다.
    if rule["deadline_days"]:
        d = _days_left(cred.get("employment_to"), rule["deadline_days"])
        if d is not None:
            notice.append(
                f"사업장 변경 신청기한: 계약 종료({cred.get('employment_to')}) 후 1개월 이내 · "
                + (f"D-{d}" if d >= 0 else f"{-d}일 경과"))
    if rule["search_days"]:
        d = _days_left(cred.get("employment_to"), rule["search_days"])
        if d is not None:
            notice.append("구직기간 최대 3개월 · "
                          + (f"잔여 {d}일" if d >= 0 else f"{-d}일 경과"))

    visa_until = cred.get("visa_valid_until")
    if visa_until:
        try:
            left = (datetime.strptime(visa_until, "%Y-%m-%d").date()
                    - datetime.now(timezone.utc).date()).days
            if left < 0:
                notice.append(f"체류 만료일 경과({visa_until})")
            elif left <= 90:
                notice.append(f"체류 만료 임박 — {visa_until} · 잔여 {left}일")
        except Exception:
            pass
    if cred.get("visa_status") not in (None, "유효"):
        notice.insert(0, f"체류자격 {cred['visa_status']} — 고용할 수 없습니다")

    return {
        "visa_type": cred.get("visa_type"),
        "visa_rule": rule["change_rule"],
        "verified": verified,
        "attached": attached,
        "required": required,
        "procedure": procedure,
        "notice": notice,
        "summary": {"verified": len(verified), "attached": len(attached), "required": len(required)},
    }


@app.get("/agencies")
def list_agencies():
    """발급기관 목록과 목적별 조회 대상. 화면에서 배지 구분에 쓴다."""
    return {"agencies": agency_coverage(), "purposes": PURPOSE_AGENCIES}


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
            # 저장된 문자열이 아니라 체인에서 실제 상태를 읽어 온다 (AGENTS 규칙 16).
            try:
                chain = get_blockchain_client().get_status(existing["credential_id"])
                res_data["status"] = chain["status_name"]
                res_data["credential_hash"] = chain["credential_hash"]
                res_data["onchain_proof"] = chain
                res_data["chain_mode"] = chain["mode"]
            except Exception:
                pass
            return res_data

    cid = str(uuid.uuid4())
    bc = get_blockchain_client()

    # ── 기관 조회 (S2) ────────────────────────────────────────────
    # 목적은 employer 고정. 목적이 달라지면 묻는 기관도 달라진다(agency_api).
    agency_values, agency_log = run_lookups(
        {"worker_name": req.worker_name, "account_number": req.account_number},
        purpose="employer",
    )

    def agency(field, fallback=None):
        """요청에 직접 실린 값이 우선, 없으면 기관 조회 결과."""
        v = getattr(req, field, None)
        if v not in (None, ""):
            return v
        return agency_values.get(field, fallback)

    # 1. 블록체인 스마트 컨트랙트에 등록 (keccak256 해시값만 전송)
    bc_res = bc.issue(cid)

    row = {
        "credential_id": cid,
        "worker_name": req.worker_name,
        "nationality": req.nationality,
        "account_bank": req.account_bank,
        "account_number": req.account_number,
        "reg_no": agency("reg_no"),
        "birth_date": agency("birth_date"),
        "gender": agency("gender"),
        "visa_type": agency("visa_type", "E-9"),
        "visa_valid_until": agency("visa_valid_until"),
        "employer_name": agency("employer_name"),
        "employment_from": agency("employment_from"),
        "employment_to": agency("employment_to"),
        "job_category": agency("job_category"),
        "job_change_used": agency("job_change_used"),
        "job_change_limit": agency("job_change_limit", 3),
        "job_change_excluded": agency("job_change_excluded"),
        "health_check_date": agency("health_check_date"),
        "topik_level": agency("topik_level"),
        "agency_lookups": agency_log,
        "status": "valid",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "credential_hash": bc_res["credential_hash"],
        "tx_hash": bc_res["tx_hash"],
        "explorer_url": bc_res["explorer_url"],
        "is_existing": False,
        "chain_mode": bc_res.get("mode"),
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
# S1 : 지갑 발급 — 최초 1회
#
#   ① 은행 창구 실명확인   → 30분짜리 확인 토큰
#   ② 단말에서 키 쌍 생성  → 공개키만 서버로 (개인키는 폰 밖으로 나가지 않는다)
#   ③ 출입국 조회(필수)    → 기록이 없으면 발급 중단. 위조 등록증은 여기서 걸린다
#   ④ 나머지 기관 조회     → 없으면 빈칸으로 두고 발급은 진행
#   ⑤ 체인 등록           → 여기서만 트랜잭션이 나간다
#
# 이후 제출할 때는 체인에 아무것도 쓰지 않는다. 갱신도 마찬가지다 —
# 체인에 올라간 것은 번호의 지문이라 내용이 바뀌어도 그대로 유효하다.
# ---------------------------------------------------------------------------


@app.post("/wallet/bank-verify")
def wallet_bank_verify(req: BankVerifyRequest):
    row, err = wallet_svc.bank_verify(req.worker_name)
    if err:
        raise HTTPException(
            status_code=403,
            detail="BANK_KYC_NOT_FOUND: 창구 실명확인 기록이 없습니다. 급여계좌 개설 후 다시 시도하십시오.",
        )
    return {
        "verification_token": row["token"],
        "verified_by": row["verified_by"],
        "bank_name": row["bank_name"],
        "id_document": row["id_document"],
        "verified_at": row["verified_at"],
        "expires_at": row["expires_at"].isoformat(),
        "bank_signature": row["bank_signature"],
        "account_number": row["account_number"],
        "kyc_date": row["kyc_date"],
        "message": "은행 창구 실명확인이 완료되었습니다. 30분 내에 지갑을 등록하세요.",
    }


@app.post("/wallet/register")
def wallet_register(req: WalletRegisterRequest):
    verification, err = wallet_svc.consume_verification(req.verification_token)
    if err:
        raise HTTPException(status_code=403, detail=err)

    worker = {"worker_name": verification["worker_name"]}

    # ③ 출입국은 필수다. 은행 실명확인을 통과했더라도 체류 기록이 없으면 발급하지 않는다.
    immigration_values, immigration_log = run_lookups(worker, purpose="hospital")
    imm = next((l for l in immigration_log if l["agency_id"] == "immigration"), None)
    if not imm or imm["status"] != "ok":
        raise HTTPException(
            status_code=403,
            detail="IMMIGRATION_RECORD_NOT_FOUND: 출입국 체류 기록을 확인할 수 없어 지갑을 발급하지 않습니다.",
        )

    # 기록은 있으나 체류자격이 말소·취소된 경우. 은행 실명확인만으로는 잡히지 않는다.
    imm_values = immigration_values.get("visa_status")
    if imm_values not in (None, "유효"):
        raise HTTPException(
            status_code=403,
            detail=f"VISA_NOT_ACTIVE: 체류자격이 {imm_values} 상태입니다. 지갑을 발급할 수 없습니다.",
        )

    # 이미 지갑이 있으면 새로 만들지 않는다 (지갑은 1인 1개).
    # 다만 단말 키는 다시 등록한다 — 폰을 바꾸거나 앱을 다시 깔면
    # 새 키 쌍이 만들어지고, 은행 실명확인을 다시 거쳐 그 단말을 묶는다.
    for existing in _local_db.values():
        if existing.get("worker_name") == worker["worker_name"]:
            cid = existing["credential_id"]
            holder = wallet_svc.register_holder_key(cid, req.public_key, verification)
            if not existing.get("agency_lookups"):
                vals, log = run_lookups(worker, purpose="employer")
                vals.pop("account_verified", None)
                existing.update({k: v for k, v in vals.items() if v is not None})
                existing["agency_lookups"] = log
            return {
                "credential_id": cid,
                "is_existing": True,
                "message": "이미 지갑이 있습니다. 이 단말을 기존 지갑에 연결했습니다.",
                "wallet": {k: holder[k] for k in ("verified_by", "bank_name", "id_document", "registered_at")},
            }

    agency_values, agency_log = run_lookups(worker, purpose="employer")

    cid = str(uuid.uuid4())
    bc = get_blockchain_client()
    bc_res = bc.issue(cid)

    row = {
        "credential_id": cid,
        "worker_name": verification["worker_name"],
        "account_bank": verification["bank_name"],
        "account_number": verification["account_number"],
        "status": "valid",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "credential_hash": bc_res["credential_hash"],
        "tx_hash": bc_res["tx_hash"],
        "explorer_url": bc_res["explorer_url"],
        "chain_mode": bc_res.get("mode"),
        "agency_lookups": agency_log,
        "verified_by": verification["verified_by"],
        "id_document": verification["id_document"],
        "is_existing": False,
        "message": "지갑 발급 및 블록체인 등록 완료",
    }
    row.update(agency_values)
    row.pop("account_verified", None)
    row.setdefault("job_change_limit", 3)

    _local_db[cid] = row
    holder = wallet_svc.register_holder_key(cid, req.public_key, verification)
    row["wallet"] = {k: holder[k] for k in ("verified_by", "bank_name", "id_document", "registered_at")}

    sb = _get_supabase_safe()
    if sb:
        try:
            sb.table("credentials").insert(
                {k: v for k, v in row.items()
                 if k not in ("agency_lookups", "wallet", "is_existing", "message")}
            ).execute()
        except Exception as e:
            print(f"[Supabase sync error]: {e}")

    return row


@app.get("/wallets")
def list_wallets():
    """
    발급된 지갑 목록. **심사·시연에서 인물을 바꿔가며 보기 위한 것**이고,
    실제 서비스에서 근로자는 자기 지갑 하나만 갖는다.
    """
    rows = []
    for cid, cred in _local_db.items():
        holder = wallet_svc.get_wallet(cid)
        rows.append({
            "credential_id": cid,
            "worker_name": cred.get("worker_name"),
            "nationality": cred.get("nationality"),
            "visa_type": cred.get("visa_type"),
            "visa_status": cred.get("visa_status"),
            "employer_name": cred.get("employer_name"),
            "holder_registered": bool(holder),
        })
    rows.sort(key=lambda r: r["worker_name"] or "")
    return {"wallets": rows}


@app.get("/wallet/{credential_id}")
def wallet_status(credential_id: str):
    """내 지갑 상태. 저장된 문자열이 아니라 체인에서 읽어 온다."""
    cred = _local_db.get(credential_id)
    if not cred:
        raise HTTPException(status_code=404, detail="wallet not found")

    chain = get_blockchain_client().get_status(credential_id)
    holder = wallet_svc.get_wallet(credential_id)

    return {
        "credential_id": credential_id,
        "worker_name": cred.get("worker_name"),
        "nationality": cred.get("nationality"),
        "visa_type": cred.get("visa_type"),
        "visa_valid_until": cred.get("visa_valid_until"),
        "account_bank": cred.get("account_bank"),
        "account_number": cred.get("account_number"),
        "onchain_proof": chain,
        "chain_mode": chain["mode"],
        "tx_hash": cred.get("tx_hash"),
        "explorer_url": cred.get("explorer_url") if chain["mode"] == "live_testnet" else None,
        "agency_lookups": cred.get("agency_lookups", []),
        "holder_registered": bool(holder),
        "wallet": holder and {k: holder[k] for k in ("verified_by", "bank_name", "id_document", "registered_at")},
        "dossier": _build_job_change_dossier(cred),
    }


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

    # 이 지갑의 주인이 보낸 요청인지 단말 서명으로 확인한다.
    ok, why = wallet_svc.verify_holder_signature(
        req.credential_id,
        f"{req.credential_id}|{req.target_id}|{req.signed_at or ''}",
        req.holder_signature,
    )
    if not ok:
        raise HTTPException(status_code=403, detail=why)

    # 제출하는 순간 기관에 다시 묻는다. 카드를 미리 쌓아두지 않으므로
    # 낡은 버전이라는 것이 존재하지 않는다. 체인에는 아무것도 쓰지 않는다.
    if req.target_id in _SITE_TARGETS:
        # 출퇴근은 매일 두 번이라 기관 재조회를 하지 않는다.
        # 필요한 것은 체류자격이 살아 있는지뿐이고, 그건 스캔 시 체인 조회로 확인한다.
        fresh, refresh_log = {}, []
    else:
        purpose = "hospital" if req.target_id == "hospital_1" else "employer"
        fresh, refresh_log = run_lookups(cred, purpose=purpose)
    fresh.pop("account_verified", None)
    cred.update({k: v for k, v in fresh.items() if v is not None})
    cred["agency_lookups"] = refresh_log
    cred["refreshed_at"] = datetime.now(timezone.utc).isoformat()

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=60)
    _presentation_sessions[_token_hash(token)] = {
        "credential_id": req.credential_id,
        "target_id": req.target_id,
        "symptom": req.symptom if req.target_id == "hospital_1" else None,
        "symptom_original": req.symptom_original if req.target_id == "hospital_1" else None,
        "symptom_locale": req.symptom_locale if req.target_id == "hospital_1" else None,
        "expires_at": expires_at,
        "status": "created",
    }
    payload = {"v": 1, "t": token}
    return {
        "qr_payload": payload,
        "qr_image_base64": _make_qr_base64(payload),
        "expires_at": expires_at.isoformat(),
        "agency_lookups": refresh_log,
        "refreshed_at": cred["refreshed_at"],
        "holder_verified": why != "NO_WALLET_REGISTERED",
    }


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
        return {"result": "fail", "reason": "REVOKED", "onchain_proof": status}

    cid = session["credential_id"]
    vid = req.verifier_id
    out = {"result": "pass", "onchain_proof": status}

    # ── 수령처마다 열리는 칸이 다르다 (v0.5 §3 · 수치값 최소 제공) ─────────
    # 같은 증명서라도 목적에 필요한 항목만 내보낸다.
    if vid.startswith("company"):
        # 급여계좌 등록에 필요한 항목
        out.update({
            "worker_name": cred["worker_name"],
            "nationality": cred.get("nationality"),
            "reg_no": cred.get("reg_no"),
            "account_bank": cred.get("account_bank"),
            "account_number": cred.get("account_number"),
            "visa_type": cred.get("visa_type") or "E-9",
            "visa_valid_until": cred.get("visa_valid_until"),
            "dossier": _build_job_change_dossier(cred),
        })
    elif vid == "insurer_1":
        # 체류자격 + 본인명의 계좌 확인. 가입 사실을 기록해 두고 카드는 발급하지 않는다.
        out.update({
            "worker_name": cred["worker_name"],
            "nationality": cred.get("nationality"),
            "visa_type": cred.get("visa_type") or "E-9",
            "account_bank": cred.get("account_bank"),
            "account_number": cred.get("account_number"),
        })
        _insurance_db[cid] = {
            "product": "일상 상해보험",
            "company": "○○손해보험",
            "enrolled_at": datetime.now(timezone.utc).isoformat(),
        }
    elif vid == "hospital_1":
        # 접수 등록에 필요한 신원 항목 + 증상. 계좌 정보는 보내지 않는다.
        out.update({
            "worker_name": cred["worker_name"],
            "nationality": cred.get("nationality"),
            "reg_no": cred.get("reg_no"),
            "birth_date": cred.get("birth_date"),
            "gender": cred.get("gender"),
            "visa_type": cred.get("visa_type") or "E-9",
            "visa_valid_until": cred.get("visa_valid_until"),
            "symptom": session.get("symptom"),
            "symptom_original": session.get("symptom_original"),
            "symptom_locale": session.get("symptom_locale"),
        })
        # 자리 3에서 가입했으면 그 사실이 여기서 자동으로 조회된다 (카드 보관 없음).
        ins = _insurance_db.get(cid)
        if ins:
            out.update({
                "insurance_active": True,
                "insurance_product": ins["product"],
                "insurance_company": ins["company"],
            })
    else:
        out.update({"worker_name": cred["worker_name"], "nationality": cred.get("nationality")})

    return out


# ---------------------------------------------------------------------------
# 자리 4 : 출퇴근 — 지갑을 매일 쓰는 자리
#
# 새 크리덴셜을 발행하지 않는다. 이미 있는 것을 그대로 쓴다.
#   · 단말 키 서명    -> 본인 확인 (지갑이 은행 앱 안이라 대리 출근은 계좌 비밀번호를 넘기는 일)
#   · 온체인 상태 조회 -> 체류자격이 취소되면 내일 아침 출근이 막힌다. 읽기라 가스 0원.
#
# 시각을 찍고 보관하는 주체는 **회사 근태 시스템**이다. 은행은 유효 여부만 답하고 빠진다.
# 근태 조작 방지는 의도적으로 범위 밖이다 (attendance.py 상단 참조).
# ---------------------------------------------------------------------------

_SITE_TARGETS = {"site_A": "SCANNER-BIZ-001", "site_B": "SCANNER-BIZ-002"}


@app.get("/attendance/sites")
def attendance_sites():
    return {"targets": _SITE_TARGETS, "sites": att.SITES}


@app.post("/attendance/scan")
def attendance_scan(req: AttendanceScanRequest):
    """사업장 스캐너가 출퇴근 QR을 읽었을 때."""
    token = req.payload.get("t") if isinstance(req.payload, dict) else None
    if not isinstance(token, str):
        raise HTTPException(status_code=400, detail="token payload required")

    session = _presentation_sessions.get(_token_hash(token))
    if not session:
        raise HTTPException(status_code=404, detail="session not found")
    if session["expires_at"] <= datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="session expired")
    if session["status"] != "created":
        raise HTTPException(status_code=409, detail="session already consumed")
    if _SITE_TARGETS.get(session["target_id"]) != req.scanner_id:
        raise HTTPException(status_code=403, detail="TARGET_MISMATCH")

    cid = session["credential_id"]
    cred = _local_db.get(cid, {})
    status = get_blockchain_client().get_status(cid)
    session["status"] = "consumed"

    # 여기가 이 자리의 핵심. 체류자격이 철회되면 출근 자체가 기록되지 않는다.
    if not status["is_valid"]:
        return {
            "result": "fail",
            "reason": "REVOKED",
            "worker_name": cred.get("worker_name"),
            "onchain_proof": status,
            "message": "체류자격이 철회되어 출근을 기록할 수 없습니다. 고용노동부·출입국에 확인하십시오.",
        }

    row, err = att.record_scan(cid, cred.get("worker_name"), req.scanner_id)
    if err:
        raise HTTPException(status_code=400, detail=err)

    return {
        "result": "pass",
        "onchain_proof": status,
        "record": row,
        "message": "출근이 기록되었습니다." if row["check_type"] == "in" else "퇴근이 기록되었습니다.",
    }


@app.get("/attendance/site/{site_id}")
def attendance_site(site_id: str):
    """회사 근태 시스템 화면이 읽는다."""
    return {
        "site_id": site_id,
        "summary": att.today_summary(site_id),
        "records": att.records_of(site_id),
    }


@app.get("/attendance/worker/{credential_id}")
def attendance_worker(credential_id: str):
    """근로자 폰에 마지막 기록 한 건만 돌려준다. 지갑에 근무 기록을 쌓지 않는다."""
    rows = [r for r in att._records.values() if r["credential_id"] == credential_id]
    rows.sort(key=lambda r: r["server_time"], reverse=True)
    return {"last": rows[0] if rows else None}


# ---------------------------------------------------------------------------
# S7 : 보험 — QR 없는 자리
#
# 보험사는 눈앞의 다른 기기가 아니라 앱 안에서 접수한다. QR은 "이 제출을 누가
# 받을지 정하는 일회용 번호표"이므로 여기서는 필요 없다. 대신 상품을 고르는
# 시점에 audience=INS-001 이 확정되고, 그 값이 제출 인증에 박힌다.
# 가상 스캐너를 만들지 않는다 (설계 축 1).
#
# 카드는 지갑에 쌓지 않는다 (설계 축 3). 여기서 만들어지는 것은 이번 전송에만
# 쓰이는 1회용 제출 인증이고, 전송되면 소멸한다. 승인 결과는 보험사 원천 기록
# (_insurance_db)에만 남고, 병원 접수 시 그쪽을 조회해 쓴다.
# ---------------------------------------------------------------------------
INSURER_AUDIENCE = "INS-001"

_INSURANCE_PRODUCTS = [
    {
        "product_id": "ins-accident-basic",
        "name": "일상 상해보험 (기본형)",
        "company": "○○손해보험",
        "premium": "월 9,900원",
        "summary": "업무 외 상해 치료비 보장 · 가입기간 1년",
    },
    {
        "product_id": "ins-accident-plus",
        "name": "일상 상해보험 (확장형)",
        "company": "○○손해보험",
        "premium": "월 14,500원",
        "summary": "상해 치료비 + 입원 일당 · 가입기간 1년",
    },
    {
        "product_id": "ins-liability",
        "name": "생활 배상책임보험",
        "company": "○○손해보험",
        "premium": "월 4,200원",
        "summary": "일상생활 중 타인 신체·재물 손해 배상 · 가입기간 1년",
    },
]

# 제출 인증에 실리는 항목. 화면에서 전송 전에 그대로 펼쳐 보여준다.
# 소득 정보·진단 정보·사본 이미지는 스키마에서 제외한다.
_INSURANCE_DISCLOSURE = [
    ("worker_name", "성명"),
    ("birth_date", "생년월일"),
    ("reg_no", "외국인등록번호"),
    ("visa_status", "체류자격 유효 여부"),
    ("job_category", "직종 (위험등급 산정용)"),
    ("account", "납부 계좌"),
]

_insurance_submissions = {}


def _find_product(product_id: str):
    for p in _INSURANCE_PRODUCTS:
        if p["product_id"] == product_id:
            return p
    return None


def _disclosure_from(cred: dict) -> dict:
    """이 보험사에 나가는 항목만 뽑는다. 여기 없는 값은 전송되지 않는다."""
    visa_ok = bool(cred.get("visa_valid_until"))
    return {
        "worker_name": cred.get("worker_name"),
        "birth_date": cred.get("birth_date"),
        "reg_no": cred.get("reg_no"),
        "visa_status": (
            f"{cred.get('visa_type') or 'E-9'} 유효 (만료 {cred.get('visa_valid_until')})"
            if visa_ok else "확인 불가"
        ),
        "job_category": cred.get("job_category"),
        "account": f"{cred.get('account_bank')} {cred.get('account_number')}",
    }


@app.get("/insurance/products")
def insurance_products():
    """고정 3종. 비교·추천을 하지 않는다 (모집 행위로 읽히지 않도록)."""
    return {"audience": INSURER_AUDIENCE, "products": _INSURANCE_PRODUCTS}


@app.post("/insurance/submissions")
def submit_insurance(req: InsuranceSubmitRequest):
    cred = _local_db.get(req.credential_id)
    if not cred:
        raise HTTPException(status_code=404, detail="credential not found")
    product = _find_product(req.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    # 상품을 고른 시점에 수령처가 확정된다. 이 값이 제출 인증에 박히므로
    # 다른 수령처에 그대로 내면 audience 불일치로 거부된다.
    status = get_blockchain_client().get_status(req.credential_id)
    disclosure = _disclosure_from(cred)

    sub_id = "SUB-" + secrets.token_hex(4).upper()
    row = {
        "submission_id": sub_id,
        "credential_id": req.credential_id,
        "audience": INSURER_AUDIENCE,
        "product": product,
        "disclosure": disclosure,
        "disclosure_labels": [{"key": k, "label": l} for k, l in _INSURANCE_DISCLOSURE],
        "onchain_proof": status,
        "verified": bool(status.get("is_valid")),
        "status": "submitted" if status.get("is_valid") else "rejected",
        "reason": None if status.get("is_valid") else "REVOKED",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "decided_at": None,
        "decided_by": None,
        "policy_no": None,
    }
    _insurance_submissions[sub_id] = row
    return row


@app.get("/insurance/submissions")
def list_insurance_submissions():
    """보험사 접수함. 최근 건이 위로."""
    rows = sorted(
        _insurance_submissions.values(),
        key=lambda r: r["submitted_at"],
        reverse=True,
    )
    return {"submissions": rows}


@app.get("/insurance/submissions/{submission_id}")
def get_insurance_submission(submission_id: str):
    row = _insurance_submissions.get(submission_id)
    if not row:
        raise HTTPException(status_code=404, detail="submission not found")
    return row


@app.post("/insurance/submissions/{submission_id}/decide")
def decide_insurance_submission(submission_id: str, req: InsuranceDecisionRequest):
    """보험사 담당자의 수동 처리. 자동 승인하지 않는다."""
    row = _insurance_submissions.get(submission_id)
    if not row:
        raise HTTPException(status_code=404, detail="submission not found")
    if row["status"] != "submitted":
        raise HTTPException(status_code=409, detail=f"already {row['status']}")

    # 담당자가 누르는 순간 온체인 상태를 다시 본다.
    # 접수 후 철회된 건은 승인되지 않아야 한다.
    status = get_blockchain_client().get_status(row["credential_id"])
    row["onchain_proof"] = status
    if not status.get("is_valid"):
        row["status"] = "rejected"
        row["reason"] = "REVOKED"
        row["decided_at"] = datetime.now(timezone.utc).isoformat()
        row["decided_by"] = req.officer or "보험사 담당자"
        return row

    if req.decision == "approve":
        row["status"] = "approved"
        row["policy_no"] = "POL-" + secrets.token_hex(3).upper()
        # 가입 사실은 보험사 원천 기록에만 남는다. 지갑에 카드를 발급하지 않는다.
        _insurance_db[row["credential_id"]] = {
            "product": row["product"]["name"],
            "company": row["product"]["company"],
            "policy_no": row["policy_no"],
            "enrolled_at": datetime.now(timezone.utc).isoformat(),
        }
    else:
        row["status"] = "rejected"
        row["reason"] = req.reason or "심사 거절"

    row["decided_at"] = datetime.now(timezone.utc).isoformat()
    row["decided_by"] = req.officer or "보험사 담당자"
    return row


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
