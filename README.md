# iM Worker Pass — Web3 & 블록체인 프로토타입

기획서 S0~S10에 대응하는 외국인 근로자 분산신원인증(DID) 및 스마트 컨트랙트 상태 레지스트리 시스템입니다.

```
im-worker-pass/
├─ contracts/                  # Solidity 스마트 컨트랙트 (S1)
│  └─ CredentialRegistry.sol   # W3C DID 자격증 상태(발급/철회) 레지스트리
├─ 기관서버/                  # 기관 발급·체인 등록 서버
│  ├─ contracts/              # Solidity 레지스트리
│  └─ server/                 # FastAPI + Web3 기관 API
│     ├─ main.py
│     ├─ blockchain_client.py
│     ├─ crypto_utils.py
│     ├─ models.py
│     ├─ supabase_client.py
│     ├─ schema.sql
│     ├─ requirements.txt
│     ├─ .env.example
│     └─ tests/
│     ├─ test_blockchain_registry.py  # S1 로드맵 테스트 8개 (All Pass)
│     └─ test_api_flow.py             # 전체 E2E 통합 테스트
└─ 심사자/                     # 제출·검증 화면
   └─ web/                     # 정적 HTML/JS (Vercel 등에 배포)
   ├─ issue.html   # ① 근로자 지갑: 온체인 발급 + 서명된 QR 생성
   ├─ scan.html    # ② 회사/병원/보험 스캐너: 온체인 실시간 검증 & 기관별 특화 UI
   ├─ admin.html   # ③ 관리자: 온체인 철회/복구 트랜잭션 전송 (S9 시연)
   ├─ config.js
   └─ style.css
```

---

## 1. 스마트 컨트랙트 및 단위 테스트 (S1: 테스트 8개 통과)

로드맵의 **S1 "블록체인 기록장 - 테스트 8개 통과"**가 구현되어 있습니다:

```bash
# 8개 단위 테스트 및 통합 테스트 실행
python -m pytest backend/tests/ -v
```

테스트 항목:
1. `test_01_initial_state_and_ownership`: 컨트랙트 초기화 및 소유자 권한
2. `test_02_issue_credential`: 신규 자격증 온체인 등록 (Valid=1) 및 Tx Hash 생성
3. `test_03_query_status`: 온체인 상태 조회 및 유효성 확인
4. `test_04_unauthorized_issuer_rejection`: 비소유자 발급 시도 차단
5. `test_05_revoke_credential`: 자격증 온체인 철회 (Revoked=2) 및 즉시 무효화
6. `test_06_restore_credential`: 철회된 자격증 온체인 재복구
7. `test_07_unregistered_credential_query`: 미등록 자격증 조회 시 None(0) 반환
8. `test_08_duplicate_issue_prevention`: 이미 등록된 자격증의 중복 발급 시도 차단

---

## 2. 백엔드 실행

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

- `http://localhost:8000/health` : 블록체인 연동 상태 확인 (`{"ok": true, "blockchain": ...}`)
- `http://localhost:8000/docs` : Swagger API 문서

> **참고**: 별도의 `.env` 설정 없이도 내장 온체인 시뮬레이터가 동작하여 즉시 데모가 가능하며, 실제 Polygon Amoy / Sepolia에 배포 시 `.env`의 `RPC_URL`, `CONTRACT_ADDRESS`, `ADMIN_PRIVATE_KEY`를 넣으면 실제 퍼블릭 체인 트랜잭션이 전송됩니다.

---

## 3. 프론트엔드 실행

```bash
cd frontend
python -m http.server 5500
```

브라우저에서 `http://localhost:5500/issue.html` 접속

---

## 4. 시연 순서 (발표용 시나리오)

1. **[issue.html] 근로자 지갑 발급 & 블록체인 등록**
   - 정보 입력 후 "발급 & 블록체인 등록" 클릭 → 온체인 Tx Hash 및 블록체인 등록 완료 확인
   - `target_id = company_A` 선택 후 "QR 생성" 클릭

2. **[scan.html] 정상 검증 통과**
   - verifier = `company_A` 선택 후 payload 붙여넣기 (또는 카메라 스캔)
   - ✅ **검사 통과 (블록체인 분산 원장 검증 완료)** 확인
   - 사내 ERP 급여계좌 자동 연동 완료 카드 표출

3. **[scan.html] 오류 케이스 1: 위변조 차단**
   - payload의 `account_number`를 한 글자 임의로 변경 후 검증
   - ❌ **SIGNATURE_INVALID** (전자서명 불일치 차단)

4. **[scan.html] 오류 케이스 2: 대상 불일치(오배송) 차단**
   - verifier를 `company_B`로 바꾼 후 원래 payload 검증
   - ❌ **TARGET_MISMATCH** (제출 대상 불일치 차단)

5. **[admin.html] 오류 케이스 3: 법무부 체류자격 철회 시연**
   - 관리자 화면에서 해당 근로자의 "온체인 철회" 클릭 → 체류자격 철회 블록체인 트랜잭션 전송
   - **scan.html**로 돌아가 원래(변조 안 한) payload로 다시 검증
   - ❌ **REVOKED (체류자격이 블록체인 원장에서 철회되었습니다)** 차단 및 On-Chain Proof 증명
