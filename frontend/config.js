// 배포된 Render 백엔드 URL이 기본값으로 설정되어 있어,
// 링크를 받은 어떤 사람(교수님, 심사위원, 스마트폰 등)이 접속해도 F12 설정 없이 영구적으로 동작합니다.
const API_BASE_URL = (location.hostname === "127.0.0.1" || location.hostname === "localhost")
  ? "http://127.0.0.1:8000"
  : "https://im-worker-pass.onrender.com";

// 레거시 HTML의 닫는 태그를 브라우저가 보정하면서 하단 탭이 .phone 밖으로
// 이동하는 페이지가 있다. 모든 근로자 화면에서 탭을 목업의 마지막 자식으로
// 되돌려 헤더 / 스크롤 본문 / 고정 하단 탭 구조를 보장한다.
document.addEventListener("DOMContentLoaded", function () {
  const phone = document.querySelector(".phone");
  const tabs = document.querySelector(".ph-tabs");
  if (phone && tabs && tabs.parentElement !== phone) phone.appendChild(tabs);
});

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
})();
