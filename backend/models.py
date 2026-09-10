from typing import Any, Dict

from pydantic import BaseModel


class CredentialIssueRequest(BaseModel):
    worker_name: str
    nationality: str
    account_bank: str
    account_number: str
    # 병원 접수에 필요한 신원 항목 (출입국 증명 가정). 없으면 화면에 "—"로 표시된다.
    reg_no: str | None = None            # 외국인등록번호
    birth_date: str | None = None        # YYYY-MM-DD
    gender: str | None = None            # 남 / 여
    visa_type: str | None = None         # E-9 등
    visa_valid_until: str | None = None  # 체류 만료일


class PresentationRequest(BaseModel):
    """근로자가 지갑에서 '이 QR은 어디 제출용인지'를 지정해서 생성 요청."""

    credential_id: str
    target_id: str  # 예: "company_A", "hospital_1", "insurer_1"
    symptom: str | None = None  # hospital only; fixed catalogue statement
    symptom_original: str | None = None  # 모국어 원문 (번역 대조용)
    symptom_locale: str | None = None    # vi / ko 등


class VerifyRequest(BaseModel):
    """스캔한 QR의 내용(payload)과, 스캔하는 쪽이 누구인지(verifier_id)."""

    payload: Dict[str, Any]
    verifier_id: str
