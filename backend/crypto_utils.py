"""
발급기관 전자서명을 시뮬레이션하는 모듈.

실제 서비스라면 기관마다 별도의 비대칭키(공개키/개인키)로 서명하지만,
프로토타입에서는 서버만 아는 비밀키(ISSUER_SECRET)로 HMAC 서명을 만들어
"위변조 여부"를 판별하는 개념만 정확히 시연합니다.

핵심 아이디어:
- QR 안의 데이터(계좌번호 등)를 정렬된 JSON 문자열로 만든 뒤 HMAC-SHA256으로 서명.
- 데이터가 단 한 글자라도 바뀌면 서명이 완전히 달라져서 검증에 실패합니다.
"""

import hashlib
import hmac
import json
from typing import Any, Dict


def canonical_json(data: Dict[str, Any]) -> str:
    """키 순서에 상관없이 항상 동일한 문자열이 나오도록 정렬해서 직렬화."""
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sign_payload(data: Dict[str, Any], secret: str) -> str:
    message = canonical_json(data).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_signature(data: Dict[str, Any], signature: str, secret: str) -> bool:
    if not signature:
        return False
    expected = sign_payload(data, secret)
    # 타이밍 공격 방지를 위해 constant-time 비교 사용
    return hmac.compare_digest(expected, signature)
