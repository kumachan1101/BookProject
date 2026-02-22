import re

with open('05_生成/md_to_epub_with_pdf.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove DL replacement logic entirely
content = re.sub(
    r"# --- 定義リスト（Description List）の処理（Kindle互換性向上のため） ---.*?text = re\.sub\(r'\(\?:.*?, list_to_dl_repl, text, flags=re\.MULTILINE\)",
    "",
    content,
    flags=re.DOTALL
)

# 2. Fix CSS text-indent
content = re.sub(r'p\s*\{\s*margin:\s*0\.5em\s*0;\s*text-indent:\s*1em;\s*\}', r'p {margin: 0.5em 0;}', content)

# 3. Enhance PDF mapping logic inside split_pdf_by_pages
pdf_logic_replacement = """        # PDFの各ページは「各章」に対応しているが、MDファイルのインデックスとは異なる。
        # 以下は PDFのページ数(0-14) を MDファイルのインデックス にマッピングする辞書
        PAGE_TO_MD_INDEX = {
            0: 2,   # 第1部 第1章
            1: 3,   # 第1部 第2章
            2: 4,   # 第1部 第3章 (_01)
            3: 6,   # 第1部 第4章
            4: 7,   # 第1部 第5章
            5: 8,   # 第1部 第6章 (_01)
            6: 10,  # 第1部 第7章 (_01)
            7: 12,  # 第2部 第8章 (_01)
            8: 14,  # 第2部 第9章 (_01)
            9: 19,  # 第2部 第10章 (_01)
            10: 22, # 第2部 第11章 (_01)
            11: 24, # 第2部 第12章 (_01)
            12: 27, # 第2部 第13章 (_01)
            13: 29, # 第2部 第14章 (_01)
            14: 31  # 第2部 第15章
        }
        
        for page_num in range(total_pages):
            if page_num not in PAGE_TO_MD_INDEX:
                print(f"[WARN] ページ{page_num}に対応するMDファイルが設定されていません")
                continue
                
            chapter_index = PAGE_TO_MD_INDEX[page_num]"""

content = re.sub(
    r'for page_num in range\(total_pages\):\s+chapter_index = page_num\s*# ページ0→章0, ページ1→章1, \.\.\.',
    pdf_logic_replacement,
    content
)

with open('05_生成/md_to_epub_with_pdf.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("md_to_epub_with_pdf.py patched successfully.")
