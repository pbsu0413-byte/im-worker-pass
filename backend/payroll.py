"""
근태 -> 이번 달 근무일수 -> 예상 급여

**이 숫자는 회사 것이지 은행 것이 아니다.** 급여를 계산해 주는 게 아니라,
근로자가 자기 근태를 보고 "이번 달 대략 얼마"를 가늠하게 돕는 화면용 값이다.
그래서 4대보험 공제, 연장·야간 가산의 정확한 요율은 구현하지 않고
세전 총액만 낸다. 화면에도 공제 전 금액임을 항상 함께 표시한다.

시드(`seeds/attendance.json`)는 날짜 대신 '이번 달 근무일 순번'으로 적혀 있다.
달이 바뀌어도 같은 모양이 재현되고, 시연 중 실제로 찍은 기록은 이 위에 얹힌다.
"""

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

_SEEDS = Path(__file__).resolve().parent / "seeds"

OVERTIME_MULTIPLIER = 1.5      # 연장근로 가산 (근로기준법 제56조)
LATE_DEDUCT_MINUTES = 30       # 지각 1회 = 30분 미근무로 단순화


def _load(name: str) -> dict:
    with open(_SEEDS / name, encoding="utf-8") as f:
        return json.load(f)


def _row(seed_file: str, worker_name: str):
    for r in _load(seed_file)["records"]:
        if r["worker_name"] == worker_name:
            return r
    return None


def payroll_of(worker_name: str):
    return _row("payroll.json", worker_name)


def workdays_this_month(today: date | None = None) -> list[date]:
    """이번 달 1일부터 어제까지의 평일. 오늘은 아직 안 끝났으므로 제외한다."""
    today = today or datetime.now(timezone.utc).date()
    days, d = [], today.replace(day=1)
    while d < today:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    return days


def month_attendance(worker_name: str, today: date | None = None) -> dict:
    """시드 패턴을 이번 달 실제 날짜에 입혀 하루 단위 기록으로 펼친다."""
    pay = payroll_of(worker_name)
    seed = _row("attendance.json", worker_name)
    if not pay:
        return {"available": False, "reason": "PAYROLL_NOT_FOUND"}
    seed = seed or {"absent": [], "late": [], "overtime": []}

    absent = set(seed.get("absent", []))
    late = set(seed.get("late", []))
    extra = {o["i"]: o["hours"] for o in seed.get("overtime", [])}
    base = pay["daily_hours"]

    days = []
    for i, d in enumerate(workdays_this_month(today)):
        if i in absent:
            days.append({"date": d.isoformat(), "status": "absent", "hours": 0, "overtime": 0})
            continue
        ot = extra.get(i, 0)
        hours = base - (LATE_DEDUCT_MINUTES / 60 if i in late else 0)
        days.append({
            "date": d.isoformat(),
            "status": "late" if i in late else "present",
            "hours": round(hours, 2),
            "overtime": ot,
        })
    return {"available": True, "days": days, "payroll": pay}


def month_summary(worker_name: str, live_records: list | None = None,
                  today: date | None = None) -> dict:
    """
    시드 근태 + 시연 중 실제로 찍은 기록을 합친 이번 달 요약.
    live_records 는 attendance._records 에서 넘어온 이 사람의 완료된 교대들이다.
    """
    m = month_attendance(worker_name, today)
    if not m["available"]:
        return m
    pay = m["payroll"]

    worked = [d for d in m["days"] if d["status"] != "absent"]
    base_hours = sum(d["hours"] for d in worked)
    ot_hours = sum(d["overtime"] for d in worked)

    live_days, live_minutes = 0, 0
    for r in (live_records or []):
        if r.get("worked_minutes"):
            live_days += 1
            live_minutes += r["worked_minutes"]
    live_hours = round(live_minutes / 60, 2)

    wage = pay["hourly_wage"]
    gross = int(round(wage * (base_hours + live_hours)
                      + wage * OVERTIME_MULTIPLIER * ot_hours))

    return {
        "available": True,
        "month": (today or datetime.now(timezone.utc).date()).strftime("%Y-%m"),
        "site_id": pay["site_id"],
        "job_title": pay["job_title"],
        "hourly_wage": wage,
        "workdays": len(worked) + live_days,
        "absent_days": sum(1 for d in m["days"] if d["status"] == "absent"),
        "late_days": sum(1 for d in m["days"] if d["status"] == "late"),
        "base_hours": round(base_hours + live_hours, 2),
        "overtime_hours": ot_hours,
        "live_days": live_days,          # 시연 중 새로 찍힌 것 (서버 재시작 시 사라짐)
        "estimated_gross_pay": gross,
        "authority": "mock",
        "notice": "공제 전 세전 총액입니다. 실제 급여는 회사 급여명세가 기준입니다.",
    }
