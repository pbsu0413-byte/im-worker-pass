"""
모의 발급기관 API (Phase 1)

실제 서비스에서는 출입국·고용센터·은행·의료기관이 각자 자기 시스템에서 답하고
자기 키로 서명한다. Phase 1에서는 이 파일이 그 기관들을 대신한다.

중요한 것은 값이 아니라 **경로**다. 어느 기관에 무엇을 물었는지가 기록으로 남고,
실제 연동 시 각 함수의 본문만 교체하면 나머지 코드는 바뀌지 않는다.

발급기관은 두 부류로 나뉜다 (Core planner §5-5).
  REAL : 자기 정보의 원천 주체 — 실서비스에서도 그대로 발급한다
  MOCK : Phase 2 협력 인터페이스 제안 — 지금은 시드 데이터
이 구분을 화면에서 지우지 말 것.
"""

from datetime import datetime, timezone

REAL = "real"
MOCK = "mock"

# 기관이 보유하고 있다고 가정하는 원천 데이터.
# 조회 키는 (성명, 계좌번호). 일치하지 않으면 기본 레코드를 쓴다.
_RECORDS = {
    ("NGUYEN VAN A", "512-123456-01"): {
        "reg_no": "980312-5123456",
        "birth_date": "1998-03-12",
        "gender": "남",
        "visa_type": "E-9",
        "visa_valid_until": "2029-03-14",
        "employer_name": "A제조 (주)대구정밀",
        "employment_from": "2024-04-01",
        "employment_to": "2026-08-31",
        "job_category": "제조업 (금속가공)",
        "job_change_used": 1,
        "job_change_limit": 3,
        "job_change_excluded": 1,
        "health_check_date": "2026-07-15",
        "topik_level": "TOPIK 3급",
    },
    ("SITI RAHAYU", "512-987654-02"): {
        "reg_no": "010725-6234567",
        "birth_date": "2001-07-25",
        "gender": "여",
        "visa_type": "E-9",
        "visa_valid_until": "2028-11-30",
        "employer_name": "B식품 (주)경산푸드",
        "employment_from": "2023-12-01",
        "employment_to": "2026-08-20",
        "job_category": "제조업 (식품가공)",
        "job_change_used": 2,
        "job_change_limit": 3,
        "job_change_excluded": 0,
        "health_check_date": "2026-06-02",
        "topik_level": "TOPIK 2급",
    },
}

# 시연용으로 출입국에 등록되어 있는 사람들. 여기 없으면 "체류 기록 없음"이다.
_RECORDS[("TRAN VAN C", "512-333333-03")] = {
    "reg_no": "970118-5345678",
    "birth_date": "1997-01-18",
    "gender": "남",
    "visa_type": "E-9",
    "visa_valid_until": "2030-01-17",
    "employer_name": None,
    "employment_from": None,
    "employment_to": None,
    "job_category": None,
    "job_change_used": None,
    "job_change_limit": 3,
    "job_change_excluded": None,
    "health_check_date": None,
    "topik_level": None,
}


def _record(worker: dict):
    """기관에 그 사람 기록이 있는지. 없으면 None — '해당 없음'이 아니라 '미등록'이다."""
    key = (worker.get("worker_name"), worker.get("account_number"))
    rec = _RECORDS.get(key)
    return dict(rec) if rec else None


def _pick(worker: dict, fields: list) -> dict:
    """기관이 보유한 항목만 잘라서 돌려준다. 기록이 없으면 빈 값."""
    rec = _record(worker)
    if not rec:
        return {}
    return {f: rec[f] for f in fields if rec.get(f) is not None}


# ── 기관별 조회 함수 ────────────────────────────────────────────────
# 실제 연동 시 이 함수 본문만 각 기관 API 호출로 교체한다.

def immigration_lookup(worker):
    """출입국·외국인청 — 체류자격과 신원."""
    return _pick(worker, ["reg_no", "birth_date", "gender", "visa_type", "visa_valid_until"])


def eps_lookup(worker):
    """고용노동부 고용센터(EPS) — 고용이력과 사업장 변경 횟수."""
    return _pick(worker, [
        "employer_name", "employment_from", "employment_to", "job_category",
        "job_change_used", "job_change_limit", "job_change_excluded",
    ])


def bank_lookup(worker):
    """iM뱅크 — 본인 명의 급여 수령 계좌 확인. 자기 은행 계좌이므로 실권한."""
    if not worker.get("account_number"):
        return {}
    return {"account_verified": True}


def clinic_lookup(worker):
    """지정 의료기관 — 건강진단 실시일만. 진단 내용은 조회하지 않는다."""
    return _pick(worker, ["health_check_date"])


def language_lookup(worker):
    """국립국제교육원 — 한국어능력시험 등급. 해당자만."""
    return _pick(worker, ["topik_level"])


AGENCIES = [
    {"id": "immigration", "name": "출입국·외국인청", "authority": MOCK,
     "purpose": "체류자격·신원", "fn": immigration_lookup},
    {"id": "eps", "name": "고용노동부 고용센터", "authority": MOCK,
     "purpose": "고용이력·사업장 변경", "fn": eps_lookup},
    {"id": "im_bank", "name": "iM뱅크", "authority": REAL,
     "purpose": "급여계좌 실명확인", "fn": bank_lookup},
    {"id": "clinic", "name": "지정 의료기관", "authority": MOCK,
     "purpose": "건강진단 유효기간", "fn": clinic_lookup},
    {"id": "niied", "name": "국립국제교육원", "authority": MOCK,
     "purpose": "한국어능력시험", "fn": language_lookup},
]

# 제출 목적에 따라 물어보는 기관이 다르다. 목적에 필요 없는 기관에는 묻지 않는다.
PURPOSE_AGENCIES = {
    "employer": ["immigration", "eps", "im_bank", "clinic", "niied"],
    "insurance": ["immigration", "eps", "im_bank"],
    "hospital": ["immigration", "clinic"],
}


def run_lookups(worker: dict, purpose: str = "employer"):
    """
    목적에 필요한 기관만 순서대로 조회한다.
    반환: (수집된 값, 조회 기록). 기록은 화면에 그대로 뿌린다.
    """
    wanted = PURPOSE_AGENCIES.get(purpose, PURPOSE_AGENCIES["employer"])
    values, log = {}, []

    for agency in AGENCIES:
        if agency["id"] not in wanted:
            continue
        try:
            got = agency["fn"](worker) or {}
            status = "ok" if got else "none"
            error = None
        except Exception as e:          # 한 기관이 실패해도 나머지는 계속 조회한다
            got, status, error = {}, "error", str(e)

        values.update(got)
        log.append({
            "agency_id": agency["id"],
            "agency": agency["name"],
            "authority": agency["authority"],
            "purpose": agency["purpose"],
            "status": status,
            "fields": sorted(got.keys()),
            "error": error,
            "queried_at": datetime.now(timezone.utc).isoformat(),
        })

    return values, log
