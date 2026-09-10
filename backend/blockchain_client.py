"""
iM Worker Pass - Web3 / Blockchain Client
Solidity 스마트 컨트랙트(CredentialRegistry)와의 상호작용을 담당합니다.
- 개인정보는 체인에 올리지 않으며, 오직 keccak256(credential_id) 해시와 상태값(Valid/Revoked)만 기록합니다.
- RPC_URL과 CONTRACT_ADDRESS가 주어지면 실제 테스트넷(Polygon Amoy, Sepolia 등)에 트랜잭션을 전송합니다.
- 설정되지 않은 경우 로컬 개발/시연용 온체인 시뮬레이터로 안전하게 동작합니다.
"""

import os
import json
from enum import IntEnum
from typing import Optional, Dict, Any
from web3 import Web3

class CredentialStatus(IntEnum):
    NONE = 0      # 미등록
    VALID = 1     # 유효
    REVOKED = 2   # 철회 (체류자격 취소)

# CredentialRegistry ABI
REGISTRY_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "bytes32", "name": "credentialHash", "type": "bytes32"},
            {"indexed": True, "internalType": "address", "name": "issuer", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "CredentialIssued",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "bytes32", "name": "credentialHash", "type": "bytes32"},
            {"indexed": True, "internalType": "address", "name": "issuer", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "CredentialRevoked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "bytes32", "name": "credentialHash", "type": "bytes32"},
            {"indexed": True, "internalType": "address", "name": "issuer", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "CredentialRestored",
        "type": "event"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "credentialHash", "type": "bytes32"}],
        "name": "issue",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "credentialHash", "type": "bytes32"}],
        "name": "revoke",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "credentialHash", "type": "bytes32"}],
        "name": "restore",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "credentialHash", "type": "bytes32"}],
        "name": "getStatus",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "credentialHash", "type": "bytes32"}],
        "name": "isValid",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class BlockchainRegistryClient:
    def __init__(self):
        self.rpc_url = os.environ.get("RPC_URL", "")
        self.contract_address = os.environ.get("CONTRACT_ADDRESS", "")
        self.admin_private_key = os.environ.get("ADMIN_PRIVATE_KEY", "")
        self.explorer_base_url = os.environ.get("EXPLORER_BASE_URL", "https://amoy.polygonscan.com")

        self.w3 = None
        self.contract = None
        self.account = None
        self.is_live_network = False

        # 온체인 시뮬레이터 저장소 (로컬 또는 테스트 환경용)
        self._simulated_statuses: Dict[str, int] = {}
        self._simulated_history: list = []

        if self.rpc_url and self.contract_address and self.admin_private_key:
            try:
                self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
                if self.w3.is_connected():
                    self.account = self.w3.eth.account.from_key(self.admin_private_key)
                    self.contract = self.w3.eth.contract(
                        address=Web3.to_checksum_address(self.contract_address),
                        abi=REGISTRY_ABI
                    )
                    self.is_live_network = True
            except Exception as e:
                print(f"[Web3 Warning] Real network connection failed, falling back to simulator: {e}")
                self.is_live_network = False

    def to_credential_hash(self, credential_id: str) -> bytes:
        """credential_id 문자열을 keccak256 해시(bytes32)로 변환"""
        return Web3.keccak(text=credential_id)

    def issue(self, credential_id: str) -> Dict[str, Any]:
        """자격증을 온체인 레지스트리에 유효(Valid=1) 상태로 등록"""
        cred_hash = self.to_credential_hash(credential_id)
        hex_hash = "0x" + cred_hash.hex()

        if self.is_live_network:
            tx = self.contract.functions.issue(cred_hash).build_transaction({
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "gas": 150000,
                "gasPrice": self.w3.eth.gas_price,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.admin_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = tx_hash.hex()
            return {
                "onchain": True,
                "mode": "live_testnet",
                "credential_hash": hex_hash,
                "tx_hash": tx_hash_hex,
                "block_number": tx_receipt.blockNumber,
                "explorer_url": f"{self.explorer_base_url}/tx/{tx_hash_hex}",
                "status": "valid"
            }

        # 시뮬레이션 모드 (결정론적 해시 및 트랜잭션 생성)
        if self._simulated_statuses.get(hex_hash) == CredentialStatus.VALID:
            raise ValueError("Credential already exists on-chain")
            
        self._simulated_statuses[hex_hash] = CredentialStatus.VALID
        mock_tx_hash = "0x" + Web3.keccak(text=f"issue:{credential_id}:{len(self._simulated_history)}").hex()
        entry = {
            "onchain": True,
            "mode": "simulator",
            "credential_hash": hex_hash,
            "tx_hash": mock_tx_hash,
            "block_number": 5120000 + len(self._simulated_history),
            "explorer_url": f"{self.explorer_base_url}/tx/{mock_tx_hash}",
            "status": "valid"
        }
        self._simulated_history.append(entry)
        return entry

    def revoke(self, credential_id: str) -> Dict[str, Any]:
        """자격증을 온체인 레지스트리에서 철회(Revoked=2) 상태로 전환"""
        cred_hash = self.to_credential_hash(credential_id)
        hex_hash = "0x" + cred_hash.hex()

        if self.is_live_network:
            tx = self.contract.functions.revoke(cred_hash).build_transaction({
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "gas": 150000,
                "gasPrice": self.w3.eth.gas_price,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.admin_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = tx_hash.hex()
            return {
                "onchain": True,
                "mode": "live_testnet",
                "credential_hash": hex_hash,
                "tx_hash": tx_hash_hex,
                "block_number": tx_receipt.blockNumber,
                "explorer_url": f"{self.explorer_base_url}/tx/{tx_hash_hex}",
                "status": "revoked"
            }

        # 시뮬레이션 모드
        curr = self._simulated_statuses.get(hex_hash, CredentialStatus.NONE)
        if curr == CredentialStatus.NONE:
            # 기존 DB에만 있던 레코드 대응
            self._simulated_statuses[hex_hash] = CredentialStatus.REVOKED
        elif curr == CredentialStatus.REVOKED:
            raise ValueError("Credential is already revoked")
        else:
            self._simulated_statuses[hex_hash] = CredentialStatus.REVOKED

        mock_tx_hash = "0x" + Web3.keccak(text=f"revoke:{credential_id}:{len(self._simulated_history)}").hex()
        entry = {
            "onchain": True,
            "mode": "simulator",
            "credential_hash": hex_hash,
            "tx_hash": mock_tx_hash,
            "block_number": 5120000 + len(self._simulated_history),
            "explorer_url": f"{self.explorer_base_url}/tx/{mock_tx_hash}",
            "status": "revoked"
        }
        self._simulated_history.append(entry)
        return entry

    def restore(self, credential_id: str) -> Dict[str, Any]:
        """철회된 자격증을 다시 유효(Valid=1) 상태로 복구"""
        cred_hash = self.to_credential_hash(credential_id)
        hex_hash = "0x" + cred_hash.hex()

        if self.is_live_network:
            tx = self.contract.functions.restore(cred_hash).build_transaction({
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "gas": 150000,
                "gasPrice": self.w3.eth.gas_price,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.admin_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = tx_hash.hex()
            return {
                "onchain": True,
                "mode": "live_testnet",
                "credential_hash": hex_hash,
                "tx_hash": tx_hash_hex,
                "block_number": tx_receipt.blockNumber,
                "explorer_url": f"{self.explorer_base_url}/tx/{tx_hash_hex}",
                "status": "valid"
            }

        self._simulated_statuses[hex_hash] = CredentialStatus.VALID
        mock_tx_hash = "0x" + Web3.keccak(text=f"restore:{credential_id}:{len(self._simulated_history)}").hex()
        entry = {
            "onchain": True,
            "mode": "simulator",
            "credential_hash": hex_hash,
            "tx_hash": mock_tx_hash,
            "block_number": 5120000 + len(self._simulated_history),
            "explorer_url": f"{self.explorer_base_url}/tx/{mock_tx_hash}",
            "status": "valid"
        }
        self._simulated_history.append(entry)
        return entry

    def get_status(self, credential_id: str) -> Dict[str, Any]:
        """자격증의 온체인 상태 조회"""
        cred_hash = self.to_credential_hash(credential_id)
        hex_hash = "0x" + cred_hash.hex()

        if self.is_live_network:
            status_code = self.contract.functions.getStatus(cred_hash).call()
        else:
            status_code = self._simulated_statuses.get(hex_hash, CredentialStatus.NONE)

        status_names = {0: "none", 1: "valid", 2: "revoked"}
        return {
            "onchain": True,
            "mode": "live_testnet" if self.is_live_network else "simulator",
            "credential_hash": hex_hash,
            "status_code": int(status_code),
            "status_name": status_names.get(status_code, "unknown"),
            "is_valid": (status_code == CredentialStatus.VALID)
        }

# 싱글톤 인스턴스
_client = None

def get_blockchain_client() -> BlockchainRegistryClient:
    global _client
    if _client is None:
        _client = BlockchainRegistryClient()
    return _client
