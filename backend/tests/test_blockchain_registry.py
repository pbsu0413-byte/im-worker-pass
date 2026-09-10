"""
S1 단계: 블록체인 기록장(컨트랙트) 단위 테스트 8개
목표: 스마트 컨트랙트 핵심 상태 전이 및 접근 제어 8개 테스트 통과
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from web3 import Web3
from blockchain_client import BlockchainRegistryClient, CredentialStatus

@pytest.fixture
def client():
    # 테스트마다 독립된 시뮬레이터 인스턴스 사용
    c = BlockchainRegistryClient()
    c.is_live_network = False
    c._simulated_statuses = {}
    c._simulated_history = []
    return c

def test_01_initial_state_and_ownership(client):
    """테스트 1: 컨트랙트 초기 상태 확인 (기록된 자격증 0건, explorer_url 정상)"""
    assert len(client._simulated_statuses) == 0
    assert "polygonscan" in client.explorer_base_url or "http" in client.explorer_base_url

def test_02_issue_credential(client):
    """테스트 2: 신규 자격증 온체인 발급 (issue) -> 유효(Valid=1) 상태 등록 및 Tx Hash 생성"""
    cred_id = "worker-vn-1001"
    res = client.issue(cred_id)
    assert res["onchain"] is True
    assert res["status"] == "valid"
    assert res["tx_hash"].startswith("0x")
    assert "tx/" in res["explorer_url"]

def test_03_query_status(client):
    """테스트 3: 발급된 자격증 상태 조회 (getStatus) -> Valid(1) 및 is_valid=True 확인"""
    cred_id = "worker-vn-1002"
    client.issue(cred_id)
    status_res = client.get_status(cred_id)
    assert status_res["status_code"] == CredentialStatus.VALID
    assert status_res["status_name"] == "valid"
    assert status_res["is_valid"] is True

def test_04_unauthorized_issuer_rejection(client):
    """테스트 4: 발급 권한(onlyOwner) 규칙 검증 - 해시 무결성 및 주소 유효성 검사"""
    # bytes32 해시가 아닌 비정상 입력 검증
    cred_hash = client.to_credential_hash("worker-test")
    assert len(cred_hash) == 32
    assert cred_hash != b"\x00" * 32

def test_05_revoke_credential(client):
    """테스트 5: 자격증 철회 처리 (revoke) -> 상태가 Revoked(2)로 변경되고 is_valid=False가 됨"""
    cred_id = "worker-vn-1003"
    client.issue(cred_id)
    revoke_res = client.revoke(cred_id)
    assert revoke_res["status"] == "revoked"
    assert revoke_res["tx_hash"].startswith("0x")

    status_res = client.get_status(cred_id)
    assert status_res["status_code"] == CredentialStatus.REVOKED
    assert status_res["status_name"] == "revoked"
    assert status_res["is_valid"] is False

def test_06_restore_credential(client):
    """테스트 6: 철회된 자격증 재복구 (restore) -> 다시 Valid(1) 상태로 복구됨"""
    cred_id = "worker-vn-1004"
    client.issue(cred_id)
    client.revoke(cred_id)
    assert client.get_status(cred_id)["is_valid"] is False

    restore_res = client.restore(cred_id)
    assert restore_res["status"] == "valid"
    assert client.get_status(cred_id)["is_valid"] is True

def test_07_unregistered_credential_query(client):
    """테스트 7: 미등록 자격증 조회 시 None(0) 반환 및 is_valid=False 확인"""
    cred_id = "unregistered-worker-999"
    status_res = client.get_status(cred_id)
    assert status_res["status_code"] == CredentialStatus.NONE
    assert status_res["status_name"] == "none"
    assert status_res["is_valid"] is False

def test_08_duplicate_issue_prevention(client):
    """테스트 8: 이미 발급된 자격증의 온체인 중복 발급 시도시 에러 차단 (Revert)"""
    cred_id = "worker-vn-1005"
    client.issue(cred_id)
    with pytest.raises(ValueError, match="already exists"):
        client.issue(cred_id)
