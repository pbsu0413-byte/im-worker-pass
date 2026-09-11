"""
출퇴근 (자리 4) — 지갑을 매일 쓰는 자리

새 크리덴셜을 발행하지 않는다. 이미 만들어둔 것을 그대로 쓴다.
  · 단말 키 서명    -> 본인 확인. 지갑이 은행 앱 안에 있으므로 대리 출근은
                       급여계좌 비밀번호를 넘기는 일이 된다. 불가능은 아니지만 비용이 크다.
  · 온체인 상태 조회 -> 체류자격이 취소되면 내일 아침 출근이 막힌다. 읽기라 가스 0원.

**근태 기록은 회사 것이다.** 시각을 찍고 보관하는 주체는 회사 근태 시스템이고,
은행은 "이 사람이 유효한가"만 답하고 빠진다. 근무 시각은 은행에 남지 않는다.

근태 조작 방지(양방 서명·온체인 앵커링)는 의도적으로 범위 밖에 둔다.
Why: 이 서비스를 도입할지 정하는 것은 사업주다. 은행이 사업주를 감시하는 도구를
팔면 도입 자체가 되지 않는다. 여기서 푸는 문제는 근로감독이 아니라 **고용 적격 여부**다.
"""

import secrets
from datetime import datetime, timedelta, timezone

OPEN_SHIFT_HOURS = 16      # 야간 교대: 출근이 열려 있으면 다음 스캔은 무조건 퇴근

SITES = {
    "SCANNER-BIZ-001": {"site_id": "BIZ-001", "site_name": "A제조 (주)대구정밀"},
    "SCANNER-BIZ-002": {"site_id": "BIZ-002", "site_name": "B제조 (주)구미사출"},
}

_records = {}      # record_id -> 근태 기록 (회사 근태 시스템)


def site_of(scanner_id: str):
    return SITES.get(scanner_id)


def open_shift(credential_id: str, site_id: str):
    """퇴근을 아직 안 찍은 출근 기록. 16시간이 지나면 자동으로 닫는다."""
    now = datetime.now(timezone.utc)
    for r in _records.values():
        if (r["credential_id"] == credential_id and r["site_id"] == site_id
                and r["check_type"] == "in" and not r["closed"]):
            if now - datetime.fromisoformat(r["server_time"]) <= timedelta(hours=OPEN_SHIFT_HOURS):
                return r
            r["closed"] = True
    return None


def record_scan(credential_id: str, worker_name: str, scanner_id: str):
    """
    스캐너가 QR을 읽은 순간. **시각은 회사 근태 시스템이 찍는다** — 폰 시계는 쓰지 않는다.
    첫 스캔이면 출근, 열린 출근이 있으면 퇴근.
    """
    site = SITES.get(scanner_id)
    if not site:
        return None, "UNKNOWN_SCANNER"

    prev = open_shift(credential_id, site["site_id"])
    now = datetime.now(timezone.utc)

    rid = "ATT-" + secrets.token_hex(4).upper()
    row = {
        "record_id": rid,
        "credential_id": credential_id,
        "worker_name": worker_name,
        "site_id": site["site_id"],
        "site_name": site["site_name"],
        "scanner_id": scanner_id,
        "check_type": "out" if prev else "in",
        "server_time": now.isoformat(),
        "closed": bool(prev),
        "paired_with": prev["record_id"] if prev else None,
        "worked_minutes": None,
    }
    if prev:
        prev["closed"] = True
        prev["paired_with"] = rid
        row["worked_minutes"] = int(
            (now - datetime.fromisoformat(prev["server_time"])).total_seconds() // 60)

    _records[rid] = row
    return row, None


def records_of(site_id: str):
    rows = [r for r in _records.values() if r["site_id"] == site_id]
    rows.sort(key=lambda r: r["server_time"], reverse=True)
    return rows


def today_summary(site_id: str):
    """오늘 기준 현황. 회사 화면 상단에 띄운다."""
    today = datetime.now(timezone.utc).date().isoformat()
    rows = [r for r in _records.values()
            if r["site_id"] == site_id and r["server_time"][:10] == today]
    working = len({r["credential_id"] for r in rows if r["check_type"] == "in" and not r["closed"]})
    return {
        "date": today,
        "scans": len(rows),
        "check_in": sum(1 for r in rows if r["check_type"] == "in"),
        "check_out": sum(1 for r in rows if r["check_type"] == "out"),
        "currently_working": working,
    }
