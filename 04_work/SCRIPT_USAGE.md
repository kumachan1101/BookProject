
# 9. Build Script Usage (ビルドスクリプト使用方法)

本書のビルドには `md_to_epub_with_pdf.py` を使用します。
スクリプトは `04_work` ディレクトリ内に配置されています。実行時は必ず `04_work` ディレクトリに移動してください。

## 基本コマンド

```bash
cd 04_work
python md_to_epub_with_pdf.py [オプション]
```

## 主なオプション

| オプション | 説明 |
| :--- | :--- |
| `--steps [step ...]` | 実行するステップを指定します。<br>デフォルト: `pdf mermaid code epub` (全て)<br>使用可能な値:<br>- `pdf`: 参考資料PDFのページ分割（`03_資料` -> `05_生成/images/pdf`）<br>- `mermaid`: Mermaid図の画像化<br>- `code`: ソースコードの画像化<br>- `epub`: EPUB/MOBI/PDF（完成版）の生成 |
| `--clean` | 生成済みの画像（Mermaid/Code/PDF）をすべて削除してから再生成します。<br>完全なクリーンビルドを行いたい場合に使用します。<br>**注意:** `--target` と併用した場合でも、**全ての画像（ターゲット以外も含む）が削除されます**。 |
| `--target [keyword ...]` | **【推奨】** 特定の章のみ画像生成（Mermaid/Code）を行います。<br>ファイル名に含まれるキーワード（例: "第14章" や "14_" など）を指定します。<br>指定されなかった章は、既存の画像を再利用するため高速に完了します。（HTML結合は全章行われます） |

## 使用例

### ケース1: 特定の章（例：第14章）だけを修正して確認したい場合
最も高速な確認方法です。修正した章の画像のみ再生成し、他はスキップします。
※PDF分割処理(`pdf`)は通常スキップして問題ありません。

```bash
cd 04_work
python md_to_epub_with_pdf_fixed.py --steps code mermaid epub --target "第14章"
```

### ケース2: 全体をクリーンビルドしたい場合
最終確認や、画像生成に失敗している場合に実行します。

```bash
cd 04_work
python md_to_epub_with_pdf_fixed.py --clean
```

### ケース3: EPUB変換のみ行いたい場合（テキスト修正のみ）
画像生成をスキップし、テキスト修正のみを反映させます。

```bash
cd 04_work
python md_to_epub_with_pdf_fixed.py --steps epub
```
