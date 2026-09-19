"""
출국만기보험 — E-9·H-2 의 퇴직급여

고용허가제 근로자에게 퇴직급여는 퇴직연금이 아니라 **출국만기보험**으로 쌓인다.
근거는 「외국인근로자의 고용 등에 관한 법률」 제13조와 같은 법 시행령 제21조다.

  · **사업주가 의무로 가입**하고 매달 월 통상임금의 1/12(약 8.3%)을 납입한다.
  · 근로자가 고를 것이 없다. 보험이라 **운용지시라는 개념 자체가 없다.**
    사업장이 DC형 퇴직연금을 운영하더라도 E-9·H-2 는 그 대상이 아니다.
  · **보험금은 출국한 날부터 14일 이내**에 지급된다(2014년 개정).
    체류자격 변경·사망 등으로 계속 머무는 경우는 신청일부터 14일 이내다.
  · 근속 1년 미만으로 끝나면 보험금은 근로자가 아니라 **사용자**가 받는다
    (시행령 제21조 제2항 단서).
  · **보험금이 법정 퇴직금에 미치지 못하면 사용자가 그 차액을 지급해야 한다**
    (시행령 제21조 제3항).

### ⛔ 법정 퇴직금과의 "부족분"은 계산하지 않는다 (2026-09-19 결정)
보험료는 통상임금의 8.3%로 쌓이고 법정 퇴직금은 평균임금 30일분이라 두 값은 다를 수 있다.
한때 그 차이를 "얼마가 모자랍니다"로 계산해 보여 줬으나 **전부 걷어냈다.** 이유는 셋이다.

  1. 은행 앱이 근로자에게 "당신 회사가 돈을 덜 줬다"고 말하는 구조가 된다.
     이 서비스는 사업장과 계약해 근로자가 따라오는 구조다. employer.py 에 적어 둔
     원칙 — "은행이 사업주를 감시하는 도구를 팔면 도입 자체가 되지 않는다" — 과 정면으로 어긋난다.
  2. 계산이 근사다. 주휴수당도 담고 있지 않다(payroll.py 참조). 틀린 금액으로
     노사 분쟁이 붙으면 그 책임이 이 화면에 온다.
  3. 판단은 근로감독관과 당사자가 할 일이지 은행이 끼어들 자리가 아니다.

대신 **"기준이 다를 수 있으니 퇴직 전에 확인해 보시라"**고만 말한다. 알아야 할 사실은
그대로 전달되면서 누구도 탓하지 않는다. 되살리자는 말이 나오면 이 세 줄을 먼저 꺼낼 것.

적립이율은 시연용 가정값이고, 금액은 주휴수당을 담지 않은 어림값이다.
"""

import json
import os
from datetime import datetime, timezone

import payroll as pay

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")

CONTRIB_RATE = 1 / 12          # 월 통상임금의 1/12 (약 8.3%)
WORKDAYS_PER_MONTH = 21.7      # 월 통상임금 환산용 가정값 (pension.py 와 동일)
OVERTIME_MULTIPLIER = 1.5      # 근로기준법 제56조
INSURED_RATE = 0.01            # 보험 적립이율 — 시연용 가정값
PAY_WITHIN_DAYS = 14           # 출국일부터 14일 이내 지급

# 이 제도가 적용되는 체류자격. 나머지는 일반 근로자와 같이 퇴직급여법을 따른다.
EPS_VISAS = ("E-9", "H-2")


def applies_to(visa_type: str | None) -> bool:
    """고용허가제 체류자격인가. E-9·H-2 만 출국만기보험 대상이다."""
    return str(visa_type or "").upper().startswith(EPS_VISAS)


def _seed(name):
    with open(os.path.join(SEED_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def _row(name, worker_name):
    for r in _seed(name)["records"]:
        if r["worker_name"] == worker_name:
            return r
    return None


def _months_between(start, end):
    return max((end.year - start.year) * 12 + (end.month - start.month), 0)


def status(worker_name: str, visa_type: str | None,
           visa_valid_until: str | None = None) -> dict:
    if not applies_to(visa_type):
        return {
            "applies": False,
            "reason": "고용허가제(E-9·H-2) 체류자격이 아닙니다.",
        }

    p = pay.payroll_of(worker_name)
    if not p or not p.get("joined_date"):
        return {"applies": False, "reason": "급여 기준 정보가 없습니다."}

    today = datetime.now(timezone.utc).date()
    joined = datetime.strptime(p["joined_date"], "%Y-%m-%d").date()
    months = _months_between(joined, today)
    years = months / 12

    # 월 통상임금 — 보험료의 기준
    ordinary = int(round(p["hourly_wage"] * p["daily_hours"] * WORKDAYS_PER_MONTH))
    premium = int(round(ordinary * CONTRIB_RATE))

    principal = premium * months
    interest = int(round(principal * INSURED_RATE * (months + 1) / 24))
    balance = principal + interest

    # 귀국(체류 만료)까지 계속 일했을 때
    left = None
    projected = None
    if visa_valid_until:
        try:
            end = datetime.strptime(visa_valid_until, "%Y-%m-%d").date()
            left = _months_between(today, end)
            tm = months + left
            pr = premium * tm
            projected = pr + int(round(pr * INSURED_RATE * (tm + 1) / 24))
        except Exception:
            left = None

    return {
        "applies": True,
        "months": months,
        "months_to_leave": left,
        "joined_date": p["joined_date"],
        "monthly_ordinary_wage": ordinary,
        "monthly_premium": premium,
        "principal": principal,
        "interest": interest,
        "balance": balance,
        "projected_balance": projected,
        "under_one_year": months < 12,
        "pay_within_days": PAY_WITHIN_DAYS,
        "authority": "real",
        # 화면이 그대로 쓰는 문구들
        "how_notice": (
            "회사가 매달 통상임금의 8.3%를 출국만기보험에 넣어 드려요. "
            "보험이라 고르실 상품은 없고, 쌓이는 동안 따로 하실 일도 없어요."
        ),
        "pay_notice": (
            f"보험금은 한국을 떠난 날부터 {PAY_WITHIN_DAYS}일 이내에 받으실 수 있어요. "
            "출국 전에 본국에서 쓰실 계좌를 등록해 두세요. "
            "체류자격을 바꿔 계속 머무르시면 신청일부터 같은 기간 안에 받으세요."
        ),
        # 누구를 탓하지 않고 "확인해 보시라"까지만 말한다. 위 머리말의 결정 참조.
        "basis_notice": (
            "보험금은 통상임금을 기준으로 쌓여요. 실제 퇴직급여는 평균임금을 기준으로 계산해서 "
            "금액이 다를 수 있으니, 퇴직하시기 전에 보험사 통지서와 회사 급여명세를 함께 확인해 보세요."
        ),
        "under_one_year_notice": (
            "아직 1년이 되지 않았어요. 1년을 채우지 못하고 그만두시면 "
            "이 보험금은 근로자가 아니라 회사가 받게 돼요."
        ),
        "notice": (
            "외국인근로자의 고용 등에 관한 법률 제13조에 따른 출국만기보험입니다. "
            "주휴수당을 넣지 않은 어림값이고 적립이율도 시연용 가정값이라, "
            "실제 금액은 보험사 통지서와 회사 급여명세가 기준입니다."
        ),
    }
