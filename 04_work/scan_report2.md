## 04_第1部 第2章 関数ポインタと間接呼び出し - 動的結合の実現_01.md
### first_terms
Line 268: バッファのフラッシュ
### pointers
Line 499: self
Line 515: self
Line 520: self
Line 527: self
Line 551: self
Line 553: self
Line 564: self
Line 567: self
Line 568: self
Line 572: self
Line 575: self
Line 600: self
Line 600: context
Line 611: self
Line 612: self
Line 614: self
Line 618: self
Line 619: self
Line 641: self
Line 642: self
Line 647: self
Line 648: self
Line 661: self
Line 671: self
Line 677: self
Line 697: self
Line 698: self
Line 699: self
Line 700: self

## 06_第1部 第4章 不完全型と不透明ポインタ - 型情報の隠蔽による契約のカプセル化.md
### pointers
Line 34: context
Line 37: context
Line 40: context
Line 103: context
Line 115: context
Line 119: context
Line 134: context
Line 152: context
Line 154: context
Line 156: context
Line 171: context
Line 185: context
Line 195: context
Line 209: context
Line 215: context
Line 229: context
Line 268: context
Line 270: context
Line 305: context
Line 330: context
Line 334: context
Line 354: context
Line 363: context
Line 374: context
Line 383: context
Line 391: context
Line 410: context
Line 428: context
Line 479: context
Line 480: context
Line 482: context
Line 483: context
Line 608: self

## 09_第1部 第7章 メモリ管理パターン - 責任の明確化_01.md
### first_terms
Line 680: DRY原則

## 09_第1部 第7章 メモリ管理パターン - 責任の明確化_02.md
### first_terms
Line 107: valgrind

## 10_第1部 総括 堅牢なコードの「基礎」は固まった.md
### bad_terms
Line 4: 螺旋 -> **第1部「基礎道具編」** では、C言語の7つの基本技術を、設計の三本柱である  **「責任」、「契約」、「依存」**  を実現するための物理的な  **道具** （ツール）として学びました。これらの技術は章ごとに異なる軸を扱いますが、それは  **螺旋的に理解を深めるための意図的な構成**  です。

## 11_第2部 導入：原則編の目的と学習ロードマップ.md
### first_terms
Line 158: 包含
Line 168: ガベージコレクション

## 12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_02.md
### first_terms
Line 20: Brotli
Line 429: Zstd

## 13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_01.md
### pointers
Line 4: context
Line 108: context
Line 117: context
Line 139: self
Line 140: self
Line 145: self
Line 149: self
Line 151: self
Line 157: context
Line 174: self
Line 175: self
Line 182: self
Line 183: self
Line 208: self
Line 295: self
Line 296: self
Line 303: self
Line 304: self
Line 329: self
Line 421: self
Line 500: self
Line 504: self
Line 523: self
Line 542: self
Line 543: self
Line 558: self
Line 572: self
Line 573: self
Line 588: self
Line 668: context
Line 815: self
Line 819: self
Line 837: self
Line 838: self
Line 853: self
Line 867: self
Line 868: self
Line 883: self
Line 902: self

## 13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_02.md
### bad_terms
Line 13: 悪臭 -> 非常によく見かけるコードの「悪臭」の一つが、 `bool` 型のフラグ（`is_scheduled` など）を利用した振る舞いの分岐です。以下の `notifier.c` を見てください。関数がフラグ引数を受け取り、内部の `if` 文で「即時送信」か「予約送信」かを決定しています。
### pointers
Line 100: self
Line 128: self
Line 129: self
Line 171: self
Line 173: self
Line 435: self
Line 444: context

## 14_第2部 第10章 リスコフ置換原則 (LSP) 多態性の安全性と契約の保証_01.md
### pointers
Line 253: self
Line 264: self
Line 267: self
Line 271: self
Line 277: self
Line 283: self
Line 287: self
Line 292: self
Line 295: self
Line 300: self
Line 317: self
Line 318: self
Line 422: self
Line 423: self
Line 526: self
Line 527: self

## 14_第2部 第10章 リスコフ置換原則 (LSP) 多態性の安全性と契約の保証_02.md
### pointers
Line 119: self
Line 120: self
Line 237: self
Line 238: self
Line 263: self
Line 267: self
Line 368: self
Line 369: self
Line 373: self
Line 399: self
Line 400: self
Line 401: self
Line 403: self
Line 538: self
Line 539: self
Line 559: self
Line 560: self
Line 580: self
Line 601: self
Line 618: self
Line 657: self

## 15_第2部 第11章 インターフェース分離原則 (ISP) 不要な依存の排除とモジュール結合度の最小化_01.md
### pointers
Line 481: self
Line 482: self
Line 483: self
Line 494: self
Line 499: self
Line 582: self
Line 595: self
Line 608: self
Line 626: self
Line 641: self
Line 642: self
Line 643: self
Line 678: self
Line 681: self
Line 687: self
Line 703: self

## 16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_01.md
### first_terms
Line 276: SDP
### pointers
Line 321: context
Line 330: context
Line 362: self
Line 363: self
Line 364: self
Line 370: self
Line 381: self
Line 383: self
Line 385: self
Line 406: self
Line 413: self
Line 414: self
Line 422: self
Line 424: self
Line 428: self
Line 429: self
Line 466: self
Line 488: self
Line 489: self
Line 497: self
Line 502: self
Line 503: self
Line 539: self
Line 796: self
Line 801: self
Line 823: self
Line 824: self
Line 836: self
Line 854: self
Line 855: self
Line 866: self
Line 882: self
Line 949: self

## 16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_02.md
### pointers
Line 125: self
Line 129: self
Line 150: self
Line 152: self
Line 169: self
Line 182: self
Line 184: self
Line 201: self
Line 211: self
Line 213: self
Line 227: self
Line 236: self
Line 261: self
Line 484: self
Line 488: self
Line 506: self
Line 513: self
Line 519: self
Line 526: self
Line 582: self
Line 794: self
Line 795: self
Line 802: self
Line 803: self
Line 809: self
Line 810: self
Line 841: self

## 16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_03.md
### pointers
Line 11: self
Line 15: self
Line 36: self
Line 44: self
Line 45: self
Line 55: self
Line 83: self
Line 84: self
Line 97: self
Line 197: self
Line 198: self
Line 199: self

## 17_第2部 第13章 統合実践（基本）_01.md
### pointers
Line 342: self
Line 344: self
Line 346: self
Line 351: self
Line 370: self
Line 376: self
Line 383: self
Line 403: self
Line 405: self
Line 407: self
Line 412: self
Line 432: self
Line 439: self
Line 450: self
Line 562: self
Line 563: self
Line 571: self
Line 572: self
Line 580: self
Line 586: self
Line 587: self
Line 588: self
Line 590: self
Line 618: self
Line 651: self
Line 652: self
Line 674: self
Line 675: self
Line 684: self
Line 685: self
Line 686: self
Line 688: self
Line 712: self
### ng_patterns
Line 310: 理由： -> *   IOの変更理由：「データの読み書き方法が変わる」
Line 311: 理由： -> *   Parserの変更理由：「データフォーマットが変わる」
Line 312: 理由： -> *   Processorの変更理由：「処理の順序が変わる」

## 17_第2部 第13章 統合実践（基本）_02.md
### pointers
Line 175: self
Line 181: self
Line 186: self
Line 200: self

## 18_第2部 第14章 統合実践（応用）_01.md
### pointers
Line 333: self
Line 334: self
Line 341: self
Line 342: self
Line 351: self
Line 352: self
Line 439: self
Line 440: self
Line 444: self
Line 449: self
Line 459: self
Line 467: self
Line 501: self
Line 502: self
Line 533: self
Line 534: self
Line 535: self
Line 676: self
Line 677: self
Line 686: self
Line 687: self
Line 714: self
Line 715: self
Line 724: self
Line 725: self
Line 810: self
Line 811: self
Line 820: self
Line 821: self
Line 833: self

## 18_第2部 第14章 統合実践（応用）_02.md
### pointers
Line 61: self
Line 62: self
Line 69: self
Line 70: self
Line 76: self
Line 395: self
Line 397: self
Line 400: self
Line 533: self
Line 534: self
Line 535: self
Line 539: self
Line 552: self
Line 560: self
Line 568: self
Line 594: self
Line 595: self
Line 615: self
Line 617: self
Line 618: self
Line 620: self
Line 623: self
Line 624: self
Line 626: self
Line 631: self
Line 635: self
Line 636: self
Line 672: self
Line 673: self
Line 690: self
Line 691: self
Line 696: self
Line 697: self
Line 699: self
Line 723: self
Line 761: self
Line 762: self
Line 771: self
Line 772: self
Line 776: self
Line 779: self
Line 781: self
Line 794: self
