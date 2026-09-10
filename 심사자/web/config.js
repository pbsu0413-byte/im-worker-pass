// 배포된 Render 백엔드 URL이 기본값으로 설정되어 있어,
// 링크를 받은 어떤 사람(교수님, 심사위원, 스마트폰 등)이 접속해도 F12 설정 없이 영구적으로 동작합니다.
const API_BASE_URL = window.localStorage.getItem("API_BASE_URL") || "http://127.0.0.1:8000";
