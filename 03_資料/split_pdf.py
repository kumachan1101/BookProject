import fitz  # PyMuPDF
from pathlib import Path
import shutil

# ========= 設定 =========
# スクリプトが存在するディレクトリ（03_資料）
CURRENT_DIR = Path(__file__).resolve().parent
SLIDES_DIR = CURRENT_DIR / "slides"

# 自動で CURRENT_DIR 内の対象PDFを検索 (split_pdf.py 自身以外の最初のPDF)
pdf_files = [f for f in CURRENT_DIR.glob("*.pdf")]
if not pdf_files:
    print("[エラー] 03_資料 フォルダ内にPDFファイルが見つかりません。")
    PDF_PATH = None
else:
    PDF_PATH = pdf_files[0]

# PDFページ → 保存するチャプター番号
# 元のbuild_epub.pyにあったPAGE_TO_MD_INDEXをベースに、出力ファイル名用の番号を定義します。
PAGE_TO_CHAPTER_NUM = {
    0:  "01",   # PDF p1  → 01_section_1 (序論)
    1:  "02",   # PDF p2  → 02_第1部
    2:  "03",   # PDF p3  → 03_第1部 第1章
    3:  "04",   # PDF p4  → 04_第1部 第2章
    4:  "05",   # PDF p5  → 05_第1部 第3章
    5:  "06",   # PDF p6  → 06_第1部 第4章
    6:  "07",   # PDF p7  → 07_第1部 第5章
    7:  "08",   # PDF p8  → 08_第1部 第6章
    8:  "09",   # PDF p9  → 09_第1部 第7章
    9:  "10",   # PDF p10 → 10_第1部 まとめ
    10: "11",   # PDF p11 → 11_第2部
    11: "12",   # PDF p12 → 12_第2部 第8章
    12: "13",   # PDF p13 → 13_第2部 第9章
    13: "14",   # PDF p14 → 14_第2部 第10章
    14: "15",   # PDF p15 → 15_第2部 第11章
    15: "16",   # PDF p16 → 16_第2部 第12章
    16: "17",   # PDF p17 → 17_第2部 第13章
    17: "18",   # PDF p18 → 18_第2部 第14章
    18: "19",   # PDF p19 → 19_第2部 第15章
    19: "20",   # PDF p20 → 20_おわりに
}

def split_pdf():
    if PDF_PATH is None:
        return
        
    print(f"[PDF処理開始] 元ファイル: {PDF_PATH}")
    if not PDF_PATH.exists():
        print(f"[エラー] {PDF_PATH} が存在しません。")
        return

    # 古い画像ファイルなどを一度削除
    if SLIDES_DIR.exists():
        shutil.rmtree(SLIDES_DIR)
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    
    doc = fitz.open(str(PDF_PATH))
    total_pages = len(doc)
    print(f"総ページ数: {total_pages}")

    for page_num in range(total_pages):
        chapter_num_str = PAGE_TO_CHAPTER_NUM.get(page_num)
        
        if not chapter_num_str:
            print(f"  -> [スキップ] ページ {page_num+1} はマッピング情報なし")
            continue
            
        page = doc[page_num]
        
        # Kindle等のために高画質(150dpi想定)で画像化
        zoom = 150 / 72  
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        img_out_path = SLIDES_DIR / f"chapter_{chapter_num_str}.png"
        pix.save(str(img_out_path))
        
        print(f"  -> ページ {page_num+1} を {img_out_path.name} として保存完了")

    doc.close()
    print("\n[すべての画像抽出完了]")
    print(f"出力先フォルダ: {SLIDES_DIR}")

if __name__ == "__main__":
    split_pdf()
