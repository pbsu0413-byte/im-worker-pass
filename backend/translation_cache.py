"""
번역 결과 캐시 (Phase 1: 파일 기반)

문제: 지금까지 /api/translate는 요청이 들어올 때마다 무조건 Gemini를 불렀다.
같은 "안녕하세요"를 100명이 영어로 봐도 100번 다 LLM을 호출한 것이다.
화면 문구는 거의 바뀌지 않으므로, 한 번 번역된 (원문, 언어) 조합은
두 번 다시 LLM에 물어볼 필요가 없다.

해결: (원문, 언어) 쌍을 키로 삼아 번역 결과를 저장해두고, 같은 키가 다시
들어오면 LLM 호출 없이 즉시 반환한다.

- 메모리 캐시: 프로세스가 떠 있는 동안은 디스크도 안 거치고 바로 반환 (가장 빠름)
- 파일 캐시: 서버가 재시작돼도(예: 야간 슬립 후 깨어남) 그대로 남아있게 디스크에 저장
- 주의: Render 같은 플랫폼은 재배포(deploy) 시 디스크를 새로 만들기 때문에,
  재배포 직후 각 언어의 "첫 번째 방문자"는 다시 한번 LLM 비용을 치른다.
  배포를 넘어서도 영구히 남기고 싶으면 이 파일 캐시를 Supabase 테이블로
  옮기면 된다(이 모듈의 get/set 두 함수만 바꾸면 나머지 코드는 그대로 쓸 수 있다).
"""

import json
import os
import threading

_CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translation_cache.json")
_lock = threading.Lock()
_cache = {}          # {"en|안녕하세요": "Hello", ...}
_loaded = False


def _key(lang: str, text: str) -> str:
    return f"{lang}|{text}"


def _load():
    global _loaded
    if _loaded:
        return
    with _lock:
        if _loaded:
            return
        if os.path.exists(_CACHE_PATH):
            try:
                with open(_CACHE_PATH, encoding="utf-8") as f:
                    _cache.update(json.load(f))
            except Exception:
                pass  # 캐시 파일이 깨져 있어도 서비스는 계속되어야 한다 — 그냥 빈 캐시로 시작
        _loaded = True


def _persist():
    """디스크에 저장한다. 실패해도(예: 읽기 전용 파일시스템) 서비스는 계속된다."""
    try:
        tmp_path = _CACHE_PATH + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(_cache, f, ensure_ascii=False)
        os.replace(tmp_path, _CACHE_PATH)
    except Exception:
        pass


def get_many(lang: str, texts: list[str]) -> dict[str, str]:
    """이미 캐시에 있는 것만 {원문: 번역} 형태로 돌려준다. 없는 건 결과에 아예 안 들어있다."""
    _load()
    found = {}
    for t in texts:
        v = _cache.get(_key(lang, t))
        if v is not None:
            found[t] = v
    return found


def set_many(lang: str, mapping: dict[str, str]) -> None:
    """새로 번역된 것들을 캐시에 넣고 디스크에 반영한다."""
    if not mapping:
        return
    _load()
    with _lock:
        for original, translated in mapping.items():
            _cache[_key(lang, original)] = translated
        _persist()


def stats() -> dict:
    """디버그/모니터링용. 언어별로 캐시에 몇 개가 쌓여 있는지."""
    _load()
    by_lang = {}
    for k in _cache:
        lang = k.split("|", 1)[0]
        by_lang[lang] = by_lang.get(lang, 0) + 1
    return {"total_entries": len(_cache), "by_lang": by_lang}
