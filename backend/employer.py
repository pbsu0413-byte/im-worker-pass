"""
사업장·은행 콘솔 (B2B2C)

**회사용 대시보드는 만들지 않는다.**
회사는 이미 인사시스템이 있고 근로자 명단·체류 만료일을 안다. 회사가 이 서비스에서
얻는 것은 **일이 줄어드는 것**이지 새 화면이 아니다 — 지금 인사담당자가 하는
금융 민원 창구 노릇(계좌 개설 동행, 송금 방법 설명, 서류 통역, 보험 조회 대행)이
근로자 앱으로 넘어간다. 그 혜택은 계약 제안서로 말할 것이지 대시보드로 증명할 게 아니고,
들여다봐야 할 화면이 하나 더 생기면 그것 자체가 일이다.

그래서 이 모듈은 **은행 영업담당자 화면 하나만** 만든다. 개인은 보이지 않고
국적별 인원 집계에서 규모만 계산한다. 근태 스캐너는 대시보드가 아니라 공장 입구에
설치된 장치이므로 별개로 남는다.

이 서비스는 근로자 한 명씩 모으는 구조가 아니다. **사업장 한 곳과 계약하면
근로자 수백 명이 한 번에 온다.** 그래서 이 화면이 사업 모델의 중심이다.

사업장에 주는 것: 관리해야 할 사람이 자동으로 추려진다(체류 만료 임박, 건강진단
기한 경과, 사업장 변경 신청기한). 지금은 회사가 일일이 챙기거나 아예 모르고 있다가
과태료를 맞는 영역이다.

은행에 생기는 것: ① 급여계좌 수백 개 ② **환율보장보험에 필요한 보장 규모** — 개인 50만원은
최소 계약 단위가 안 되지만 같은 급여일에 같은 통화로 나가는 300명분은 보험 포트폴리오 규모가 된다
③ 법인 접점 — 급여이체에서 기업계좌·외환·운전자금으로 이어지는 경로.
"""

import json
import os
from datetime import datetime, timezone

import products

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")
_cache = None
FX_GUARD_PREMIUM_RATE = 0.008  # 환율보장보험 예상 보험료율. 시연용 가정값.


def _employers():
    global _cache
    if _cache is None:
        with open(os.path.join(SEED_DIR, "employers.json"), encoding="utf-8") as f:
            doc = json.load(f)
        doc["_index"] = {r["site_id"]: r for r in doc["records"]}
        _cache = doc
    return _cache


def list_sites():
    return [{k: r[k] for k in ("site_id", "site_name", "industry", "location",
                               "foreign_employees")} for r in _employers()["records"]]


def _days_until(d):
    if not d:
        return None
    try:
        return (datetime.strptime(d, "%Y-%m-%d").date()
                - datetime.now(timezone.utc).date()).days
    except Exception:
        return None


def _fx_guard_summary(site, tiers, hedge_people):
    """은행 콘솔용 환율보장보험 규모 요약. 모두 집계값이며 개인은 표시하지 않는다."""
    coverage_monthly = tiers["A"]["amount"] + tiers["B"]["amount"]
    coverage_annual = coverage_monthly * 12
    premium_rate = site.get("fx_guard_premium_rate", FX_GUARD_PREMIUM_RATE)
    premium_monthly = int(round(coverage_monthly * premium_rate))
    premium_annual = premium_monthly * 12
    ratio = (hedge_people / site["foreign_employees"] * 100) if site["foreign_employees"] else 0
    return {
        "product": "환율보장보험",
        "covered_people": hedge_people,
        "coverage_monthly": coverage_monthly,
        "coverage_annual": coverage_annual,
        "premium_rate_pct": round(premium_rate * 100, 2),
        "premium_monthly": premium_monthly,
        "premium_annual": premium_annual,
        "covered_ratio_pct": round(ratio, 1),
        "new_registration_demo_excluded": True,
    }


def _attention(site, local_db):
    """관리가 필요한 근로자. 시드의 실명 근로자 중 이 사업장 소속만."""
    out = []
    today = datetime.now(timezone.utc).date().isoformat()
    for cred in local_db.values():
        if cred.get("employer_name") != site["site_name"]:
            continue
        items = []
        if cred.get("visa_status") not in (None, "유효"):
            items.append(f"체류자격 {cred['visa_status']}")
        visa_left = _days_until(cred.get("visa_valid_until"))
        if visa_left is not None and visa_left <= 90:
            items.append(f"체류 만료 D-{visa_left}" if visa_left >= 0 else "체류 만료 경과")
        hc = cred.get("health_check_valid_until")
        if not hc:
            items.append("건강진단 기록 없음")
        elif hc < today:
            items.append(f"건강진단 기한 경과 ({hc})")
        end_left = _days_until(cred.get("employment_to"))
        if end_left is not None and -30 <= end_left <= 7:
            items.append("계약 종료 · 사업장 변경 신청기한 임박")
        if items:
            out.append({
                "worker_name": cred.get("worker_name"),
                "nationality": cred.get("nationality"),
                "visa_type": cred.get("visa_type"),
                "items": items,
            })
    return out


def bank_view(site_id: str):
    """
    은행 영업담당자가 보는 화면.
    **개인은 보이지 않는다.** 국적별 인원 집계에서 규모만 계산한다.
    """
    site = _employers()["_index"].get(site_id)
    if not site:
        return None

    avg = site["avg_monthly_remit"]
    tiers = {"A": {"people": 0, "amount": 0, "nationalities": []},
             "B": {"people": 0, "amount": 0, "nationalities": []}}
    by_currency = {}

    for nat, n in site["nationalities"].items():
        fx = products.currency_of(nat)
        if not fx:
            continue
        t = tiers.setdefault(fx["tier"], {"people": 0, "amount": 0, "nationalities": []})
        t["people"] += n
        t["amount"] += n * avg
        t["nationalities"].append(f"{nat} {n}")
        cur = by_currency.setdefault(
            fx["currency"], {"currency": fx["currency"], "name": fx["currency_name"],
                             "tier": fx["tier"], "people": 0, "amount": 0})
        cur["people"] += n
        cur["amount"] += n * avg

    total = site["foreign_employees"] * avg
    hedge_people = tiers["A"]["people"] + tiers["B"]["people"]
    fx_guard = _fx_guard_summary(site, tiers, hedge_people)

    return {
        "viewer": "은행 영업담당자",
        "site": {k: site[k] for k in ("site_id", "site_name", "industry", "location",
                                      "foreign_employees", "payday", "im_payroll_accounts")},
        "remit": {
            "avg_monthly": avg,
            "total_monthly": total,
            "hedge_people": hedge_people,
            "currencies": sorted(by_currency.values(), key=lambda c: -c["people"]),
        },
        "fx_guard": fx_guard,
        "tiers": tiers,
        "nationality_count": len(site["nationalities"]),
        "pipeline": {
            "payroll_open": site["im_payroll_accounts"],
            "payroll_gap": site["foreign_employees"] - site["im_payroll_accounts"],
            "gap_amount": (site["foreign_employees"] - site["im_payroll_accounts"]) * avg,
            "export_company": site.get("export_company", False),
            "fx_annual": site.get("fx_annual"),
        },
        "expansion": [
            {"name": "급여이체", "value": f"{site['im_payroll_accounts']}계좌 · 월 {total:,}원 유입"},
            {"name": "환율보장보험",
             "value": (f"{hedge_people}명 · 월 보장 {fx_guard['coverage_monthly']:,}원 · "
                       f"연 예상보험료 {fx_guard['premium_annual']:,}원")},
            {"name": "외환·송금", "value": f"월 {total:,}원 · 통화별 보장 대상 {hedge_people}명"},
            {"name": "법인 접점",
             "value": (f"수출입 법인 — 연 외환거래 {site['fx_annual']:,}원 규모 · 기업계좌·운전자금·무역금융"
                       if site.get("export_company") else "기업계좌·운전자금 확장 가능")},
        ],
        "pitch": [
            "직원 금융 민원이 앱으로 넘어갑니다 — 계좌 개설 동행, 송금 방법 설명, 서류 통역, 보험 조회 대행",
            "체류자격이 취소된 근로자는 다음 날 출근 스캔에서 자동으로 막힙니다",
            "채용 공고·면접에서 제시할 수 있는 복지: 다국어 급여관리 · 해외송금 · 환율보장보험 · 귀국자산 적립 · 보험조회",
        ],
        "note": (
            "개인은 표시되지 않습니다. 신규등록 시연용 A/B 기업은 제외하고, 은행 계약기업의 국적별 인원 집계에서 산출한 규모입니다. "
            "인원과 평균 송금액은 시연용 가정값입니다."
        ),
    }
