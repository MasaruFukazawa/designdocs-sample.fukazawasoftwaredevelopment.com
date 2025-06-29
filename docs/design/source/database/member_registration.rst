会員登録データベース設計
==========================================

概要
--------------------------------------------

ECサイトの会員登録機能に関するデータベース設計。
DDD設計で定義したエンティティと値オブジェクトを基に、実際のテーブル構造を定義する。

関連文書
--------------------------------------------

* :doc:`../user_story/member_registration`
* :doc:`../usecase/member_registration`
* :doc:`../ddd/member_registration`
* :doc:`../domain_model`

データベース概要
--------------------------------------------

**データベース種別**: PostgreSQL 13以降

**文字コード**: UTF8

**タイムゾーン**: Asia/Tokyo

**命名規則**:
- テーブル名: snake_case（複数形）
- カラム名: snake_case（単数形）
- インデックス名: idx_テーブル名_カラム名
- 制約名: 制約種別_テーブル名_カラム名

テーブル設計
--------------------------------------------

members（会員テーブル）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**概要**: 会員の基本情報を管理するメインテーブル

**関連エンティティ**: Member（会員）

.. list-table::
   :header-rows: 1

   * - カラム名
     - データ型
     - NOT NULL
     - デフォルト値
     - 説明
   * - member_id
     - UUID
     - ○
     - gen_random_uuid()
     - 会員ID（主キー）
   * - email_address
     - VARCHAR(254)
     - ○
     - 
     - メールアドレス（一意）
   * - password_hash
     - VARCHAR(255)
     - ○
     - 
     - ハッシュ化されたパスワード
   * - password_salt
     - VARCHAR(32)
     - ○
     - 
     - パスワードソルト
   * - last_name
     - VARCHAR(50)
     - ○
     - 
     - 姓
   * - first_name
     - VARCHAR(50)
     - ○
     - 
     - 名
   * - postal_code
     - CHAR(7)
     - ○
     - 
     - 郵便番号（ハイフンなし7桁）
   * - prefecture
     - VARCHAR(20)
     - ○
     - 
     - 都道府県
   * - city
     - VARCHAR(100)
     - ○
     - 
     - 市区町村
   * - street_address
     - VARCHAR(200)
     - ○
     - 
     - 番地・建物名
   * - phone_number
     - VARCHAR(15)
     - ○
     - 
     - 電話番号（ハイフン付き正規化済み）
   * - status
     - VARCHAR(20)
     - ○
     - 'ACTIVE'
     - 会員ステータス（ACTIVE/INACTIVE/SUSPENDED）
   * - created_at
     - TIMESTAMP WITH TIME ZONE
     - ○
     - CURRENT_TIMESTAMP
     - 作成日時
   * - updated_at
     - TIMESTAMP WITH TIME ZONE
     - ○
     - CURRENT_TIMESTAMP
     - 更新日時

**制約**:

.. code-block:: sql

   -- 主キー制約
   ALTER TABLE members ADD CONSTRAINT pk_members PRIMARY KEY (member_id);
   
   -- 一意制約
   ALTER TABLE members ADD CONSTRAINT uk_members_email_address UNIQUE (email_address);
   
   -- チェック制約
   ALTER TABLE members ADD CONSTRAINT ck_members_status 
   CHECK (status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED'));
   
   ALTER TABLE members ADD CONSTRAINT ck_members_postal_code 
   CHECK (postal_code ~ '^[0-9]{7}$');
   
   ALTER TABLE members ADD CONSTRAINT ck_members_email_format 
   CHECK (email_address ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

**インデックス**:

.. code-block:: sql

   -- メールアドレス検索用（一意制約で自動作成されるが明示）
   CREATE UNIQUE INDEX idx_members_email_address ON members (email_address);
   
   -- ステータス検索用
   CREATE INDEX idx_members_status ON members (status);
   
   -- 作成日時検索用
   CREATE INDEX idx_members_created_at ON members (created_at);
   
   -- 氏名検索用（複合インデックス）
   CREATE INDEX idx_members_name ON members (last_name, first_name);

registration_requests（登録リクエストテーブル）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**概要**: 会員登録リクエストの処理状況を管理するテーブル

**関連エンティティ**: RegistrationRequest（登録リクエスト）

.. list-table::
   :header-rows: 1

   * - カラム名
     - データ型
     - NOT NULL
     - デフォルト値
     - 説明
   * - request_id
     - UUID
     - ○
     - gen_random_uuid()
     - 登録リクエストID（主キー）
   * - email_address
     - VARCHAR(254)
     - ○
     - 
     - 登録試行メールアドレス
   * - request_data
     - JSONB
     - ○
     - 
     - 登録リクエストデータ（JSON形式）
   * - status
     - VARCHAR(20)
     - ○
     - 'PENDING'
     - 処理ステータス（PENDING/COMPLETED/FAILED）
   * - member_id
     - UUID
     - 
     - 
     - 作成された会員ID（成功時のみ）
   * - error_details
     - JSONB
     - 
     - 
     - エラー詳細（失敗時のみ）
   * - submitted_at
     - TIMESTAMP WITH TIME ZONE
     - ○
     - CURRENT_TIMESTAMP
     - 送信日時
   * - completed_at
     - TIMESTAMP WITH TIME ZONE
     - 
     - 
     - 完了日時
   * - expires_at
     - TIMESTAMP WITH TIME ZONE
     - ○
     - CURRENT_TIMESTAMP + interval '24 hours'
     - 有効期限

**制約**:

.. code-block:: sql

   -- 主キー制約
   ALTER TABLE registration_requests ADD CONSTRAINT pk_registration_requests PRIMARY KEY (request_id);
   
   -- 外部キー制約
   ALTER TABLE registration_requests ADD CONSTRAINT fk_registration_requests_member_id 
   FOREIGN KEY (member_id) REFERENCES members (member_id);
   
   -- チェック制約
   ALTER TABLE registration_requests ADD CONSTRAINT ck_registration_requests_status 
   CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED'));
   
   -- 完了時は完了日時が必須
   ALTER TABLE registration_requests ADD CONSTRAINT ck_registration_requests_completed_at 
   CHECK ((status = 'COMPLETED' AND completed_at IS NOT NULL) OR status != 'COMPLETED');

**インデックス**:

.. code-block:: sql

   -- ステータス検索用
   CREATE INDEX idx_registration_requests_status ON registration_requests (status);
   
   -- メールアドレス検索用
   CREATE INDEX idx_registration_requests_email ON registration_requests (email_address);
   
   -- 有効期限検索用（期限切れデータのクリーンアップ用）
   CREATE INDEX idx_registration_requests_expires_at ON registration_requests (expires_at);
   
   -- 送信日時検索用
   CREATE INDEX idx_registration_requests_submitted_at ON registration_requests (submitted_at);

member_events（会員イベントテーブル）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**概要**: 会員関連のドメインイベントを記録するテーブル

**関連概念**: ドメインイベント（MemberRegistered、MemberRegistrationFailed）

.. list-table::
   :header-rows: 1

   * - カラム名
     - データ型
     - NOT NULL
     - デフォルト値
     - 説明
   * - event_id
     - UUID
     - ○
     - gen_random_uuid()
     - イベントID（主キー）
   * - event_type
     - VARCHAR(100)
     - ○
     - 
     - イベント種別
   * - member_id
     - UUID
     - 
     - 
     - 会員ID（存在する場合）
   * - email_address
     - VARCHAR(254)
     - ○
     - 
     - 対象メールアドレス
   * - event_data
     - JSONB
     - ○
     - 
     - イベントデータ（JSON形式）
   * - occurred_at
     - TIMESTAMP WITH TIME ZONE
     - ○
     - CURRENT_TIMESTAMP
     - 発生日時
   * - processed_at
     - TIMESTAMP WITH TIME ZONE
     - 
     - 
     - 処理完了日時

**制約**:

.. code-block:: sql

   -- 主キー制約
   ALTER TABLE member_events ADD CONSTRAINT pk_member_events PRIMARY KEY (event_id);
   
   -- 外部キー制約（NULL許可）
   ALTER TABLE member_events ADD CONSTRAINT fk_member_events_member_id 
   FOREIGN KEY (member_id) REFERENCES members (member_id);
   
   -- チェック制約
   ALTER TABLE member_events ADD CONSTRAINT ck_member_events_event_type 
   CHECK (event_type IN ('MemberRegistered', 'MemberRegistrationFailed', 'MemberUpdated', 'MemberDeactivated'));

**インデックス**:

.. code-block:: sql

   -- イベント種別検索用
   CREATE INDEX idx_member_events_event_type ON member_events (event_type);
   
   -- 会員ID検索用
   CREATE INDEX idx_member_events_member_id ON member_events (member_id);
   
   -- 発生日時検索用
   CREATE INDEX idx_member_events_occurred_at ON member_events (occurred_at);
   
   -- 未処理イベント検索用
   CREATE INDEX idx_member_events_unprocessed ON member_events (processed_at) WHERE processed_at IS NULL;

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
       
       registration_requests {
           uuid request_id PK
           varchar email_address
           jsonb request_data
           varchar status
           uuid member_id FK
           jsonb error_details
           timestamp submitted_at
           timestamp completed_at
           timestamp expires_at
       }
       
       member_events {
           uuid event_id PK
           varchar event_type
           uuid member_id FK
           varchar email_address
           jsonb event_data
           timestamp occurred_at
           timestamp processed_at
       }
       
       members ||--o{ registration_requests : "creates"
       members ||--o{ member_events : "generates"

初期データ設定
--------------------------------------------

**都道府県マスタ（prefecture_master）**:

.. code-block:: sql

   -- 都道府県マスタテーブル（参考）
   CREATE TABLE prefecture_master (
       prefecture_code CHAR(2) PRIMARY KEY,
       prefecture_name VARCHAR(20) NOT NULL,
       region VARCHAR(20) NOT NULL
   );
   
   -- 都道府県データ挿入
   INSERT INTO prefecture_master VALUES
       ('01', '北海道', '北海道'),
       ('02', '青森県', '東北'),
       ('03', '岩手県', '東北'),
       -- ... 47都道府県すべて

データメンテナンス
--------------------------------------------

**期限切れデータの削除**:

.. code-block:: sql

   -- 期限切れの登録リクエスト削除（日次バッチ）
   DELETE FROM registration_requests 
   WHERE expires_at < CURRENT_TIMESTAMP - interval '7 days'
   AND status IN ('FAILED', 'COMPLETED');

**統計情報の更新**:

.. code-block:: sql

   -- 統計情報更新（週次メンテナンス）
   ANALYZE members;
   ANALYZE registration_requests;
   ANALYZE member_events;

パフォーマンス考慮事項
--------------------------------------------

**パーティショニング**:
- member_eventsテーブルは日付でパーティション分割を検討
- 大量のイベントデータが蓄積される場合に有効

**レプリケーション**:
- 読み取り専用のレプリカDBの活用
- 統計・分析クエリの負荷分散

**キャッシュ戦略**:
- 会員情報の頻繁な読み取りにはRedisキャッシュを活用
- セッション情報もキャッシュで管理

セキュリティ考慮事項
--------------------------------------------

**データ暗号化**:
- password_hashは必ずbcryptでハッシュ化
- 個人情報のTDE（Transparent Data Encryption）適用

**アクセス制御**:
- アプリケーション専用DBユーザーの作成
- 最小権限の原則に基づく権限設定
- 本番環境での直接アクセス制限

**監査ログ**:
- 個人情報へのアクセスログ記録
- データ変更履歴の保持

バックアップ・リカバリ
--------------------------------------------

**バックアップ戦略**:
- 日次フルバックアップ
- 時間ごとの差分バックアップ
- WALアーカイブによるポイントインタイムリカバリ

**リカバリテスト**:
- 月次でのリカバリテスト実施
- RTO/RPO要件の確認

運用監視
--------------------------------------------

**監視項目**:
- 会員登録成功/失敗率
- 登録リクエスト処理時間
- データベース接続数
- ディスク使用率

**アラート設定**:
- 登録失敗率が閾値を超えた場合
- データベース接続エラーが連続した場合
- ディスク使用率が80%を超えた場合 