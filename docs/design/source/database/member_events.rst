member_events
============================================

概要
--------------------------------------------

**テーブル目的**: 会員関連のドメインイベントを記録するテーブル

**設計方針**: イベントソーシング、監査ログ、非同期処理トリガー

**想定レコード数**: 日次5000件、月次15万件（1年保持）

**データベース**: PostgreSQL 13以降

**関連概念**: ドメインイベント（MemberRegistered、MemberRegistrationFailed）

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
   * - event_id
     - イベントID
     - UUID
     - NOT NULL
     - gen_random_uuid()
     - イベントID（主キー）
   * - event_type
     - イベント種別
     - VARCHAR(100)
     - NOT NULL
     - 
     - イベント種別
   * - member_id
     - 会員ID
     - UUID
     - NULL
     - 
     - 会員ID（存在する場合）
   * - email_address
     - メールアドレス
     - VARCHAR(254)
     - NOT NULL
     - 
     - 対象メールアドレス
   * - event_data
     - イベントデータ
     - JSONB
     - NOT NULL
     - 
     - イベントデータ（JSON形式）
   * - occurred_at
     - 発生日時
     - TIMESTAMP WITH TIME ZONE
     - NOT NULL
     - CURRENT_TIMESTAMP
     - 発生日時
   * - processed_at
     - 処理完了日時
     - TIMESTAMP WITH TIME ZONE
     - NULL
     - 
     - 処理完了日時

制約定義
--------------------------------------------

**主キー制約**:

- **制約名**: pk_member_events
- **対象カラム**: event_id
- **説明**: イベントIDによる一意識別

**外部キー制約**:

.. list-table::
   :header-rows: 1

   * - 制約名
     - カラム名
     - 参照テーブル
     - 参照カラム
     - ON DELETE
     - ON UPDATE
   * - fk_member_events_member_id
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
   * - ck_member_events_event_type
     - event_type IN ('MemberRegistered', 'MemberRegistrationFailed', 'MemberUpdated', 'MemberDeactivated')
     - イベント種別の値制限

インデックス定義
--------------------------------------------

**パフォーマンス用インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 種類
     - 対象カラム
     - 用途
   * - idx_member_events_event_type
     - B-tree
     - event_type
     - イベント種別検索の高速化
   * - idx_member_events_member_id
     - B-tree
     - member_id
     - 会員ID別検索の高速化
   * - idx_member_events_occurred_at
     - B-tree
     - occurred_at
     - 時系列検索・レポート用

**部分インデックス**:

.. list-table::
   :header-rows: 1

   * - インデックス名
     - 対象カラム
     - WHERE条件
     - 用途
   * - idx_member_events_unprocessed
     - processed_at
     - processed_at IS NULL
     - 未処理イベント検索用

SQL定義
--------------------------------------------

**テーブル作成**:

.. code-block:: sql

   -- member_eventsテーブル作成（制約含む）
   CREATE TABLE member_events (
       event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       event_type VARCHAR(100) NOT NULL,
       member_id UUID,
       email_address VARCHAR(254) NOT NULL,
       event_data JSONB NOT NULL,
       occurred_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
       processed_at TIMESTAMP WITH TIME ZONE
   );

**制約追加**:

.. code-block:: sql

   -- 外部キー制約（NULL許可）
   ALTER TABLE member_events ADD CONSTRAINT fk_member_events_member_id 
   FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE SET NULL ON UPDATE CASCADE;
   
   -- チェック制約
   ALTER TABLE member_events ADD CONSTRAINT ck_member_events_event_type 
   CHECK (event_type IN ('MemberRegistered', 'MemberRegistrationFailed', 'MemberUpdated', 'MemberDeactivated'));

**インデックス作成**:

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
           varchar status
           timestamp created_at
           timestamp updated_at
       }
       
       member_events {
           uuid event_id PK
           varchar event_type
           uuid member_id FK "NULL許可"
           varchar email_address
           jsonb event_data
           timestamp occurred_at
           timestamp processed_at "NULL許可"
       }
       
       members ||--o{ member_events : "generates"

イベント種別定義
--------------------------------------------

**MemberRegistered（会員登録成功）**:

.. code-block:: json

   {
       "eventType": "MemberRegistered",
       "data": {
           "memberId": "123e4567-e89b-12d3-a456-426614174000",
           "email": "user@example.com",
           "registrationSource": "web",
           "timestamp": "2024-01-15T10:30:00Z"
       }
   }

**MemberRegistrationFailed（会員登録失敗）**:

.. code-block:: json

   {
       "eventType": "MemberRegistrationFailed",
       "data": {
           "email": "user@example.com",
           "failureReason": "DUPLICATE_EMAIL",
           "errorCode": "E001",
           "registrationSource": "web",
           "timestamp": "2024-01-15T10:30:00Z"
       }
   }

**MemberUpdated（会員情報更新）**:

.. code-block:: json

   {
       "eventType": "MemberUpdated",
       "data": {
           "memberId": "123e4567-e89b-12d3-a456-426614174000",
           "updatedFields": ["phoneNumber", "address"],
           "previousValues": {
               "phoneNumber": "03-1234-5678",
               "prefecture": "東京都"
           },
           "timestamp": "2024-01-15T10:30:00Z"
       }
   }

**MemberDeactivated（会員無効化）**:

.. code-block:: json

   {
       "eventType": "MemberDeactivated",
       "data": {
           "memberId": "123e4567-e89b-12d3-a456-426614174000",
           "deactivationReason": "USER_REQUEST",
           "finalLoginAt": "2024-01-10T15:20:00Z",
           "timestamp": "2024-01-15T10:30:00Z"
       }
   }

イベント処理パターン
--------------------------------------------

**同期処理**:
- MemberRegistered: 会員作成の即座確認
- MemberRegistrationFailed: エラー通知の即座送信

**非同期処理**:
- 全イベント: メール通知、外部システム連携
- MemberRegistered: ウェルカムメール送信
- MemberDeactivated: データアーカイブ処理

データメンテナンス
--------------------------------------------

**古いイベントデータの削除**:

.. code-block:: sql

   -- 1年以上古いイベントデータ削除（月次バッチ）
   DELETE FROM member_events 
   WHERE occurred_at < CURRENT_TIMESTAMP - interval '1 year'
   AND processed_at IS NOT NULL;

**統計情報の更新**:

.. code-block:: sql

   -- 統計情報更新（週次メンテナンス）
   ANALYZE member_events;

**レポート用クエリ**:

.. code-block:: sql

   -- 日別イベント集計
   SELECT DATE(occurred_at) as event_date,
          event_type,
          COUNT(*) as event_count
   FROM member_events 
   WHERE occurred_at >= CURRENT_DATE - interval '30 days'
   GROUP BY DATE(occurred_at), event_type
   ORDER BY event_date DESC, event_type;
   
   -- 未処理イベントの確認
   SELECT event_id, event_type, email_address, occurred_at
   FROM member_events 
   WHERE processed_at IS NULL 
   AND occurred_at < CURRENT_TIMESTAMP - interval '1 hour'
   ORDER BY occurred_at;

パフォーマンス考慮事項
--------------------------------------------

**パーティショニング**:
- occurred_atでの月次パーティション分割を推奨
- 古いパーティションの自動アーカイブ・削除
- クエリパフォーマンスの向上

**インデックス最適化**:
- event_typeとoccurred_atの複合インデックス検討
- JSONBデータ検索用のGINインデックス
- 部分インデックスによる未処理データ高速検索

**クエリ最適化**:
- 日付範囲検索での適切なインデックス利用
- イベント種別での絞り込み最適化
- 大量データ処理時のバッチサイズ調整

セキュリティ考慮事項
--------------------------------------------

**データ保護**:
- event_dataの個人情報は最小限に制限
- ログ出力時の自動マスキング
- 削除されたユーザーのイベント保持ポリシー

**アクセス制御**:
- 読み取り専用権限での分析アクセス
- 更新権限はアプリケーションのみ
- 本番環境での直接操作制限

**監査ログ**:
- イベントデータ自体が監査ログの役割
- データ変更履歴の追跡可能性
- 規制要件への対応

運用監視
--------------------------------------------

**監視項目**:
- 未処理イベント数の推移
- イベント種別ごとの発生頻度
- 処理遅延時間の監視
- エラーイベントの増加傾向

**アラート設定**:
- 未処理イベントが100件を超過
- 1時間以上処理が滞留
- 特定エラーイベントが急増
- パーティション容量の逼迫

**パフォーマンス監視**:
- クエリ実行時間の監視
- インデックス使用率の確認
- パーティション別の負荷分散

関連テーブル
--------------------------------------------

**参照するテーブル**:
- :doc:`members`: イベント発生源
- :doc:`registration_requests`: 登録関連イベント

**将来連携予定**:
- notifications（通知テーブル）
- external_integrations（外部連携ログ）
- analytics_summary（分析サマリー） 