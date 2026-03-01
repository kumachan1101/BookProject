import re
from pathlib import Path

# Fixes for 02_章別 and 01_原稿 directories
directories = [
    Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"),
    Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\01_原稿")
]

def apply_fixes():
    for base_dir in directories:
        # File 1: 16_第2部 第12章_03.md
        file1 = base_dir / "16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_03.md"
        if file1.exists():
            with open(file1, "r", encoding="utf-8") as f:
                content = f.read()
            # Remove the marker
            content = content.replace("★Kindle本では以下のようなリンクはできないのは？\n", "")
            with open(file1, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)
            print(f"Fixed {file1.name}")

        # File 2: 15_第2部 第11章_02.md
        file2 = base_dir / "15_第2部 第11章 インターフェース分離原則 (ISP) 不要な依存の排除とモジュール結合度の最小化_02.md"
        if file2.exists():
            with open(file2, "r", encoding="utf-8") as f:
                content = f.read()
            # Remove the marker
            content = content.replace("★Kindle本では、以下のようなリンクはできないと思います。\n", "")
            with open(file2, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)
            print(f"Fixed {file2.name}")

        # File 3: 13_第2部 第9章_02.md
        file3 = base_dir / "13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_02.md"
        if file3.exists():
            with open(file3, "r", encoding="utf-8") as f:
                content = f.read()
            old_str = "★コラム的な内容、背景が水色の説明をここで入れたい。上記のオブジェクト指向言語を仕組みを模倣とした継承とVテーブルによるオーバーライドを実現している。オブジェクト指向言語を知っている人も、内部的に継承とオーバーライドがどのように動いているかは知らない人が多いと思うが、実際なこのように作られているであっていますか？そうであれば、オブジェクト指向言語を知っている人にも内部の作りを理解するきっかけにもなり、知らない人にとっても、これからオブジェクト指向言語を学ぶのにとても有益な情報だと思っている。オブジェクト指向言語でも内部的にはVテーブルを作り出し、継承時も親と子の共通部分でアクセスする？認識で、なので同じ共通部分は同じメンバーを先頭に配置することで成り立っている。このことを詳しくここで掘り下げて理解を深める形にしたい。\n"
            new_str = "> [!INFO] コラム：オブジェクト指向言語の裏側 —— 継承とオーバーライドの正体\n> これまで見てきた「構造体の先頭メンバへの配置」による継承の模倣と、「関数ポインタ（VTable）」による振る舞いの差し替えは、実はC++やJavaなどのオブジェクト指向言語が内部的に行っている仕組みそのものです。\n> オブジェクト指向言語を知っている方でも、継承やオーバーライドがメモリ上でどのように動いているかを意識する機会は少ないかもしれません。しかし実際のところ、コンパイラはクラスの継承ツリーに合わせて共通部分（親クラス）を先頭に配置し、各インスタンスの裏側にひっそりとVTableへのポインタを用意することで、あの便利な「ポリモーフィズム（多態性）」を実現しています。\n> つまり、この章で学んだC言語での手動実装は、オブジェクト指向のブラックボックスを開け、そのエンジンの作りを理解するための最高のテキストでもあります。これからオブジェクト指向言語を学ぶ人にとっては強固な基礎となり、すでに使いこなしている人にとっては「なぜ動くのか」という深い洞察に繋がる、非常に有益なメカニズムなのです。\n"
            content = content.replace(old_str, new_str)
            with open(file3, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)
            print(f"Fixed {file3.name}")

        # File 4: 06_第1部 第4章.md
        file4 = base_dir / "06_第1部 第4章 不完全型と不透明ポインタ - 型情報の隠蔽による契約のカプセル化.md"
        if file4.exists():
            with open(file4, "r", encoding="utf-8") as f:
                content = f.read()
            # 1. ABI互換性
            old_abi = "★以下突如、ABI互換性が現れるが、どういう話の経緯でこの用語が登場するのか、分かるようにしてほしい。\n#### ABI互換性 (Application Binary Interface Compatibility)"
            new_abi = "前述のような物理的な依存の遮断（カプセル化）は、単に再コンパイルを防ぐだけではなく、実行環境全体に影響を及ぼす「安定した境界線」を作り出します。ここで重要になるのが、不完全型がもたらす **ABI互換性** という概念です。\n\n#### ABI互換性 (Application Binary Interface Compatibility)"
            content = content.replace(old_abi, new_abi)

            # 2. 活用パターン1のコードを使う前提
            old_pattern = "#### Setter関数のシグネチャによる契約追加\n★活用パターン1のコードを使う前提なのか？それであれば、活用パターン2にもってきて、話の流れが続いた方が良いのではないか？前提がないので混乱する。\nSetter関数の追加定義です。`context_set_value` を追加します。"
            new_pattern = "#### Setter関数のシグネチャによる契約追加\nここでは、先述の「2.1. 活用パターン1」で作成した基本的な `Context` モジュールのコードをベースとして、Setter関数と不変条件の概念を組み込んで拡張していきます。\nSetter関数の追加定義です。`context.h` に `context_set_value` を追加します。"
            content = content.replace(old_pattern, new_pattern)

            # 3. コメントアウトされている初期化
            old_init = "★何故、以下コメントアウトになっている？\n#### context.c(続き)\n```c\n// 初期化：internal_stateを10に設定する場合の修正イメージ\n// （※既存の context_create の初期値を 10 に書き換えてください）\n/*\nContext_t* context_create(void)\n{\n    ...\n    if (ctx != NULL) {\n        ctx->internal_state = 10; // 初期値を変更\n    }\n    return ctx;\n}\n*/\n```"
            new_init = "#### context.c(続き)\n```c\n// 初期化：internal_stateを10に設定するように既存の context_create を書き換えます\nContext_t* context_create(void)\n{\n    Context_t* ctx = (Context_t*)calloc(1, sizeof(struct Context));\n    if (ctx != NULL) {\n        ctx->internal_state = 10; // 初期値を0から10に変更\n    }\n    return ctx;\n}\n```"
            content = content.replace(old_init, new_init)

            # 4. 2.1とは？
            old_2_1 = "★以下の2.1とは？どこの章からの話のは流れなのか？基本、章完結にしている。\n#### context.c\n```c\n// （※値読み出し関数 context_get_value は2.1節ですでに定義済みのため省略）\n```"
            new_2_1 = "#### context.c\n```c\n// （※値読み出し関数 context_get_value は先述の「活用パターン1」ですでに定義済みのため省略）\n```"
            content = content.replace(old_2_1, new_2_1)
            
            with open(file4, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)
            print(f"Fixed {file4.name}")

        # File 5: 05_第1部 第3章_01.md
        file5 = base_dir / "05_第1部 第3章 構造体設計とコンポジション - データと責任の統合_01.md"
        if file5.exists():
            with open(file5, "r", encoding="utf-8") as f:
                content = f.read()
            # 1. ServiceObject補足
            old_so = "と **Entity Object** の設計と、それらを組み合わせる **コンポジション** （合成）に焦点を当てます。★なぜ、ServiceObjectは取り扱わないのか、その理由は簡単に補足してほしい。"
            new_so = "と **Entity Object** の設計と、それらを組み合わせる **コンポジション** （合成）に焦点を当てます。Service Objectは、特定のデータ構造を持たず「振る舞い（インターフェース）の提供」が主な責務となるため、第2部の「SOLID原則編」でより本格的に扱います。"
            content = content.replace(old_so, new_so)

            # 2. V1, V2補足
            old_mermaid = "V1がOpに入力され、V2が出力される、上から下へのデータの流れです。\n★以下mermaidにV1とV2という文字が登場していないが？？\n\n```mermaid\n    graph TB\n    %% 1. 入力データ\n    V1[\"<b>【元データ：書き換え不可】</b><br/>Original Instance<br/>(R:100, G:50, B:200)\"]"
            new_mermaid = "V1がOpに入力され、V2が出力される、上から下へのデータの流れです。\n\n```mermaid\n    graph TB\n    %% 1. 入力データ\n    V1[\"<b>【元データ(V1)：書き換え不可】</b><br/>Original Instance<br/>(R:100, G:50, B:200)\"]"
            content = content.replace(old_mermaid, new_mermaid)
            
            # and fix V2 in the mermaid
            old_v2 = "V2[\"<b>【新データ：戻り値】</b><br/>New Instance<br/>(R:110, G:110, B:110)\"]"
            new_v2 = "V2[\"<b>【新データ(V2)：戻り値】</b><br/>New Instance<br/>(R:110, G:110, B:110)\"]"
            content = content.replace(old_v2, new_v2)

            with open(file5, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)
            print(f"Fixed {file5.name}")

        # File 6: 01_section_1.md (Only in 02_章別 and 01_原稿)
        file6 = base_dir / "01_section_1.md"
        if file6.exists():
            with open(file6, "r", encoding="utf-8") as f:
                content = f.read()
            old_intro = "★以下を自然な話の流れで入れてほしい。オブジェクト指向言語を知っている人、知らない人、それぞれのレベルアップになると思っている。\nオブジェクト指向言語を知っている私は、オブジェクト指向の仕組みが改めて理解が深まりました。継承、多態性、カプセル化、thisポインタなど。正直、この本で紹介した抽象化は、極端な例が多いが、抽象化を導入するための仕組みを理解する、オブジェクト指向の作りも理解するレベルが上がると思ってます。\n"
            new_intro = "また、本書はオブジェクト指向言語（OOP）の経験者・未経験者を問わず、両者にとって大きなレベルアップの契機となります。C言語という極限まで削ぎ落とされた環境で「オブジェクト指向的な仕組み（継承、多態性、カプセル化、thisポインタなど）」をゼロから手作りすることで、OOPの背後にあるメカニズムへの解像度が飛躍的に高まるからです。\n\n本書の例には、C言語の作法としてはあえて極端とも言える抽象化手法も含まれていますが、それらの仕組みを深く理解することは、OOPの真のパワフルさとアーキテクチャ設計の勘所を掴むための最高のトレーニングとなるでしょう。\n"
            content = content.replace(old_intro, new_intro)
            with open(file6, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)
            print(f"Fixed {file6.name}")

if __name__ == '__main__':
    apply_fixes()
