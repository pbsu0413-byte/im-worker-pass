// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CredentialRegistry
 * @dev W3C DID 자격증 상태(발급/철회) 관리를 위한 분산 원장 스마트 컨트랙트
 * 개인정보(이름, 계좌번호)는 온체인에 저장하지 않고, 
 * 오직 credential_id의 해시값과 상태값(Status)만 기록합니다.
 */
contract CredentialRegistry {
    address public owner;

    enum CredentialStatus {
        None,     // 0: 미등록
        Valid,    // 1: 유효 (정상 발급 상태)
        Revoked   // 2: 철회 (체류자격 취소 등)
    }

    // credential_id의 bytes32 해시 => 상태값
    mapping(bytes32 => CredentialStatus) private _statuses;

    // 이벤트 로깅 (블록체인 탐색기 및 오프체인 모니터링용)
    event CredentialIssued(bytes32 indexed credentialHash, address indexed issuer, uint256 timestamp);
    event CredentialRevoked(bytes32 indexed credentialHash, address indexed issuer, uint256 timestamp);
    event CredentialRestored(bytes32 indexed credentialHash, address indexed issuer, uint256 timestamp);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only registry authority can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
        emit OwnershipTransferred(address(0), msg.sender);
    }

    /**
     * @notice 신규 자격증을 유효 상태로 등록합니다.
     * @param credentialHash 자격증 고유 식별자(ID)의 keccak256 해시
     */
    function issue(bytes32 credentialHash) external onlyOwner {
        require(credentialHash != bytes32(0), "Invalid credential hash");
        require(_statuses[credentialHash] == CredentialStatus.None, "Credential already exists");

        _statuses[credentialHash] = CredentialStatus.Valid;
        emit CredentialIssued(credentialHash, msg.sender, block.timestamp);
    }

    /**
     * @notice 자격증을 철회(취소)합니다. (체류자격 취소 시)
     * @param credentialHash 자격증 고유 식별자(ID)의 keccak256 해시
     */
    function revoke(bytes32 credentialHash) external onlyOwner {
        require(_statuses[credentialHash] != CredentialStatus.None, "Credential does not exist");
        require(_statuses[credentialHash] != CredentialStatus.Revoked, "Credential is already revoked");

        _statuses[credentialHash] = CredentialStatus.Revoked;
        emit CredentialRevoked(credentialHash, msg.sender, block.timestamp);
    }

    /**
     * @notice 철회된 자격증을 다시 유효 상태로 복구합니다.
     * @param credentialHash 자격증 고유 식별자(ID)의 keccak256 해시
     */
    function restore(bytes32 credentialHash) external onlyOwner {
        require(_statuses[credentialHash] == CredentialStatus.Revoked, "Credential is not revoked");

        _statuses[credentialHash] = CredentialStatus.Valid;
        emit CredentialRestored(credentialHash, msg.sender, block.timestamp);
    }

    /**
     * @notice 자격증의 현재 온체인 상태를 조회합니다.
     * @param credentialHash 자격증 고유 식별자(ID)의 keccak256 해시
     * @return status (0: None, 1: Valid, 2: Revoked)
     */
    function getStatus(bytes32 credentialHash) external view returns (CredentialStatus) {
        return _statuses[credentialHash];
    }

    /**
     * @notice 자격증이 유효한지 여부를 확인합니다.
     */
    function isValid(bytes32 credentialHash) external view returns (bool) {
        return _statuses[credentialHash] == CredentialStatus.Valid;
    }

    /**
     * @notice 관리자 권한을 이전합니다.
     */
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid new owner");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
