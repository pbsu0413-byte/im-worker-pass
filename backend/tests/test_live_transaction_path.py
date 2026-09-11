"""
BlockchainRegistryClient의 실제 온체인(live_testnet) 트랜잭션 전송 경로 테스트

배경: 실제 배포(Render) 환경에서 RPC_URL/CONTRACT_ADDRESS/ADMIN_PRIVATE_KEY를
모두 채워 live_testnet 모드로 전환한 뒤 /credentials를 호출하자 아래 에러로
500이 발생했다:

    AttributeError: 'SignedTransaction' object has no attribute 'rawTransaction'.
    Did you mean: 'raw_transaction'?

기존 테스트 스위트(test_blockchain_registry.py의 8개, test_onchain_access_control.py의
7개) 중 어느 것도 BlockchainRegistryClient.issue/revoke/restore의 `is_live_network=True`
분기(실제 서명 트랜잭션 전송 코드)를 통과하지 않았기 때문에, web3.py 버전업으로
`SignedTransaction.rawTransaction` → `.raw_transaction`으로 속성명이 바뀐 걸
아무 테스트도 잡아내지 못했다.

이 파일은 BlockchainRegistryClient가 실제로 `is_live_network=True`가 되도록
환경변수를 세팅하고, 로컬 EVM(py-evm)에 배포된 실제 컨트랙트를 상대로
issue/revoke/restore를 그대로 호출해 회귀를 방지한다.
"""

import os

import pytest
import solcx
from eth_account import Account
from eth_tester import EthereumTester, PyEVMBackend
from web3 import Web3

CONTRACT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "contracts",
    "CredentialRegistry.sol",
)
SOLC_VERSION = "0.8.20"


@pytest.fixture(scope="session")
def compiled_contract():
    installed = solcx.get_installed_solc_versions()
    if SOLC_VERSION not in [str(v) for v in installed]:
        solcx.install_solc(SOLC_VERSION)
    solcx.set_solc_version(SOLC_VERSION)

    compiled = solcx.compile_files(
        [CONTRACT_PATH],
        output_values=["abi", "bin"],
        solc_version=SOLC_VERSION,
    )
    key = f"{CONTRACT_PATH}:CredentialRegistry"
    entry = compiled.get(key)
    if entry is None:
        entry = next(v for k, v in compiled.items() if k.endswith(":CredentialRegistry"))
    return entry["abi"], entry["bin"]


@pytest.fixture
def live_client(compiled_contract, monkeypatch):
    """
    실제 live_testnet 코드 경로를 타는 BlockchainRegistryClient를 만든다.
    RPC_URL은 진짜 네트워크 대신 로컬 EVM(py-evm)에 연결되도록 monkeypatch한다.
    """
    abi, bytecode = compiled_contract
    w3 = Web3(Web3.EthereumTesterProvider(EthereumTester(backend=PyEVMBackend())))
    funder = w3.eth.accounts[0]

    # 알 수 있는 개인키를 가진 새 관리자 계정을 만들고 가스비를 지원한다
    admin = Account.create()
    w3.eth.send_transaction({
        "from": funder,
        "to": admin.address,
        "value": w3.to_wei(50, "ether"),
    })

    # admin은 eth_tester가 관리하는 계정이 아니라 방금 새로 만든 계정이라
    # transact({"from": admin.address})로는 서명할 수 없다. 실제 프로덕션
    # 코드와 동일하게 raw signing으로 직접 배포한다.
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    deploy_tx = Contract.constructor().build_transaction({
        "from": admin.address,
        "nonce": w3.eth.get_transaction_count(admin.address),
        "gas": 3000000,
        "gasPrice": w3.eth.gas_price,
    })
    signed_deploy_tx = w3.eth.account.sign_transaction(deploy_tx, private_key=admin.key)
    tx_hash = w3.eth.send_raw_transaction(signed_deploy_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = receipt.contractAddress

    import blockchain_client as bc_module

    # BlockchainRegistryClient가 RPC_URL로 HTTPProvider를 만들려고 하는데,
    # 실제 네트워크 대신 위에서 만든 로컬 EVM(w3)에 그대로 연결되도록 가로챈다.
    monkeypatch.setattr(bc_module.Web3, "HTTPProvider", lambda *a, **kw: w3.provider)

    monkeypatch.setenv("RPC_URL", "http://localhost:00000/fake-rpc-for-test")
    monkeypatch.setenv("CONTRACT_ADDRESS", contract_address)
    monkeypatch.setenv("ADMIN_PRIVATE_KEY", admin.key.hex())
    monkeypatch.setenv("EXPLORER_BASE_URL", "https://amoy.polygonscan.com")

    client = bc_module.BlockchainRegistryClient()
    assert client.is_live_network is True, "테스트 환경에서 live_testnet 모드로 전환되지 않음"
    return client


def test_issue_sends_real_signed_transaction(live_client):
    """
    /credentials 발급 시 실제로 겪었던 버그(SignedTransaction.rawTransaction)를
    재현하는 테스트. 이 테스트가 실패하면 실제 배포에서도 발급이 500으로 깨진다.
    """
    result = live_client.issue("regression-test-worker-1")
    assert result["mode"] == "live_testnet"
    assert result["onchain"] is True
    assert result["status"] == "valid"
    assert result["tx_hash"].startswith("0x")
    assert isinstance(result["block_number"], int)


def test_revoke_sends_real_signed_transaction(live_client):
    """revoke()도 issue()와 동일한 send_raw_transaction 경로를 타므로 함께 검증"""
    live_client.issue("regression-test-worker-2")
    result = live_client.revoke("regression-test-worker-2")
    assert result["mode"] == "live_testnet"
    assert result["status"] == "revoked"
    assert result["tx_hash"].startswith("0x")


def test_restore_sends_real_signed_transaction(live_client):
    """restore()도 동일한 경로를 타므로 함께 검증"""
    live_client.issue("regression-test-worker-3")
    live_client.revoke("regression-test-worker-3")
    result = live_client.restore("regression-test-worker-3")
    assert result["mode"] == "live_testnet"
    assert result["status"] == "valid"
    assert result["tx_hash"].startswith("0x")
