"""
통합 E2E 테스트: 자격증 발급 -> QR 프리젠테이션 생성 -> 온체인 검증 -> 철회 -> 위변조 차단 시나리오
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_full_scenario_flow(client):
    # 1. 자격증 발급 (온체인 스마트 컨트랙트 등록)
    issue_resp = client.post("/credentials", json={
        "worker_name": "TEST WORKER",
        "nationality": "베트남",
        "account_bank": "iM뱅크",
        "account_number": "512-999999-01"
    })
    assert issue_resp.status_code == 200
    cred_data = issue_resp.json()
    cid = cred_data["credential_id"]
    assert cred_data["tx_hash"].startswith("0x")
    assert cred_data["status"] == "valid"

    # 2. QR 제출용 Presentation 생성 (대상: company_A)
    pres_resp = client.post("/presentations", json={
        "credential_id": cid,
        "target_id": "company_A"
    })
    assert pres_resp.status_code == 200
    pres_data = pres_resp.json()
    payload = pres_data["payload"]
    assert "qr_image_base64" in pres_data

    # 3. 정상 검증 (verifier_id = company_A) -> 통과
    verify_resp = client.post("/verify", json={
        "payload": payload,
        "verifier_id": "company_A"
    })
    assert verify_resp.status_code == 200
    v_data = verify_resp.json()
    assert v_data["result"] == "pass"
    assert v_data["onchain_verified"] is True
    assert v_data["onchain_proof"]["is_valid"] is True

    # 4. 오류 1: 위변조 테스트 (계좌번호 한 자리 변경) -> SIGNATURE_INVALID
    tampered_payload = dict(payload)
    tampered_payload["account_number"] = "512-999999-02"
    tamper_resp = client.post("/verify", json={
        "payload": tampered_payload,
        "verifier_id": "company_A"
    })
    assert tamper_resp.status_code == 200
    t_data = tamper_resp.json()
    assert t_data["result"] == "fail"
    assert t_data["reason"] == "SIGNATURE_INVALID"

    # 5. 오류 2: 다른 기관 제출 (verifier_id = company_B) -> TARGET_MISMATCH
    mismatch_resp = client.post("/verify", json={
        "payload": payload,
        "verifier_id": "company_B"
    })
    assert mismatch_resp.status_code == 200
    m_data = mismatch_resp.json()
    assert m_data["result"] == "fail"
    assert m_data["reason"] == "TARGET_MISMATCH"

    # 6. 오류 3: 체류자격 철회 (Admin 온체인 revoke) -> REVOKED
    revoke_resp = client.post(f"/admin/credentials/{cid}/revoke")
    assert revoke_resp.status_code == 200
    r_data = revoke_resp.json()
    assert r_data["status"] == "revoked"
    assert r_data["tx_hash"].startswith("0x")

    # 원본(위변조 안 한) payload로 다시 검증 시도 -> 온체인 철회로 즉시 차단
    reverify_resp = client.post("/verify", json={
        "payload": payload,
        "verifier_id": "company_A"
    })
    assert reverify_resp.status_code == 200
    rv_data = reverify_resp.json()
    assert rv_data["result"] == "fail"
    assert rv_data["reason"] == "REVOKED"
    assert rv_data["onchain_proof"]["is_valid"] is False

    # 7. 온체인 복구 (Admin 온체인 restore) -> 다시 정상 통과
    restore_resp = client.post(f"/admin/credentials/{cid}/restore")
    assert restore_resp.status_code == 200

    reverify_pass_resp = client.post("/verify", json={
        "payload": payload,
        "verifier_id": "company_A"
    })
    assert reverify_pass_resp.json()["result"] == "pass"
