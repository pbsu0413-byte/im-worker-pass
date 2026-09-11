"""
지갑 발급 — 본인확인과 홀더 키 (S1)

카카오 인증서가 통신사 본인확인 위에 세워지듯, 이 지갑은 **은행 창구 실명확인**
위에 세워진다. 외국인 근로자는 급여를 받으려면 어차피 은행에 가고, 그 자리에서
여권·외국인등록증 대조가 법적으로 이미 일어난다. 절차를 늘리지 않는 유일한 접점이다.

은행이 보증하는 것은 "이 지갑이 이 사람의 것"이라는 사실 **하나뿐**이다.
체류자격은 출입국이, 고용이력은 고용센터가 답한다. 은행이 남의 것까지 서명하지 않는다.

홀더 키:
  브라우저가 ECDSA P-256 키 쌍을 만들고 개인키는 단말에 남는다. 서버는 공개키만 받는다.
  이후 제출할 때마다 단말이 서명하고 서버가 이 공개키로 검증한다.
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone

import agency_api
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils as asym_utils
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, SECP256R1

BANK_SECRET = os.environ.get("BANK_SECRET", "dev-bank-secret")
BANK_ID = "iM-BANK-001"
VERIFICATION_TTL_MIN = 30

# 창구 실명확인 명단은 은행 자기 파일(seeds/bank_kyc.json)에서 읽는다.
# 여기에 없으면 지갑 발급 1단계에서 막힌다 — 출입국 미등록(위조 등록증)과는 다른 이유다.
_verifications = {}   # token -> 본인확인 결과
_wallets = {}         # credential_id -> 홀더 공개키 등록 정보


def _b64u_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def bank_verify(worker_name: str):
    """
    은행 창구 실명확인 (시뮬레이션).
    은행 명단에 있어야 한다. 성공하면 30분짜리 1회용 확인 토큰을 내준다.
    """
    kyc = agency_api.load_agency("bank_kyc.json")["_index"].get(worker_name)
    if not kyc:
        return None, "BANK_KYC_NOT_FOUND"

    token = secrets.token_urlsafe(24)
    row = {
        "token": token,
        "verified_by": BANK_ID,
        "bank_name": kyc["account_bank"],
        "worker_name": worker_name,
        "account_number": kyc["account_number"],
        "id_document": "여권 + 외국인등록증 대조",
        "passport_no": kyc.get("passport_no"),
        "kyc_date": kyc.get("kyc_date"),
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=VERIFICATION_TTL_MIN),
        "used": False,
    }
    # 은행이 이 확인 결과에 서명한다. 서버가 뒤에서 내용을 바꾸면 서명이 깨진다.
    row["bank_signature"] = hmac.new(
        BANK_SECRET.encode(),
        f"{token}|{worker_name}|{row['account_number']}".encode(),
        hashlib.sha256,
    ).hexdigest()
    _verifications[token] = row
    return row, None


def consume_verification(token: str):
    """확인 토큰을 1회용으로 소비한다. 만료·재사용은 거절."""
    row = _verifications.get(token)
    if not row:
        return None, "VERIFICATION_NOT_FOUND"
    if row["used"]:
        return None, "VERIFICATION_ALREADY_USED"
    if row["expires_at"] <= datetime.now(timezone.utc):
        return None, "VERIFICATION_EXPIRED"
    row["used"] = True
    return row, None


def register_holder_key(credential_id: str, public_key_jwk: dict, verification: dict):
    """단말이 만든 공개키를 지갑으로 등록한다. 개인키는 서버로 오지 않는다."""
    _wallets[credential_id] = {
        "credential_id": credential_id,
        "public_key": public_key_jwk,
        "verified_by": verification["verified_by"],
        "bank_name": verification["bank_name"],
        "id_document": verification["id_document"],
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    return _wallets[credential_id]


def get_wallet(credential_id: str):
    return _wallets.get(credential_id)


def _load_public_key(jwk: dict):
    x = int.from_bytes(_b64u_decode(jwk["x"]), "big")
    y = int.from_bytes(_b64u_decode(jwk["y"]), "big")
    return ec.EllipticCurvePublicNumbers(x, y, SECP256R1()).public_key()


def verify_holder_signature(credential_id: str, message: str, signature_b64u: str):
    """
    단말 서명 검증. 서명이 맞아야 그 지갑의 주인이 보낸 요청이다.
    지갑이 등록되어 있지 않으면 (구버전 데이터) 검증을 건너뛴다.
    """
    wallet = _wallets.get(credential_id)
    if not wallet:
        return True, "NO_WALLET_REGISTERED"
    if not signature_b64u:
        return False, "HOLDER_SIGNATURE_MISSING"
    try:
        raw = _b64u_decode(signature_b64u)          # WebCrypto는 r||s 형식으로 준다
        half = len(raw) // 2
        der = asym_utils.encode_dss_signature(
            int.from_bytes(raw[:half], "big"), int.from_bytes(raw[half:], "big")
        )
        _load_public_key(wallet["public_key"]).verify(der, message.encode(), ECDSA(hashes.SHA256()))
        return True, None
    except InvalidSignature:
        return False, "HOLDER_SIGNATURE_INVALID"
    except Exception:
        return False, "HOLDER_SIGNATURE_MALFORMED"
