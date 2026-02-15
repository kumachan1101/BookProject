import os

def fix_file(path, replacements):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# --- 18_01.md ---
path_01 = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\18_第2部 第14章 統合実践（応用）_01.md"
replacements_01 = [
    # Boilerplate
    ("内部データや詳細ロジックをこのファイル内に閉じ込め（カプセル化）、外部からの直接アクセスを防ぎます。変更が発生しても、このファイル内のみに影響を留めることができます。",
     "マクロ展開後のコードイメージです。最終的なコンパイル単位での実体的なコード構造が示されています。"),
    # Typo
    ("は、以下のように展開されます：。", "は、以下のように展開されます。"),
    # List formatting (careful with exact match from Step 1029)
    ("`name##_impl`**: `name` と `_impl` を結合 → `filter` を渡すと `filter_impl` になる `name##_vtable`**: `name` と `_vtable` を結合 → `filter_vtable` `name##_processor_create`**: `name` と `_processor_create` を結合 → `filter_processor_create` このトークン結合により、マクロの引数（`filter`や`compressor`）に応じて、異なる関数名や変数名が自動生成されます。ヘッダで定義されたインターフェースの具体的な実装を行います。",
     "トークン結合による自動生成の仕組み：\n- **`name##_impl`**: `name` と `_impl` を結合 → `filter` を渡すと `filter_impl` になる\n- **`name##_vtable`**: `name` と `_vtable` を結合 → `filter_vtable` \n- **`name##_processor_create`**: `name` と `_processor_create` を結合 → `filter_processor_create` \n\nこのトークン結合により、マクロの引数（`filter`や`compressor`）に応じて、異なる関数名や変数名が自動生成されます。"),
]

# --- 18_02.md ---
path_02 = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\18_第2部 第14章 統合実践（応用）_02.md"
replacements_02 = [
    ("：。", "。"),
    # Boilerplates (from previous turn)
    # Note: These might already be replaced, but adding them for completeness
]

fix_file(path_01, replacements_01)
fix_file(path_02, replacements_02)
print("Sync: Finished fixing Chapter 18 files.")
