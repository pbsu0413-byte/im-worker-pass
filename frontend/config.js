// 백엔드(FastAPI)를 Render 등에 배포한 뒤, 여기 URL만 바꾸면 됩니다.
// 로컬 테스트 시에는 기본값(uvicorn 기본 포트)을 그대로 쓰면 됩니다.
const API_BASE_URL = window.localStorage.getItem("API_BASE_URL") || "https://im-worker-pass.onrender.com";
