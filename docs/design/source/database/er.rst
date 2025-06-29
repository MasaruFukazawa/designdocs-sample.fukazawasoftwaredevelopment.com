データベース全体ER図
============================================

概要
--------------------------------------------

このページでは、システム全体のデータベース構造をER図で表現し、テーブル間の関係性を明確に示します。

**設計方針**:

- PostgreSQL 13以降での実装を想定
- UUID主キーによる一意性保証
- 外部キー制約による参照整合性の確保
- 正規化による重複データの排除
- インデックス最適化によるパフォーマンス向上

**対象システム**: ECサイト会員管理システム

**最終更新**: 2024年（会員登録機能実装時）

全体ER図
--------------------------------------------

.. mermaid::

   %%{init: {"theme": "default"}}%%
   erDiagram
       members {
           UUID id PK "会員ID"
           VARCHAR email "メールアドレス（一意）"
           VARCHAR password_hash "パスワードハッシュ"
           VARCHAR last_name "姓"
           VARCHAR first_name "名"
           VARCHAR last_name_kana "姓（カナ）"
           VARCHAR first_name_kana "名（カナ）"
           DATE birth_date "生年月日"
           VARCHAR gender "性別"
           VARCHAR postal_code "郵便番号"
           VARCHAR prefecture "都道府県"
           VARCHAR city "市区町村"
           VARCHAR address_line "住所詳細"
           VARCHAR phone_number "電話番号"
           VARCHAR status "会員ステータス"
           TIMESTAMP created_at "作成日時"
           TIMESTAMP updated_at "更新日時"
       }
       
       registration_requests {
           UUID id PK "登録リクエストID"
           JSONB request_data "登録データ（JSON）"
           VARCHAR status "ステータス"
           TIMESTAMP expires_at "有効期限"
           TIMESTAMP created_at "作成日時"
           TIMESTAMP updated_at "更新日時"
       }
       
       member_events {
           UUID id PK "イベントID"
           UUID member_id FK "会員ID"
           VARCHAR event_type "イベント種別"
           JSONB event_data "イベントデータ（JSON）"
           TIMESTAMP occurred_at "発生日時"
           TIMESTAMP created_at "作成日時"
       }
       
       %% リレーション定義
       members ||--o{ member_events : "1人の会員が複数のイベントを持つ"
       
       %% 将来拡張用のテーブル（コメントアウト状態）
       %% products {
       %%     UUID id PK "商品ID"
       %%     VARCHAR name "商品名"
       %%     TEXT description "商品説明"  
       %%     INTEGER price "価格"
       %%     INTEGER stock_quantity "在庫数"
       %%     VARCHAR status "商品ステータス"
       %%     TIMESTAMP created_at "作成日時"
       %%     TIMESTAMP updated_at "更新日時"
       %% }
       %%
       %% orders {
       %%     UUID id PK "注文ID"
       %%     UUID member_id FK "会員ID"
       %%     INTEGER total_amount "総額"
       %%     VARCHAR status "注文ステータス"
       %%     TIMESTAMP ordered_at "注文日時"
       %%     TIMESTAMP created_at "作成日時"
       %%     TIMESTAMP updated_at "更新日時"
       %% }
       %%
       %% order_items {
       %%     UUID id PK "注文明細ID"
       %%     UUID order_id FK "注文ID"
       %%     UUID product_id FK "商品ID"
       %%     INTEGER quantity "数量"
       %%     INTEGER unit_price "単価"
       %%     INTEGER subtotal "小計"
       %%     TIMESTAMP created_at "作成日時"
       %% }
       %%
       %% 将来のリレーション
       %% members ||--o{ orders : "1人の会員が複数の注文を持つ"
       %% orders ||--o{ order_items : "1つの注文が複数の注文明細を持つ"
       %% products ||--o{ order_items : "1つの商品が複数の注文明細で使用される"

テーブル一覧
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - テーブル名
     - 論理名
     - 主要用途
     - 詳細設計書
   * - members
     - 会員
     - 会員基本情報の管理
     - :doc:`member_registration`
   * - registration_requests
     - 登録リクエスト
     - 会員登録プロセスの管理
     - :doc:`member_registration`
   * - member_events
     - 会員イベント
     - ドメインイベントの記録
     - :doc:`member_registration`

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
   * - members
     - member_events
     - 会員とイベントの関係
     - member_events.member_id
     - 1:多（1人の会員が複数のイベントを持つ）

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

**独立テーブル**:

.. list-table::
   :header-rows: 1

   * - テーブル名
     - 説明
     - 関連性
   * - registration_requests
     - 登録リクエスト管理
     - 会員登録プロセスで使用、完了後は参照のみ

データベース制約サマリー
--------------------------------------------

**一意制約**:

- `members.email`: メールアドレスの重複禁止
- `members.id`: 会員IDの一意性（主キー）
- `registration_requests.id`: 登録リクエストIDの一意性（主キー）  
- `member_events.id`: イベントIDの一意性（主キー）

**外部キー制約**:

- `member_events.member_id` → `members.id`: 会員イベントは必ず会員に紐づく

**チェック制約**:

- `members.status`: 'active', 'inactive', 'suspended' のみ許可
- `members.gender`: 'male', 'female', 'other', 'not_specified' のみ許可
- `registration_requests.status`: 'pending', 'completed', 'expired', 'failed' のみ許可
- `member_events.event_type`: 'registered', 'updated', 'deleted' など定義済み値のみ許可

インデックス戦略
--------------------------------------------

**高頻度検索用インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 対象テーブル
     - 対象カラム
     - 用途
   * - idx_members_email
     - members
     - email
     - ログイン認証での高速検索
   * - idx_members_status
     - members
     - status
     - アクティブ会員の絞り込み
   * - idx_member_events_member_id
     - member_events
     - member_id
     - 会員別イベント履歴の取得
   * - idx_member_events_occurred_at
     - member_events
     - occurred_at
     - 時系列でのイベント検索

**複合インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 対象テーブル
     - 対象カラム
     - 用途
   * - idx_members_status_created_at
     - members
     - status, created_at
     - ステータス別の登録日順ソート
   * - idx_member_events_type_occurred
     - member_events
     - event_type, occurred_at
     - イベント種別での時系列検索

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

ER図更新ルール
--------------------------------------------

**新機能追加時の手順**:

1. **ER図の更新**: 新しいテーブル追加時は必ずこのページのER図を更新
2. **詳細設計書作成**: 個別テーブルの詳細設計書も同時に作成
3. **リレーション検証**: 既存テーブルとの関係性を慎重に検討し、データ整合性を確保
4. **インデックス最適化**: 新しいアクセスパターンに合わせてインデックス戦略を見直し
5. **制約の追加**: 必要に応じて新しいチェック制約や外部キー制約を追加

**コメントアウト運用**:

- 将来実装予定のテーブルは、ER図内でコメントアウト（%%）して記載
- 実装時にコメントアウトを解除し、実際のリレーションを定義
- 設計変更があった場合は、コメントアウト部分も更新

**テンプレート構造**:

新しいテーブル追加時のMermaid構文例：

.. code-block:: text

   new_table_name {
       UUID id PK "主キーの説明"
       UUID foreign_id FK "外部キーの説明"
       VARCHAR column_name "カラムの説明"
       INTEGER numeric_column "数値カラムの説明"
       TIMESTAMP created_at "作成日時"
       TIMESTAMP updated_at "更新日時"
   }
   
   %% リレーション定義例
   parent_table ||--o{ new_table_name : "リレーションの説明"

管理情報
--------------------------------------------

**作成履歴**:

- 2024年: 会員登録機能実装に伴う初期設計
- 今後: 機能追加に伴う段階的拡張予定

**レビュー要件**:

- **新機能追加時**: データベース設計の全体整合性確認必須
- **四半期ごと**: パフォーマンス監視結果に基づく最適化検討
- **年次**: セキュリティ要件の見直しとアップデート
- **重要変更時**: アーキテクチャレビューの実施

**品質基準**:

- すべてのテーブルに created_at, updated_at カラムを必須とする
- UUID主キーによる一意性保証を標準とする
- 外部キー制約による参照整合性を必ず設定する
- 適切なインデックス設計によるパフォーマンス確保

**関連ドキュメント**:

- :doc:`../ddd/member_registration`: 会員登録ドメイン設計
- :doc:`../usecase/member_registration`: 会員登録ユースケース
- :doc:`member_registration`: 会員登録テーブル詳細設計
- :doc:`template`: データベーステーブル設計テンプレート
