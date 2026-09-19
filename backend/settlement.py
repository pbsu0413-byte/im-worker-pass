"""
귀국정산 — 돌아갈 때 손에 쥐는 돈

퇴직연금·출국만기보험은 넣지 않는다. 고용허가제(E-9·H-2)에서 퇴직급여는
출국만기보험이 갈음하도록 설계돼 있어 퇴직연금 DC/DB 는 표준 경로가 아니고,
이 프로토타입의 범위는 **은행이 직접 제공하는 상품**이기 때문이다.

급여도 합산하지 않는다. 남은 기간의 급여는 생활비로 쓰이는 돈이라
"귀국할 때 가져가는 금액"에 더하면 실제보다 부풀려진다. 남은 근무 기간만
참고로 보여준다.

환산 환율은 seeds/currencies.json 의 가정값이다. 실서비스에서는 고시환율을 읽는다.

### ⛔ 프로토타입 범위 — 세전이고, 빠진 항목이 있다
  · 적금 만기액은 **이자소득세 15.4% 를 빼기 전** 금액이다(savings.py 참조).
  · **국민연금 반환일시금**을 더하지 않는다. 외국인 근로자도 사업장가입자로
    국민연금에 들고, 국외이주 시 본인 청구로 반환일시금을 받을 수 있다
    (수급권 발생일부터 5년 이내). 다만 받을 수 있는지는 **국가별로 갈리므로**
    (상호주의·사회보장협정) 시연에서 단정하지 않고 빼 두었다.
  · **귀국비용보험금**(외고법 제15조)도 넣지 않는다. E-9·H-2 가 본인 부담으로
    가입하는 별도 보험이다.
이 셋은 실제로는 귀국할 때 손에 쥐는 돈에 들어간다 — 넣으면 금액이 늘어난다.
"""

from datetime import datetime, timezone

from products import currency_of


def _d(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def build(cred: dict, savings: dict) -> dict:
    """savings 는 savings.status() 결과를 그대로 받는다."""
    today = datetime.now(timezone.utc).date()
    leave = _d(cred.get("visa_valid_until"))
    fx = currency_of(cred.get("nationality"))

    days_left = (leave - today).days if leave else None
    out = {
        "leave_date": leave.isoformat() if leave else None,
        "days_left": days_left,
        "months_left": (days_left // 30) if days_left is not None else None,
        "basis": "체류 만료일 기준입니다. 연장·이직으로 바뀌면 이 날짜도 함께 바뀝니다.",
    }

    amount = savings.get("expected_total") if savings.get("enrolled") else 0
    out["savings_total"] = amount
    out["enrolled"] = bool(savings.get("enrolled"))
    out["fx_guard"] = bool(savings.get("fx_guard"))

    if fx and amount:
        out["home"] = {
            "currency": fx["currency"],
            "currency_name": fx["currency_name"],
            "amount": round(amount * fx["unit_per_krw"], 2),
            "unit_per_krw": fx["unit_per_krw"],
            "swing_6m_pct": fx["swing_6m_pct"],
            # 환율이 6개월 변동폭만큼 불리하게 움직였을 때 줄어드는 금액
            "downside": round(amount * fx["unit_per_krw"] * (1 - fx["swing_6m_pct"] / 100), 2),
        }
    out["notice"] = (
        "환율 보장을 적용해 두어 만기 환율이 미리 고정됩니다."
        if out["fx_guard"] else
        "환율은 만기 시점에 정해집니다. 환율 보장을 적용하면 지금 고정할 수 있습니다."
    )
    return out
