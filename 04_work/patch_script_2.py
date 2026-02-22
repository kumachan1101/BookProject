import re

with open('05_生成/md_to_epub_with_pdf.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix COVER_IMAGE path
content = content.replace('COVER_IMAGE = Path("cover.png")', 'COVER_IMAGE = Path("05_生成/cover.png")')

# Fix PAGE_TO_MD_INDEX correctly
correct_mapping = """        PAGE_TO_MD_INDEX = {
            0: 0,   # 第1部 第1章
            1: 1,   # 第1部 第2章
            2: 2,   # 第1部 第3章
            3: 4,   # 第1部 第4章
            4: 5,   # 第1部 第5章
            5: 6,   # 第1部 第6章
            6: 8,   # 第1部 第7章
            7: 11,  # 第2部 第8章
            8: 13,  # 第2部 第9章
            9: 15,  # 第2部 第10章
            10: 17, # 第2部 第11章
            11: 19, # 第2部 第12章
            12: 22, # 第2部 第13章
            13: 24, # 第2部 第14章
            14: 26  # 第2部 第15章
        }"""
content = re.sub(r'PAGE_TO_MD_INDEX = \{[^}]+\}', correct_mapping, content)

with open('05_生成/md_to_epub_with_pdf.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("md_to_epub_with_pdf.py patched successfully.")
