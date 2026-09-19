"""
DC형 퇴직연금 — 근로자가 직접 운용을 고르는 퇴직급여

제도의 사실관계를 화면과 계산에 그대로 반영한다.
  · **가입은 회사가 한다.** 사업장이 DC 제도를 도입해야 근로자 계정이 생긴다.
    근로자가 앱에서 "가입"을 누르는 상품이 아니다.
  · **근로자가 하는 선택은 운용상품이다.** 그리고 그 지시는 언제든 바꿀 수 있다
    (근로자퇴직급여 보장법은 반기 1회 이상 변경 기회를 보장한다 — 상한이 아니라 하한이다).
  · 사용자 부담금은 **연간 임금총액의 1/12 이상**이다. 월로 환산하면 월 임금의 약 8.3%.

### 운용지시를 바꿔도 과거는 바뀌지 않는다
예전 계산은 상품을 고르는 순간 **그동안 쌓인 적립금 전체에 새 수익률을 소급**했다.
안정형에서 성장형으로 옮기면 지난 2년치 수익까지 좋아지는 셈이라 사실과 다르다.
지금은 지시를 바꾼 시점에 잔액을 **동결**하고, 그 뒤 기간에만 새 수익률을 적용한다.
그래서 화면의 "얼마 차이가 납니다"도 지나간 기간이 아니라 **귀국까지 남은 기간** 기준이다.

### 안 고르면 대기성 예금이 아니라 디폴트 상품으로 간다
2023년 7월 12일부터 사전지정운용제도(디폴트옵션)가 시행 중이다. 적립금이 들어오고
2주 동안 운용지시가 없으면 미리 정해 둔 상품으로 자동 편입된다. 방치해도 이자가
아예 안 붙는 건 아니지만, 그 상품이 본인 상황에 맞는다는 보장은 없다.
`default_rate` 는 그 디폴트 상품의 가정 수익률이다.

### 전환은 즉시·무비용이 아니다
실제로는 기존 상품을 팔고 정산한 뒤 새 상품을 사기까지 영업일이 걸린다.
원리금 보장 상품을 만기 전에 깨면 약정이율이 아니라 중도해지이율이 적용된다.
화면에서 `switch_notice` 로 그대로 안내한다.

E-9·H-2 는 이 파일의 대상이 아니다. 고용허가제 근로자의 퇴직급여는 출국만기보험으로
쌓이며 `departure.py` 가 맡는다. 사업장이 DC 를 운영하더라도 마찬가지다.

수익률은 모두 시연용 가정값이다.
"""

import json
import os
from datetime import datetime, timezone

import departure as dep
import payroll as pay

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")

CONTRIB_RATE = 1 / 12          # 연간 임금총액의 1/12
WORKDAYS_PER_MONTH = 21.7      # 월 통상임금 환산용 가정값

# 시연 중 바꾼 운용지시. 서버를 다시 켜면 시드 값으로 돌아간다.
# cid -> {"fund": 상품id, "since_month": 지시 시점의 경과 개월,
#         "locked_principal": 그때까지의 원금, "locked_interest": 그때까지의 이자}
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


# ── 이자 계산 ────────────────────────────────────────────────────────────
# 적립식 단리 근사. products.py 의 적금과 같은 방식이다.

def _accrue(monthly, m, rate):
    """m개월 동안 매달 monthly 원씩 새로 넣었을 때 붙는 이자."""
    if m <= 0:
        return 0.0
    return monthly * m * rate * (m + 1) / 24


def _carry(balance, m, rate):
    """이미 쌓여 있던 balance 를 m개월 더 굴렸을 때 붙는 이자."""
    if m <= 0 or balance <= 0:
        return 0.0
    return balance * rate * m / 12


def _project(balance_now, monthly, m_left, rate):
    """지금 잔액에서 출발해 m_left 개월 더 적립했을 때의 예상 잔액."""
    if m_left <= 0:
        return balance_now
    return (balance_now
            + monthly * m_left
            + _accrue(monthly, m_left, rate)
            + _carry(balance_now, m_left, rate))


def _elapsed_months(rec):
    return int(rec.get("started_months_ago", 0)) + 1


def _accrued(credential_id, rec, monthly):
    """
    지금까지 쌓인 것을 돌려준다 — (원금, 이자, 현재 적용 수익률, 상품, 지시 후 경과개월).

    운용지시를 바꾼 적이 있으면 그 시점 잔액은 동결돼 있고, 그 뒤 기간에만
    새 수익률이 붙는다. 과거로 소급하지 않는다.
    """
    months = _elapsed_months(rec)
    doc = _doc()
    ch = _choices.get(credential_id)

    if ch:
        f = _fund(ch["fund"])
        rate = f["rate"]
        m_after = max(months - ch["since_month"], 0)
        locked_bal = ch["locked_principal"] + ch["locked_interest"]
        principal = ch["locked_principal"] + monthly * m_after
        interest = (ch["locked_interest"]
                    + _accrue(monthly, m_after, rate)
                    + _carry(locked_bal, m_after, rate))
        return principal, int(round(interest)), rate, f, m_after

    # 아직 이 세션에서 바꾼 적이 없다. 시드에 상품이 있으면 처음부터 그 상품이었다고 본다.
    fid = rec.get("fund")
    f = _fund(fid) if fid else None
    rate = f["rate"] if f else doc["default_rate"]
    principal = monthly * months
    interest = int(round(_accrue(monthly, months, rate)))
    return principal, interest, rate, f, months


def choose_fund(credential_id: str, fund_id: str, worker_name: str):
    """
    운용지시를 바꾼다. 바꾸는 순간의 잔액을 동결해 두어, 과거 수익이
    새 수익률로 다시 계산되지 않게 한다. 횟수 제한은 두지 않는다.
    """
    if not _fund(fund_id):
        return None
    rec = _record(worker_name)
    if not rec:
        return None
    wage = _monthly_wage(worker_name)
    if not wage:
        return None

    monthly = int(round(wage * CONTRIB_RATE))
    principal, interest, _rate, _f, _m = _accrued(credential_id, rec, monthly)

    _choices[credential_id] = {
        "fund": fund_id,
        "since_month": _elapsed_months(rec),
        "locked_principal": principal,
        "locked_interest": interest,
    }
    return fund_id


def status(credential_id: str, worker_name: str, visa_valid_until: str | None = None,
           visa_type: str | None = None) -> dict:
    rec = _record(worker_name)
    doc = _doc()

    # 고용허가제(E-9·H-2)는 퇴직급여가 출국만기보험으로 쌓인다. DC 대상이 아니다.
    # 사업장이 DC 를 운영하더라도 마찬가지다 — 화면은 departure.py 쪽을 보여 준다.
    if dep.applies_to(visa_type):
        return {
            "enrolled": False,
            "eps": True,
            "reason": "고용허가제(E-9·H-2)는 퇴직급여가 출국만기보험으로 쌓입니다.",
        }

    if not rec or not rec.get("dc_enrolled"):
        return {
            "enrolled": False,
            "eps": False,
            "reason": "사업장이 DC형 퇴직연금을 도입하지 않았습니다.",
        }

    wage = _monthly_wage(worker_name)
    if not wage:
        return {"enrolled": False, "eps": False, "reason": "급여 기준 정보가 없습니다."}

    months = _elapsed_months(rec)
    monthly = int(round(wage * CONTRIB_RATE))
    default_rate = doc["default_rate"]

    principal, interest, rate, f, _m_after = _accrued(credential_id, rec, monthly)
    balance = principal + interest

    # 귀국(체류 만료)까지 남은 개월. 비교는 전부 "앞으로 남은 기간" 기준이다.
    left = None
    if visa_valid_until:
        try:
            end = datetime.strptime(visa_valid_until, "%Y-%m-%d").date()
            today = datetime.now(timezone.utc).date()
            left = max((end.year - today.year) * 12 + (end.month - today.month), 0)
        except Exception:
            left = None

    projected = idle_projected = best_projected = None
    if left is not None:
        best_rate = max(x["rate"] for x in doc["funds"])
        projected = int(round(_project(balance, monthly, left, rate)))
        idle_projected = int(round(_project(balance, monthly, left, default_rate)))
        best_projected = int(round(_project(balance, monthly, left, best_rate)))

    return {
        "enrolled": True,
        "months": months,
        "months_to_leave": left,
        "projected_balance": projected,
        # 디폴트 상품에 그대로 두었을 때의 귀국 시점 예상액. 비교 기준선이다.
        "idle_projected_balance": idle_projected,
        "monthly_wage": wage,
        "monthly_contribution": monthly,
        "principal": principal,
        "interest": interest,
        "balance": balance,
        "rate": rate,
        "default_rate": default_rate,
        "fund": f and {k: f[k] for k in ("id", "name", "desc", "risk", "rate")},
        "chosen": bool(f),
        # ── 차이는 모두 "지금부터 귀국까지" 기준이다. 과거로 소급하지 않는다. ──
        "gain_vs_idle": None if projected is None else projected - idle_projected,
        "gain_vs_idle_max": None if best_projected is None else best_projected - idle_projected,
        "funds": doc["funds"],
        "authority": "real",
        # 화면이 그대로 보여 주는 안내 문구들
        "switch_notice": (
            "운용상품은 언제든 바꿀 수 있어요. 다만 기존 상품을 정리하고 새 상품을 사기까지 "
            "영업일이 걸리고, 원리금 보장 상품을 만기 전에 바꾸면 이율이 낮아질 수 있어요. "
            "바꾸기 전까지 쌓인 수익은 그대로 남습니다."
        ),
        "idle_notice": (
            "운용지시를 하지 않으면 2주 뒤 미리 정해 둔 상품(사전지정운용제도)으로 자동 편입돼요. "
            "이자가 아예 붙지 않는 건 아니지만, 그 상품이 내 상황에 맞는다는 보장은 없어요."
        ),
        # 이 문구는 DC 가입자에게만 보인다. 고용허가제 설명은 출국만기보험 화면이 맡으므로
        # 여기에 섞지 않는다 — 이 카드를 보는 사람에게는 해당 사항이 없다.
        "notice": (
            "사용자 부담금은 연간 임금총액의 1/12 이상입니다. 수익률과 금액은 시연용 예시이고 "
            "주휴수당을 넣지 않은 어림값입니다. 회사가 퇴직연금 제도를 도입한 경우에 적용됩니다."
        ),
    }


def balance_of(credential_id: str, worker_name: str):
    """관리자 콘솔의 근로자 목록에 쓰는 잔액 한 줄."""
    st = status(credential_id, worker_name)
    return st["balance"] if st.get("enrolled") else None
