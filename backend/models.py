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
    # 이직(사업장 변경)에 필요한 항목. 고용허가서·표준근로계약서에서 파생된다고 가정.
    employer_name: str | None = None         # 직전 사업장명
    employment_from: str | None = None       # YYYY-MM-DD
    employment_to: str | None = None         # YYYY-MM-DD (근로계약 종료일)
    job_category: str | None = None          # 제조업 등
    job_change_used: int | None = None       # 사용한 사업장 변경 횟수
    job_change_limit: int | None = None      # 한도 (초기 취업기간 3회)
    job_change_excluded: int | None = None   # 사용자 귀책으로 횟수 미산입된 건수
    health_check_date: str | None = None     # 건강진단 실시일 (내용은 공개하지 않는다)
    topik_level: str | None = None           # 한국어능력시험 등급 (해당자)


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
