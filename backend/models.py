from typing import Any, Dict

from pydantic import BaseModel


class CredentialIssueRequest(BaseModel):
    worker_name: str
    nationality: str
    account_bank: str
    account_number: str


class PresentationRequest(BaseModel):
    """근로자가 지갑에서 '이 QR은 어디 제출용인지'를 지정해서 생성 요청."""

    credential_id: str
    target_id: str  # 예: "company_A", "hospital_1", "insurer_1"


class VerifyRequest(BaseModel):
    """스캔한 QR의 내용(payload)과, 스캔하는 쪽이 누구인지(verifier_id)."""

    payload: Dict[str, Any]
    verifier_id: str
