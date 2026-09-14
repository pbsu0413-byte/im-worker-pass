"""
금융상품 추천 (iM금융지주 종합 서비스)

지갑이 이미 아는 값 — 체류 만료일, 재직 여부, 급여일 — 에서 조건을 뽑아
지금 의미 있는 상품만 카드로 올린다. 상품을 새로 만드는 것이 아니라
**이미 있는 상품을 외국인 근로자 상황에 맞게 엮는다.**

① 환율 보장 송금
   근로자는 "다음 달 1,400원 보장"만 본다. 뒤에서는 같은 달 같은 통화로 나갈
   송금을 한 덩어리로 묶어 헷지 포지션을 잡는다. 개인 50만원은 최소 계약
   단위도 안 되지만 수백 명이면 규모가 나온다. **그 수요 예측이 지갑에서 나온다.**
   근로자는 파생 계약 당사자가 아니라 은행과 단순 예약 계약을 맺는다 —
   파생은 지주 내부(iM증권)에 머문다.

② 귀국 목표 적금
   만기를 **체류 만료일에 자동으로 맞춘다.** 본국 통화는 은행이 취급하지 않는
   경우가 많아 달러 기준이다. 본인 귀책이 아닌 조기 출국이면 지갑이 그 사유를
   증명하므로 우대 해지가 가능하다 — 다른 은행은 확인할 방법이 없어 못 하는 조건.

수치는 모두 시연용 가정값이다. 실서비스에서는 시세·계좌 입금 내역을 읽는다.
"""

import json
import os
from datetime import datetime, timezone

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")
_fx_cache = None


def _currencies():
    """국적별 송금 통화와 헷지 등급."""
    global _fx_cache
    if _fx_cache is None:
        with open(os.path.join(SEED_DIR, "currencies.json"), encoding="utf-8") as f:
            doc = json.load(f)
        doc["_index"] = {r["nationality"]: r for r in doc["records"]}
        _fx_cache = doc
    return _fx_cache


def currency_of(nationality: str):
    return _currencies()["_index"].get(nationality)


# 헷지 수수료 (등급별). 시연용 가정값.
HEDGE_FEE = {"A": 10000, "B": 20000}
MIN_REMIT_FOR_HEDGE = 300000      # 이보다 적게 보내면 기대 절감이 수수료보다 작다
DEFAULT_MONTHLY_REMIT = 800000    # 월 송금액 가정 (E-9 평균 소득의 절반 남짓)

PAYDAY = 25                  # 급여일 가정
PAYDAY_WINDOW = 3            # 급여일 며칠 전부터 띄울지
SAVINGS_MIN_DAYS = 180       # 적금은 만기까지 이만큼 남아야 의미가 있다
SAVINGS_DEFAULT_MONTHLY = 300000
SAVINGS_RATE = 0.030         # 연 3.0% 가정


def _today():
    return datetime.now(timezone.utc).date()


def _days_until(date_str):
    if not date_str:
        return None
    try:
        return (datetime.strptime(date_str, "%Y-%m-%d").date() - _today()).days
    except Exception:
        return None


def _days_to_payday():
    t = _today()
    if t.day <= PAYDAY:
        return PAYDAY - t.day
    # 다음 달 급여일까지
    nxt = (t.replace(day=1).replace(month=t.month % 12 + 1,
                                    year=t.year + (1 if t.month == 12 else 0)))
    return (nxt.replace(day=PAYDAY) - t).days


def hedge_tier(cred: dict, monthly_remit: int = DEFAULT_MONTHLY_REMIT):
    """
    3단계 판정.
      A : 자국통화가 달러에 붙어 있다 -> 원화-달러만 고정해도 사실상 완전 헷지. 싸다.
      B : 자국통화가 따로 움직인다 -> 달러만 고정하면 절반만 막힌다. 크로스 보장이 필요하고 비싸다.
      C : 송금액이 작아 기대 절감이 수수료보다 작다 -> 권하지 않는다.

    **안 팔아야 할 사람에게 안 파는 것**이 이 판정의 핵심이다.
    """
    fx = currency_of(cred.get("nationality"))
    if not fx:
        return None

    # 기대 절감 = 송금액 × 변동폭의 절반 (한 방향으로 벗어날 기대치)
    expected_saving = int(monthly_remit * (fx["swing_6m_pct"] / 100) / 2)
    tier = fx["tier"]
    fee = HEDGE_FEE.get(tier, 0)

    if monthly_remit < MIN_REMIT_FOR_HEDGE or expected_saving < fee:
        tier, fee = "C", 0

    return {
        "tier": tier,
        "fee": fee,
        "currency": fx["currency"],
        "currency_name": fx["currency_name"],
        "usd_linked": fx["usd_linked"],
        "swing_6m_pct": fx["swing_6m_pct"],
        "own_vol_pct": fx["own_vol_pct"],
        "unit_per_krw": fx["unit_per_krw"],
        "monthly_remit": monthly_remit,
        "expected_saving": expected_saving,
        "tier_note": _currencies()["_tiers"][tier],
    }


def _remittance_card(cred, force=False):
    """재직 중이고 급여일이 가까울 때. 등급에 따라 카드 내용이 갈린다."""
    left = _days_to_payday()
    if left > PAYDAY_WINDOW and not force:
        return None

    h = hedge_tier(cred)
    if not h:
        return None

    amount = h["monthly_remit"]
    unit = h["unit_per_krw"]
    recv = amount * unit
    swing_amount = recv * h["swing_6m_pct"] / 100
    cur = h["currency_name"]

    def fmt(v):
        return f"{v:,.0f}" if v >= 100 else f"{v:,.2f}"

    if h["tier"] == "A":
        title = "다음 달 송금, 금액을 미리 정해둘까요?"
        lead = f"수수료 {h['fee']:,}원 · 다음 달에도 같은 금액이 도착합니다"
        verdict = "권장"
    elif h["tier"] == "B":
        title = f"{cur} 환율이 자주 바뀝니다"
        lead = f"수수료 {h['fee']:,}원 · 다음 달에도 같은 금액이 도착합니다"
        verdict = "권장"
    else:
        title = "환율 보장은 필요하지 않습니다"
        lead = "그냥 보내셔도 됩니다"
        verdict = "권하지 않음"

    rows = [
        {"label": "보내는 금액", "value": f"{amount:,}원"},
        {"label": "가족이 받는 금액", "value": f"약 {fmt(recv)} {h['currency']}"},
        {"label": "지난 6개월 차이", "value": f"최대 {fmt(swing_amount)} {h['currency']}"},
    ]
    if h["tier"] != "C":
        rows.append({"label": "보장 수수료", "value": f"{h['fee']:,}원"})

    if h["tier"] == "A":
        detail = (
            f"{cur}는 달러에 거의 붙어 움직입니다(대달러 변동 {h['own_vol_pct']}%). "
            "받는 금액이 흔들리는 것은 대부분 원화가 움직이기 때문이며, "
            "원화-달러 사이만 고정하면 사실상 전부 막힙니다. 시장이 깊어 수수료가 낮습니다."
        )
    elif h["tier"] == "B":
        detail = (
            f"{cur}는 달러와 따로 움직입니다(대달러 변동 {h['own_vol_pct']}%). "
            "달러만 고정하면 원화-달러 구간만 막히고 "
            f"달러-{cur} 구간은 그대로 열려 있어 절반만 막히는 셈입니다. "
            "그래서 원화-{cur} 직접 보장이 필요하며, 시장이 얕아 수수료가 높습니다. "
            "같은 국적 송금 예정자를 모아 처리하므로 개인 단가가 낮아집니다."
        ).replace("{cur}", cur)
    else:
        detail = (
            f"{cur}의 최근 6개월 변동폭이 작고 송금액도 크지 않아, "
            "수수료를 내고 보장받는 것보다 그냥 보내는 편이 낫습니다."
        )

    return {
        "id": "fx_guaranteed_remittance",
        "kind": verdict,
        "tier": h["tier"],
        "title": title,
        "lead": lead,
        "why": f"급여일 D-{left}" if left else "오늘 급여일",
        "rows": rows,
        "detail": detail,
        "note": (
            "보장 환율은 현재 환율보다 다소 불리하게 제시됩니다. 오를 때의 이익을 포기하는 대신 "
            "내릴 때의 손실을 막는 구조입니다. 근로자는 파생상품이 아니라 은행과 예약 계약을 맺습니다."
            if h["tier"] != "C" else
            "판정은 국적별 통화 성격과 송금액으로 계산됩니다. 필요하지 않을 때는 권하지 않습니다."
        ),
        "engine": (
            "같은 달 같은 통화로 나갈 송금을 모아 iM증권이 합산 포지션으로 처리합니다. "
            "개인 단위로는 최소 계약 규모가 나오지 않지만, 지갑이 재직 인원·급여일·체류 잔여기간을 "
            "알고 있어 다음 달 송금 규모를 예측할 수 있습니다."
        ),
        "cta": "환율 보장 신청" if h["tier"] != "C" else "그냥 보내기",
    }


def _savings_card(cred, enrolled, force=False):
    """체류 만료까지 충분히 남았고 아직 가입하지 않았을 때."""
    if enrolled and not force:
        return None
    left = _days_until(cred.get("visa_valid_until"))
    if left is None:
        return None
    if left < SAVINGS_MIN_DAYS and not force:
        return None
    left = max(left, SAVINGS_MIN_DAYS) if force else left

    months = max(left // 30, 1)
    monthly = SAVINGS_DEFAULT_MONTHLY
    principal = monthly * months
    # 적립식 단리 근사 — 시연용 예시값이다
    interest = int(principal * SAVINGS_RATE * (months + 1) / 24)
    total = principal + interest

    # 목표 금액을 직접 정할 수 있게 계산 파라미터를 같이 내려준다.
    # 화면에서 슬라이더를 끌면 월 납입이 역산된다.
    factor = 1 + SAVINGS_RATE * (months + 1) / 24      # 총수령액 = 원금 × factor
    calc = {
        "months": months,
        "rate": SAVINGS_RATE,
        "factor": round(factor, 6),
        "monthly_min": 100000,
        "monthly_max": 1500000,
        "monthly_step": 10000,
        "monthly_default": monthly,
        "target_min": int(round(100000 * months * factor, -5)),
        "target_max": int(round(1500000 * months * factor, -5)),
        "target_step": 100000,
        "target_default": int(round(total, -4)),
    }

    return {
        "id": "return_goal_savings",
        "kind": "권유",
        "title": "적금을 드시겠습니까?",
        "lead": f"만기 {cred.get('visa_valid_until')} · 체류 만료일에 자동으로 맞췄습니다",
        "why": f"체류 만료까지 {left}일 ({months}개월)",
        "rows": [
            {"label": "만기일", "value": f"{cred.get('visa_valid_until')} (체류 만료일)"},
            {"label": "적립 기간", "value": f"{months}개월"},
            {"label": "적용 금리 (예시)", "value": f"연 {SAVINGS_RATE * 100:.1f}%"},
        ],
        "calc": calc,
        "options": [
            {"id": "fx_guard", "label": "만기 송금분 환율 보장 함께 적용"},
        ],
        "note": (
            "달러 기준으로 적립합니다. 본국 통화는 예금으로 취급되지 않는 경우가 많습니다. "
            "본인 귀책이 아닌 조기 출국(사업장 폐업·체류자격 변경 등)이면 지갑이 그 사유를 "
            "증명해 우대 해지가 적용됩니다. 이자율과 금액은 시연용 예시입니다."
        ),
        "engine": (
            "지갑이 체류 만료일을 알고 있어 만기를 따로 설정할 필요가 없습니다. "
            "운용은 iM에셋자산운용, 만기 송금은 iM뱅크로 이어집니다."
        ),
        "cta": "이 조건으로 적금 가입",
    }


def recommend(cred: dict, enrolled_savings: bool = False, force: bool = False):
    """
    조건에 맞는 카드만, 우선순위 순으로.
    force=True 는 **시연 전용** — 조건을 무시하고 모든 카드를 보여준다.
    실제 노출은 조건을 그대로 따른다.
    """
    cards = [c for c in (_remittance_card(cred, force),
                         _savings_card(cred, enrolled_savings, force)) if c]
    return {
        "cards": cards,
        "hedge": hedge_tier(cred),
        "payday": PAYDAY,
        "days_to_payday": _days_to_payday(),
        "forced": force,
    }
