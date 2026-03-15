# -*- coding: utf-8 -*-
"""
章別MDファイルの整合性チェックスクリプト
チェック項目:
1. コードブロックの開閉対称性（```の対）
2. Calloutの形式チェック（> [!TYPE] タイトル）
3. ##### * の誤記法チェック（見出し+箇条書き混在）
4. 標準MarkdownリンクのURL残存
5. Mermaidブロックの開閉確認
6. 「読者の疑問」Calloutに「はい/いいえ」が入っているか
7. YAMLフロントマターの有無
"""

import re
from pathlib import Path

CHAPTER_DIR = Path("../02_章別")
issues = []

def check_file(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    fname = path.name
    file_issues = []

    # --- 1. コードブロック開閉チェック ---
    code_fence_count = sum(1 for l in lines if re.match(r'^```', l))
    if code_fence_count % 2 != 0:
        file_issues.append(f"  [コードブロック] ``` が奇数個 ({code_fence_count}個) → 未閉じの可能性")

    # --- 2. Callout形式チェック ---
    for i, line in enumerate(lines, 1):
        m = re.match(r'^> \[!(\w+)\]', line)
        if m:
            ctype = m.group(1).upper()
            valid_types = {'INFO', 'TIP', 'NOTE', 'WARNING', 'CAUTION', 'IMPORTANT', 'SUCCESS'}
            if ctype not in valid_types:
                file_issues.append(f"  [Callout] L{i}: 未知のタイプ [!{ctype}]")

    # --- 3. ##### * の誤記法チェック ---
    for i, line in enumerate(lines, 1):
        if re.match(r'^#{1,6}\s+\*+\s', line):
            file_issues.append(f"  [見出し誤記] L{i}: `{line.strip()[:60]}` → 見出し+箇条書き混在")

    # --- 4. 標準MarkdownリンクにURLが残っていないか ---
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.startswith('```'):
            in_code = not in_code
        if not in_code:
            urls = re.findall(r'\]\(https?://[^\)]+\)', line)
            if urls:
                file_issues.append(f"  [URLリンク] L{i}: {urls[0][:60]}")

    # --- 5. Mermaidブロックの開閉チェック ---
    mermaid_opens = sum(1 for l in lines if re.match(r'^```mermaid', l))
    # mermaid は ``` で閉じるのでコードブロック全体で奇数でないことを別途確認
    # ここでは mermaid の個数だけ確認
    if mermaid_opens > 0:
        # count closing ``` after mermaid
        pass  # コードブロックの全体チェックで対応済み

    # --- 6. 「読者の疑問」Calloutに回答（はい/いいえ）があるか ---
    in_reader_callout = False
    callout_start_line = 0
    callout_body_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^> \[!INFO\] 読者の疑問[:：]', line)
        if m:
            in_reader_callout = True
            callout_start_line = i + 1
            callout_body_lines = []
        elif in_reader_callout:
            if line.startswith('> '):
                callout_body_lines.append(line)
            else:
                # Callout終了 → はい/いいえチェック
                body = ' '.join(callout_body_lines)
                if not re.search(r'(はい|いいえ|その通り)', body):
                    file_issues.append(f"  [読者の疑問] L{callout_start_line}: 「はい/いいえ」の回答が見当たらない可能性")
                in_reader_callout = False
        i += 1

    # --- 7. YAMLフロントマターチェック ---
    if lines and lines[0].startswith('---'):
        pass  # フロントマターあり
    # フロントマターは任意なのでここでは警告なし

    # --- 8. 「補足：」「コラム：」がないINFO Calloutチェック ---
    for i, line in enumerate(lines, 1):
        m = re.match(r'^> \[!INFO\] (.+)$', line)
        if m:
            title = m.group(1).strip()
            # 読者の疑問/著書紹介/書籍タイトル（英語）などは除外
            if not re.search(r'(読者の疑問|補足：|コラム：|著書紹介|Clean Architecture|Refactoring|Design Patterns|C Interfaces|SOLID原則)', title):
                # 補足もコラムも読者の疑問でもない → 要確認
                file_issues.append(f"  [Calloutプレフィックス] L{i}: [!INFO] のタイトルにプレフィックスなし → 「{title[:40]}」")

    return file_issues

print("=" * 70)
print("章別MDファイル 整合性チェック")
print("=" * 70)

total_issues = 0
for md_path in sorted(CHAPTER_DIR.glob("*.md")):
    result = check_file(md_path)
    if result:
        print(f"\n📄 {md_path.name}")
        for r in result:
            print(r)
        total_issues += len(result)
    else:
        print(f"✅ {md_path.name}")

print("\n" + "=" * 70)
print(f"チェック完了: 合計 {total_issues} 件の要確認事項")
print("=" * 70)
