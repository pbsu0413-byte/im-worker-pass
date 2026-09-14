"""
DC형 퇴직연금 — 근로자가 직접 운용을 고르는 퇴직급여

제도의 사실관계를 화면과 계산에 그대로 반영한다.
  · **가입은 회사가 한다.** 사업장이 DC 제도를 도입해야 근로자 계정이 생긴다.
    근로자가 앱에서 "가입"을 누르는 상품이 아니다.
  · **근로자가 하는 선택은 운용상품이다.** 고르지 않으면 대기성 예금에 머문다.
    DC 적립금을 방치해 저금리로 두는 것이 실제로 흔한 문제이고,
    이 화면이 푸는 것도 그 지점이다.
  · 사용자 부담금은 **연간 임금총액의 1/12 이상**이다. 월로 환산하면 월 임금의 약 8.3%.

E-9·H-2 는 출국만기보험이 퇴직금을 갈음하므로 DC 는 사업장이 별도로 도입한 경우에만
적용된다. 이 단서를 화면에 함께 표시한다.

수익률은 모두 시연용 가정값이다.
"""

import json
import os
from datetime import datetime, timezone

import payroll as pay

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")

CONTRIB_RATE = 1 / 12          # 연간 임금총액의 1/12
WORKDAYS_PER_MONTH = 21.7      # 월 통상임금 환산용 가정값

# 시연 중 바꾼 운용상품. 서버를 다시 켜면 시드 값으로 돌아간다.
_choices = {}


def _doc():
    with open(os.path.join(SEED_DIR, "pension.json"), encoding="utf-8") as f:
        return json.load(f)


def funds():
    return _doc()["funds"]


def _fund(fid):
    for f in funds():
        if f["id"] == fid:
            return f
    return None


def _record(worker_name):
    for r in _doc()["records"]:
        if r["worker_name"] == worker_name:
            return r
    return None


def _monthly_wage(worker_name):
    p = pay.payroll_of(worker_name)
    if not p:
        return None
    return int(round(p["hourly_wage"] * p["daily_hours"] * WORKDAYS_PER_MONTH))


def choose_fund(credential_id: str, fund_id: str):
    if not _fund(fund_id):
        return None
    _choices[credential_id] = fund_id
    return fund_id


def status(credential_id: str, worker_name: str, visa_valid_until: str | None = None) -> dict:
    rec = _record(worker_name)
    doc = _doc()
    if not rec or not rec.get("dc_enrolled"):
        return {
            "enrolled": False,
            "reason": "사업장이 DC형 퇴직연금을 도입하지 않았습니다.",
        }

    wage = _monthly_wage(worker_name)
    if not wage:
        return {"enrolled": False, "reason": "급여 기준 정보가 없습니다."}

    months = int(rec.get("started_months_ago", 0)) + 1
    monthly = int(round(wage * CONTRIB_RATE))
    principal = monthly * months

    fid = _choices.get(credential_id, rec.get("fund"))
    f = _fund(fid) if fid else None
    rate = f["rate"] if f else doc["default_rate"]

    # 적립식 단리 근사 — products.py 의 적금과 같은 방식이다
    interest = int(round(principal * rate * (months + 1) / 24))

    # 고르지 않고 두었을 때와의 차이. 이 화면이 왜 있는지를 숫자로 보여준다.
    idle = int(round(principal * doc["default_rate"] * (months + 1) / 24))

    # 귀국(체류 만료) 시점까지 계속 적립했을 때의 예상액.
    # 목표 금액을 정할 때 "이미 확보된 돈"으로 잡아야 하는 값이다.
    projected = None
    if visa_valid_until:
        try:
            end = datetime.strptime(visa_valid_until, "%Y-%m-%d").date()
            today = datetime.now(timezone.utc).date()
            left = max((end.year - today.year) * 12 + (end.month - today.month), 0)
            tm = months + left
            pr = monthly * tm
            projected = pr + int(round(pr * rate * (tm + 1) / 24))
        except Exception:
            projected = None

    return {
        "enrolled": True,
        "months": months,
        "months_to_leave": None if projected is None else left,
        "projected_balance": projected,
        "monthly_wage": wage,
        "monthly_contribution": monthly,
        "principal": principal,
        "interest": interest,
        "balance": principal + interest,
        "rate": rate,
        "fund": f and {k: f[k] for k in ("id", "name", "desc", "risk", "rate")},
        "chosen": bool(f),
        "idle_interest": idle,
        "gain_vs_idle": interest - idle,
        # 아직 고르지 않은 사람에게 보여줄 "가장 좋았을 경우"와의 차이
        "gain_vs_idle_max": int(round(
            principal * max(x["rate"] for x in doc["funds"]) * (months + 1) / 24)) - idle,
        "funds": doc["funds"],
        "authority": "real",
        "notice": (
            "사용자 부담금은 연간 임금총액의 1/12입니다. 수익률과 금액은 시연용 예시입니다. "
            "E-9·H-2는 출국만기보험이 퇴직금을 갈음하므로, DC형은 사업장이 별도로 도입한 경우에 적용됩니다."
        ),
    }


def balance_of(credential_id: str, worker_name: str):
    """관리자 콘솔의 근로자 목록에 쓰는 잔액 한 줄."""
    st = status(credential_id, worker_name)
    return st["balance"] if st.get("enrolled") else None
