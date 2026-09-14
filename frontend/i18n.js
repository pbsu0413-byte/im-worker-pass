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
  },

  en: {
    lang_name: "English",
    app_title: "iM PASS",
    worker_role: "Worker",
    switch_service: "Switch Service",
    wallet_heading: "My Digital Wallet",
    wallet_subheading: "Visa & Employment & Financial Passport",
    first_time_notice: "Wallet issuance is required <b>only once</b>. Submit documents anytime from the <b>Submit</b> tab below.",

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
  },

  vi: {
    lang_name: "Tiếng Việt",
    app_title: "iM PASS",
    worker_role: "Người lao động",
    switch_service: "Đổi dịch vụ",
    wallet_heading: "Ví số của tôi",
    wallet_subheading: "Tư cách lưu trú, việc làm & Hộ chiếu tài chính",
    first_time_notice: "Đăng ký ví chỉ cần thực hiện <b>lần đầu tiên</b>. Khi cần nộp giấy tờ, hãy dùng tab <b>Gửi QR</b> bên dưới.",

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
  },

  id: {
    lang_name: "Bahasa Indonesia",
    app_title: "iM PASS",
    worker_role: "Pekerja",
    switch_service: "Ganti Layanan",
    wallet_heading: "Dompet Digital Saya",
    wallet_subheading: "Status Izin Tinggal & Paspor Keuangan",
    first_time_notice: "Penerbitan dompet hanya dilakukan <b>satu kali di awal</b>. Gunakan tab <b>Kirim</b> di bawah untuk menyerahkan dokumen.",

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
  },

  uz: {
    lang_name: "Oʻzbekcha",
    app_title: "iM PASS",
    worker_role: "Ishchi",
    switch_service: "Xizmatni almashtirish",
    wallet_heading: "Raqamli hamyonim",
    wallet_subheading: "Yashash va mehnat maqomi hamda moliyaviy pasport",
    first_time_notice: "Hamyon berish <b>faqat bir marta</b> amalga oshiriladi. Hujjatlarni topshirish uchun quyidagi <b>Yuborish</b> boʻlimidan foydalaning.",

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
  },

  zh: {
    lang_name: "中文",
    app_title: "iM PASS",
    worker_role: "劳动者",
    switch_service: "切换服务",
    wallet_heading: "我的数字钱包",
    wallet_subheading: "居留与就业资格及金融通行证",
    first_time_notice: "钱包仅需在<b>首次注册</b>一次。后续提交请使用下方的<b>提交</b>标签页。",

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
    this.apply(lang);
    // 언어 변경 이벤트 디스패치
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

    // 선택기 UI 값 동기화
    const sel = document.getElementById("imLangSelect");
    if (sel && sel.value !== lang) {
      sel.value = lang;
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
    };

    el.innerHTML = `
      <div class="lang-picker-box">
        <span class="lang-flag" id="imLangFlag">${flags[current] || "🌐"}</span>
        <select id="imLangSelect" class="lang-select-dropdown" onchange="I18N.setLang(this.value)" aria-label="Language">
          <option value="ko"${current === "ko" ? " selected" : ""}>한국어</option>
          <option value="en"${current === "en" ? " selected" : ""}>English</option>
          <option value="vi"${current === "vi" ? " selected" : ""}>Tiếng Việt</option>
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
if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", () => {
    I18N.apply();
  });
}
