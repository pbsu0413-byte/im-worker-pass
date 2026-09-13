"""
귀국 목표 적금 — 가입 기록과 현재 상태

카드를 지갑에 쌓지 않는다는 원칙은 여기서도 같다. 가입 사실은 **은행 원천 기록**에
남고, 패스포트 홈은 제출이 아니라 조회로 그 값을 읽어 보여줄 뿐이다.

만기는 체류 만료일이다. 지갑이 이미 그 날짜를 알고 있어 근로자가 따로 정하지
않는다 — 이것이 다른 은행이 흉내 낼 수 없는 조건이다.

이자 계산식은 products.py 와 같은 것을 쓴다. 두 화면이 다른 숫자를 말하면
심사에서 바로 드러난다.
"""

import json
import os
from datetime import datetime, timezone

from products import SAVINGS_RATE

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")

# 시연 중 새로 가입한 건. 서버를 다시 켜면 사라지고 시드만 남는다.
_enrollments = {}


def _seed_rows():
    with open(os.path.join(SEED_DIR, "savings.json"), encoding="utf-8") as f:
        return json.load(f)["records"]


def _months_between(y1, m1, y2, m2):
    return (y2 - y1) * 12 + (m2 - m1)


def _add_months(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return d.replace(year=y, month=m, day=1)


def enroll(credential_id: str, worker_name: str, monthly: int,
           auto_remit: bool = False, fx_guard: bool = False):
    """시연 중 가입. 이번 달부터 넣기 시작한 것으로 본다."""
    row = {
        "worker_name": worker_name,
        "monthly": int(monthly),
        "start_months_ago": 0,
        "auto_remit": bool(auto_remit),
        "fx_guard": bool(fx_guard),
        "enrolled_now": True,
        "enrolled_at": datetime.now(timezone.utc).isoformat(),
    }
    _enrollments[credential_id] = row
    return row


def _record_of(credential_id: str, worker_name: str):
    if credential_id in _enrollments:
        return _enrollments[credential_id]
    for r in _seed_rows():
        if r["worker_name"] == worker_name:
            return r
    return None


def status(credential_id: str, worker_name: str, visa_valid_until: str | None):
    """
    가입하지 않았으면 {"enrolled": False}. 가입했으면 지금까지 쌓인 금액과
    만기 예상액을 낸다. 둘 다 화면에 '예시'임을 함께 적는다.
    """
    rec = _record_of(credential_id, worker_name)
    if not rec:
        return {"enrolled": False}

    today = datetime.now(timezone.utc).date()
    start = _add_months(today.replace(day=1), -int(rec.get("start_months_ago", 0)))

    maturity = None
    months_total = None
    if visa_valid_until:
        try:
            maturity = datetime.strptime(visa_valid_until, "%Y-%m-%d").date()
            months_total = max(_months_between(start.year, start.month,
                                               maturity.year, maturity.month), 1)
        except Exception:
            maturity = None

    monthly = int(rec["monthly"])
    paid_months = max(int(rec.get("start_months_ago", 0)), 0) + 1   # 이번 달 포함
    accrued = monthly * paid_months

    out = {
        "enrolled": True,
        "enrolled_now": bool(rec.get("enrolled_now")),
        "monthly": monthly,
        "start_month": start.strftime("%Y-%m"),
        "paid_months": paid_months,
        "accrued": accrued,
        "auto_remit": bool(rec.get("auto_remit")),
        "fx_guard": bool(rec.get("fx_guard")),
        "rate": SAVINGS_RATE,
        "authority": "real",
        "notice": "이자율과 금액은 시연용 예시입니다.",
    }
    if maturity and months_total:
        factor = 1 + SAVINGS_RATE * (months_total + 1) / 24
        out.update({
            "maturity_date": maturity.isoformat(),
            "months_total": months_total,
            "months_left": max(months_total - paid_months, 0),
            "expected_total": int(round(monthly * months_total * factor)),
        })
    return out
