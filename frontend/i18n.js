/**
 * iM Worker Pass - 다국어(i18n) 모듈
 * 지원 언어: 한국어(ko), English(en), Tiếng Việt(vi), Bahasa Indonesia(id), Oʻzbekcha(uz), 中文(zh)
 */

const I18N_DICT = {
  ko: {
    // 공통 및 상단
    lang_name: "한국어",
    app_title: "iM PASS",
    worker_role: "근로자",
    switch_service: "서비스 전환",
    wallet_heading: "내 디지털 지갑",
    wallet_subheading: "체류·취업 자격 및 금융 패스포트",
    first_time_notice: "지갑 발급은 <b>최초 1회</b>입니다. 제출은 낼 때마다 아래 <b>제출</b> 탭에서 합니다.",

    // 메인 홈 화면 (home.html)
    home_kicker: "생활과 금융을 연결하는 새로운 신원지갑",
    home_heading: "이용할 서비스를 선택해 주세요",
    badge_worker: "개인",
    app_worker_name: "iM PASS 근로자",
    app_worker_desc: "내 자격을 보관하고 필요한 곳에 제출해요",
    badge_biz: "기업",
    app_biz_name: "iM PASS 사업자",
    app_biz_desc: "근로자의 자격을 빠르고 안전하게 확인해요",
    badge_admin: "관리자",
    app_admin_name: "iM PASS 은행·기관",
    app_admin_desc: "자격을 발급하고 변경 상태를 관리해요",
    trust_title: "안심하고 쓸 수 있는 이유",
    trust_1_t: "자격을 원장에 등록해요",
    trust_1_d: "은행 창구에서 본인 확인을 마치면 자격이 분산원장에 등록돼요. 등록 이후 변경 이력이 안전하게 보호돼요.",
    trust_2_t: "필요한 정보만 골라 제출해요",
    trust_2_d: "제출할 곳을 정하면 그곳에 필요한 항목만 담긴 QR이 만들어져요. 이름과 계좌는 원장에 올라가지 않아요.",
    trust_3_t: "받는 곳에서 바로 확인해요",
    trust_3_d: "사업장 단말이 자격 상태를 그 자리에서 대조해요. 철회되거나 만료된 자격은 즉시 걸러져요.",

    // 인물 선택 (people.html)
    people_title: "누구로 볼까요",
    people_sub: "외국인 근로자 프로필 선택 (E-9 / H-2)",
    people_desc: "실제 서비스에서 근로자는 자기 지갑 하나만 갖습니다. 고르면 그 사람으로 지갑 발급부터 시작합니다.",

    // 디지털 패스 카드
    pass_title: "iM뱅크 · Worker Pass",
    digital_identity: "Digital Identity",
    status_active: "사용 가능",
    status_disabled: "사용 불가",
    btn_qr_submit: "QR 제출",
    chain_verified: "분산원장 등록 확인됨",
    chain_not_verified: "분산원장에서 확인되지 않음",
    expiry_left: "만료 D-",
    expiry_expired: "체류기간 만료됨",
    expiry_suffix: " 만료",

    // 오늘의 상태 카드
    today_status_caption: "오늘의 자격 상태",
    today_status_safe: "안심하고 사용할 수 있어요",
    today_status_check: "지금은 제출할 수 없어요",
    badge_normal: "정상",
    badge_check_needed: "확인 필요",
    label_visa_type: "체류자격",
    label_valid_until: "유효기간",
    submit_lead: "제출할 서류가 있나요?",
    submit_sub: "필요한 정보만 담은 60초 QR을 만들어요",

    // 이번 달 및 금융 섹션
    this_month_title: "이번 달",
    loading: "불러오는 중…",
    tab_mypass: "내 패스",
    tab_submit: "제출",
    tab_finance: "금융생활",

    // 본인확인 및 지갑 발급 (최초 1회)
    step1_title: "1) 은행 창구 본인확인",
    step1_desc: "카카오 인증서가 통신사 본인확인 위에 세워지듯, 이 지갑은 <b>은행 실명확인</b> 위에 세워집니다. 외국인 근로자는 급여 계좌를 만들며 여권·외국인등록증 대조를 이미 거치므로 절차가 늘지 않습니다.",
    label_worker_name: "근로자 이름",
    btn_bank_verify: "창구 실명확인",
    step2_title: "2) 지갑 등록",
    step2_key_title: "단말 키 생성",
    step2_key_desc: "이 브라우저에서 키 한 쌍을 만듭니다. <b>개인키는 단말에 남고 서버로 전송되지 않습니다.</b>",
    step2_immi_title: "출입국 조회 (필수)",
    step2_immi_desc: "체류 기록이 없으면 지갑을 발급하지 않습니다. 은행 실명확인만으로는 잡히지 않는 위조·말소 외국인등록증이 여기서 걸립니다.",
    step2_etc_title: "나머지 기관 조회 · 블록체인 등록",
    step2_etc_desc: "고용센터·의료기관·교육원은 기록이 없어도 빈칸으로 두고 발급은 진행합니다.",
    btn_register_wallet: "지갑 발급 & 블록체인 등록",

    // 제출 화면 (submit.html)
    submit_dest_title: "어디에 제출하시나요?",
    submit_dest_desc: "목적지에 필요한 최소한의 정보만 골라 담은 60초 일회용 QR을 만듭니다.",
    dest_biz: "사업장 출퇴근",
    dest_biz_desc: "출퇴근 기록 및 체류자격 유효성 확인",
    dest_clinic: "병원 · 약국",
    dest_clinic_desc: "건강보험 자격 및 본인부담 감면 확인",
    dest_bank: "은행 금융거래",
    dest_bank_desc: "급여계좌 개설, 환율보장보험 및 해외송금",
    dest_insurer: "보험사 가입",
    dest_insurer_desc: "출국만기보험 및 상해보험 청구/가입",
    btn_generate_qr: "60초 일회용 QR 생성",
    submit_page_title: "iM Worker Pass - 제출",
    submit_h1: "증명 QR 제출",
    submit_who_desc: "필요한 기관에 필요한 자격만 안전하게 제출",
    submit_lead_desc: "제출은 낼 때마다 합니다. 체인에는 아무것도 쓰지 않고, 기관에 다시 물어 최신 값으로 만듭니다.",
    no_wallet_title: "지갑이 없습니다",
    no_wallet_desc: "먼저 지갑을 발급받아야 합니다. 발급은 최초 1회입니다.",
    btn_goto_wallet: "지갑 발급하러 가기 →",
    submit_step1_title: "1) 어디에 낼지 고르기",
    label_submit_target: "제출 대상",
    label_symptom: "병원에 전달할 증상",
    symptom_note: "환자 본인의 진술이며 진단이 아닙니다.",
    symptom_cough: "기침이 있어요",
    symptom_back_pain: "허리가 아파요",
    symptom_fever: "열이 나는 것 같아요",
    symptom_stomach: "속이 불편해요",
    symptom_itchy: "피부가 가려워요",
    attend_hint: "출퇴근은 기관 재조회를 하지 않습니다. 매일 두 번 물어볼 일이 아니고, 필요한 것은 체류자격이 살아 있는지뿐이며 그것은 스캔 시 체인 조회로 확인됩니다. <b>시각은 회사 스캐너가 읽는 순간 회사 근태 시스템이 찍습니다.</b>",
    insurance_redirect_note: "보험은 상품 선택이 곧 수령처 선택이라 QR이 필요 없습니다 — <a href=\"insurance.html\">④ 보험</a> 화면에서 진행합니다.",
    btn_sign_and_generate_qr: "단말 서명 & QR 생성",
    submit_step2_title: "2) 제출용 QR",
    btn_renew_qr: "QR 다시 생성",
    payload_copy_note: "아래 payload를 복사해 <b>③ 스캐너</b>의 붙여넣기 창에 넣으면 카메라 없이도 검증을 테스트할 수 있습니다. 계좌번호를 한 글자 바꿔 넣으면 위변조 시연이 됩니다.",
    copy_payload_title: "payload 복사",
    copy_done_title: "복사됨",
    copy_fail_title: "복사 실패 — 직접 선택하세요",
    submit_rejected: "제출이 거부되었습니다.",
    sig_verified_msg: "✓ 단말 서명 검증 통과 — 이 지갑의 주인이 보낸 요청입니다.",
    sig_not_registered_msg: "단말 키가 등록되지 않은 지갑입니다. 서명 검증을 건너뛰었습니다.",
    attend_wait_msg: "사업장 스캐너가 이 QR을 읽으면 결과가 여기에 표시됩니다.",
    checkin_label: "출근",
    checkout_label: "퇴근",
    worked_time_label: "근무",
    site_scanner_time_note: "회사 스캐너 기준 시각으로 기록되었습니다.",
    lookup_count_label: "제출 시점 재조회",
    lookup_real_badge: "실제 발급기관",
    lookup_mock_badge: "모의 API",
    lookup_footer_note: "카드를 미리 받아 보관하지 않고 낼 때마다 다시 물으므로, 낡은 버전이라는 것이 존재하지 않습니다. 목적에 필요 없는 기관에는 묻지 않습니다.",
    qr_time_left_label: "QR 유효시간: ",
    qr_expired_label: "QR 만료됨",
    current_wallet_label: "현재 지갑: ",
    switch_person_link: "다른 인물로 바꾸기",
    qr_expired_payload_msg: "만료된 QR은 사용할 수 없습니다.",
  },

  en: {
    lang_name: "English",
    app_title: "iM PASS",
    worker_role: "Worker",
    switch_service: "Switch Service",
    wallet_heading: "My Digital Wallet",
    wallet_subheading: "Visa & Employment & Financial Passport",
    first_time_notice: "Wallet issuance is required <b>only once</b>. Submit documents anytime from the <b>Submit</b> tab below.",

    home_kicker: "Connecting Life and Finance with a New Identity Wallet",
    home_heading: "Please select a service to use",
    badge_worker: "Personal",
    app_worker_name: "iM PASS Worker",
    app_worker_desc: "Keep your credentials safe and submit them when needed",
    badge_biz: "Business",
    app_biz_name: "iM PASS Business",
    app_biz_desc: "Verify workers' credentials fast and securely",
    badge_admin: "Admin",
    app_admin_name: "iM PASS Bank & Institution",
    app_admin_desc: "Issue credentials and manage status lifecycle",
    trust_title: "Why You Can Trust iM PASS",
    trust_1_t: "Registered on the Ledger",
    trust_1_d: "Once verified at the bank counter, credentials are registered on the distributed ledger. History is immutably protected.",
    trust_2_t: "Submit Only What's Needed",
    trust_2_d: "When you select a destination, a QR is created containing only the necessary fields. Names and accounts never go to the chain.",
    trust_3_t: "Instant On-Site Verification",
    trust_3_d: "The terminal checks credential validity on the spot. Revoked or expired credentials are immediately blocked.",

    people_title: "Select a Persona",
    people_sub: "Foreign Worker Profiles (E-9 / H-2)",
    people_desc: "In real service, a worker holds only their personal wallet. Selecting a profile begins wallet onboarding for that worker.",

    pass_title: "iM Bank · Worker Pass",
    digital_identity: "Digital Identity",
    status_active: "Active",
    status_disabled: "Unavailable",
    btn_qr_submit: "Submit QR",
    chain_verified: "Verified on Blockchain",
    chain_not_verified: "Not Verified on Blockchain",
    expiry_left: "Expires in D-",
    expiry_expired: "Visa Expired",
    expiry_suffix: " Expires",

    today_status_caption: "Today's Status",
    today_status_safe: "Valid & Safe to Use",
    today_status_check: "Submission currently unavailable",
    badge_normal: "Valid",
    badge_check_needed: "Check Needed",
    label_visa_type: "Visa Status",
    label_valid_until: "Valid Until",
    submit_lead: "Need to submit credentials?",
    submit_sub: "Create a 60-second QR containing only required data",

    this_month_title: "This Month",
    loading: "Loading…",
    tab_mypass: "My Pass",
    tab_submit: "Submit",
    tab_finance: "Finance",

    step1_title: "1) Identity Verification at Bank",
    step1_desc: "Just as national IDs are verified via telecommunications, this wallet is established upon <b>bank real-name KYC</b>. As foreign workers undergo passport and alien card verification when opening payroll accounts, no extra steps are required.",
    label_worker_name: "Worker Name",
    btn_bank_verify: "Verify at Counter",
    step2_title: "2) Issue Wallet",
    step2_key_title: "Device Key Generation",
    step2_key_desc: "A key pair is generated inside your device. <b>The private key stays strictly on your device and is never sent to any server.</b>",
    step2_immi_title: "Immigration Inquiry (Required)",
    step2_immi_desc: "If no stay record exists, wallet issuance is denied. Forged or revoked alien cards are filtered here.",
    step2_etc_title: "Government Agency Check & Blockchain Record",
    step2_etc_desc: "Employment centers, clinics, and test institutes are verified, and your credential hash is registered on the ledger.",
    btn_register_wallet: "Issue Wallet & Register on Chain",

    submit_dest_title: "Where are you submitting to?",
    submit_dest_desc: "Generates a 60-second one-time QR containing only the minimum information required for the destination.",
    dest_biz: "Workplace Attendance",
    dest_biz_desc: "Commute clock-in and work eligibility verification",
    dest_clinic: "Hospital & Clinic",
    dest_clinic_desc: "National health insurance and medical check record",
    dest_bank: "Bank & Remittance",
    dest_bank_desc: "Payroll account, Forex Guard Insurance and overseas transfers",
    dest_insurer: "Insurance Claim",
    dest_insurer_desc: "Departure guarantee insurance & accident compensation",
    btn_generate_qr: "Generate 60-second One-Time QR",
    submit_page_title: "iM Worker Pass - Submit",
    submit_h1: "Submit Proof QR",
    submit_who_desc: "Safely submit only the credentials each institution needs",
    submit_lead_desc: "You submit fresh each time. Nothing is written on-chain — the latest values are re-checked with each institution.",
    no_wallet_title: "No wallet found",
    no_wallet_desc: "You need to issue a wallet first. This is a one-time step.",
    btn_goto_wallet: "Go issue a wallet →",
    submit_step1_title: "1) Choose where to submit",
    label_submit_target: "Submit to",
    label_symptom: "Symptom to tell the hospital",
    symptom_note: "This is the patient's own statement, not a diagnosis.",
    symptom_cough: "I have a cough",
    symptom_back_pain: "My back hurts",
    symptom_fever: "I think I have a fever",
    symptom_stomach: "My stomach feels upset",
    symptom_itchy: "My skin is itchy",
    attend_hint: "Clock-in/out doesn't re-query institutions. There's no need to ask twice a day — all that's needed is whether the stay status is still valid, checked on-chain at scan time. <b>The time itself is stamped by the company's own attendance system the instant its scanner reads the QR.</b>",
    insurance_redirect_note: "For insurance, choosing the product is the same as choosing the recipient, so no QR is needed — proceed on the <a href=\"insurance.html\">④ Insurance</a> screen.",
    btn_sign_and_generate_qr: "Sign on device & Generate QR",
    submit_step2_title: "2) QR to submit",
    btn_renew_qr: "Regenerate QR",
    payload_copy_note: "Copy the payload below and paste it into the <b>③ Scanner</b> screen to test verification without a camera. Changing one digit of the account number demonstrates tampering.",
    copy_payload_title: "Copy payload",
    copy_done_title: "Copied",
    copy_fail_title: "Copy failed — please select manually",
    submit_rejected: "Submission was rejected.",
    sig_verified_msg: "✓ Device signature verified — this request came from this wallet's owner.",
    sig_not_registered_msg: "This wallet has no registered device key. Signature verification was skipped.",
    attend_wait_msg: "The result will appear here once the site scanner reads this QR.",
    checkin_label: "Clock-in",
    checkout_label: "Clock-out",
    worked_time_label: "Worked",
    site_scanner_time_note: "Recorded using the time from the company's own scanner.",
    lookup_count_label: "Re-checked at submission",
    lookup_real_badge: "Real issuer",
    lookup_mock_badge: "Mock API",
    lookup_footer_note: "Nothing is pre-fetched and stored — every submission asks again, so there is no such thing as a stale copy. Institutions not needed for the purpose are never asked.",
    qr_time_left_label: "QR valid for: ",
    qr_expired_label: "QR expired",
    current_wallet_label: "Current wallet: ",
    switch_person_link: "Switch person",
    qr_expired_payload_msg: "This QR has expired and can no longer be used.",
  },

  vi: {
    lang_name: "Tiếng Việt",
    app_title: "iM PASS",
    worker_role: "Người lao động",
    switch_service: "Đổi dịch vụ",
    wallet_heading: "Ví số của tôi",
    wallet_subheading: "Tư cách lưu trú, việc làm & Hộ chiếu tài chính",
    first_time_notice: "Đăng ký ví chỉ cần thực hiện <b>lần đầu tiên</b>. Khi cần nộp giấy tờ, hãy dùng tab <b>Gửi QR</b> bên dưới.",

    home_kicker: "Ví định danh số mới kết nối đời sống và tài chính",
    home_heading: "Vui lòng chọn dịch vụ bạn muốn sử dụng",
    badge_worker: "Cá nhân",
    app_worker_name: "iM PASS Người lao động",
    app_worker_desc: "Lưu trữ giấy tờ và nộp vào những nơi cần thiết",
    badge_biz: "Doanh nghiệp",
    app_biz_name: "iM PASS Doanh nghiệp",
    app_biz_desc: "Xác minh tư cách người lao động nhanh chóng và an toàn",
    badge_admin: "Quản trị",
    app_admin_name: "iM PASS Ngân hàng & Cơ quan",
    app_admin_desc: "Phát hành tư cách và quản lý trạng thái thay đổi",
    trust_title: "Lý do bạn hoàn toàn có thể an tâm sử dụng",
    trust_1_t: "Đăng ký tư cách trên sổ cái",
    trust_1_d: "Sau khi xác thực tại ngân hàng, tư cách được ghi nhận trên sổ cái phân tán. Lịch sử thay đổi được bảo vệ an toàn.",
    trust_2_t: "Chỉ chọn nộp thông tin cần thiết",
    trust_2_d: "Khi chọn nơi nộp, mã QR chỉ chứa các mục cần thiết. Tên và tài khoản không bao giờ lưu trên chuỗi khối.",
    trust_3_t: "Xác nhận tức thì tại nơi tiếp nhận",
    trust_3_d: "Thiết bị đầu cuối sẽ đối chiếu tình trạng ngay tại chỗ. Thẻ bị thu hồi hoặc hết hạn sẽ bị chặn ngay lập tức.",

    people_title: "Chọn nhân vật trải nghiệm",
    people_sub: "Hồ sơ lao động nước ngoài (E-9 / H-2)",
    people_desc: "Trong thực tế, mỗi người chỉ có một ví duy nhất. Khi chọn, hệ thống sẽ bắt đầu cấp ví cho người đó.",

    pass_title: "Ngân hàng iM · Worker Pass",
    digital_identity: "Digital Identity",
    status_active: "Khả dụng",
    status_disabled: "Không khả dụng",
    btn_qr_submit: "Gửi QR",
    chain_verified: "Đã xác thực trên chuỗi khối",
    chain_not_verified: "Chưa xác thực trên chuỗi",
    expiry_left: "Hết hạn D-",
    expiry_expired: "Đã hết hạn lưu trú",
    expiry_suffix: " Hết hạn",

    today_status_caption: "Tình trạng hôm nay",
    today_status_safe: "Hợp lệ & Yên tâm sử dụng",
    today_status_check: "Hiện không thể xuất trình",
    badge_normal: "Bình thường",
    badge_check_needed: "Cần kiểm tra",
    label_visa_type: "Tư cách lưu trú (Visa)",
    label_valid_until: "Thời hạn đến",
    submit_lead: "Cần nộp giấy tờ xác nhận?",
    submit_sub: "Tạo mã QR 60 giây chỉ chứa các thông tin cần thiết",

    this_month_title: "Tháng này",
    loading: "Đang tải…",
    tab_mypass: "Thẻ của tôi",
    tab_submit: "Gửi QR",
    tab_finance: "Tài chính",

    step1_title: "1) Xác thực danh tính tại ngân hàng",
    step1_desc: "Ví này được thiết lập dựa trên <b>xác thực tên thật của ngân hàng</b>. Người lao động đã được đối chiếu hộ chiếu và thẻ cư trú khi mở tài khoản nhận lương nên không cần thủ tục phát sinh.",
    label_worker_name: "Tên người lao động",
    btn_bank_verify: "Xác thực tại quầy",
    step2_title: "2) Đăng ký ví",
    step2_key_title: "Tạo khóa bảo mật thiết bị",
    step2_key_desc: "Tạo cặp khóa ngay trên thiết bị của bạn. <b>Khóa riêng tư (private key) chỉ lưu trên máy và không bao giờ gửi lên máy chủ.</b>",
    step2_immi_title: "Tra cứu Cục Xuất nhập cảnh (Bắt buộc)",
    step2_immi_desc: "Nếu không có hồ sơ lưu trú hợp lệ, ví sẽ bị từ chối phát hành nhằm ngăn chặn thẻ cư trú giả mạo.",
    step2_etc_title: "Tra cứu cơ quan & Ghi nhận trên Blockchain",
    step2_etc_desc: "Thông tin việc làm, y tế và bảo hiểm được tích hợp và lưu dấu vân tay trên sổ cái an toàn.",
    btn_register_wallet: "Phát hành ví & Đăng ký Blockchain",

    submit_dest_title: "Bạn muốn gửi thông tin đến đâu?",
    submit_dest_desc: "Tạo mã QR dùng một lần trong 60 giây chỉ chứa thông tin tối thiểu theo yêu cầu của nơi nộp.",
    dest_biz: "Điểm danh nơi làm việc",
    dest_biz_desc: "Ghi nhận chấm công và xác thực tính hợp lệ của visa",
    dest_clinic: "Bệnh viện · Hiệu thuốc",
    dest_clinic_desc: "Xác thực bảo hiểm y tế và lịch sử khám sức khỏe",
    dest_bank: "Giao dịch ngân hàng",
    dest_bank_desc: "Mở tài khoản nhận lương, bảo hiểm tỷ giá và chuyển tiền về nước",
    dest_insurer: "Hồ sơ bảo hiểm",
    dest_insurer_desc: "Bảo hiểm mãn hạn xuất cảnh và bảo hiểm tai nạn",
    btn_generate_qr: "Tạo mã QR 60 giây",
    submit_page_title: "iM Worker Pass - Nộp hồ sơ",
    submit_h1: "Gửi mã QR chứng minh",
    submit_who_desc: "Chỉ gửi an toàn thông tin cần thiết cho từng cơ quan",
    submit_lead_desc: "Bạn gửi lại mỗi lần nộp. Không có gì được ghi lên blockchain — dữ liệu mới nhất được kiểm tra lại với từng cơ quan.",
    no_wallet_title: "Chưa có ví",
    no_wallet_desc: "Bạn cần cấp ví trước. Đây là bước chỉ thực hiện một lần.",
    btn_goto_wallet: "Đi cấp ví →",
    submit_step1_title: "1) Chọn nơi nộp",
    label_submit_target: "Nơi nhận",
    label_symptom: "Triệu chứng cần báo cho bệnh viện",
    symptom_note: "Đây là lời khai của bệnh nhân, không phải chẩn đoán.",
    symptom_cough: "Tôi bị ho",
    symptom_back_pain: "Tôi đau lưng",
    symptom_fever: "Tôi có vẻ bị sốt",
    symptom_stomach: "Tôi khó chịu ở bụng",
    symptom_itchy: "Da tôi bị ngứa",
    attend_hint: "Chấm công không cần hỏi lại cơ quan. Không cần hỏi hai lần mỗi ngày — điều cần biết chỉ là tư cách cư trú còn hiệu lực hay không, được xác nhận qua blockchain khi quét. <b>Thời gian được hệ thống chấm công của công ty ghi lại ngay khi máy quét đọc mã.</b>",
    insurance_redirect_note: "Với bảo hiểm, chọn sản phẩm cũng là chọn nơi nhận, nên không cần mã QR — thực hiện ở màn hình <a href=\"insurance.html\">④ Bảo hiểm</a>.",
    btn_sign_and_generate_qr: "Ký trên thiết bị & Tạo QR",
    submit_step2_title: "2) Mã QR để nộp",
    btn_renew_qr: "Tạo lại mã QR",
    payload_copy_note: "Sao chép payload bên dưới và dán vào màn hình <b>③ Máy quét</b> để thử xác minh mà không cần camera. Đổi một chữ số của số tài khoản để minh họa việc giả mạo.",
    copy_payload_title: "Sao chép payload",
    copy_done_title: "Đã sao chép",
    copy_fail_title: "Sao chép thất bại — vui lòng chọn thủ công",
    submit_rejected: "Việc nộp đã bị từ chối.",
    sig_verified_msg: "✓ Đã xác minh chữ ký thiết bị — yêu cầu này đến từ chủ sở hữu ví.",
    sig_not_registered_msg: "Ví này chưa đăng ký khóa thiết bị. Đã bỏ qua xác minh chữ ký.",
    attend_wait_msg: "Kết quả sẽ hiện ở đây khi máy quét tại công trường đọc mã QR này.",
    checkin_label: "Vào ca",
    checkout_label: "Tan ca",
    worked_time_label: "Đã làm",
    site_scanner_time_note: "Được ghi nhận theo thời gian của máy quét công ty.",
    lookup_count_label: "Đã kiểm tra lại lúc nộp",
    lookup_real_badge: "Cơ quan cấp thực tế",
    lookup_mock_badge: "API giả lập",
    lookup_footer_note: "Không có gì được lấy trước và lưu trữ — mỗi lần nộp đều hỏi lại, nên không tồn tại bản cũ. Các cơ quan không cần thiết cho mục đích sẽ không bị hỏi.",
    qr_time_left_label: "QR còn hiệu lực: ",
    qr_expired_label: "Mã QR đã hết hạn",
    current_wallet_label: "Ví hiện tại: ",
    switch_person_link: "Đổi người khác",
    qr_expired_payload_msg: "Mã QR đã hết hạn và không thể sử dụng.",
  },

  id: {
    lang_name: "Bahasa Indonesia",
    app_title: "iM PASS",
    worker_role: "Pekerja",
    switch_service: "Ganti Layanan",
    wallet_heading: "Dompet Digital Saya",
    wallet_subheading: "Status Izin Tinggal & Paspor Keuangan",
    first_time_notice: "Penerbitan dompet hanya dilakukan <b>satu kali di awal</b>. Gunakan tab <b>Kirim</b> di bawah untuk menyerahkan dokumen.",

    home_kicker: "Dompet identitas baru yang menghubungkan kehidupan dan keuangan",
    home_heading: "Silakan pilih layanan yang ingin digunakan",
    badge_worker: "Pribadi",
    app_worker_name: "iM PASS Pekerja",
    app_worker_desc: "Simpan dokumen Anda dan serahkan saat dibutuhkan",
    badge_biz: "Perusahaan",
    app_biz_name: "iM PASS Perusahaan",
    app_biz_desc: "Verifikasi dokumen pekerja dengan cepat dan aman",
    badge_admin: "Pengelola",
    app_admin_name: "iM PASS Bank & Lembaga",
    app_admin_desc: "Menerbitkan kredensial dan mengelola status perubahan",
    trust_title: "Mengapa Anda Dapat Menggunakannya dengan Tenang",
    trust_1_t: "Mendaftarkan dokumen ke buku besar",
    trust_1_d: "Setelah verifikasi di bank, dokumen dicatat di buku besar terdesentralisasi dan terlindungi secara aman.",
    trust_2_t: "Hanya serahkan data yang diperlukan",
    trust_2_d: "Saat memilih tujuan, QR dibuat hanya dengan data yang dibutuhkan. Nama dan rekening tidak diunggah ke blockchain.",
    trust_3_t: "Langsung diverifikasi di lokasi penerima",
    trust_3_d: "Terminal memverifikasi status dokumen di tempat. Kredensial yang dibatalkan atau kedaluwarsa segera disaring.",

    people_title: "Pilih Profil Pengguna",
    people_sub: "Profil Pekerja Asing (E-9 / H-2)",
    people_desc: "Dalam praktiknya, pekerja hanya memiliki satu dompet. Memilih profil akan memulai penerbitan dompet untuk orang tersebut.",

    pass_title: "Bank iM · Worker Pass",
    digital_identity: "Digital Identity",
    status_active: "Aktif",
    status_disabled: "Tidak Aktif",
    btn_qr_submit: "Kirim QR",
    chain_verified: "Terverifikasi di Blockchain",
    chain_not_verified: "Belum Terverifikasi",
    expiry_left: "Kedaluwarsa D-",
    expiry_expired: "Izin Tinggal Kedaluwarsa",
    expiry_suffix: " Kedaluwarsa",

    today_status_caption: "Status Hari Ini",
    today_status_safe: "Aman & Siap Digunakan",
    today_status_check: "Saat ini tidak dapat diajukan",
    badge_normal: "Normal",
    badge_check_needed: "Perlu Cek",
    label_visa_type: "Jenis Visa",
    label_valid_until: "Masa Berlaku",
    submit_lead: "Perlu menyerahkan dokumen?",
    submit_sub: "Buat QR 60 detik berisi informasi yang diperlukan saja",

    this_month_title: "Bulan Ini",
    loading: "Memuat…",
    tab_mypass: "Pass Saya",
    tab_submit: "Kirim",
    tab_finance: "Keuangan",

    step1_title: "1) Verifikasi Identitas di Bank",
    step1_desc: "Dompet ini dibangun di atas <b>verifikasi nama asli bank</b>. Pekerja asing telah mencocokkan paspor dan kartu ARC saat membuka rekening gaji sehingga prosesnya praktis.",
    label_worker_name: "Nama Pekerja",
    btn_bank_verify: "Verifikasi di Loket",
    step2_title: "2) Registrasi Dompet",
    step2_key_title: "Pembuatan Kunci Perangkat",
    step2_key_desc: "Membuat sepasang kunci di peramban ini. <b>Kunci privat tetap ada di perangkat dan tidak pernah dikirim ke server.</b>",
    step2_immi_title: "Pemeriksaan Imigrasi (Wajib)",
    step2_immi_desc: "Jika tidak ada catatan izin tinggal, penerbitan dompet akan dibatalkan untuk mencegah pemalsuan.",
    step2_etc_title: "Pengecekan Instansi & Catatan Blockchain",
    step2_etc_desc: "Data ketenagakerjaan, kesehatan, dan asuransi diverifikasi ke buku besar terdesentralisasi.",
    btn_register_wallet: "Terbitkan Dompet & Catat ke Blockchain",

    submit_dest_title: "Ke mana Anda ingin menyerahkan dokumen?",
    submit_dest_desc: "Membuat QR satu kali pakai (60 detik) berisi data minimum yang dibutuhkan.",
    dest_biz: "Kehadiran Tempat Kerja",
    dest_biz_desc: "Pencatatan absensi dan keabsahan izin kerja",
    dest_clinic: "Rumah Sakit & Apotek",
    dest_clinic_desc: "Verifikasi asuransi kesehatan nasional",
    dest_bank: "Layanan Bank",
    dest_bank_desc: "Rekening gaji, asuransi lindung nilai kurs & remitansi",
    dest_insurer: "Pengajuan Asuransi",
    dest_insurer_desc: "Asuransi kepulangan dan asuransi kecelakaan",
    btn_generate_qr: "Buat QR 60 Detik",
    submit_page_title: "iM Worker Pass - Kirim",
    submit_h1: "Kirim QR Bukti",
    submit_who_desc: "Kirim dengan aman hanya kredensial yang dibutuhkan setiap lembaga",
    submit_lead_desc: "Anda mengirim ulang setiap kali. Tidak ada yang ditulis on-chain — nilai terbaru diperiksa ulang ke setiap lembaga.",
    no_wallet_title: "Dompet tidak ditemukan",
    no_wallet_desc: "Anda perlu menerbitkan dompet terlebih dahulu. Ini hanya dilakukan sekali.",
    btn_goto_wallet: "Buat dompet →",
    submit_step1_title: "1) Pilih tujuan pengiriman",
    label_submit_target: "Kirim ke",
    label_symptom: "Gejala untuk disampaikan ke rumah sakit",
    symptom_note: "Ini pernyataan pasien sendiri, bukan diagnosis.",
    symptom_cough: "Saya batuk",
    symptom_back_pain: "Punggung saya sakit",
    symptom_fever: "Sepertinya saya demam",
    symptom_stomach: "Perut saya tidak nyaman",
    symptom_itchy: "Kulit saya gatal",
    attend_hint: "Absensi tidak melakukan query ulang ke lembaga. Tidak perlu ditanyakan dua kali sehari — yang dibutuhkan hanyalah apakah status tinggal masih berlaku, dicek on-chain saat pemindaian. <b>Waktu dicatat oleh sistem absensi perusahaan sendiri saat pemindai membaca QR.</b>",
    insurance_redirect_note: "Untuk asuransi, memilih produk sama dengan memilih penerima, jadi QR tidak diperlukan — lanjutkan di layar <a href=\"insurance.html\">④ Asuransi</a>.",
    btn_sign_and_generate_qr: "Tanda tangan perangkat & Buat QR",
    submit_step2_title: "2) QR untuk dikirim",
    btn_renew_qr: "Buat ulang QR",
    payload_copy_note: "Salin payload di bawah dan tempel di layar <b>③ Pemindai</b> untuk menguji verifikasi tanpa kamera. Mengubah satu digit nomor rekening mendemonstrasikan pemalsuan.",
    copy_payload_title: "Salin payload",
    copy_done_title: "Tersalin",
    copy_fail_title: "Gagal menyalin — silakan pilih manual",
    submit_rejected: "Pengiriman ditolak.",
    sig_verified_msg: "✓ Tanda tangan perangkat terverifikasi — permintaan ini dari pemilik dompet ini.",
    sig_not_registered_msg: "Dompet ini belum mendaftarkan kunci perangkat. Verifikasi tanda tangan dilewati.",
    attend_wait_msg: "Hasil akan muncul di sini setelah pemindai lokasi membaca QR ini.",
    checkin_label: "Masuk kerja",
    checkout_label: "Pulang kerja",
    worked_time_label: "Bekerja",
    site_scanner_time_note: "Dicatat berdasarkan waktu dari pemindai perusahaan.",
    lookup_count_label: "Diperiksa ulang saat pengiriman",
    lookup_real_badge: "Penerbit asli",
    lookup_mock_badge: "API simulasi",
    lookup_footer_note: "Tidak ada yang diambil dan disimpan sebelumnya — setiap pengiriman selalu bertanya ulang, sehingga tidak ada versi usang. Lembaga yang tidak diperlukan tidak akan ditanya.",
    qr_time_left_label: "QR berlaku: ",
    qr_expired_label: "QR kedaluwarsa",
    current_wallet_label: "Dompet saat ini: ",
    switch_person_link: "Ganti orang",
    qr_expired_payload_msg: "QR ini sudah kedaluwarsa dan tidak dapat digunakan.",
  },

  uz: {
    lang_name: "Oʻzbekcha",
    app_title: "iM PASS",
    worker_role: "Ishchi",
    switch_service: "Xizmatni almashtirish",
    wallet_heading: "Raqamli hamyonim",
    wallet_subheading: "Yashash va mehnat maqomi hamda moliyaviy pasport",
    first_time_notice: "Hamyon berish <b>faqat bir marta</b> amalga oshiriladi. Hujjatlarni topshirish uchun quyidagi <b>Yuborish</b> boʻlimidan foydalaning.",

    home_kicker: "Hayot va moliyani bogʻlovchi yangi raqamli identifikatsiya hamyoni",
    home_heading: "Foydalanmoqchi boʻlgan xizmatni tanlang",
    badge_worker: "Shaxsiy",
    app_worker_name: "iM PASS Ishchi",
    app_worker_desc: "Hujjatlaringizni xavfsiz saqlang va kerakli joyga topshiring",
    badge_biz: "Korxona",
    app_biz_name: "iM PASS Korxona",
    app_biz_desc: "Ishchilarning hujjatlarini tez va xavfsiz tekshiring",
    badge_admin: "Boshqaruv",
    app_admin_name: "iM PASS Bank & Tashkilot",
    app_admin_desc: "Hujjatlarni berish va ularning holatini boshqarish",
    trust_title: "Nega xavfsiz foydalanishingiz mumkin?",
    trust_1_t: "Hujjatlarni blokcheynga kiritish",
    trust_1_d: "Bankda shaxs tasdiqlangach, maʼlumotlar blokcheynga kiritiladi va oʻzgarishlar tarixi xavfsiz saqlanadi.",
    trust_2_t: "Faqat kerakli maʼlumotlarni tanlab topshiring",
    trust_2_d: "Topshirish joyini tanlaganda faqat kerakli qismli QR yaratiladi. Ism va hisob raqami blokcheynga chiqmaydi.",
    trust_3_t: "Qabul qiluvchi joyda darhol tekshirish",
    trust_3_d: "Terminal darhol hujjat holatini tekshiradi. Bekor qilingan yoki muddati oʻtgan hujjatlar shu zahoti toʻxtatiladi.",

    people_title: "Profilni tanlang",
    people_sub: "Chet ellik ishchi profillari (E-9 / H-2)",
    people_desc: "Haqiqiy xizmatda ishchida faqat bitta shaxsiy hamyon boʻladi. Profil tanlangach, oʻsha shaxs uchun hamyon ochiladi.",

    pass_title: "iM Bank · Worker Pass",
    digital_identity: "Digital Identity",
    status_active: "Faol",
    status_disabled: "Faol emas",
    btn_qr_submit: "QR yuborish",
    chain_verified: "Blokcheynda tasdiqlangan",
    chain_not_verified: "Blokcheynda tasdiqlanmagan",
    expiry_left: "Muddati D-",
    expiry_expired: "Muddati tugagan",
    expiry_suffix: " Tugash sanasi",

    today_status_caption: "Bugungi maqom",
    today_status_safe: "Foydalanish uchun xavfsiz va toʻgʻri",
    today_status_check: "Hozircha topshirish mumkin emas",
    badge_normal: "Normal",
    badge_check_needed: "Tekshirish kerak",
    label_visa_type: "Viza maqomi",
    label_valid_until: "Amal qilish muddati",
    submit_lead: "Hujjat topshirishingiz kerakmi?",
    submit_sub: "Faqat kerakli maʼlumotlarni oʻz ichiga olgan 60 soniyalik QR yaratish",

    this_month_title: "Shu oy",
    loading: "Yuklanmoqda…",
    tab_mypass: "Passim",
    tab_submit: "Yuborish",
    tab_finance: "Moliya",

    step1_title: "1) Bankda shaxsni tasdiqlash",
    step1_desc: "Ushbu hamyon <b>bankning haqiqiy ism tekshiruvi</b> asosida yaratilgan. Ishchilar oylik hisobini ochishda pasport va ID kartani tekshirganlari sababli qoʻshimcha jarayon talab etilmaydi.",
    label_worker_name: "Ishchining ismi",
    btn_bank_verify: "Kassada tekshirish",
    step2_title: "2) Hamyonni roʻyxatdan oʻtkazish",
    step2_key_title: "Qurilma kalitini yaratish",
    step2_key_desc: "Qurilmangizda shaxsiy kalit juftligi yaratiladi. <b>Shaxsiy kalit (private key) faqat qurilmada qoladi va serverga yuborilmaydi.</b>",
    step2_immi_title: "Immigratsiya xizmatini tekshirish (Majburiy)",
    step2_immi_desc: "Agar yashash qaydi boʻlmasa, soxta kartalarni aniqlash uchun hamyon berilmaydi.",
    step2_etc_title: "Tashkilotlar va Blokcheyn roʻyxati",
    step2_etc_desc: "Bandlik markazi, shifoxona maʼlumotlari blokcheyn xavfsiz reyestriga kiritiladi.",
    btn_register_wallet: "Hamyon berish va Blokcheynga kiritish",

    submit_dest_title: "Qayerga topshirmoqchisiz?",
    submit_dest_desc: "Manzil uchun faqat minimal kerakli maʼlumotlarni oʻz ichiga olgan 60 soniyalik bir martalik QR yaratadi.",
    dest_biz: "Ish joyidagi davomat",
    dest_biz_desc: "Keldi-ketdini qayd qilish va viza qonuniyligini tekshirish",
    dest_clinic: "Shifoxona va dorixona",
    dest_clinic_desc: "Tibbiy sugʻurta va koʻrik maʼlumotlarini tekshirish",
    dest_bank: "Bank xizmatlari",
    dest_bank_desc: "Ish haqi hisobi, valyuta kafolati sugʻurtasi va oʻtkazmalar",
    dest_insurer: "Sugʻurta arizasi",
    dest_insurer_desc: "Chiqish muddati sugʻurtasi va baxtsiz hodisa sugʻurtasi",
    btn_generate_qr: "60 soniyalik QR yaratish",
    submit_page_title: "iM Worker Pass - Topshirish",
    submit_h1: "Tasdiqlovchi QR yuborish",
    submit_who_desc: "Har bir muassasaga faqat kerakli ma'lumotni xavfsiz yuboring",
    submit_lead_desc: "Har safar yangidan yuborasiz. Zanjirga hech narsa yozilmaydi — eng so'nggi qiymatlar har bir muassasadan qayta so'raladi.",
    no_wallet_title: "Hamyon topilmadi",
    no_wallet_desc: "Avval hamyon ochishingiz kerak. Bu faqat bir marta bajariladi.",
    btn_goto_wallet: "Hamyon ochishga o'tish →",
    submit_step1_title: "1) Qayerga topshirishni tanlang",
    label_submit_target: "Kimga topshiriladi",
    label_symptom: "Kasalxonaga aytiladigan alomat",
    symptom_note: "Bu bemorning o'z bayonoti, tashxis emas.",
    symptom_cough: "Yo'talim bor",
    symptom_back_pain: "Belim og'rimoqda",
    symptom_fever: "Isitmam bor shekilli",
    symptom_stomach: "Qornim behuzur",
    symptom_itchy: "Terim qichimoqda",
    attend_hint: "Kelish/ketishni qayd etishda muassasalardan qayta so'ralmaydi. Kuniga ikki marta so'rash shart emas — faqat turar joy maqomi hali kuchdami, skanerlashda zanjirdan tekshiriladi. <b>Vaqtning o'zini kompaniyaning davomat tizimi skaner QR ni o'qigan zahoti belgilaydi.</b>",
    insurance_redirect_note: "Sug'urta uchun mahsulotni tanlash qabul qiluvchini tanlash bilan bir xil, shuning uchun QR shart emas — <a href=\"insurance.html\">④ Sug'urta</a> ekranida davom eting.",
    btn_sign_and_generate_qr: "Qurilmada imzolash va QR yaratish",
    submit_step2_title: "2) Topshiriladigan QR",
    btn_renew_qr: "QR ni qayta yaratish",
    payload_copy_note: "Quyidagi payload'ni nusxalab, <b>③ Skaner</b> ekraniga joylashtiring — kamerasiz tekshirishni sinab ko'rasiz. Hisob raqamining bitta raqamini o'zgartirish soxtalashtirishni namoyish etadi.",
    copy_payload_title: "Payload nusxalash",
    copy_done_title: "Nusxalandi",
    copy_fail_title: "Nusxalash muvaffaqiyatsiz — qo'lda tanlang",
    submit_rejected: "Topshirish rad etildi.",
    sig_verified_msg: "✓ Qurilma imzosi tasdiqlandi — bu so'rov ushbu hamyon egasidan kelgan.",
    sig_not_registered_msg: "Bu hamyonda qurilma kaliti ro'yxatdan o'tmagan. Imzo tekshiruvi o'tkazib yuborildi.",
    attend_wait_msg: "Ish joyi skaneri ushbu QR ni o'qigach, natija shu yerda ko'rinadi.",
    checkin_label: "Ishga kelish",
    checkout_label: "Ishdan ketish",
    worked_time_label: "Ishlangan",
    site_scanner_time_note: "Kompaniya skaneri vaqti bo'yicha qayd etildi.",
    lookup_count_label: "Topshirish vaqtida qayta tekshirildi",
    lookup_real_badge: "Haqiqiy beruvchi",
    lookup_mock_badge: "Sinov API",
    lookup_footer_note: "Hech narsa oldindan olib saqlanmaydi — har topshirishda qayta so'raladi, shuning uchun eskirgan nusxa bo'lmaydi. Maqsad uchun kerak bo'lmagan muassasalardan so'ralmaydi.",
    qr_time_left_label: "QR amal qilish muddati: ",
    qr_expired_label: "QR muddati tugadi",
    current_wallet_label: "Joriy hamyon: ",
    switch_person_link: "Boshqa shaxsga almashtirish",
    qr_expired_payload_msg: "Ushbu QR muddati tugagan va endi ishlatib bo'lmaydi.",
  },

  zh: {
    lang_name: "中文",
    app_title: "iM PASS",
    worker_role: "劳动者",
    switch_service: "切换服务",
    wallet_heading: "我的数字钱包",
    wallet_subheading: "居留与就业资格及金融通行证",
    first_time_notice: "钱包仅需在<b>首次注册</b>一次。后续提交请使用下方的<b>提交</b>标签页。",

    home_kicker: "连接生活与金融的全新数字身份钱包",
    home_heading: "请选择您要使用的服务",
    badge_worker: "个人",
    app_worker_name: "iM PASS 劳动者",
    app_worker_desc: "安全保存您的个人资格，随时按需出示提交",
    badge_biz: "企业",
    app_biz_name: "iM PASS 企业端",
    app_biz_desc: "快速、安全地核验外籍劳动者的合法身份与资质",
    badge_admin: "管理端",
    app_admin_name: "iM PASS 银行与监管机构",
    app_admin_desc: "签发数字凭证，对资质全生命周期变更进行存证管理",
    trust_title: "值得安心信赖的核心技术保障",
    trust_1_t: "分布式账本登记",
    trust_1_d: "在银行网点完成实名确认后，凭证哈希即登记于分布式账本，后续变更历史受密码学严密保护。",
    trust_2_t: "最小化自主披露",
    trust_2_d: "选择提交机构后，系统仅提取必要字段生成动态QR码。真实姓名与银行账号绝不上链。",
    trust_3_t: "现场秒级对账核验",
    trust_3_d: "验证终端当场连线核对链上存证。已被撤回或已过期的无效资格将被立即拦截。",

    people_title: "请选择演示身份",
    people_sub: "外籍劳动者画像档案 (E-9 / H-2)",
    people_desc: "在真实服务场景中，每位劳动者仅持有唯一独立钱包。选择后即可开启该身份的开卡与链上登记流程。",

    pass_title: "iM银行 · Worker Pass",
    digital_identity: "Digital Identity",
    status_active: "可使用",
    status_disabled: "不可用",
    btn_qr_submit: "出示QR",
    chain_verified: "区块链已核验",
    chain_not_verified: "区块链未核验",
    expiry_left: "到期 D-",
    expiry_expired: "居留期已满",
    expiry_suffix: " 到期",

    today_status_caption: "今日资格状态",
    today_status_safe: "资格正常，可放心使用",
    today_status_check: "当前无法出示",
    badge_normal: "正常",
    badge_check_needed: "需确认",
    label_visa_type: "居留资格 (签证)",
    label_valid_until: "有效期至",
    submit_lead: "有需要提交的证明吗？",
    submit_sub: "生成仅包含必要信息的60秒一次性动态QR码",

    this_month_title: "本月",
    loading: "加载中…",
    tab_mypass: "我的卡片",
    tab_submit: "提交",
    tab_finance: "金融生活",

    step1_title: "1) 银行网点实名认证",
    step1_desc: "正如各类数字凭证基于实名体系建立，本钱包建立在<b>银行实名认证</b>之上。外籍劳动者在开立工资账户时已完成护照与外国人登录证核验，无需额外繁琐流程。",
    label_worker_name: "劳动者姓名",
    btn_bank_verify: "网点实名核验",
    step2_title: "2) 钱包注册",
    step2_key_title: "终端密钥生成",
    step2_key_desc: "在此设备本地生成一对非对称密钥。<b>私钥仅保存在您的终端设备，绝不上传至服务器。</b>",
    step2_immi_title: "出入境记录核查 (必需)",
    step2_immi_desc: "若无合法有效居留记录，系统将阻断签发，以识别伪造或已被注销的外国人登录证。",
    step2_etc_title: "机构核验与区块链存证",
    step2_etc_desc: "劳动部门、体检机构等资格核验哈希登记于分布式账本，保障数据真实性。",
    btn_register_wallet: "签发钱包并登记至区块链",

    submit_dest_title: "要向何处提交？",
    submit_dest_desc: "生成仅包含目标机构所需最低限度信息的60秒一次性动态QR码。",
    dest_biz: "工作单位出勤",
    dest_biz_desc: "打卡考勤及合法就业资格核对",
    dest_clinic: "医院 · 药店",
    dest_clinic_desc: "国民健康保险及体检资质核验",
    dest_bank: "银行金融业务",
    dest_bank_desc: "工资账户开立、汇率保障保险及境外汇款",
    dest_insurer: "保险理赔与加入",
    dest_insurer_desc: "出国期满保险及意外伤害险",
    btn_generate_qr: "生成60秒一次性QR码",
    submit_page_title: "iM Worker Pass - 提交",
    submit_h1: "提交证明二维码",
    submit_who_desc: "只向相关机构安全提交所需的资格信息",
    submit_lead_desc: "每次提交都会重新生成。区块链上不会写入任何内容，系统会向各机构重新查询最新状态。",
    no_wallet_title: "尚未开通钱包",
    no_wallet_desc: "请先开通数字钱包，此步骤仅需一次。",
    btn_goto_wallet: "前往开通钱包 →",
    submit_step1_title: "1）选择提交对象",
    label_submit_target: "提交对象",
    label_symptom: "需告知医院的症状",
    symptom_note: "此为患者本人陈述，并非诊断结果。",
    symptom_cough: "我咳嗽",
    symptom_back_pain: "我腰痛",
    symptom_fever: "我好像发烧了",
    symptom_stomach: "我肚子不舒服",
    symptom_itchy: "我皮肤发痒",
    attend_hint: "打卡不会重新查询各机构。不需要每天问两次——只需确认停留资格是否仍然有效，扫码时通过链上查询确认。<b>时间由公司自己的考勤系统在扫描仪读取二维码的瞬间记录。</b>",
    insurance_redirect_note: "保险业务中选择产品即选择接收方，因此不需要二维码——请在<a href=\"insurance.html\">④ 保险</a>页面办理。",
    btn_sign_and_generate_qr: "设备签名并生成二维码",
    submit_step2_title: "2）提交用二维码",
    btn_renew_qr: "重新生成二维码",
    payload_copy_note: "复制下方的 payload 并粘贴到<b>③ 扫描仪</b>的输入框，即可在没有摄像头的情况下测试验证。将账号中的一位数字改动即可演示篡改检测。",
    copy_payload_title: "复制payload",
    copy_done_title: "已复制",
    copy_fail_title: "复制失败——请手动选择",
    submit_rejected: "提交被拒绝。",
    sig_verified_msg: "✓ 设备签名验证通过——该请求来自此钱包的所有者。",
    sig_not_registered_msg: "该钱包尚未注册设备密钥，已跳过签名验证。",
    attend_wait_msg: "工地扫描仪读取此二维码后，结果将显示在此处。",
    checkin_label: "上班",
    checkout_label: "下班",
    worked_time_label: "工作时长",
    site_scanner_time_note: "以公司扫描仪的时间为准记录。",
    lookup_count_label: "提交时重新查询",
    lookup_real_badge: "真实发证机构",
    lookup_mock_badge: "模拟接口",
    lookup_footer_note: "不会预先获取并保存任何信息——每次提交都会重新查询，因此不存在过期版本。与目的无关的机构不会被查询。",
    qr_time_left_label: "二维码有效时间：",
    qr_expired_label: "二维码已过期",
    current_wallet_label: "当前钱包：",
    switch_person_link: "切换其他人员",
    qr_expired_payload_msg: "该二维码已过期，无法使用。",
  },

  th: {
    lang_name: "ไทย",
    app_title: "iM PASS",
    worker_role: "แรงงาน",
    switch_service: "เปลี่ยนบริการ",
    wallet_heading: "กระเป๋าเงินดิจิทัลของฉัน",
    wallet_subheading: "สถานะการพำนัก การทำงาน และพาสปอร์ตการเงิน",
    first_time_notice: "การออกกระเป๋าเงินทำเพียง <b>ครั้งแรกครั้งเดียว</b> เท่านั้น เมื่อต้องการยื่นเอกสาร ให้ใช้แท็บ <b>ส่ง QR</b> ด้านล่าง",

    home_kicker: "กระเป๋าเงินระบุตัวตนดิจิทัลใหม่ เชื่อมโยงชีวิตและการเงิน",
    home_heading: "โปรดเลือกบริการที่คุณต้องการใช้งาน",
    badge_worker: "บุคคล",
    app_worker_name: "iM PASS แรงงาน",
    app_worker_desc: "เก็บรักษาเอกสารสิทธิ์ของคุณอย่างปลอดภัย และยื่นส่งเมื่อจำเป็น",
    badge_biz: "สถานประกอบการ",
    app_biz_name: "iM PASS สถานประกอบการ",
    app_biz_desc: "ตรวจสอบคุณสมบัติของแรงงานได้อย่างรวดเร็วและปลอดภัย",
    badge_admin: "ผู้ดูแลระบบ",
    app_admin_name: "iM PASS ธนาคารและหน่วยงาน",
    app_admin_desc: "ออกเอกสารรับรองและจัดการสถานะการเปลี่ยนแปลง",
    trust_title: "เหตุผลที่คุณมั่นใจและใช้งานได้อย่างปลอดภัย",
    trust_1_t: "ลงทะเบียนคุณสมบัติบนบัญชีแยกประเภท",
    trust_1_d: "เมื่อยืนยันตัวตนที่เคาน์เตอร์ธนาคารแล้ว ข้อมูลจะถูกบันทึกบนบัญชีแยกประเภทแบบกระจายศูนย์ ประวัติการเปลี่ยนแปลงได้รับการปกป้องอย่างปลอดภัย",
    trust_2_t: "เลือกส่งเฉพาะข้อมูลที่จำเป็นเท่านั้น",
    trust_2_d: "เมื่อเลือกปลายทาง ระบบจะสร้าง QR ที่มีเฉพาะข้อมูลที่จำเป็นเท่านั้น ชื่อและบัญชีจะไม่ถูกบันทึกบนบล็อกเชน",
    trust_3_t: "ตรวจสอบได้ทันที ณ จุดรับเรื่อง",
    trust_3_d: "เครื่องปลายทางของสถานประกอบการจะตรวจสอบสถานะทันที คุณสมบัติที่ถูกเพิกถอนหรือหมดอายุจะถูกคัดกรองทันที",

    people_title: "เลือกโปรไฟล์เพื่อดูการทำงาน",
    people_sub: "เลือกโปรไฟล์แรงงานต่างชาติ (E-9 / H-2)",
    people_desc: "ในบริการจริง แรงงานจะมีกระเป๋าเงินเพียงใบเดียว เมื่อเลือกแล้ว จะเริ่มตั้งแต่ขั้นตอนการออกกระเป๋าเงินของบุคคลนั้น",

    pass_title: "ธนาคาร iM · Worker Pass",
    digital_identity: "Digital Identity",
    status_active: "ใช้งานได้",
    status_disabled: "ใช้งานไม่ได้",
    btn_qr_submit: "ส่ง QR",
    chain_verified: "ยืนยันบนบล็อกเชนแล้ว",
    chain_not_verified: "ไม่พบการยืนยันบนบล็อกเชน",
    expiry_left: "หมดอายุ D-",
    expiry_expired: "ระยะเวลาการพำนักหมดอายุแล้ว",
    expiry_suffix: " หมดอายุ",

    today_status_caption: "สถานะคุณสมบัติวันนี้",
    today_status_safe: "ถูกต้อง ปลอดภัย พร้อมใช้งาน",
    today_status_check: "ขณะนี้ไม่สามารถยื่นเอกสารได้",
    badge_normal: "ปกติ",
    badge_check_needed: "ต้องตรวจสอบ",
    label_visa_type: "ประเภทวีซ่า (สถานะพำนัก)",
    label_valid_until: "วันหมดอายุ",
    submit_lead: "มีเอกสารที่ต้องยื่นหรือไม่?",
    submit_sub: "สร้าง QR ชั่วคราว 60 วินาที ที่มีเฉพาะข้อมูลที่จำเป็น",

    this_month_title: "เดือนนี้",
    loading: "กำลังโหลด…",
    tab_mypass: "พาสของฉัน",
    tab_submit: "ส่ง QR",
    tab_finance: "การเงิน",

    step1_title: "1) ยืนยันตัวตนที่เคาน์เตอร์ธนาคาร",
    step1_desc: "กระเป๋าเงินนี้สร้างขึ้นบน <b>การยืนยันตัวตนด้วยชื่อจริงของธนาคาร</b> แรงงานต่างชาติได้ผ่านการตรวจสอบหนังสือเดินทางและบัตรลงทะเบียนคนต่างด้าวเมื่อเปิดบัญชีเงินเดือนแล้ว จึงไม่มีขั้นตอนที่ซับซ้อนเพิ่มเติม",
    label_worker_name: "ชื่อแรงงาน",
    btn_bank_verify: "ยืนยันตัวตนที่เคาน์เตอร์",
    step2_title: "2) ลงทะเบียนกระเป๋าเงิน",
    step2_key_title: "สร้างคีย์บนอุปกรณ์",
    step2_key_desc: "สร้างคู่คีย์บนเบราว์เซอร์นี้ <b>ไพรเวตคีย์จะถูกเก็บไว้ในอุปกรณ์เท่านั้นและไม่ถูกส่งไปยังเซิร์ฟเวอร์</b>",
    step2_immi_title: "ตรวจสอบสำนักงานตรวจคนเข้าเมือง (จำเป็น)",
    step2_immi_desc: "หากไม่มีบันทึกการพำนัก จะไม่ออกกระเป๋าเงิน เพื่อป้องกันบัตรคนต่างด้าวปลอมหรือถูกเพิกถอน",
    step2_etc_title: "ตรวจสอบหน่วยงานและบันทึกบนบล็อกเชน",
    step2_etc_desc: "ข้อมูลการจ้างงาน การแพทย์ และการศึกษาจะถูกบันทึกแฮชไว้บนบล็อกเชนอย่างปลอดภัย",
    btn_register_wallet: "ออกกระเป๋าเงินและลงทะเบียนบนบล็อกเชน",

    submit_dest_title: "คุณต้องการยื่นเอกสารที่ใด?",
    submit_dest_desc: "สร้าง QR ใช้ครั้งเดียว 60 วินาที ที่มีเฉพาะข้อมูลขั้นต่ำตามที่ปลายทางต้องการ",
    dest_biz: "การลงเวลาทำงาน",
    dest_biz_desc: "บันทึกเวลาเข้าออกงานและตรวจสอบความถูกต้องของสถานะการพำนัก",
    dest_clinic: "โรงพยาบาลและร้านขายยา",
    dest_clinic_desc: "ตรวจสอบสิทธิ์ประกันสุขภาพและการตรวจสุขภาพ",
    dest_bank: "ธุรกรรมธนาคาร",
    dest_bank_desc: "เปิดบัญชีเงินเดือน ประกันอัตราแลกเปลี่ยน และโอนเงินไปต่างประเทศ",
    dest_insurer: "การยื่นประกันภัย",
    dest_insurer_desc: "ประกันการเดินทางกลับและประกันอุบัติเหตุ",
    btn_generate_qr: "สร้าง QR ใช้ครั้งเดียว 60 วินาที",
    submit_page_title: "iM Worker Pass - ยื่นเอกสาร",
    submit_h1: "ยื่น QR ยืนยันตัวตน",
    submit_who_desc: "ส่งเฉพาะข้อมูลที่จำเป็นให้แต่ละหน่วยงานอย่างปลอดภัย",
    submit_lead_desc: "ยื่นใหม่ทุกครั้งที่ส่ง ไม่มีการบันทึกใด ๆ ลงบล็อกเชน ระบบจะสอบถามหน่วยงานอีกครั้งเพื่อดึงค่าล่าสุด",
    no_wallet_title: "ยังไม่มีกระเป๋าเงิน",
    no_wallet_desc: "คุณต้องออกกระเป๋าเงินก่อน ขั้นตอนนี้ทำเพียงครั้งเดียว",
    btn_goto_wallet: "ไปออกกระเป๋าเงิน →",
    submit_step1_title: "1) เลือกสถานที่ยื่นเอกสาร",
    label_submit_target: "ส่งถึง",
    label_symptom: "อาการที่จะแจ้งโรงพยาบาล",
    symptom_note: "นี่คือคำบอกเล่าของผู้ป่วยเอง ไม่ใช่การวินิจฉัย",
    symptom_cough: "ฉันมีอาการไอ",
    symptom_back_pain: "ฉันปวดหลัง",
    symptom_fever: "ฉันน่าจะมีไข้",
    symptom_stomach: "ฉันรู้สึกไม่สบายท้อง",
    symptom_itchy: "ผิวหนังฉันคัน",
    attend_hint: "การสแกนเข้า-ออกงานไม่ต้องสอบถามหน่วยงานซ้ำ ไม่จำเป็นต้องถามวันละสองครั้ง สิ่งที่ต้องรู้คือสถานะการพำนักยังใช้ได้หรือไม่ ซึ่งตรวจสอบผ่านบล็อกเชนตอนสแกน <b>เวลาจะถูกบันทึกโดยระบบลงเวลาของบริษัทเองทันทีที่เครื่องสแกนอ่าน QR</b>",
    insurance_redirect_note: "สำหรับประกัน การเลือกผลิตภัณฑ์ก็คือการเลือกผู้รับ จึงไม่ต้องใช้ QR — ดำเนินการที่หน้าจอ <a href=\"insurance.html\">④ ประกัน</a>",
    btn_sign_and_generate_qr: "ลงลายเซ็นบนเครื่องและสร้าง QR",
    submit_step2_title: "2) QR สำหรับยื่น",
    btn_renew_qr: "สร้าง QR ใหม่",
    payload_copy_note: "คัดลอก payload ด้านล่างไปวางที่หน้าจอ <b>③ เครื่องสแกน</b> เพื่อทดสอบการตรวจสอบโดยไม่ต้องใช้กล้อง การเปลี่ยนเลขบัญชีหนึ่งหลักจะสาธิตการปลอมแปลงข้อมูล",
    copy_payload_title: "คัดลอก payload",
    copy_done_title: "คัดลอกแล้ว",
    copy_fail_title: "คัดลอกไม่สำเร็จ — กรุณาเลือกด้วยตนเอง",
    submit_rejected: "การยื่นเอกสารถูกปฏิเสธ",
    sig_verified_msg: "✓ ตรวจสอบลายเซ็นอุปกรณ์ผ่าน — คำขอนี้มาจากเจ้าของกระเป๋าเงินนี้จริง",
    sig_not_registered_msg: "กระเป๋าเงินนี้ยังไม่ได้ลงทะเบียนคีย์อุปกรณ์ ข้ามการตรวจสอบลายเซ็น",
    attend_wait_msg: "ผลลัพธ์จะแสดงที่นี่เมื่อเครื่องสแกนของสถานประกอบการอ่าน QR นี้",
    checkin_label: "เข้างาน",
    checkout_label: "เลิกงาน",
    worked_time_label: "ทำงาน",
    site_scanner_time_note: "บันทึกตามเวลาของเครื่องสแกนบริษัท",
    lookup_count_label: "ตรวจสอบซ้ำตอนยื่นเอกสาร",
    lookup_real_badge: "หน่วยงานผู้ออกจริง",
    lookup_mock_badge: "API จำลอง",
    lookup_footer_note: "ไม่มีการดึงข้อมูลมาเก็บไว้ล่วงหน้า ทุกการยื่นจะสอบถามใหม่เสมอ จึงไม่มีข้อมูลที่ล้าสมัย หน่วยงานที่ไม่จำเป็นต่อวัตถุประสงค์จะไม่ถูกสอบถาม",
    qr_time_left_label: "QR ใช้ได้อีก: ",
    qr_expired_label: "QR หมดอายุแล้ว",
    current_wallet_label: "กระเป๋าเงินปัจจุบัน: ",
    switch_person_link: "เปลี่ยนบุคคล",
    qr_expired_payload_msg: "QR นี้หมดอายุแล้วและไม่สามารถใช้งานได้",
  },
};

const I18N = {
  LANG_KEY: "imwp_lang",

  getLang() {
    try {
      const stored = localStorage.getItem(this.LANG_KEY);
      if (stored && I18N_DICT[stored]) return stored;
    } catch (e) {}
    return "ko";
  },

  setLang(lang) {
    if (!I18N_DICT[lang]) return;
    try {
      localStorage.setItem(this.LANG_KEY, lang);
    } catch (e) {}
    // LLM 번역 시도 (비동기). 실패 시 내부에서 apply()로 폴백됨.
    this.translatePage(lang);
    // 언어 변경 이벤트 디스패치 (동적 카드 리렌더링 등 페이지별 후처리용)
    window.dispatchEvent(new CustomEvent("imwp-lang-change", { detail: { lang } }));
  },

  t(key, fallback = "") {
    const lang = this.getLang();
    const dict = I18N_DICT[lang] || I18N_DICT.ko;
    if (dict && dict[key] != null) return dict[key];
    if (I18N_DICT.ko && I18N_DICT.ko[key] != null) return I18N_DICT.ko[key];
    return fallback || key;
  },

  apply(lang) {
    if (!lang) lang = this.getLang();
    const dict = I18N_DICT[lang] || I18N_DICT.ko;

    // data-i18n 속성을 가진 모든 엘리먼트 텍스트 치환
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (dict[key] != null) {
        if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
          el.placeholder = dict[key];
        } else {
          el.innerHTML = dict[key];
        }
      }
    });

    // title / aria-label 속성 번역 (예: 아이콘 버튼의 툴팁)
    document.querySelectorAll("[data-i18n-title]").forEach((el) => {
      const key = el.getAttribute("data-i18n-title");
      if (dict[key] != null) el.setAttribute("title", dict[key]);
    });
    document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const key = el.getAttribute("data-i18n-aria");
      if (dict[key] != null) el.setAttribute("aria-label", dict[key]);
    });

    // 선택기 UI 값 동기화
    const sel = document.getElementById("imLangSelect");
    if (sel && sel.value !== lang) {
      sel.value = lang;
    }
  },

  // ─────────────────────────────────────────────────────────────
  // LLM 기반 동적 번역 (알리페이 방식)
  // 현재 페이지의 텍스트 노드를 수집해 /api/translate 에 배치 요청.
  // sessionStorage에 캐시 → 같은 페이지·언어 조합은 API 미호출.
  // 실패 시 기존 사전(data-i18n) 방식으로 폴백.
  // ─────────────────────────────────────────────────────────────
  _SKIP_TAGS: new Set(["SCRIPT", "STYLE", "NOSCRIPT", "IFRAME", "TEMPLATE", "CODE", "PRE"]),
  _SKIP_CLASSES: ["lang-picker-box", "lang-select-dropdown", "lang-flag", "no-translate"],

  /**
   * 텍스트 노드 -> "이 노드에서 최초로 관찰된 한국어 원문" 매핑.
   *
   * 왜 필요한가: 언어를 A -> B -> C로 새로고침 없이 연속으로 바꾸면, C로
   * 바꾸는 시점의 DOM에는 이미 B의 번역 결과가 들어있다. 이때 "지금 DOM에
   * 보이는 값"을 원문으로 삼아버리면(예전 방식) 그 값은 한국어가 아니라
   * B 언어라서, 캐시 매칭도 새 LLM 요청도 전부 엉뚱한 값을 기준으로 돌게
   * 된다 — 결과적으로 아무것도 안 바뀌고 조용히 실패한다.
   *
   * 해결: 각 텍스트 노드를 "처음 만나는 순간"의 값을 WeakMap에 딱 한 번
   * 기록해둔다. 페이지가 막 로드된 시점이든, 스캔 결과처럼 나중에 새로
   * 생성된 노드든, 처음 보는 시점의 값은 항상 한국어(서버가 원래 내려주는
   * 언어)이므로 이 값이 진짜 원문이다. 이후 몇 번을 다른 언어로 바꿔도
   * 이 기록된 원문을 기준으로 삼는다.
   */
  _originalMap: new WeakMap(),

  /** 노드의 "진짜" 한국어 원문을 반환한다 (처음 보는 노드면 지금 값을 원문으로 기록). */
  _getOriginal(node) {
    if (!this._originalMap.has(node)) {
      this._originalMap.set(node, node.nodeValue.trim());
    }
    return this._originalMap.get(node);
  },

  /**
   * 개인정보·건강정보 격리:
   * 실명·계좌번호·외국인등록번호·체류자격·증상 진술 등 사용자별 동적 값은
   * 절대 LLM(Gemini) 번역 API로 보내지 않는다. 해당 값을 렌더링하는 요소에
   * data-no-translate 속성(또는 no-translate 클래스)을 붙이면 이 값들은
   * _collectTextNodes()가 아예 수집하지 않으므로 서버로 전송되지 않는다.
   * (번역이 필요 없는 고유명사·숫자·코드값이기도 하다.)
   */
  /** 번역 대상 텍스트 노드를 DOM에서 수집한다. */
  _collectTextNodes() {
    const nodes = [];
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: (node) => {
          const text = node.nodeValue.trim();
          if (!text || text.length < 2) return NodeFilter.FILTER_REJECT;

          // 부모 태그 확인
          let parent = node.parentElement;
          while (parent && parent !== document.body) {
            if (this._SKIP_TAGS.has(parent.tagName)) return NodeFilter.FILTER_REJECT;
            if (this._SKIP_CLASSES.some(c => parent.classList.contains(c))) return NodeFilter.FILTER_REJECT;
            // 개인정보/건강정보 격리 — data-no-translate가 붙은 요소(및 그 하위)는 전송 대상에서 제외
            if (parent.hasAttribute && parent.hasAttribute("data-no-translate")) return NodeFilter.FILTER_REJECT;
            // 언어 선택기 자체는 번역 제외
            if (parent.id === "langSelectorArea" || parent.id === "imLangSelect") return NodeFilter.FILTER_REJECT;
            parent = parent.parentElement;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    let node;
    while ((node = walker.nextNode())) {
      nodes.push(node);
    }
    return nodes;
  },

  /**
   * sessionStorage 캐시 키 생성.
   * "v2"는 버전 태그다 — 이전 버전은 "지금 화면에 보이는 값"을 원문으로
   * 잘못 캐시하는 버그가 있었다. 버전을 올려서 그 시절 오염된 캐시(예: uz
   * 키인데 원문이 인도네시아어로 박혀있는 것)를 자동으로 무시하게 만든다.
   * 이 태그가 없으면 이미 버그 있는 캐시가 저장된 브라우저 탭은 이 수정을
   * 배포해도 세션이 끝날 때까지 계속 그 오염된 캐시를 읽게 된다.
   */
  _cacheKey(lang) {
    const path = location.pathname.replace(/\//g, "_").replace(/\.html$/, "") || "root";
    return `imwp_tr_v2_${path}_${lang}`;
  },

  /** 스피너를 언어 선택기 옆에 표시/숨김 */
  _setLoading(on) {
    const box = document.querySelector(".lang-picker-box");
    if (!box) return;
    let spinner = box.querySelector(".lang-spinner");
    if (on) {
      if (!spinner) {
        spinner = document.createElement("span");
        spinner.className = "lang-spinner";
        spinner.textContent = "⏳";
        spinner.style.cssText = "font-size:12px;animation:spin 1s linear infinite;display:inline-block;";
        box.appendChild(spinner);
      }
      const sel = box.querySelector("select");
      if (sel) sel.disabled = true;
    } else {
      if (spinner) spinner.remove();
      const sel = box.querySelector("select");
      if (sel) sel.disabled = false;
    }
  },

  async translatePage(lang, force = false) {
    if (!lang) lang = this.getLang();

    // setLang()이 직접 호출하는 것과, 대부분 화면이 imwp-lang-change 이벤트를 받아
    // 다시 호출하는 것이 거의 동시에 겹친다. 같은 언어로 이미 진행 중인 번역이 있으면
    // 새로 fetch를 또 쏘지 않고 그 결과를 같이 기다린다 (번역 시간이 매번 2배로
    // 걸리던 원인).
    if (this._inFlight && this._inFlight.lang === lang) {
      return this._inFlight.promise;
    }

    // 세대(generation) 번호 발급.
    //
    // 문제: 언어를 빠르게 연달아 바꾸면(예: id → uz), 두 개의 서로 다른
    // _doTranslatePage 호출이 동시에 진행 중일 수 있다. 네트워크 응답은
    // "요청을 보낸 순서"가 아니라 "먼저 도착한 순서"로 처리되므로, 나중에
    // 선택한 언어(uz)의 응답이 먼저 와서 화면에 반영된 뒤, 뒤늦게 도착한
    // 이전 언어(id)의 응답이 아무 확인 없이 화면을 덮어써버릴 수 있다.
    // 사용자 입장에서는 "우즈베크어를 골랐는데 다시 인니어로 보이네? 안
    // 바뀌네?"로 보이고, 새로고침하면 캐시에서 최신 언어만 곧장 불러오니
    // 그제서야 맞는 것처럼 보인다.
    //
    // 해결: 매 요청마다 증가하는 번호를 매기고, 응답이 왔을 때 그 사이에 더
    // 최신 요청이 시작되지는 않았는지 확인해서, 아니라면(내가 최신이 아니면)
    // 화면에 반영하지 않고 조용히 버린다.
    this._gen = (this._gen || 0) + 1;
    const myGen = this._gen;

    const promise = this._doTranslatePage(lang, force, myGen);
    this._inFlight = { lang, promise };
    try {
      return await promise;
    } finally {
      if (this._inFlight && this._inFlight.promise === promise) this._inFlight = null;
    }
  },

  /**
   * LLM으로 현재 페이지 전체를 번역한다.
   * @param {string} lang - 목적 언어 코드 (en, vi, th, id, uz, zh)
   * @param {boolean} force - true면 캐시 무시하고 재번역
   * @param {number} myGen - 이 호출의 세대 번호. 응답 도착 시 this._gen과 달라져
   *   있으면(그 사이 더 최신 언어 전환이 시작됐으면) 화면 반영을 건너뛴다.
   */
  async _doTranslatePage(lang, force = false, myGen) {
    if (!lang) lang = this.getLang();

    // 한국어는 원문 = 번역이므로 기존 사전 방식만 적용
    if (lang === "ko") {
      this.apply("ko");
      return;
    }

    // 캐시 확인
    const cacheKey = this._cacheKey(lang);
    if (!force) {
      try {
        const cached = sessionStorage.getItem(cacheKey);
        if (cached) {
          // 이 사이 더 최신 언어 전환이 시작됐다면(캐시 조회는 동기라 실제로는
          // 거의 안 일어나지만 방어적으로) 화면 반영을 건너뛴다.
          if (myGen !== undefined && myGen !== this._gen) return;
          const { originals, translations } = JSON.parse(cached);
          const nodes = this._collectTextNodes();
          // 원문 매칭으로 캐시 적용 — 반드시 "기록된 한국어 원문" 기준으로 찾는다.
          // (여기서 n.nodeValue.trim()을 그대로 쓰면, 화면이 이미 다른 언어로
          // 바뀌어 있을 때 원문이 아닌 값으로 조회하게 되어 매칭이 실패한다.)
          const origMap = new Map(originals.map((o, i) => [o, translations[i]]));
          nodes.forEach(n => {
            const orig = this._getOriginal(n);
            const t = origMap.get(orig);
            if (t) n.nodeValue = t;
          });
          this.apply(lang); // data-i18n 사전도 함께 적용
          return;
        }
      } catch (e) {}
    }

    // 기존 사전 우선 적용 (즉각 반응)
    this.apply(lang);

    // 텍스트 노드 수집 — 반드시 "기록된 한국어 원문" 기준으로 모은다 (위 설명 참고)
    const nodes = this._collectTextNodes();
    const originals = nodes.map(n => this._getOriginal(n));
    const unique = [...new Set(originals.filter(Boolean))];

    if (unique.length === 0) return;

    this._setLoading(true);

    try {
      // 200개 초과 시 청크로 분할
      const CHUNK = 150;
      const allTranslated = [];
      for (let i = 0; i < unique.length; i += CHUNK) {
        const chunk = unique.slice(i, i + CHUNK);
        // config.js는 `const API_BASE_URL = ...`로 선언한다 — 일반 <script>의 최상위
        // const/let은 window의 프로퍼티가 되지 않으므로 window.API_BASE_URL은 항상
        // undefined다. 다른 화면의 모든 fetch가 쓰는 것과 동일하게 식별자를 직접
        // 참조해야 실제 백엔드(Render) 주소로 나간다.
        const base = (typeof API_BASE_URL !== "undefined") ? API_BASE_URL : (window.API_BASE_URL || "");
        const res = await fetch(`${base}/api/translate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ lang, texts: chunk }),
        });
        if (!res.ok) {
          // 서버는 실패 이유를 { detail: "..." } 로 내려준다. 지금까지는 이 값을
          // 버리고 "HTTP 502"만 남겨서 콘솔로는 진짜 원인(할당량 초과/타임아웃/키 오류 등)을
          // 알 수 없었다. 읽을 수 있으면 읽어서 함께 로그로 남긴다.
          let detail = "";
          try {
            const body = await res.json();
            detail = body && body.detail ? body.detail : "";
          } catch (e) {}
          throw new Error(`HTTP ${res.status}${detail ? " — " + detail : ""}`);
        }
        const data = await res.json();
        allTranslated.push(...data.translations);

        // 이 청크가 도착한 사이에 더 최신 언어 전환이 시작됐다면, 나머지 청크
        // 요청도 마저 보낼 필요 없이 여기서 그냥 중단한다 (낭비되는 API 호출도
        // 줄이고, 뒤에서 화면을 잘못 덮어쓸 일도 원천적으로 막는다).
        if (myGen !== undefined && myGen !== this._gen) return;
      }

      // 번역 맵 구성 (원문 → 번역)
      const trMap = new Map(unique.map((orig, i) => [orig, allTranslated[i]]));

      // DOM 텍스트 노드 교체
      //
      // 주의: 위에서 만든 `nodes`는 API를 부르기 *전*(Gemini 응답을 몇 초씩 기다리기
      // 전) 시점의 스냅샷이다. 그 사이에 이 페이지 자신이 "imwp-lang-change" 이벤트를
      // 받아 동적 영역(지갑 카드, 스캔 결과 등)을 다시 그려버리면, 그 순간 `nodes`가
      // 가리키던 텍스트 노드는 이미 화면에서 떨어져나간(교체된) 옛 노드가 된다.
      // 그 옛 노드에 번역을 넣어봐야 화면엔 아무 변화가 없다 — 에러 없이 조용히
      // 실패하는 것처럼 보이고, 새로고침(F5)하면 sessionStorage 캐시가 경쟁할 시간 없이
      // 바로 적용되니 그제서야 되는 것처럼 보이는 원인이 바로 이거였다.
      //
      // 해결: 적용 직전에 DOM을 다시 한번 훑어서(최신 노드 기준으로) 매칭한다.
      const freshNodes = this._collectTextNodes();
      freshNodes.forEach(n => {
        // 조회는 "기록된 한국어 원문" 기준, 치환은 "지금 화면에 있는 값" 기준.
        // (조회 키를 현재 값으로 하면 이미 다른 언어로 바뀐 노드는 매칭이 안 된다.)
        const orig = this._getOriginal(n);
        const translated = trMap.get(orig);
        const current = n.nodeValue.trim();
        if (translated && translated !== current) {
          n.nodeValue = n.nodeValue.replace(current, translated);
        }
      });

      // 캐시 저장 (페이지 재방문 시 재사용)
      try {
        sessionStorage.setItem(cacheKey, JSON.stringify({ originals: unique, translations: allTranslated }));
      } catch (e) {}

    } catch (err) {
      // 실패 시 기존 사전 폴백 (이미 apply() 호출됨)
      console.warn("[i18n] LLM translation failed, using dictionary fallback:", err.message);
    } finally {
      this._setLoading(false);
    }
  },

  renderSelector(containerId = "langSelectorArea") {
    const el = document.getElementById(containerId);
    if (!el) return;

    const current = this.getLang();
    const flags = {
      ko: "🇰🇷",
      en: "🇺🇸",
      vi: "🇻🇳",
      id: "🇮🇩",
      uz: "🇺🇿",
      zh: "🇨🇳",
      th: "🇹🇭",
    };

    el.innerHTML = `
      <div class="lang-picker-box">
        <span class="lang-flag" id="imLangFlag">${flags[current] || "🌐"}</span>
        <select id="imLangSelect" class="lang-select-dropdown" onchange="I18N.setLang(this.value)" aria-label="Language">
          <option value="ko"${current === "ko" ? " selected" : ""}>한국어</option>
          <option value="en"${current === "en" ? " selected" : ""}>English</option>
          <option value="vi"${current === "vi" ? " selected" : ""}>Tiếng Việt</option>
          <option value="th"${current === "th" ? " selected" : ""}>ไทย</option>
          <option value="id"${current === "id" ? " selected" : ""}>Indonesia</option>
          <option value="uz"${current === "uz" ? " selected" : ""}>Oʻzbekcha</option>
          <option value="zh"${current === "zh" ? " selected" : ""}>中文</option>
        </select>
      </div>
    `;

    document.getElementById("imLangSelect")?.addEventListener("change", (e) => {
      const flagEl = document.getElementById("imLangFlag");
      if (flagEl) flagEl.textContent = flags[e.target.value] || "🌐";
    });
  },
};

// DOM 로드 완료 시 자동 적용
// 저장된 언어가 한국어이면 사전 방식, 외국어이면 LLM 번역 시작
if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", () => {
    const lang = I18N.getLang();
    if (lang === "ko") {
      I18N.apply("ko");
    } else {
      // 사전 즉시 적용 (즉각 반응) + LLM 번역 비동기 시작
      I18N.apply(lang);
      I18N.translatePage(lang);
    }
  });
}
