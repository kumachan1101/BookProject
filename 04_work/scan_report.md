## 04_第1部 第2章 関数ポインタと間接呼び出し - 動的結合の実現_01.md
### 初出用語
Line 268: バッファのフラッシュ -> *   **バッファのフラッシュ**
### `self` / `context` 使用箇所
Line 499: self -> さらに発展させ、関数ポインタ構造体に **「状態」を持つデータ** を組み合わせるパターンです。`self`引数を通じて各インスタンスが独自の状態を保持できるようにし、C言語でクラスのインスタンスに相当する概念を実現します。
Line 515: self -> このような「異なる状態（データ構造）を持ちつつ、共通のインターフェースで振る舞いを呼び出したい」というオブジェクト指向的な課題を解決するため、ここではVTable（関数ポインタのセット）とContext（任意の状態データへのポインタ `void* self`）をペアにした構造体を定義します。関数の第一引数に自分自身（`self`）へのポインタを渡すように規約を定めることで、C言語でも「データと振る舞いの統合」というカプセル化を強力に実現します。
Line 520: self -> 関数が呼び出される際、必ず `self` ポインタを経由して、そのオブジェクト専用のデータ領域にアクセスします。
Line 527: self -> CP["self (状態)<br/>void* ptr"]
Line 551: self -> 状態（データ）と振る舞い（VTable）を統合した「クラスのような構造」を定義しています。`MessageWriter` 構造体に `vtable`（関数ポインタ配列）と `self`（インスタンス固有データへのポインタ `void*`）を持たせています。
Line 553: self -> メソッドの第1引数に具象データへのポインタ `void* self` を取るように設計されています。C言語でオブジェクト指向のカプセル化と多態性を実現するための標準的なイディオムです。ポインタを `void*` にすることで、任意のデータ構造を保持できるようにしています（ジェネリクス）。非常に柔軟性が高く、本格的なフレームワーク開発でも使用される強力なパターンです。
Line 564: self -> // 各関数の第1引数に具象データの不透明ポインタ void* (self) を取ることで、
Line 567: self -> void (*write)(void* self, const char* msg);
Line 568: self -> void (*clear)(void* self);
Line 572: self -> // 「振る舞い(vtable)」と「インスタンス固有のデータ(self)」をセットで管理する。
Line 575: self -> void* self; // 具象実装ごとの固有データ（状態）を保持するポインタ
Line 600: self -> `prefix_write_impl` では `self->context` を `PrefixContext*` にキャストして、インスタンス固有のプレフィックス文字列にアクセスしています。異なるデータ構造を持つオブジェクトを、同じ `MessageWriter` インターフェースで扱えるようにしています。
Line 600: context -> `prefix_write_impl` では `self->context` を `PrefixContext*` にキャストして、インスタンス固有のプレフィックス文字列にアクセスしています。異なるデータ構造を持つオブジェクトを、同じ `MessageWriter` インターフェースで扱えるようにしています。
Line 611: self -> static void prefix_write_impl(void* self, const char* msg) {
Line 612: self -> // self を具象型にキャストして固有データにアクセス
Line 614: self -> PrefixContext* ctx = (PrefixContext*)self;
Line 618: self -> static void prefix_clear_impl(void* self) {
Line 619: self -> PrefixContext* ctx = (PrefixContext*)self;
Line 641: self -> static void counter_write_impl(void* self, const char* msg) {
Line 642: self -> CounterContext* ctx = (CounterContext*)self;
Line 647: self -> static void counter_clear_impl(void* self) {
Line 648: self -> CounterContext* ctx = (CounterContext*)self;
Line 661: self -> 最後に、これらのロガーを使用可能にするための初期化（コンストラクタ相当）関数です。`vtable` に適切な実装テーブルを、`self` にデータ領域を設定して、オブジェクトを構築します。
Line 671: self -> writer->self = ctx;
Line 677: self -> writer->self = ctx;
Line 697: self -> // 抽象インターフェース経由での呼び出し（内部状態ポインタ self を渡すのがポイント）
Line 698: self -> writer->vtable->write(writer->self, "Hello, C World!");
Line 699: self -> writer->vtable->write(writer->self, "Function pointers are powerful.");
Line 700: self -> writer->vtable->clear(writer->self);

## 06_第1部 第4章 不完全型と不透明ポインタ - 型情報の隠蔽による契約のカプセル化.md
### `self` / `context` 使用箇所
Line 34: context -> H["context.h<br/>struct Context;<br/>typedef ... Context_t;"]
Line 37: context -> C["context.c<br/>#include 'context.h'<br/>struct Context { ... };"]
Line 40: context -> U["main.c<br/>#include 'context.h'<br/>Context_t* ptr;"]
Line 103: context -> この不要な依存と再コンパイルの連鎖を断ち切るための強力な技法が、 **PIMPL (Pointer to Implementation) パターン** です。ヘッダには「構造体の名前だけ（不完全型）」と「そのポインタ（不透明ポインタ）」を残し、中身の完全な定義は実装ファイル（`context.c`）に移動させます。これにより、変更の波及を実装ファイル内に物理的に隔離し、クライアント側には一切影響を与えない（ABI互換性の維持）という強固なカプセル化を実現します。
Line 115: context -> subgraph Header ["公開ヘッダ (context.h)"]
Line 119: context -> subgraph Impl ["実装ファイル (context.c)"]
Line 134: context -> #### context.h
Line 152: context -> ここで初めて `struct Context { ... }` を定義します（完全型）。データ構造の定義を `.c` ファイル内に閉じ込めることで、このファイルの変更が外部に波及することを防ぎます（ABI互換性）。構造体のメンバを修正しても `context.h` には影響がないため、利用側の再コンパイルは不要となります。
Line 154: context -> #### context.c
Line 156: context -> #include "context.h"
Line 171: context -> #### context.c (構造体のメモリ確保と初期化（生成）)
Line 185: context -> printf("[context.c] Context struct secured: %p\n", (void*)ctx);
Line 195: context -> #### context.c (値の取得（アクセサ）)
Line 209: context -> #### context.c (リソースの解放（破棄）)
Line 215: context -> printf("[context.c] Context struct freed: %p\n", (void*)ctx);
Line 229: context -> #include "context.h"
Line 268: context -> [context.c] Context struct secured: 0x...
Line 270: context -> [context.c] Context struct freed: 0x...
Line 305: context -> Setter["<b>【Entity：context.c】</b><br/>セッター関数による受付"]
Line 330: context -> Setter関数の追加定義です。`context.h` に `context_set_value` を追加します。
Line 334: context -> #### context.h への追加
Line 354: context -> #### context.c
Line 363: context -> printf("[context.c] Attempting to set value to %d...\n",
Line 374: context -> printf("[context.c] Validation FAILED: "
Line 383: context -> printf("[context.c] Validation SUCCESS: "
Line 391: context -> #### context.c(続き)
Line 410: context -> #### context.c
Line 428: context -> #include "context.h"
Line 479: context -> [context.c] Attempting to set value to 50...
Line 480: context -> [context.c] Validation SUCCESS: Value set to 50.
Line 482: context -> [context.c] Attempting to set value to 200...
Line 483: context -> [context.c] Validation FAILED: Value 200 is outside [0, 100].
Line 608: self -> // self(obj)を渡すことで、実装側が状態にアクセスできるようにする

## 09_第1部 第7章 メモリ管理パターン - 責任の明確化_01.md
### 初出用語
Line 680: DRY原則 -> この「複雑な後始末の組み合わせ」と「コピペによる解放漏れ」を劇的に改善するのが、C言語における **`goto cleanup` パターン** です。「モダンなプログラミングにおいて `goto` は悪である」と教えられがちですが、C言語においてはこの **「エラー時のリソース解放の一元化」に限り、もっとも推奨されるベストプラクティス** として認知されています。関数の末尾に `cleanup:` ラベルを一つだけ用意し、すべてのエラー脱出経路をここへジャンプ（`goto`）させることで、「確保した逆順での安全な解放処理（DRY原則の適用）」を美しい一本の流れとして記述することができます。

## 09_第1部 第7章 メモリ管理パターン - 責任の明確化_02.md
### 初出用語
Line 107: valgrind -> * メモリリークチェックツール（valgrind等）を実行した

## 10_第1部 総括 堅牢なコードの「基礎」は固まった.md
### 修正対象用語 (悪臭・螺旋など)
Line 4: 螺旋 -> **第1部「基礎道具編」** では、C言語の7つの基本技術を、設計の三本柱である  **「責任」、「契約」、「依存」**  を実現するための物理的な  **道具** （ツール）として学びました。これらの技術は章ごとに異なる軸を扱いますが、それは  **螺旋的に理解を深めるための意図的な構成**  です。

## 11_第2部 導入：原則編の目的と学習ロードマップ.md
### 初出用語
Line 158: 包含 -> 継承（Inheritance）の代わりとなるのは、 **構造体の包含（Embedding）** と **コンポジション（合成）** です。
Line 168: ガベージコレクション -> ガベージコレクションがないC言語では、 **メモリ管理パターン** や  **`goto cleanup`**  による一括処理が不可欠です。一見手間に思えるこの制約は、実は「責任（誰が消すか）」と「契約（失敗時にリソースはどうなるか）」を設計レベルで突き詰める良い動機となります。

## 12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_02.md
### 初出用語
Line 20: Brotli -> この設計のままでは、将来「Brotli」などの第3のアルゴリズムを追加しようとした際にも、この `if-else` 分岐の中に直接手を入れなければならず、既存の（安定して動いていたはずの）LZ4やGzipのロジックにまで破壊的な影響を及ぼす危険性があります。
Line 429: Zstd -> | **新アルゴリズム（Zstd）を追加** | `compress_data`にelse-if分岐を追加 | 新しい`zstd_strategy.c`を追加し、`compression_selector.c`に1行追加するだけ |

## 13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_01.md
### `self` / `context` 使用箇所
Line 4: context -> この原則を実現するためには、 **第2章 関数ポインタと間接呼び出し** で学んだ **VTableパターン** と **context** による状態管理が鍵となります。
Line 108: context -> IF["IDevice<br/>（vtable + context）"]
Line 117: context -> IF -->|"context*"| Data
Line 139: self -> int (*write_data)(void* self, const char* data, size_t len);
Line 140: self -> void (*close)(void* self);
Line 145: self -> void* self;
Line 149: self -> (d)->vtable->write_data((d)->self, (data), (len))
Line 151: self -> (d)->vtable->close((d)->self)
Line 157: context -> 各デバイスは固有のデータ構造（context）を持ちますが、クライアントからは`void*`として隠蔽されます。`IDevice` インターフェースのシリアル通信版実装です。
Line 174: self -> static int serial_write(void* self, const char* data, size_t len) {
Line 175: self -> SerialContext* ctx = (SerialContext*)self;
Line 182: self -> static void serial_close(void* self) {
Line 183: self -> SerialContext* ctx = (SerialContext*)self;
Line 208: self -> device->self = ctx;
Line 295: self -> static int usb_write(void* self, const char* data, size_t length) {
Line 296: self -> UsbContext* ctx = (UsbContext*)self;
Line 303: self -> static void usb_close(void* self) {
Line 304: self -> UsbContext* ctx = (UsbContext*)self;
Line 329: self -> device->self = ctx;
Line 421: self -> | **void* self** | 具象データの隠蔽 | 情報隠蔽・カプセル化 |
Line 500: self -> int (*apply)(void* self, int base_price);
Line 504: self -> void* self; // 戦略固有のデータを隠蔽
Line 523: self -> result = strategy->vtable->apply(strategy->self, base_price);
Line 542: self -> static int apply_percent(void* self, int base_price) {
Line 543: self -> PercentContext* ctx = (PercentContext*)self;
Line 558: self -> s->self = ctx;
Line 572: self -> static int apply_fixed(void* self, int base_price) {
Line 573: self -> FixedContext* ctx = (FixedContext*)self;
Line 588: self -> s->self = ctx;
Line 668: context -> | **データの持ち方** | `int value` 1つでやりくり | `context` により戦略ごとに自由 |
Line 815: self -> int (*calculate)(void* self, int price);
Line 819: self -> void* self; // 具体的な戦略（クレカ、コンビニ等）が持つデータを隠蔽
Line 837: self -> static int calc_credit(void* self, int price) {
Line 838: self -> CreditContext* ctx = (CreditContext*)self;
Line 853: self -> fee->self = ctx;
Line 867: self -> static int calc_convenience(void* self, int price) {
Line 868: self -> ConvenienceContext* ctx = (ConvenienceContext*)self;
Line 883: self -> fee->self = ctx;
Line 902: self -> int fee = strategy->vtable->calculate(strategy->self, price);

## 13_第2部 第9章 開放閉鎖原則（OCP）：拡張のために開き、修正に対して閉じる_02.md
### 修正対象用語 (悪臭・螺旋など)
Line 13: 悪臭 -> 非常によく見かけるコードの「悪臭」の一つが、 `bool` 型のフラグ（`is_scheduled` など）を利用した振る舞いの分岐です。以下の `notifier.c` を見てください。関数がフラグ引数を受け取り、内部の `if` 文で「即時送信」か「予約送信」かを決定しています。
### `self` / `context` 使用箇所
Line 100: self -> void (*send)(INotifyStrategy* self, const char* message);
Line 128: self -> static void immediate_send(INotifyStrategy* self, const char* message) {
Line 129: self -> ImmediateNotify* notify = (ImmediateNotify*)self;
Line 171: self -> static void scheduled_send(INotifyStrategy* self, const char* message) {
Line 173: self -> ScheduledNotify* notify = (ScheduledNotify*)self;
Line 435: self -> | **void* self** | 具象データの隠蔽 | 情報隠蔽・カプセル化 |
Line 444: context -> * **データと振る舞いの分離** : 具象データ（`context`）を `void*` 等で隠蔽し、操作を関数ポインタ（VTable）経由に限定しているか？

## 14_第2部 第10章 リスコフ置換原則 (LSP) 多態性の安全性と契約の保証_01.md
### `self` / `context` 使用箇所
Line 253: self -> * - self != NULL, error_code != NULL
Line 264: self -> void* (*read_data)(void* self, size_t size, int* error_code);
Line 267: self -> * * [前提条件] self != NULL
Line 271: self -> int (*close)(void* self);
Line 277: self -> void* self;
Line 283: self -> return stream->vtable->read_data(stream->self, size, error_code);
Line 287: self -> return stream->vtable->close(stream->self);
Line 292: self -> ### 2.3. 不完全型と`void* self`による具象データからの隔離
Line 295: self -> *  **`void* self`** : VTableのメソッドは、第1引数として具象データへの不透明なポインタ (`void* self`) を受け取ります。これにより、クライアントコードは具象データへの **静的な依存** を断ち切ることができます。
Line 300: self -> この図は、クライアントが「抽象」のみに依存し、具象実装の「詳細」から物理的に隔離されている様子を示しています。クライアント層は具象クラス（`ConcreteA`, `ConcreteB`）を知らず、`VTable` という契約のみを知っています。`void* self` というポインタを経由することで、型情報を漏らさずに具象データを操作します。図中の矢印は依存の方向を、点線は実行時の動的な参照を表しています。
Line 317: self -> VTable -.->|"void* self"| ConcreteA
Line 318: self -> VTable -.->|"void* self"| ConcreteB
Line 422: self -> static int unaligned_write_impl(void* self, const void* data, size_t size) {
Line 423: self -> UnalignedStorage_Data* storage = (UnalignedStorage_Data*)self;
Line 526: self -> static int aligned_write_impl(void* self, const void* data, size_t size) {
Line 527: self -> AlignedStorage_Data* storage = (AlignedStorage_Data*)self;

## 14_第2部 第10章 リスコフ置換原則 (LSP) 多態性の安全性と契約の保証_02.md
### `self` / `context` 使用箇所
Line 119: self -> static float get_value_impl(void* self) {
Line 120: self -> EcoSensor_Data* sensor = (EcoSensor_Data*)self;
Line 237: self -> static float get_value_impl(void* self) {
Line 238: self -> RealTimeSensor_Data* sensor = (RealTimeSensor_Data*)self;
Line 263: self -> float (*get_value)(void* self);
Line 267: self -> void* self;
Line 368: self -> int (*acquire_resource)(void* self);
Line 369: self -> void (*release_resource)(void* self);
Line 373: self -> void* self;
Line 399: self -> static int net_acquire_impl(void* self) {
Line 400: self -> // 【解説】(void)self; は「未使用引数」の警告を抑制するためのC言語のイディオムです。
Line 401: self -> // この例ではモック関数しか呼ばないため self を使いませんが、
Line 403: self -> (void)self;
Line 538: self -> static int net_acquire_impl(void* self) {
Line 539: self -> NetResource_Data* res = (NetResource_Data*)self;
Line 559: self -> static void net_release_impl(void* self) {
Line 560: self -> if (self) free(self);
Line 580: self -> res->self = data; // 内部データ（コンテキスト）の注入
Line 601: self -> int result = res->vtable->acquire_resource(res->self);
Line 618: self -> res->vtable->release_resource(res->self);
Line 657: self -> - **不透明ポインタと不完全型（第4章）** : `void* self` や構造体の前方宣言により、具象の詳細をクライアントから物理的に隔離する。

## 15_第2部 第11章 インターフェース分離原則 (ISP) 不要な依存の排除とモジュール結合度の最小化_01.md
### `self` / `context` 使用箇所
Line 481: self -> int (*read_data)(void* self);
Line 482: self -> int (*write_config)(void* self); // 読み取り専用デバイスには「不要な契約」
Line 483: self -> int (*optimize_db)(void* self);  // 特定のデバイスにしか関係ない契約
Line 494: self -> static int read_only_read_data(void* self) {
Line 499: self -> static int read_only_write_config(void* self) {
Line 582: self -> int (*read_data)(void* self);
Line 595: self -> int (*write_config)(void* self);
Line 608: self -> int (*optimize_db)(void* self);
Line 626: self -> void* self;                     // 具象データへの不透明ポインタ（第4章の応用）
Line 641: self -> static int readonly_read_data(void* self) {
Line 642: self -> // コンパイラの未使用警告を抑制（実務では self を使用してデータを読み込む）
Line 643: self -> (void)self;
Line 678: self -> /* 各VTableの関数に対し、共通の self を渡すことで多態性を実現 */
Line 681: self -> if (device->reader->read_data(device->self) != 0) {
Line 687: self -> if (device->config->write_config(device->self) != 0) {
Line 703: self -> .self = NULL,

## 16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_01.md
### 初出用語
Line 276: SDP -> ### 1.3. 安定依存の原則（SDP: Stable Dependencies Principle）
### `self` / `context` 使用箇所
Line 321: context -> IF["インターフェース構造体<br/>vtable + context"]
Line 330: context -> IF -->|"context*"| CTX
Line 362: self -> bool (*connect)(void* self, const char* conn_str);
Line 363: self -> void (*execute)(void* self, const char* query);
Line 364: self -> void (*disconnect)(void* self);
Line 370: self -> void* self;                    // 実装の詳細（隠蔽された状態）
Line 381: self -> (db)->vtable->connect((db)->self, (str))
Line 383: self -> (db)->vtable->execute((db)->self, (query))
Line 385: self -> (db)->vtable->disconnect((db)->self)
Line 406: self -> そして、契約（VTable）で要求された「接続」「実行」「切断」の具体的な処理を、ファイル内部（`static`）で実装します。ここで `void* self` を元の具象型にキャストして操作するのがお決まりのパターンです。
Line 413: self -> static bool mysql_connect(void* self, const char* conn_str) {
Line 414: self -> MySQLContext* ctx = (MySQLContext*)self;
Line 422: self -> static void mysql_execute(void* self, const char* query) {
Line 424: self -> MySQLContext* ctx = (MySQLContext*)self;
Line 428: self -> static void mysql_disconnect(void* self) {
Line 429: self -> MySQLContext* ctx = (MySQLContext*)self;
Line 466: self -> db->self = ctx;
Line 488: self -> static bool postgres_connect(void* self, const char* conn_str) {
Line 489: self -> PostgresContext* ctx = (PostgresContext*)self;
Line 497: self -> static void postgres_execute(void* self, const char* query) {
Line 502: self -> static void postgres_disconnect(void* self) {
Line 503: self -> PostgresContext* ctx = (PostgresContext*)self;
Line 539: self -> db->self = ctx;
Line 796: self -> typedef int (*ReadTempAction)(void* self);
Line 801: self -> void* self;               // 具象側のデータ
Line 823: self -> static int hw_read_impl(void* self) {
Line 824: self -> HardwareContext* ctx = (HardwareContext*)self;
Line 836: self -> sensor->self = ctx;
Line 854: self -> static int mock_read_impl(void* self) {
Line 855: self -> MockContext* ctx = (MockContext*)self;
Line 866: self -> sensor->self = ctx;
Line 882: self -> if (sensor->self) free(sensor->self);
Line 949: self -> int temp = rep->sensor->read_temp(rep->sensor->self);

## 16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_02.md
### `self` / `context` 使用箇所
Line 125: self -> typedef char* (*TransformFunc)(void* self, const char* data);
Line 129: self -> void* self;
Line 150: self -> static char* aes_impl(void* self, const char* data) {
Line 152: self -> int key_len = self ? *(int*)self : 256;
Line 169: self -> t->self = key_len;
Line 182: self -> static char* zip_impl(void* self, const char* data) {
Line 184: self -> int level = self ? *(int*)self : 6;
Line 201: self -> t->self = level;
Line 211: self -> static char* noop_impl(void* self, const char* data) {
Line 213: self -> const char* prefix = self ? (const char*)self : "";
Line 227: self -> t->self = "NOOP:"; // 特定のプレフィックスを付ける
Line 236: self -> free(t->self);
Line 261: self -> char* result = strategy->transform(strategy->self, data);
Line 484: self -> typedef void (*NotifyAction)(void* self, const char* message);
Line 488: self -> void* self;
Line 506: self -> static void email_notify_impl(void* self, const char* msg) {
Line 513: self -> n->self = NULL;
Line 519: self -> static void sms_notify_impl(void* self, const char* msg) {
Line 526: self -> n->self = NULL;
Line 582: self -> service->notifier->notify(service->notifier->self, "Welcome!");
Line 794: self -> static bool mock_connect(void* self, const char* conn_str) {
Line 795: self -> MockDatabaseContext* ctx = (MockDatabaseContext*)self;
Line 802: self -> static void mock_execute(void* self, const char* query) {
Line 803: self -> MockDatabaseContext* ctx = (MockDatabaseContext*)self;
Line 809: self -> static void mock_disconnect(void* self) {
Line 810: self -> MockDatabaseContext* ctx = (MockDatabaseContext*)self;
Line 841: self -> db->self = ctx;

## 16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_03.md
### `self` / `context` 使用箇所
Line 11: self -> double (*calculate_tax)(void* self, double amount);
Line 15: self -> void* self;
Line 36: self -> return amount + tax->vtable->calculate_tax(tax->self, amount);
Line 44: self -> static double mock_calc(void* self, double amount) {
Line 45: self -> MockTax* m = (MockTax*)self;
Line 55: self -> tax->self = mock;
Line 83: self -> static double japan_tax_calc(void* self, double amount) {
Line 84: self -> (void)self; // 日本の税率は固定（10%）
Line 97: self -> tax->self = NULL;
Line 197: self -> bool (*open)(void* self, const char* path);
Line 198: self -> bool (*write)(void* self, const void* data, size_t size);
Line 199: self -> void (*close)(void* self);

## 17_第2部 第13章 統合実践（基本）_01.md
### `self` / `context` 使用箇所
Line 342: self -> char* (*read)(void* self, const char* path);
Line 344: self -> int (*write)(void* self, const char* path, ProcessedData* data);
Line 346: self -> void (*destroy)(void* self);
Line 351: self -> void* self;  // 具象データへの不透明ポインタ
Line 370: self -> return io->vtable->read(io->self, path);
Line 376: self -> return io->vtable->write(io->self, path, data);
Line 383: self -> io->vtable->destroy(io->self);
Line 403: self -> ProcessedData* (*parse)(void* self, const char* raw_data);
Line 405: self -> void (*free_data)(void* self, ProcessedData* data);
Line 407: self -> void (*destroy)(void* self);
Line 412: self -> void* self;  // 具象データへの不透明ポインタ
Line 432: self -> return parser->vtable->parse(parser->self, raw_data);
Line 439: self -> parser->vtable->free_data(parser->self, data);
Line 450: self -> parser->vtable->destroy(parser->self);
Line 562: self -> static char* file_io_read_impl(void* self, const char* path) {
Line 563: self -> FileIOData* data = (FileIOData*)self;
Line 571: self -> static int file_io_write_impl(void* self, const char* path, ProcessedData* d) {
Line 572: self -> FileIOData* data = (FileIOData*)self;
Line 580: self -> リソースの破棄処理と、これら全ての機能をまとめたVTableの定義です。最後にファクトリ関数（`file_io_create`）の中で、具象データ（`self`）と振る舞い（`vtable`）をガッチリと結合し、外界に対しては抽象的な `IIO` の顔をして送り出します。
Line 586: self -> static void file_io_destroy_impl(void* self) {
Line 587: self -> if (self) {
Line 588: self -> FileIOData* data = (FileIOData*)self;
Line 590: self -> free(self);
Line 618: self -> io->self = file_data;
Line 651: self -> static ProcessedData* json_parser_parse_impl(void* self, const char* raw_data) {
Line 652: self -> JsonParserData* parser_state = (JsonParserData*)self;
Line 674: self -> static void json_parser_free_data_impl(void* self, ProcessedData* data) {
Line 675: self -> JsonParserData* parser_state = (JsonParserData*)self;
Line 684: self -> static void json_parser_destroy_impl(void* self) {
Line 685: self -> if (self) {
Line 686: self -> JsonParserData* parser_state = (JsonParserData*)self;
Line 688: self -> free(self);
Line 712: self -> parser->self = parser_data;

## 17_第2部 第13章 統合実践（基本）_02.md
### `self` / `context` 使用箇所
Line 175: self -> static char* net_read_impl(void* self, const char* path) {
Line 181: self -> static int net_write_impl(void* self, const char* path, ProcessedData* data) {
Line 186: self -> static void net_destroy_impl(void* self) {
Line 200: self -> io->self = NULL; // 今回はコンテキスト不要

## 18_第2部 第14章 統合実践（応用）_01.md
### `self` / `context` 使用箇所
Line 333: self -> char* (*process)(void* self, const char* input_data);
Line 334: self -> void (*destroy)(void* self);
Line 341: self -> static char* name##_impl(void* self, const char* input) { \
Line 342: self -> name##_data_t* data = (name##_data_t*)self; \
Line 351: self -> static void name##_destroy(void* self) { \
Line 352: self -> free(self); /* name##_data_t を解放 */ \
Line 439: self -> char* (*process)(void* self, const char* input_data);
Line 440: self -> void (*destroy)(void* self);
Line 444: self -> void* self;
Line 449: self -> return p->vtable->process(p->self, input_data);
Line 459: self -> p->self = NULL;
Line 467: self -> p->vtable->destroy(p->self);
Line 501: self -> static char* pipeline_process_impl(void* self, const char* input_data) {
Line 502: self -> PipelineProcessorImpl* p = (PipelineProcessorImpl*)self;
Line 533: self -> static void pipeline_destroy_impl(void* self) {
Line 534: self -> if (self) {
Line 535: self -> PipelineProcessorImpl* impl = (PipelineProcessorImpl*)self;
Line 676: self -> static char* filter_impl(void* self, const char* input) {
Line 677: self -> filter_data_t* data = (filter_data_t*)self;
Line 686: self -> static void filter_destroy(void* self) {
Line 687: self -> free(self);
Line 714: self -> static char* compressor_impl(void* self, const char* input) {
Line 715: self -> compressor_data_t* data = (compressor_data_t*)self;
Line 724: self -> static void compressor_destroy(void* self) {
Line 725: self -> free(self);
Line 810: self -> static char* name##_impl(void* self, const char* input) { \
Line 811: self -> name##_data_t* data = (name##_data_t*)self; \
Line 820: self -> static void name##_destroy(void* self) { \
Line 821: self -> free(self); /* name##_data_t を解放 */ \
Line 833: self -> p->self = d; \

## 18_第2部 第14章 統合実践（応用）_02.md
### `self` / `context` 使用箇所
Line 61: self -> char* (*process)(void* self, const char* input_data);
Line 62: self -> void (*destroy)(void* self);
Line 69: self -> static char* name##_impl(void* self, const char* input) { \
Line 70: self -> (void)self; \
Line 76: self -> static void name##_destroy(void* self) { free(self); } \
Line 395: self -> CustomerModule* self = malloc(sizeof(CustomerModule));
Line 397: self -> return self;
Line 400: self -> void customer_save(CustomerModule* self, CustomerData* data) {
Line 533: self -> char* (*encrypt)(void* self, const char* plain_text);
Line 534: self -> void (*free_encrypted)(void* self, char* encrypted);
Line 535: self -> void (*destroy)(void* self);
Line 539: self -> void* self;
Line 552: self -> return engine->vtable->encrypt(engine->self, plain_text);
Line 560: self -> engine->vtable->free_encrypted(engine->self, encrypted);
Line 568: self -> engine->vtable->destroy(engine->self);
Line 594: self -> void customer_save(CustomerModule* self, CustomerData* data);
Line 595: self -> void customer_module_destroy(CustomerModule* self);
Line 615: self -> CustomerModule* self = malloc(sizeof(CustomerModule));
Line 617: self -> if (!self) return NULL;
Line 618: self -> self->crypto = crypto;
Line 620: self -> return self;
Line 623: self -> void customer_save(CustomerModule* self, CustomerData* data) {
Line 624: self -> if (!self || !data) return;
Line 626: self -> char* encrypted = crypto_encrypt(self->crypto, data->credit_card);
Line 631: self -> crypto_free_encrypted(self->crypto, encrypted);
Line 635: self -> void customer_module_destroy(CustomerModule* self) {
Line 636: self -> free(self);
Line 672: self -> static char* aes_encrypt_impl(void* self, const char* plain_text) {
Line 673: self -> AESEngineData* data = (AESEngineData*)self;
Line 690: self -> static void aes_free_impl(void* self, char* encrypted) {
Line 691: self -> (void)self;
Line 696: self -> static void aes_destroy_impl(void* self) {
Line 697: self -> if (self) {
Line 699: self -> free(self); // AESEngineDataの解放
Line 723: self -> engine->self = data;
Line 761: self -> static char* mock_encrypt_impl(void* self, const char* plain_text) {
Line 762: self -> MockCryptoData* data = (MockCryptoData*)self;
Line 771: self -> static void mock_free_impl(void* self, char* encrypted) {
Line 772: self -> (void)self;
Line 776: self -> static void mock_destroy_impl(void* self) {
Line 779: self -> // ここで free(self) を実行してはならない（クラッシュの原因となる）。
Line 781: self -> (void)self;
Line 794: self -> engine->self = shared_data; // 外部データを参照として保持
