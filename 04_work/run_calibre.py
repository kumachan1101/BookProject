"""Calibre EPUB/MOBI変換のみを実行するスクリプト"""
import subprocess
from pathlib import Path

DIST_DIR = Path('dist')
BOOK_HTML = DIST_DIR / 'book.html'
BOOK_EPUB = DIST_DIR / 'book.epub'
BOOK_MOBI = DIST_DIR / 'book.mobi'
IMG_DIR = DIST_DIR / 'images'

cover_dest_path = None
for ext in ['png', 'jpg']:
    p = Path(f'../cover.{ext}')
    if p.exists():
        cover_dest_path = IMG_DIR / p.name
        break

epub_options = [
    'ebook-convert', str(BOOK_HTML), str(BOOK_EPUB),
    '--language', 'ja',
    '--epub-version', '2',
    '--chapter', "//*[name()='h1']",
    '--level1-toc', '//h:h1',
    '--chapter-mark', 'pagebreak',
    '--disable-font-rescaling',
    '--margin-top', '0', '--margin-bottom', '0',
    '--margin-left', '0', '--margin-right', '0',
    '--pretty-print'
]
if cover_dest_path and cover_dest_path.exists():
    epub_options.extend(['--cover', str(cover_dest_path)])

print('[EPUB変換開始...]')
result = subprocess.run(epub_options, capture_output=True)
if result.returncode == 0:
    print('[OK] EPUB完了:', BOOK_EPUB)
else:
    stderr = result.stderr.decode('utf-8', errors='replace')
    print('[ERROR] EPUB変換失敗:')
    print(stderr[:2000])
    exit(1)

# MOBI変換
if BOOK_EPUB.exists():
    print('[MOBI変換開始...]')
    r2 = subprocess.run([
        'ebook-convert', str(BOOK_EPUB), str(BOOK_MOBI),
        '--output-profile', 'kindle',
        '--mobi-file-type', 'both'
    ], capture_output=True)
    if r2.returncode == 0:
        print('[OK] MOBI完了:', BOOK_MOBI)
    else:
        stderr2 = r2.stderr.decode('utf-8', errors='replace')
        print('[MOBI ERROR]:')
        print(stderr2[:1000])
