データベース全体ER図
============================================

**最終更新**: [ 更新日を記載 ]

概要
--------------------------------------------

このページでは、システム全体のデータベース構造をER図で表現し、テーブル間の関係性を明確に示します。


全体ER図
--------------------------------------------

.. mermaid::

   erDiagram
       %% サンプルECサイトのデータベース設計
       members {
           UUID id PK "会員ID"
           VARCHAR email UK "メールアドレス"
           VARCHAR password "パスワード（ハッシュ化）"
           VARCHAR name "会員名"
           VARCHAR phone "電話番号"
           VARCHAR status "会員ステータス"
           TIMESTAMP created_at "作成日時"
           TIMESTAMP updated_at "更新日時"
       }
       
       products {
           UUID id PK "商品ID"
           VARCHAR name "商品名"
           TEXT description "商品説明"  
           INTEGER price "価格"
           INTEGER stock_quantity "在庫数"
           VARCHAR status "商品ステータス"
           TIMESTAMP created_at "作成日時"
           TIMESTAMP updated_at "更新日時"
       }

       orders {
           UUID id PK "注文ID"
           UUID member_id FK "会員ID"
           INTEGER total_amount "総額"
           VARCHAR status "注文ステータス"
           TIMESTAMP ordered_at "注文日時"
           TIMESTAMP created_at "作成日時"
           TIMESTAMP updated_at "更新日時"
       }

       order_items {
           UUID id PK "注文明細ID"
           UUID order_id FK "注文ID"
           UUID product_id FK "商品ID"
           INTEGER quantity "数量"
           INTEGER unit_price "単価"
           INTEGER subtotal "小計"
           TIMESTAMP created_at "作成日時"
       }

       %% リレーション定義
       members ||--o{ orders : "1人の会員が複数の注文を持つ"
       orders ||--o{ order_items : "1つの注文が複数の注文明細を持つ"
       products ||--o{ order_items : "1つの商品が複数の注文明細で使用される"


テーブル一覧
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - テーブル名
     - 論理名
     - 主要用途
     - 詳細設計書
   * - [ テーブル名 ]
     - [ 論理名 ]
     - [ 用途説明 ]
     - :doc:`[ ファイル名 ]`

**将来追加予定のテーブル**:

.. list-table::
   :header-rows: 1

   * - テーブル名
     - 論理名
     - 主要用途
     - 実装予定
   * - products
     - 商品
     - 商品マスタ情報の管理
     - フェーズ2
   * - orders
     - 注文
     - 注文情報の管理
     - フェーズ2  
   * - order_items
     - 注文明細
     - 注文商品詳細の管理
     - フェーズ2

主要リレーションシップ
--------------------------------------------

**現在実装済み**:

.. list-table::
   :header-rows: 1

   * - 親テーブル
     - 子テーブル
     - 関係性
     - 外部キー
     - カーディナリティ
   * - [ 親テーブル名 ]
     - [ 子テーブル名 ]
     - [ 関係性の説明 ]
     - [ 外部キー名 ]
     - [ カーディナリティ ]

**将来実装予定**:

.. list-table::
   :header-rows: 1

   * - 親テーブル
     - 子テーブル
     - 関係性
     - 外部キー
     - カーディナリティ
   * - members
     - orders
     - 会員と注文の関係
     - orders.member_id
     - 1:多（1人の会員が複数の注文を持つ）
   * - orders
     - order_items
     - 注文と注文明細の関係
     - order_items.order_id
     - 1:多（1つの注文が複数の明細を持つ）
   * - products
     - order_items
     - 商品と注文明細の関係
     - order_items.product_id
     - 1:多（1つの商品が複数の明細で使用）

データベース制約サマリー
--------------------------------------------

**一意制約**:

- [ テーブル名.カラム名 ]: [ 制約の説明 ]

**外部キー制約**:

- [ 子テーブル.外部キー ] → [ 親テーブル.主キー ]: [ 制約の説明 ]

**チェック制約**:

- [ テーブル名.カラム名 ]: [ 許可される値の説明 ]

インデックス戦略
--------------------------------------------

**高頻度検索用インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 対象テーブル
     - 対象カラム
     - 用途
   * - [ インデックス名 ]
     - [ テーブル名 ]
     - [ カラム名 ]
     - [ 用途説明 ]

**複合インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 対象テーブル
     - 対象カラム
     - 用途
   * - [ インデックス名 ]
     - [ テーブル名 ]
     - [ カラム名, カラム名 ]
     - [ 用途説明 ]

拡張予定
--------------------------------------------

**フェーズ2（商品・注文機能）**:

- **商品テーブル**: 商品マスタ情報の管理
- **注文テーブル**: 注文情報の管理  
- **注文明細テーブル**: 注文商品詳細の管理
- **カート機能**: 一時的な商品保持

**フェーズ3（決済・配送機能）**:

- **決済テーブル**: 決済履歴の管理
- **配送テーブル**: 配送状況管理
- **配送先テーブル**: 複数配送先の管理

**フェーズ4（拡張機能）**:

- **レビューテーブル**: 商品レビュー機能
- **ポイントテーブル**: ポイント制度
- **クーポンテーブル**: 割引クーポン機能
- **お気に入りテーブル**: ウィッシュリスト機能

関連ドキュメント
--------------------------------------------

- :doc:`template`: データベーステーブル設計テンプレート
