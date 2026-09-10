"""
실제 온체인 접근 제어(onlyOwner) 검증 테스트

test_blockchain_registry.py의 8개 테스트는 blockchain_client.py의 파이썬
시뮬레이터(_simulated_statuses)를 대상으로 동작하기 때문에, 시뮬레이터에는
msg.sender 개념이 없어 "비소유자가 발급을 시도하면 차단되는가"를 실제로
검증하지 못한다.

이 파일은 CredentialRegistry.sol을 실제로 컴파일하여 로컬 EVM(py-evm)에
배포하고, 소유자(owner)와 공격자(attacker) 계정으로 각각 트랜잭션을 보내
컨트랙트 자체의 onlyOwner 접근 제어가 정말로 revert 되는지 확인한다.
"""

import os

import pytest
solcx = pytest.importorskip("solcx", reason="solcx not installed (optional on-chain compilation test)")
eth_tester = pytest.importorskip("eth_tester", reason="eth_tester not installed")
from eth_tester import EthereumTester, PyEVMBackend
from web3 import Web3
from eth_tester.exceptions import TransactionFailed

CONTRACT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "contracts",
    "CredentialRegistry.sol",
)
SOLC_VERSION = "0.8.20"


@pytest.fixture(scope="session")
def compiled_contract():
    """CredentialRegistry.sol을 실제로 컴파일 (필요 시 solc 자동 설치)"""
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
    # solcx normalizes path separators; find the matching key defensively
    entry = compiled.get(key)
    if entry is None:
        entry = next(v for k, v in compiled.items() if k.endswith(":CredentialRegistry"))
    return entry["abi"], entry["bin"]


@pytest.fixture
def deployed(compiled_contract):
    """로컬 EVM(py-evm)에 컨트랙트를 실제로 배포"""
    abi, bytecode = compiled_contract
    w3 = Web3(Web3.EthereumTesterProvider(EthereumTester(backend=PyEVMBackend())))
    owner, attacker, *_ = w3.eth.accounts

    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact({"from": owner})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract = w3.eth.contract(address=receipt.contractAddress, abi=abi)

    return {"w3": w3, "contract": contract, "owner": owner, "attacker": attacker}


def _hash(text: str) -> bytes:
    return Web3.keccak(text=text)


def test_owner_can_issue(deployed):
    """소유자(법무부/정부 인가자)는 정상적으로 issue 가능"""
    contract, owner = deployed["contract"], deployed["owner"]
    cred_hash = _hash("owner-issued-cred")
    contract.functions.issue(cred_hash).transact({"from": owner})
    assert contract.functions.getStatus(cred_hash).call() == 1  # Valid
    assert contract.functions.isValid(cred_hash).call() is True


def test_non_owner_issue_reverts(deployed):
    """비소유자가 issue를 호출하면 온체인에서 revert 되어야 한다"""
    contract, attacker = deployed["contract"], deployed["attacker"]
    cred_hash = _hash("attacker-issued-cred")
    with pytest.raises(TransactionFailed, match="Only registry authority"):
        contract.functions.issue(cred_hash).transact({"from": attacker})
    # 상태 변화가 없어야 함
    assert contract.functions.getStatus(cred_hash).call() == 0  # None


def test_non_owner_revoke_reverts(deployed):
    """비소유자가 revoke를 호출하면 revert 되어야 한다"""
    contract, owner, attacker = deployed["contract"], deployed["owner"], deployed["attacker"]
    cred_hash = _hash("cred-to-protect-from-revoke")
    contract.functions.issue(cred_hash).transact({"from": owner})

    with pytest.raises(TransactionFailed, match="Only registry authority"):
        contract.functions.revoke(cred_hash).transact({"from": attacker})
    # 공격자의 시도가 실패했으므로 여전히 Valid 상태여야 함
    assert contract.functions.getStatus(cred_hash).call() == 1


def test_non_owner_restore_reverts(deployed):
    """비소유자가 restore를 호출하면 revert 되어야 한다"""
    contract, owner, attacker = deployed["contract"], deployed["owner"], deployed["attacker"]
    cred_hash = _hash("cred-to-protect-from-restore")
    contract.functions.issue(cred_hash).transact({"from": owner})
    contract.functions.revoke(cred_hash).transact({"from": owner})

    with pytest.raises(TransactionFailed, match="Only registry authority"):
        contract.functions.restore(cred_hash).transact({"from": attacker})
    assert contract.functions.getStatus(cred_hash).call() == 2  # 여전히 Revoked


def test_non_owner_transfer_ownership_reverts(deployed):
    """비소유자가 관리자 권한을 탈취(transferOwnership)하려 하면 revert 되어야 한다"""
    contract, owner, attacker = deployed["contract"], deployed["owner"], deployed["attacker"]
    with pytest.raises(TransactionFailed, match="Only registry authority"):
        contract.functions.transferOwnership(attacker).transact({"from": attacker})
    assert contract.functions.owner().call() == owner


def test_full_lifecycle_on_real_evm(deployed):
    """실제 EVM 상에서 issue -> revoke -> restore 전체 흐름 검증 (시뮬레이터가 아닌 실제 컨트랙트)"""
    contract, owner = deployed["contract"], deployed["owner"]
    cred_hash = _hash("lifecycle-cred")

    contract.functions.issue(cred_hash).transact({"from": owner})
    assert contract.functions.getStatus(cred_hash).call() == 1

    contract.functions.revoke(cred_hash).transact({"from": owner})
    assert contract.functions.getStatus(cred_hash).call() == 2
    assert contract.functions.isValid(cred_hash).call() is False

    contract.functions.restore(cred_hash).transact({"from": owner})
    assert contract.functions.getStatus(cred_hash).call() == 1
    assert contract.functions.isValid(cred_hash).call() is True


def test_duplicate_issue_reverts_on_real_evm(deployed):
    """실제 컨트랙트에서도 중복 발급이 revert 되는지 확인"""
    contract, owner = deployed["contract"], deployed["owner"]
    cred_hash = _hash("duplicate-cred")
    contract.functions.issue(cred_hash).transact({"from": owner})
    with pytest.raises(TransactionFailed, match="already exists"):
        contract.functions.issue(cred_hash).transact({"from": owner})
