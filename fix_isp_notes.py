import os
import sys

path = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\15_第2部 第11章 インターフェース分離原則 (ISP) 不要な依存の排除とモジュール結合度の最小化_01.md'

with open(path, encoding='utf-8') as f:
    content = f.read()

# Pattern 1: NOTE block after Pattern 1 execution results
note1_start = content.find('> [!NOTE] 実行結果は同じ、でも設計の構造はまったく違う')
if note1_start == -1:
    print("NOTE1 not found")
    sys.exit(1)

# The NOTE block ends before "#### 設計のポイント"
note1_end_marker = '\n\n#### 設計のポイント：物理的な壁を作る'
note1_end = content.find(note1_end_marker, note1_start)
if note1_end == -1:
    print("End marker for NOTE1 not found")
    sys.exit(1)

old_note1 = content[note1_start:note1_end]
print(f"NOTE1 block found ({len(old_note1)} chars)")

new_note1 = '''#### 適用前後の設計差分

ISPの適用前後で、 **プログラムの実行結果はまったく変わりません。** `[Monitor] System is healthy.` という出力は適用前後どちらのコードも同じです。ISPの効果は「実行時」ではなく、 **「設計時・コンパイル時」の構造変化** に現れます。

| 観点 | 適用前（太ったヘッダ） | 適用後（分離したヘッダ） |
| --- | --- | --- |
| **監視クライアントの依存** | `device_types.h`（不要な設定定義）まで強制的に読み込む | `device_monitor.h`だけをインクルード。設定定義を一切知らない |
| **設定項目追加時の影響** | 監視クライアントも再コンパイル強制 | 監視クライアントは無傷 |
| **コードの認知負荷** | 監視担当者が設定構造体まで把握する必要がある | 監視担当者は`check_health`だけ知ればよい |
| **テスト・変更の範囲** | 設定APIの変更がテスト対象に混入する | 関心事ごとに独立してテスト・変更できる |'''

# Pattern 2: NOTE block after Pattern 2 execution results
note2_start = content.find('> [!NOTE] 実行結果は同じ、でもVTableの構造はまったく違う')
if note2_start == -1:
    print("NOTE2 not found")
    sys.exit(1)

note2_end_marker = '\n\n#### 設計のポイント：具象を「型」の制約から解放する'
note2_end = content.find(note2_end_marker, note2_start)
if note2_end == -1:
    print("End marker for NOTE2 not found")
    sys.exit(1)

old_note2 = content[note2_start:note2_end]
print(f"NOTE2 block found ({len(old_note2)} chars)")

new_note2 = '''#### 適用前後の設計差分

このパターンでも、適用前後の実行結果は同じです。`Read OK`/`Write OK` という出力は変わりません。ISPの効果は「実行時」ではなく、 **「型の安全性・設計の誠実さ」** に現れます。

| 観点 | 適用前（太ったVTable） | 適用後（分離したVTable） |
| --- | --- | --- |
| **読み取り専用デバイスの立場** | `write_config`の実装を強いられる（嘘の実装） | `IReaderVTable`だけを実装すればよい |
| **LSP準拠** | サポートしていない操作が契約に含まれる（違反） | できることだけを正直に宣言できる（準拠） |
| **クライアントの安全性** | 実行してみるまで成功するか分からない | 型として持っている機能は必ず動作する |
| **分割の軸** | デバイスが持ちそうな機能という実装都合の分類 | 読取アクター・設定アクターという利用者アクター別の契約 |'''

content2 = content.replace(old_note1, new_note1)
content3 = content2.replace(old_note2, new_note2)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content3)

print("Done. Changes applied.")
