"""
발급기관 모의 API (Phase 1)

실제 서비스에서는 출입국·고용센터·은행·의료기관이 각자 자기 시스템에서 답하고
자기 키로 서명한다. Phase 1에서는 이 파일이 그 기관들을 대신한다.

**기관마다 자기 명단만 본다.** `seeds/` 아래에 기관별 파일이 따로 있고,
각 조회 함수는 자기 파일만 읽는다. 출입국 함수는 고용센터 파일을 열지 못한다.
그래서 기관마다 아는 사람이 다르다 — 출입국 9명, 은행 8명, 고용센터 7명,
의료기관 6명, 교육원 4명. 하나의 DB를 나눠 쓰는 구조가 아니라는 뜻이다.

중요한 것은 값이 아니라 **경로**다. 실제 연동 시 각 함수의 파일 읽기만
해당 기관 API 호출로 바뀌고 나머지 코드는 그대로다.

발급기관은 두 부류다 (Core planner §5-5).
  REAL : 자기 정보의 원천 주체 — 실서비스에서도 그대로 발급한다
  MOCK : Phase 2 협력 인터페이스 제안 — 지금은 시드 데이터
이 구분을 화면에서 지우지 말 것.
"""

import json
import os
from datetime import datetime, timezone

REAL = "real"
MOCK = "mock"

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")

_cache = {}


def load_agency(agency_file: str) -> dict:
    """기관 파일 하나를 읽어 성명으로 찾을 수 있게 만든다."""
    if agency_file not in _cache:
        with open(os.path.join(SEED_DIR, agency_file), encoding="utf-8") as f:
            doc = json.load(f)
        doc["_index"] = {r["worker_name"]: r for r in doc["records"]}
        _cache[agency_file] = doc
    return _cache[agency_file]


def _find(agency_file: str, worker: dict):
    """그 기관에 이 사람 기록이 있는지. 없으면 None — '해당 없음'이 아니라 '미등록'이다."""
    name = (worker or {}).get("worker_name")
    return load_agency(agency_file)["_index"].get(name)


def _without_name(rec: dict) -> dict:
    return {k: v for k, v in rec.items() if k != "worker_name" and v is not None}


# ── 기관별 조회 함수 ────────────────────────────────────────────────
# 각 함수는 자기 파일만 연다. 실제 연동 시 이 본문만 API 호출로 교체한다.

def immigration_lookup(worker):
    """출입국·외국인청 — 체류자격과 신원. 여기에 없으면 지갑을 발급하지 않는다."""
    rec = _find("immigration.json", worker)
    return _without_name(rec) if rec else {}


def bank_lookup(worker):
    """iM뱅크 — 창구 실명확인을 마친 급여계좌. 자기 은행 계좌이므로 실권한."""
    rec = _find("bank_kyc.json", worker)
    if not rec:
        return {}
    return {
        "account_bank": rec["account_bank"],
        "account_number": rec["account_number"],
        "account_verified": True,
    }


def eps_lookup(worker):
    """고용노동부 고용센터 — 고용이력과 사업장 변경 횟수."""
    rec = _find("eps.json", worker)
    return _without_name(rec) if rec else {}


def clinic_lookup(worker):
    """지정 의료기관 — 건강진단 실시일과 유효기간. 진단 내용은 내보내지 않는다."""
    rec = _find("clinic.json", worker)
    return _without_name(rec) if rec else {}


def language_lookup(worker):
    """국립국제교육원·사회통합프로그램 — 일반 TOPIK 등급과 KIIP 이수 단계."""
    rec = _find("niied.json", worker)
    return _without_name(rec) if rec else {}


def hrdk_lookup(worker):
    """
    한국산업인력공단 — EPS-TOPIK과 취업교육.
    EPS-TOPIK은 E-9 입국 요건이고 일반 TOPIK과 다른 시험이다.
    H-2 동포는 시험 대신 16시간 취업교육을 이수한다.
    """
    rec = _find("hrdk.json", worker)
    return _without_name(rec) if rec else {}


def qnet_lookup(worker):
    """Q-Net — 국가기술자격. 자격증 번호는 내보내지 않고 보유 사실과 등급만."""
    rec = _find("qnet.json", worker)
    return _without_name(rec) if rec else {}


def kosha_lookup(worker):
    """안전보건공단 — 업종별 안전보건교육 이수. 건설업은 기초안전 4시간이 필수."""
    rec = _find("kosha.json", worker)
    return _without_name(rec) if rec else {}


AGENCIES = [
    {"id": "immigration", "name": "출입국·외국인청", "authority": MOCK,
     "purpose": "체류자격·신원", "file": "immigration.json", "fn": immigration_lookup},
    {"id": "eps", "name": "고용노동부 고용센터", "authority": MOCK,
     "purpose": "고용이력·사업장 변경", "file": "eps.json", "fn": eps_lookup},
    {"id": "im_bank", "name": "iM뱅크", "authority": REAL,
     "purpose": "급여계좌 실명확인", "file": "bank_kyc.json", "fn": bank_lookup},
    {"id": "clinic", "name": "지정 의료기관", "authority": MOCK,
     "purpose": "건강진단 유효기간", "file": "clinic.json", "fn": clinic_lookup},
    {"id": "hrdk", "name": "한국산업인력공단", "authority": MOCK,
     "purpose": "EPS-TOPIK·취업교육", "file": "hrdk.json", "fn": hrdk_lookup},
    {"id": "qnet", "name": "Q-Net 국가기술자격", "authority": MOCK,
     "purpose": "국가기술자격", "file": "qnet.json", "fn": qnet_lookup},
    {"id": "kosha", "name": "안전보건공단", "authority": MOCK,
     "purpose": "안전보건교육 이수", "file": "kosha.json", "fn": kosha_lookup},
    {"id": "niied", "name": "국립국제교육원", "authority": MOCK,
     "purpose": "TOPIK·사회통합프로그램", "file": "niied.json", "fn": language_lookup},
]

# 제출 목적에 따라 묻는 기관이 다르다. 목적에 필요 없는 기관에는 묻지 않는다.
PURPOSE_AGENCIES = {
    "employer": ["immigration", "eps", "im_bank", "clinic", "hrdk", "qnet", "kosha", "niied"],
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
            status, error = ("ok" if got else "none"), None
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


def coverage():
    """기관별 보유 인원. 심사용 데이터 명세서와 /agencies 응답에 쓴다."""
    out = []
    for a in AGENCIES:
        doc = load_agency(a["file"])
        out.append({
            "agency_id": a["id"], "agency": a["name"], "authority": a["authority"],
            "purpose": a["purpose"], "file": f"seeds/{a['file']}",
            "record_count": len(doc["records"]),
            "note": doc.get("_note"),
        })
    return out
