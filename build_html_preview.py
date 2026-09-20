# -*- coding: utf-8 -*-
"""
build_html_preview.py
Converts README2.md to a standalone, beautifully styled HTML document (README2.html)
that can be opened directly in any browser (Chrome, Edge, Whale) with a double-click.
Includes GitHub Markdown styling + iM Bank brand design tokens + Print to PDF support.
"""

import os
import markdown

def generate_html_preview():
    md_path = 'README2.md'
    html_path = 'README2.html'
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    body_html = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists']
    )

    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>iM PASS — 리드미 미리보기 (README2)</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<style>
  :root {{
    --im-mint: #00C7A9;
    --im-mint-dark: #00A98F;
    --im-mint-light: #E8FAF6;
    --im-blue: #2878FF;
    --im-blue-dark: #155ED4;
    --im-blue-light: #EDF4FF;
    --im-navy: #1F4E78;
    --im-navy-dark: #143554;
    --im-navy-light: #EEF2F7;
    --im-bg: #F4F6F9;
    --im-card-bg: #FFFFFF;
    --im-text: #24292F;
    --im-subtext: #57606A;
    --im-border: #D0D7DE;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    margin: 0;
    padding: 0;
    background-color: var(--im-bg);
    color: var(--im-text);
    font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }}

  /* Top sticky control bar */
  .top-bar {{
    position: sticky;
    top: 0;
    z-index: 999;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--im-border);
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  }}

  .top-bar-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    font-size: 16px;
    color: var(--im-navy);
  }}

  .top-bar-brand svg {{
    width: 24px;
    height: 24px;
  }}

  .top-actions {{
    display: flex;
    gap: 10px;
  }}

  .btn {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
    border: 1px solid transparent;
  }}

  .btn-primary {{
    background: var(--im-mint);
    color: #FFFFFF;
  }}
  .btn-primary:hover {{
    background: var(--im-mint-dark);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 199, 169, 0.3);
  }}

  .btn-outline {{
    background: #FFFFFF;
    border-color: var(--im-border);
    color: var(--im-text);
  }}
  .btn-outline:hover {{
    background: #F6F8FA;
    border-color: #8C959F;
  }}

  /* Main Container */
  .container {{
    max-width: 1012px;
    margin: 36px auto 60px;
    padding: 0 20px;
  }}

  .markdown-body {{
    background: var(--im-card-bg);
    border: 1px solid var(--im-border);
    border-radius: 16px;
    padding: 56px 64px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  }}

  /* Typography */
  h1, h2, h3, h4, h5, h6 {{
    margin-top: 32px;
    margin-bottom: 16px;
    font-weight: 700;
    line-height: 1.35;
    color: var(--im-navy);
  }}

  h1 {{
    font-size: 28px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--im-mint);
    text-align: center;
    margin-top: 10px;
  }}

  h2 {{
    font-size: 22px;
    padding-bottom: 8px;
    border-bottom: 1px solid #E1E4E8;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  h3 {{
    font-size: 17px;
    color: var(--im-blue-dark);
  }}

  p {{
    margin-top: 0;
    margin-bottom: 16px;
    color: #333333;
  }}

  /* Callout Blockquote */
  blockquote {{
    margin: 20px 0;
    padding: 18px 24px;
    background: #F0FBF9;
    border-left: 5px solid var(--im-mint);
    border-radius: 8px;
    color: #1A3E39;
    font-size: 15px;
    line-height: 1.65;
  }}

  blockquote p {{
    margin: 0;
  }}

  blockquote strong {{
    color: var(--im-navy);
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 14px;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--im-border);
  }}

  th, td {{
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid #EAECEF;
  }}

  th {{
    background: #F6F8FA;
    font-weight: 600;
    color: var(--im-navy);
    border-bottom: 2px solid var(--im-border);
  }}

  tr:nth-child(even) {{
    background-color: #FAFCFE;
  }}

  tr:hover {{
    background-color: #F0F6FD;
  }}

  /* Code Blocks */
  pre {{
    background: #1E293B;
    color: #F8FAFC;
    padding: 18px 20px;
    border-radius: 10px;
    overflow-x: auto;
    font-size: 13.5px;
    font-family: Consolas, Monaco, "Courier New", monospace;
    line-height: 1.6;
    margin: 20px 0;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.2);
  }}

  code {{
    background: #EDF2F7;
    color: #0F172A;
    padding: 3px 6px;
    border-radius: 5px;
    font-size: 13px;
    font-family: Consolas, Monaco, monospace;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* Images */
  img {{
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    transition: transform 0.2s ease;
  }}

  p img {{
    vertical-align: middle;
  }}

  /* Center alignment */
  p[align="center"] {{
    text-align: center;
  }}

  p[align="center"] img {{
    margin: 6px;
  }}

  /* Badges bar */
  p[align="center"] img[src*="shields.io"] {{
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }}

  /* Links */
  a {{
    color: var(--im-blue);
    text-decoration: none;
    font-weight: 500;
  }}
  a:hover {{
    text-decoration: underline;
    color: var(--im-blue-dark);
  }}

  hr {{
    height: 1px;
    border: none;
    background: #E1E4E8;
    margin: 36px 0;
  }}

  ul, ol {{
    padding-left: 24px;
    margin-bottom: 20px;
  }}

  li {{
    margin-bottom: 8px;
  }}

  /* Print Styles */
  @media print {{
    .top-bar {{ display: none; }}
    body {{ background: #FFFFFF; }}
    .container {{ margin: 0; padding: 0; max-width: 100%; }}
    .markdown-body {{ border: none; box-shadow: none; padding: 20px; }}
    pre {{ white-space: pre-wrap; word-break: break-all; }}
  }}

  @media (max-width: 768px) {{
    .markdown-body {{ padding: 28px 20px; }}
    .top-bar {{ padding: 10px 16px; }}
    h1 {{ font-size: 22px; }}
    h2 {{ font-size: 18px; }}
  }}
</style>
</head>
<body>

<header class="top-bar">
  <div class="top-bar-brand">
    <svg viewBox="0 0 26 23" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M3 19.5V8.2c0-1.9 2.4-2.8 3.6-1.3L13 14.8l6.4-7.9C20.6 5.4 23 6.3 23 8.2v11.3"
            stroke="#00C7A9" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span>iM PASS README 미리보기</span>
  </div>
  <div class="top-actions">
    <button class="btn btn-outline" onclick="window.print()">🖨️ PDF로 저장 / 인쇄</button>
    <a class="btn btn-primary" href="http://127.0.0.1:8000/home.html" target="_blank">🚀 웹앱 실행 화면 보기</a>
  </div>
</header>

<main class="container">
  <article class="markdown-body">
{body_html}
  </article>
</main>

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"Success! {html_path} generated ({len(full_html)} bytes).")

if __name__ == '__main__':
    generate_html_preview()
