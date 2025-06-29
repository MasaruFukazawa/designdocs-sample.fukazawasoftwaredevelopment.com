members
============================================

概要
--------------------------------------------

**テーブル目的**: 会員の基本情報を管理するメインテーブル

**設計方針**: 会員情報の正規化、個人情報保護重視

**想定レコード数**: 初期10万件、年間成長率30%

**データベース**: PostgreSQL 13以降

**関連集約**: Member（会員）

関連文書
--------------------------------------------

* :doc:`../user_story/member_registration`
* :doc:`../usecase/member_registration`
* :doc:`../ddd/member_registration`
* :doc:`er`

テーブル定義
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - カラム名
     - 論理名
     - データ型
     - NULL/NOT NULL
     - デフォルト値
     - 説明
   * - member_id
     - 会員ID
     - UUID
     - NOT NULL
     - gen_random_uuid()
     - 会員ID（主キー）
   * - email_address
     - メールアドレス
     - VARCHAR(254)
     - NOT NULL
     - 
     - メールアドレス（一意）
   * - password_hash
     - パスワードハッシュ
     - VARCHAR(255)
     - NOT NULL
     - 
     - ハッシュ化されたパスワード
   * - password_salt
     - パスワードソルト
     - VARCHAR(32)
     - NOT NULL
     - 
     - パスワードソルト
   * - last_name
     - 姓
     - VARCHAR(50)
     - NOT NULL
     - 
     - 姓
   * - first_name
     - 名
     - VARCHAR(50)
     - NOT NULL
     - 
     - 名
   * - postal_code
     - 郵便番号
     - CHAR(7)
     - NOT NULL
     - 
     - 郵便番号（ハイフンなし7桁）
   * - prefecture
     - 都道府県
     - VARCHAR(20)
     - NOT NULL
     - 
     - 都道府県
   * - city
     - 市区町村
     - VARCHAR(100)
     - NOT NULL
     - 
     - 市区町村
   * - street_address
     - 番地・建物名
     - VARCHAR(200)
     - NOT NULL
     - 
     - 番地・建物名
   * - phone_number
     - 電話番号
     - VARCHAR(15)
     - NOT NULL
     - 
     - 電話番号（ハイフン付き正規化済み）
   * - status
     - 会員ステータス
     - VARCHAR(20)
     - NOT NULL
     - 'ACTIVE'
     - 会員ステータス（ACTIVE/INACTIVE/SUSPENDED）
   * - created_at
     - 作成日時
     - TIMESTAMP WITH TIME ZONE
     - NOT NULL
     - CURRENT_TIMESTAMP
     - 作成日時
   * - updated_at
     - 更新日時
     - TIMESTAMP WITH TIME ZONE
     - NOT NULL
     - CURRENT_TIMESTAMP
     - 更新日時

制約定義
--------------------------------------------

**主キー制約**:

- **制約名**: pk_members
- **対象カラム**: member_id
- **説明**: 会員IDによる一意識別

**外部キー制約**:

- なし

**一意制約**:

.. list-table::
   :header-rows: 1

   * - 制約名
     - 対象カラム
     - 説明
   * - uk_members_email_address
     - email_address
     - メールアドレスの重複禁止

**チェック制約**:

.. list-table::
   :header-rows: 1

   * - 制約名
     - 条件式
     - 説明
   * - ck_members_status
     - status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED')
     - 会員ステータスの値制限
   * - ck_members_postal_code
     - postal_code ~ '^[0-9]{7}$'
     - 郵便番号の形式チェック（7桁数字）
   * - ck_members_email_format
     - email_address ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
     - メールアドレスの形式チェック

インデックス定義
--------------------------------------------

**パフォーマンス用インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 種類
     - 対象カラム
     - 用途
   * - idx_members_email_address
     - UNIQUE B-tree
     - email_address
     - ログイン時の検索高速化
   * - idx_members_status
     - B-tree
     - status
     - ステータス別検索の高速化
   * - idx_members_created_at
     - B-tree
     - created_at
     - 新規会員レポート用
   * - idx_members_name
     - B-tree
     - last_name, first_name
     - 氏名検索の高速化

SQL定義
--------------------------------------------

**テーブル作成**:

.. code-block:: sql

   -- membersテーブル作成（制約含む）
   CREATE TABLE members (
       member_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       email_address VARCHAR(254) NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       password_salt VARCHAR(32) NOT NULL,
       last_name VARCHAR(50) NOT NULL,
       first_name VARCHAR(50) NOT NULL,
       postal_code CHAR(7) NOT NULL,
       prefecture VARCHAR(20) NOT NULL,
       city VARCHAR(100) NOT NULL,
       street_address VARCHAR(200) NOT NULL,
       phone_number VARCHAR(15) NOT NULL,
       status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
       created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
   );

**制約追加**:

.. code-block:: sql

   -- 一意制約
   ALTER TABLE members ADD CONSTRAINT uk_members_email_address 
   UNIQUE (email_address);
   
   -- チェック制約
   ALTER TABLE members ADD CONSTRAINT ck_members_status 
   CHECK (status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED'));
   
   ALTER TABLE members ADD CONSTRAINT ck_members_postal_code 
   CHECK (postal_code ~ '^[0-9]{7}$');
   
   ALTER TABLE members ADD CONSTRAINT ck_members_email_format 
   CHECK (email_address ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

**インデックス作成**:

.. code-block:: sql

   -- メールアドレス検索用（一意制約で自動作成されるが明示）
   CREATE UNIQUE INDEX idx_members_email_address ON members (email_address);
   
   -- ステータス検索用
   CREATE INDEX idx_members_status ON members (status);
   
   -- 作成日時検索用
   CREATE INDEX idx_members_created_at ON members (created_at);
   
   -- 氏名検索用（複合インデックス）
   CREATE INDEX idx_members_name ON members (last_name, first_name);

**更新日時自動更新トリガー**:

.. code-block:: sql

   -- updated_at自動更新関数
   CREATE OR REPLACE FUNCTION update_updated_at_column()
   RETURNS TRIGGER AS $$
   BEGIN
       NEW.updated_at = CURRENT_TIMESTAMP;
       RETURN NEW;
   END;
   $$ LANGUAGE plpgsql;
   
   -- トリガー作成
   CREATE TRIGGER trigger_members_updated_at
       BEFORE UPDATE ON members
       FOR EACH ROW
       EXECUTE FUNCTION update_updated_at_column();

ER図
--------------------------------------------

.. mermaid::

   %%{init: {"theme": "default"}}%%
   erDiagram
       members {
           uuid member_id PK
           varchar email_address UK
           varchar password_hash
           varchar password_salt
           varchar last_name
           varchar first_name
           char postal_code
           varchar prefecture
           varchar city
           varchar street_address
           varchar phone_number
           varchar status
           timestamp created_at
           timestamp updated_at
       }

パフォーマンス考慮事項
--------------------------------------------

**クエリ最適化**:
- email_addressによる検索が最も頻繁なため、一意インデックスを活用
- 氏名検索は複合インデックスで対応
- ステータス別での絞り込みが多いため、専用インデックスを作成

**パーティショニング**:
- 現在は単一テーブルで運用
- 将来的にレコード数が100万件を超える場合、created_atでの範囲パーティション分割を検討

セキュリティ考慮事項
--------------------------------------------

**データ暗号化**:
- password_hashは必ずbcryptでハッシュ化（ソルト付き）
- 個人情報（氏名、住所、電話番号）はTDE適用検討

**アクセス制御**:
- アプリケーション専用DBユーザーでのみアクセス
- 直接的なSELECT権限は最小限に制限
- 本番環境での個人情報アクセス監査ログ必須

**データマスキング**:
- 開発環境では個人情報のマスキング実施
- テスト環境でのダミーデータ使用

運用監視
--------------------------------------------

**監視項目**:
- 新規登録数（日次・週次・月次）
- アクティブ会員数の推移
- パスワード変更頻度
- 異常なアクセスパターンの検知

**アラート設定**:
- 新規登録数が通常の50%以下になった場合
- 同一IPからの大量登録試行
- パスワード変更失敗の連続発生

関連テーブル
--------------------------------------------

**参照されるテーブル**:
- :doc:`registration_requests`: 会員登録プロセスでの参照
- :doc:`member_events`: イベント記録での参照

**将来実装予定**:
- orders（注文テーブル）
- shopping_carts（ショッピングカートテーブル）
- reviews（レビューテーブル） 