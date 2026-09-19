// 배포된 Render 백엔드 URL이 기본값으로 설정되어 있어,
// 링크를 받은 어떤 사람(교수님, 심사위원, 스마트폰 등)이 접속해도 F12 설정 없이 영구적으로 동작합니다.
const API_BASE_URL = (location.hostname === "127.0.0.1" || location.hostname === "localhost")
  ? "http://127.0.0.1:8000"
  : "https://im-worker-pass.onrender.com";

// ─────────────────────────────────────────────────────────────
// 공통 안전망 — 어느 화면에서든 서버에 닿지 못하면 사용자에게 알린다.
// 이걸 두지 않으면 fetch 실패가 조용히 삼켜져 "눌러도 아무 반응이 없는" 화면이 된다.
// ─────────────────────────────────────────────────────────────
(function () {
  let el = null;
  function notify(msg) {
    if (!el) {
      el = document.createElement("div");
      el.setAttribute("role", "status");
      el.style.cssText =
        "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:9999;" +
        "max-width:min(92vw,420px);background:#25282D;color:#fff;border-radius:14px;" +
        "padding:13px 18px;font-size:13.5px;font-weight:600;line-height:1.5;text-align:center;" +
        "box-shadow:0 8px 24px rgba(23,43,77,.28);font-family:inherit;";
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.style.display = "block";
    clearTimeout(notify._t);
    notify._t = setTimeout(function () { el.style.display = "none"; }, 6000);
  }

  window.addEventListener("unhandledrejection", function (e) {
    const m = String((e.reason && e.reason.message) || e.reason || "");
    if (/Failed to fetch|NetworkError|Load failed|ERR_/i.test(m)) {
      notify("확인 서버에 연결하지 못했어요. 잠시 후 다시 시도해 주세요.");
    }
  });

  // 화면에서도 같은 토스트를 쓸 수 있게 내보낸다.
  // (알림창 대신 이걸 쓴다 — alert 는 목업 폰 밖에 뜨고 화면을 멈춘다.)
  window.imwpNotify = notify;
})();

// ─────────────────────────────────────────────────────────────
// 잠금화면 알림 — 근로자 폰 목업 전용
//
// 근로자가 이 알림을 실제로 보는 자리는 앱 안이 아니라 폰 잠금화면이다.
// 그래서 헤더의 종을 누르면 폰이 잠긴 화면으로 바뀌고 그 위에 푸시가 떠 있다.
//
// 뜨는 알림은 **체류 만료 임박 하나뿐**이다. 판단은 서버(_worker_alerts)가 하고
// 여기서는 그리기만 한다. 은행이 절차를 대행하지 않는다 — 지갑이 이미 아는 날짜를
// 본인에게 돌려주고 어디로 가야 하는지까지만 말한다.
//
// 종은 `data-lock-bell` 이 붙은 버튼이면 어느 화면에서든 자동으로 묶인다.
// 사업장(.role-kiosk)·은행 콘솔(.role-console)·런처에는 종을 두지 않는다.
// ─────────────────────────────────────────────────────────────
(function () {
  const CID_STORE = "imwp_credential_id";
  const MARK =
    "<svg viewBox='0 0 26 23' fill='none' xmlns='http://www.w3.org/2000/svg' aria-hidden='true'>" +
    "<path d='M3 19.5V8.2c0-1.9 2.4-2.8 3.6-1.3L13 14.8l6.4-7.9C20.6 5.4 23 6.3 23 8.2v11.3' " +
    "stroke='#00C7A9' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/></svg>";
  const DAYS = ["일", "월", "화", "수", "목", "금", "토"];

  let alerts = [];
  let box = null;
  let timer = null;

  const esc = (v) => String(v == null ? "" : v)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  function bells() { return document.querySelectorAll("[data-lock-bell]"); }

  function paintDot() {
    bells().forEach((b) => {
      const d = b.querySelector(".bell-dot");
      if (d) d.hidden = alerts.length === 0;
    });
  }

  function paintClock() {
    if (!box) return;
    const d = new Date();
    const c = box.querySelector(".lock-clock");
    const t = box.querySelector(".lock-date");
    if (c) c.textContent =
      String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
    if (t) t.textContent = `${d.getMonth() + 1}월 ${d.getDate()}일 (${DAYS[d.getDay()]})`;
  }

  function ensureBox() {
    if (box) return box;
    // .phone 안에 넣어야 목업 밖으로 새지 않는다. position:fixed 를 쓰지 않는 이유다.
    const phone = document.querySelector(".phone");
    if (!phone) return null;
    box = document.createElement("div");
    box.className = "lockscreen";
    box.hidden = true;
    box.addEventListener("click", close);
    phone.appendChild(box);
    return box;
  }

  function body() {
    if (!alerts.length) {
      return '<div class="lock-empty">새로 온 알림이 없어요.<br />' +
             '체류기간이 4개월 안으로 들어오면 알려 드릴게요.</div>';
    }
    return '<div class="lock-pushes">' + alerts.map((a) => `
      <div class="lock-push${a.level === "urgent" ? " urgent" : ""}">
        <span class="mk">${MARK}</span>
        <span class="txt">
          <span class="top"><span class="app">iM PASS</span><span class="when">지금</span></span>
          <span class="ttl">${esc(a.title)}</span>
          <span class="bd">${esc(a.body)}</span>
          ${a.where ? `<span class="mt">${esc(a.where)}</span>` : ""}
        </span>
      </div>`).join("") + "</div>";
  }

  function open() {
    if (!ensureBox()) return;
    const phone = document.querySelector(".phone");
    // absolute 로 덮으므로 스크롤이 내려가 있으면 위치가 어긋난다.
    if (phone) { phone.scrollTop = 0; phone.classList.add("locked"); }
    window.scrollTo({ top: 0 });

    box.innerHTML =
      '<div class="lock-date"></div><div class="lock-clock"></div>' +
      '<div class="lock-body">' + body() + "</div>" +
      '<div class="lock-hint"><span class="bar"></span>위로 밀어 잠금 해제</div>';
    box.classList.remove("closing");
    box.hidden = false;
    paintClock();
    clearInterval(timer);
    timer = setInterval(paintClock, 10000);
  }

  function close() {
    if (!box || box.hidden) return;
    box.classList.add("closing");     // 확대되며 사라지는 잠금 해제
    setTimeout(function () {
      box.hidden = true;
      box.classList.remove("closing");
      const phone = document.querySelector(".phone");
      if (phone) phone.classList.remove("locked");
      clearInterval(timer);
      timer = null;
    }, 320);
  }

  async function load() {
    let cid = null;
    try { cid = localStorage.getItem(CID_STORE); } catch (e) {}
    alerts = [];
    if (cid) {
      try {
        const r = await fetch(`${API_BASE_URL}/wallet/${cid}`);
        if (r.ok) alerts = (await r.json()).alerts || [];
      } catch (e) { alerts = []; }
    }
    paintDot();
  }

  function wire() {
    bells().forEach(function (b) {
      if (b.dataset.lockWired) return;
      b.dataset.lockWired = "1";
      b.addEventListener("click", open);
    });
    load();
  }

  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }

  // 지갑을 막 발급한 직후처럼, 화면이 알림을 직접 다시 읽게 하고 싶을 때 쓴다.
  window.imwpLock = { open: open, close: close, reload: load };
})();
