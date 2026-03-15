import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# File 1: 05_第1部 第3章
f1 = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\05_第1部 第3章 構造体設計とコンポジション - データと責任の統合_01.md'
replace_in_file(f1, [
    ('Op["<b>color_to_grayscale()</b><br/>(新しい値を作る純粋関数)"]', 'Func["<b>color_to_grayscale()</b><br/>(新しい値を作る純粋関数)"]'),
    ('V1 ==> Op', 'V1 ==> Func'),
    ('Op ==> V2', 'Func ==> V2'),
    ('style Op fill', 'style Func fill')
])

# File 2: 16_第2部 第12章 _02
f2 = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_02.md'
replace_in_file(f2, [
    ('デフォルト処理（NoOp: コピー）', 'デフォルト処理（Plain: コピー）'),
    ('AES、ZIP、NoOp（何もしない）という', 'AES、ZIP、Plain（そのまま通す）という'),
    ('NoOp変換の実装', 'Plain変換の実装'),
    ('NoOp実装（変換なし）', 'Plain実装（そのまま通す）'),
    ('noop_impl', 'plain_impl'),
    ('create_noop_transform', 'create_plain_transform'),
    ('"NOOP:"', '"PLAIN:"'),
    ('異なる振る舞い（AES, ZIP, NoOp）を', '異なる振る舞い（AES, ZIP, Plain）を'),
    ('NoOpやモックを注入して', 'Plainやモックを注入して')
])

# File 3: 17_第2部 第13章 _02.md
f3 = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\17_第2部 第13章 統合実践（基本）_02.md'
replace_in_file(f3, [
    ('抽象インターフェースに対して、どの具象オブジェクトを流し込むかという「依存性の注入（DI）」を一箇所に集中させます。これにより、', '抽象インターフェースに対して、どの具象オブジェクトを流し込むかという「依存性の注入（DI）」を一箇所に集中させます。このように、別々に作られた部品（モジュール）同士をケーブルで繋ぐように結びつける作業を「**ワイヤリング（Wiring）**」と呼びます。これにより、')
])

# File 4: 16_第2部 第12章 _03.md
f4 = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_03.md'
replace_in_file(f4, [
    ('Main関数で具象オブジェクトを生成・注入していますか？', 'Main関数（コンポジションルート）で、別々に作られた部品同士を繋ぎ合わせるように、具象オブジェクトを生成・注入（ワイヤリング）していますか？')
])

# Also add the main function into File 4
with open(f4, 'r', encoding='utf-8') as f:
    f4_content = f.read()

main_code = """    free(tax);
}

int main(void) {
    test_total_calculation();
    printf("全てのテストが成功しました！\\n");
    return 0;
}"""
f4_content = f4_content.replace('    free(tax);\n}', main_code)

output_block = """```

#### 実行結果
```c
全てのテストが成功しました！
```

### ステップ3：本物の実装"""
f4_content = f4_content.replace('```\n\n### ステップ3：本物の実装', output_block)

with open(f4, 'w', encoding='utf-8') as f:
    f.write(f4_content)

print("All replacements done.")
