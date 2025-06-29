会員登録 DDD設計
==========================================

概要
--------------------------------------------

ECサイト来訪者が会員として登録するための機能に関するDomain-Driven Design設計。
会員登録に関わる実体、値オブジェクト、集約、ドメインサービス、リポジトリを定義する。

関連文書
--------------------------------------------

* :doc:`../user_story/member_registration`
* :doc:`../usecase/member_registration`
* :doc:`../domain_model`

エンティティ（Entity）
--------------------------------------------

**Member（会員）**

- **目的**: 会員情報を管理するコアエンティティ
- **識別子**: MemberId（UUID）
- **属性**:
  - emailAddress（メールアドレス）- EmailAddress値オブジェクト
  - password（パスワード）- Password値オブジェクト
  - profile（プロフィール）- MemberProfile値オブジェクト
  - status（ステータス）- MemberStatus列挙型
  - createdAt（作成日時）
  - updatedAt（更新日時）
- **不変条件**:
  - メールアドレスは一意である
  - パスワードは強度要件を満たす
  - ステータスはACTIVE、INACTIVE、SUSPENDEDのいずれか
- **責務**:
  - 会員情報の整合性保証
  - パスワード変更機能
  - ステータス変更機能
  - 認証用の検証機能

**RegistrationRequest（登録リクエスト）**

- **目的**: 会員登録プロセスを管理するエンティティ
- **識別子**: RegistrationRequestId（UUID）
- **属性**:
  - requestData（リクエストデータ）- RegistrationData値オブジェクト
  - status（ステータス）- RegistrationStatus列挙型
  - submittedAt（送信日時）
  - completedAt（完了日時）
  - errors（エラー情報）- ValidationError値オブジェクトのリスト
- **不変条件**:
  - ステータスはPENDING、COMPLETED、FAILEDのいずれか
  - 完了時はcompletedAtが必須
- **責務**:
  - 登録プロセスの状態管理
  - バリデーション結果の保持
  - エラー情報の管理

値オブジェクト（Value Objects）
--------------------------------------------

**EmailAddress（メールアドレス）**

- **目的**: メールアドレスの形式検証と正規化
- **属性**:
  - value（文字列値）
- **不変条件**:
  - RFC 5322準拠のフォーマット
  - 最大254文字
  - 大文字小文字の正規化済み
- **メソッド**:
  - equals（等価性比較）
  - toString（文字列変換）
  - validate（フォーマット検証）

**Password（パスワード）**

- **目的**: パスワードの強度検証とハッシュ化
- **属性**:
  - hashedValue（ハッシュ化された値）
  - salt（ソルト）
- **不変条件**:
  - 8文字以上
  - 英数字記号を含む
  - ハッシュ化された状態で保存
- **メソッド**:
  - verify（パスワード検証）
  - changePassword（パスワード変更）
  - validateStrength（強度検証）

**MemberProfile（会員プロフィール）**

- **目的**: 会員の個人情報を管理
- **属性**:
  - fullName（氏名）- FullName値オブジェクト
  - address（住所）- Address値オブジェクト
  - phoneNumber（電話番号）- PhoneNumber値オブジェクト
- **不変条件**:
  - すべての項目が必須
  - 文字数制限を満たす
- **メソッド**:
  - equals（等価性比較）
  - updateProfile（プロフィール更新）

**FullName（氏名）**

- **目的**: 氏名の正規化と検証
- **属性**:
  - lastName（姓）
  - firstName（名）
- **不変条件**:
  - 各項目最大50文字
  - 空文字列不可
- **メソッド**:
  - getDisplayName（表示名取得）
  - equals（等価性比較）

**Address（住所）**

- **目的**: 住所情報の構造化と検証
- **属性**:
  - postalCode（郵便番号）
  - prefecture（都道府県）
  - city（市区町村）
  - streetAddress（番地・建物名）
- **不変条件**:
  - 郵便番号は7桁数字
  - 都道府県は47都道府県から選択
  - 各項目の文字数制限
- **メソッド**:
  - getFullAddress（完全住所取得）
  - equals（等価性比較）

**PhoneNumber（電話番号）**

- **目的**: 電話番号の正規化と検証
- **属性**:
  - value（正規化された値）
- **不変条件**:
  - 日本の電話番号形式
  - ハイフンで正規化
- **メソッド**:
  - equals（等価性比較）
  - toString（文字列変換）

**RegistrationData（登録データ）**

- **目的**: 登録時の入力データを管理
- **属性**:
  - emailAddress（メールアドレス）- EmailAddress値オブジェクト
  - rawPassword（生パスワード）
  - profile（プロフィール）- MemberProfile値オブジェクト
  - agreedToTerms（利用規約同意）
  - agreedToPrivacyPolicy（プライバシーポリシー同意）
- **不変条件**:
  - 利用規約とプライバシーポリシーの同意が必須
- **メソッド**:
  - validate（データ検証）
  - createMember（会員エンティティ作成）

集約（Aggregates）
--------------------------------------------

**Member集約**

- **集約ルート**: Member
- **構成要素**: Member、MemberProfile、EmailAddress、Password
- **境界**:
  - 会員情報の整合性保証
  - パスワード管理
  - プロフィール変更
- **不変条件**:
  - メールアドレスの一意性
  - パスワード強度要件
  - プロフィール情報の必須項目チェック
- **操作**:
  - 会員登録
  - プロフィール更新
  - パスワード変更
  - ステータス変更

**MemberRegistration集約**

- **集約ルート**: RegistrationRequest
- **構成要素**: RegistrationRequest、RegistrationData、ValidationError
- **境界**:
  - 登録プロセス全体の管理
  - バリデーション結果の管理
  - エラー情報の管理
- **不変条件**:
  - リクエストの状態整合性
  - バリデーションルールの適用
- **操作**:
  - 登録リクエスト作成
  - バリデーション実行
  - 登録完了処理
  - エラー処理

ドメインサービス（Domain Services）
--------------------------------------------

**MemberRegistrationService（会員登録サービス）**

- **目的**: 会員登録に関する複雑なビジネスロジックを処理
- **責務**:
  - メールアドレス重複チェック
  - 登録プロセス全体の調整
  - バリデーション結果の統合
  - 会員エンティティの生成
- **メソッド**:
  - registerMember（会員登録）
  - validateRegistrationData（登録データ検証）
  - checkEmailUniqueness（メール重複チェック）

**PasswordService（パスワードサービス）**

- **目的**: パスワード関連の処理を担当
- **責務**:
  - パスワード強度検証
  - ハッシュ化処理
  - パスワード変更処理
- **メソッド**:
  - validateStrength（強度検証）
  - hashPassword（ハッシュ化）
  - verifyPassword（パスワード検証）

**EmailValidationService（メール検証サービス）**

- **目的**: メールアドレスの検証とドメイン管理
- **責務**:
  - メールアドレス形式検証
  - 禁止ドメインチェック
  - 正規化処理
- **メソッド**:
  - validateFormat（形式検証）
  - checkDomainAllowed（ドメイン許可チェック）
  - normalizeEmail（正規化）

リポジトリ（Repositories）
--------------------------------------------

**MemberRepository（会員リポジトリ）**

- **目的**: 会員エンティティの永続化を担当
- **メソッド**:
  - save（保存）
  - findById（ID検索）
  - findByEmailAddress（メールアドレス検索）
  - existsByEmailAddress（メールアドレス存在チェック）
  - delete（削除）
- **実装考慮事項**:
  - メールアドレスの一意性制約
  - パスワードの暗号化保存
  - インデックス設計

**RegistrationRequestRepository（登録リクエストリポジトリ）**

- **目的**: 登録リクエストエンティティの永続化を担当
- **メソッド**:
  - save（保存）
  - findById（ID検索）
  - findPendingRequests（保留中リクエスト検索）
  - delete（削除）
- **実装考慮事項**:
  - ステータス検索のインデックス
  - 古いリクエストの自動削除

アプリケーションサービス
--------------------------------------------

**MemberRegistrationApplicationService（会員登録アプリケーションサービス）**

- **目的**: 会員登録のユースケース実行を調整
- **依存関係**:
  - MemberRepository
  - RegistrationRequestRepository
  - MemberRegistrationService
  - EmailNotificationService
- **メソッド**:
  - registerNewMember（新規会員登録）
- **処理フロー**:
  1. 登録データの受信
  2. バリデーション実行
  3. メールアドレス重複チェック
  4. 会員エンティティ作成
  5. データベース保存
  6. 確認メール送信
  7. レスポンス返却

ドメインイベント
--------------------------------------------

**MemberRegistered（会員登録完了イベント）**

- **目的**: 会員登録完了を他の境界コンテキストに通知
- **属性**:
  - memberId（会員ID）
  - emailAddress（メールアドレス）
  - registeredAt（登録日時）
- **発生タイミング**: 会員登録完了時
- **購読者**: メール通知サービス、分析サービス

**MemberRegistrationFailed（会員登録失敗イベント）**

- **目的**: 会員登録失敗をログ・監視システムに通知
- **属性**:
  - attemptedEmailAddress（試行メールアドレス）
  - failureReason（失敗理由）
  - failedAt（失敗日時）
- **発生タイミング**: 会員登録失敗時
- **購読者**: ログサービス、監視サービス

実装上の注意点
--------------------------------------------

**セキュリティ考慮事項**

- パスワードは必ずハッシュ化して保存
- SQLインジェクション対策の実装
- CSRF対策の実装
- セッション管理の適切な実装

**パフォーマンス考慮事項**

- メールアドレスにユニーク制約とインデックス
- データベースアクセスの最適化
- 大量登録時の負荷分散

**テスト観点**

- エンティティの不変条件テスト
- 値オブジェクトのバリデーションテスト
- ドメインサービスの単体テスト
- 集約の整合性テスト
- リポジトリの永続化テスト 