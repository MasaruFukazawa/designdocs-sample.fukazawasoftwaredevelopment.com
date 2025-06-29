registration_requests
============================================

概要
--------------------------------------------

**テーブル目的**: 会員登録リクエストの処理状況を管理するテーブル

**設計方針**: 登録プロセスの状態管理、一時データ保存、期限切れ自動削除

**想定レコード数**: 日次1000件、7日間保持（約7000件）

**データベース**: PostgreSQL 13以降

**関連集約**: RegistrationRequest（登録リクエスト）

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
   * - request_id
     - 登録リクエストID
     - UUID
     - NOT NULL
     - gen_random_uuid()
     - 登録リクエストID（主キー）
   * - email_address
     - メールアドレス
     - VARCHAR(254)
     - NOT NULL
     - 
     - 登録試行メールアドレス
   * - request_data
     - 登録リクエストデータ
     - JSONB
     - NOT NULL
     - 
     - 登録リクエストデータ（JSON形式）
   * - status
     - 処理ステータス
     - VARCHAR(20)
     - NOT NULL
     - 'PENDING'
     - 処理ステータス（PENDING/COMPLETED/FAILED）
   * - member_id
     - 会員ID
     - UUID
     - NULL
     - 
     - 作成された会員ID（成功時のみ）
   * - error_details
     - エラー詳細
     - JSONB
     - NULL
     - 
     - エラー詳細（失敗時のみ）
   * - submitted_at
     - 送信日時
     - TIMESTAMP WITH TIME ZONE
     - NOT NULL
     - CURRENT_TIMESTAMP
     - 送信日時
   * - completed_at
     - 完了日時
     - TIMESTAMP WITH TIME ZONE
     - NULL
     - 
     - 完了日時
   * - expires_at
     - 有効期限
     - TIMESTAMP WITH TIME ZONE
     - NOT NULL
     - CURRENT_TIMESTAMP + interval '24 hours'
     - 有効期限

制約定義
--------------------------------------------

**主キー制約**:

- **制約名**: pk_registration_requests
- **対象カラム**: request_id
- **説明**: 登録リクエストIDによる一意識別

**外部キー制約**:

.. list-table::
   :header-rows: 1

   * - 制約名
     - カラム名
     - 参照テーブル
     - 参照カラム
     - ON DELETE
     - ON UPDATE
   * - fk_registration_requests_member_id
     - member_id
     - members
     - member_id
     - SET NULL
     - CASCADE

**一意制約**:

- なし

**チェック制約**:

.. list-table::
   :header-rows: 1

   * - 制約名
     - 条件式
     - 説明
   * - ck_registration_requests_status
     - status IN ('PENDING', 'COMPLETED', 'FAILED')
     - 処理ステータスの値制限
   * - ck_registration_requests_completed_at
     - (status = 'COMPLETED' AND completed_at IS NOT NULL) OR status != 'COMPLETED'
     - 完了時は完了日時が必須

インデックス定義
--------------------------------------------

**パフォーマンス用インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 種類
     - 対象カラム
     - 用途
   * - idx_registration_requests_status
     - B-tree
     - status
     - ステータス別検索の高速化
   * - idx_registration_requests_email
     - B-tree
     - email_address
     - メールアドレス別検索の高速化
   * - idx_registration_requests_expires_at
     - B-tree
     - expires_at
     - 期限切れデータクリーンアップ用
   * - idx_registration_requests_submitted_at
     - B-tree
     - submitted_at
     - 送信日時での検索・レポート用

SQL定義
--------------------------------------------

**テーブル作成**:

.. code-block:: sql

   -- registration_requestsテーブル作成（制約含む）
   CREATE TABLE registration_requests (
       request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       email_address VARCHAR(254) NOT NULL,
       request_data JSONB NOT NULL,
       status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
       member_id UUID,
       error_details JSONB,
       submitted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
       completed_at TIMESTAMP WITH TIME ZONE,
       expires_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP + interval '24 hours'
   );

**制約追加**:

.. code-block:: sql

   -- 外部キー制約
   ALTER TABLE registration_requests ADD CONSTRAINT fk_registration_requests_member_id 
   FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE SET NULL ON UPDATE CASCADE;
   
   -- チェック制約
   ALTER TABLE registration_requests ADD CONSTRAINT ck_registration_requests_status 
   CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED'));
   
   -- 完了時は完了日時が必須
   ALTER TABLE registration_requests ADD CONSTRAINT ck_registration_requests_completed_at 
   CHECK ((status = 'COMPLETED' AND completed_at IS NOT NULL) OR status != 'COMPLETED');

**インデックス作成**:

.. code-block:: sql

   -- ステータス検索用
   CREATE INDEX idx_registration_requests_status ON registration_requests (status);
   
   -- メールアドレス検索用
   CREATE INDEX idx_registration_requests_email ON registration_requests (email_address);
   
   -- 有効期限検索用（期限切れデータのクリーンアップ用）
   CREATE INDEX idx_registration_requests_expires_at ON registration_requests (expires_at);
   
   -- 送信日時検索用
   CREATE INDEX idx_registration_requests_submitted_at ON registration_requests (submitted_at);

ER図
--------------------------------------------

.. mermaid::

   %%{init: {"theme": "default"}}%%
   erDiagram
       members {
           uuid member_id PK
           varchar email_address UK
           varchar status
           timestamp created_at
           timestamp updated_at
       }
       
       registration_requests {
           uuid request_id PK
           varchar email_address
           jsonb request_data
           varchar status
           uuid member_id FK "NULL許可"
           jsonb error_details "NULL許可"
           timestamp submitted_at
           timestamp completed_at "NULL許可"
           timestamp expires_at
       }
       
       members ||--o{ registration_requests : "creates"

JSONデータ構造
--------------------------------------------

**request_data の構造例**:

.. code-block:: json

   {
       "email": "user@example.com",
       "password": "hashed_password_here",
       "personalInfo": {
           "lastName": "山田",
           "firstName": "太郎",
           "postalCode": "1000001",
           "prefecture": "東京都",
           "city": "千代田区",
           "streetAddress": "千代田1-1-1"
       },
       "phoneNumber": "03-1234-5678",
       "agreementVersion": "v1.0.0",
       "registrationSource": "web"
   }

**error_details の構造例**:

.. code-block:: json

   {
       "errorCode": "VALIDATION_ERROR",
       "message": "Invalid postal code format",
       "details": {
           "field": "postalCode",
           "value": "123-456",
           "expectedFormat": "1234567"
       },
       "timestamp": "2024-01-15T10:30:00Z"
   }

データメンテナンス
--------------------------------------------

**期限切れデータ削除バッチ**:

.. code-block:: sql

   -- 期限切れの登録リクエスト削除（日次バッチ）
   DELETE FROM registration_requests 
   WHERE expires_at < CURRENT_TIMESTAMP - interval '7 days'
   AND status IN ('FAILED', 'COMPLETED');

**統計情報の更新**:

.. code-block:: sql

   -- 統計情報更新（週次メンテナンス）
   ANALYZE registration_requests;

**デバッグ用クエリ**:

.. code-block:: sql

   -- 未処理リクエストの確認
   SELECT request_id, email_address, status, submitted_at, expires_at
   FROM registration_requests 
   WHERE status = 'PENDING' 
   AND expires_at > CURRENT_TIMESTAMP
   ORDER BY submitted_at;
   
   -- エラー頻度の確認
   SELECT DATE(submitted_at) as date, 
          COUNT(*) as total_requests,
          SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed_requests,
          ROUND(SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as failure_rate
   FROM registration_requests 
   WHERE submitted_at >= CURRENT_DATE - interval '30 days'
   GROUP BY DATE(submitted_at)
   ORDER BY date DESC;

パフォーマンス考慮事項
--------------------------------------------

**クエリ最適化**:
- statusとexpires_atによる複合検索が多いため、適切なインデックス配置
- email_addressでの重複チェックが頻繁なため、専用インデックス
- JSONデータの検索にはGINインデックスの検討

**データ保持戦略**:
- 期限切れデータは7日間保持後に自動削除
- 成功データは統計目的で短期間保持
- 失敗データは分析のため1ヶ月保持

**パーティショニング**:
- submitted_atでの日次パーティション分割を検討
- 古いパーティションの自動ドロップで運用効率化

セキュリティ考慮事項
--------------------------------------------

**データ暗号化**:
- request_dataの個人情報は保存時暗号化
- error_detailsには個人情報を含めない設計

**アクセス制御**:
- アプリケーション専用権限での最小アクセス
- 本番環境でのデバッグクエリ実行制限

**データ保護**:
- 期限切れデータの確実な削除
- ログ出力時の個人情報マスキング

運用監視
--------------------------------------------

**監視項目**:
- 登録成功率（時間別・日別）
- 未処理リクエスト数
- 平均処理時間
- エラー発生パターン

**アラート設定**:
- 登録成功率が90%を下回った場合
- 未処理リクエストが1時間以上滞留
- 期限切れ直前のリクエストが急増

関連テーブル
--------------------------------------------

**参照するテーブル**:
- :doc:`members`: 登録成功時の参照先

**参照されるテーブル**:
- :doc:`member_events`: 登録イベント記録での参照 