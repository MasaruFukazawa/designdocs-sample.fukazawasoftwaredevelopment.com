会員登録
==========================================

関連ユーザーストーリー
--------------------------------------------

* :doc:`../user_story/member_registration`

アクター
--------------------------------------------

- **ECサイト来訪者**: 会員登録を行う主アクター（未登録ユーザー）
- **メール配信システム**: 登録確認メールを送信する副アクター
- **ECサイトシステム**: 会員情報を管理する副アクター

事前条件
--------------------------------------------

- ECサイト来訪者がECサイトにアクセス可能である
- メール配信システムが正常に動作している
- 会員登録画面が正常に表示される
- プライバシーポリシーと利用規約が公開されている

事後条件
--------------------------------------------

**成功時**:

- 新しい会員アカウントが作成されている
- 会員ステータスがアクティブ状態になっている
- 登録確認メールが送信されている
- ECサイト来訪者が自動的にログイン状態になっている
- 商品購入機能が利用可能になっている

**失敗時**:

- 会員アカウントが作成されていない
- エラーメッセージが表示されている
- ECサイト来訪者は非ログイン状態のまま

基本コース
--------------------------------------------

1. ECサイト来訪者がECサイトのトップページにアクセスする
2. ECサイト来訪者が「会員登録」ボタンをクリックする
3. システムが会員登録画面を表示する
4. ECサイト来訪者が必要な情報を入力する
   - メールアドレス
   - パスワード
   - 氏名（姓・名）
   - 住所（郵便番号、都道府県、市区町村、番地）
   - 電話番号
5. ECサイト来訪者がプライバシーポリシーと利用規約に同意する
6. ECサイト来訪者が「登録」ボタンをクリックする
7. システムが入力データのバリデーションを実行する
8. システムがメールアドレスの重複チェックを実行する
9. システムがパスワードの強度チェックを実行する
10. システムが会員情報をデータベースに保存する
11. システムがメール配信システムに確認メール送信を依頼する
12. メール配信システムが登録したメールアドレスに確認メールを送信する
13. システムが会員登録完了画面を表示する
14. システムがECサイト来訪者を自動的にログイン状態にする
15. ユースケース終了

代替コース
--------------------------------------------

**7a. 入力データにエラーがある場合**

7a1. システムがバリデーションエラーを検出する
7a2. システムが該当項目にエラーメッセージを表示する
7a3. ECサイト来訪者がエラーを修正する
7a4. 基本コースの手順7に戻る

**8a. メールアドレスが既に登録済みの場合**

8a1. システムがメールアドレスの重複を検出する
8a2. システムが「このメールアドレスは既に登録されています」というエラーメッセージを表示する
8a3. システムが「ログイン画面へ」リンクを提供する
8a4. システムが「パスワードを忘れた方」リンクを提供する
8a5. ユースケース終了

**9a. パスワード強度が不足している場合**

9a1. システムがパスワード強度の不足を検出する
9a2. システムが「パスワードは8文字以上で英数字記号を含む必要があります」というエラーメッセージを表示する
9a3. ECサイト来訪者がパスワードを修正する
9a4. 基本コースの手順9に戻る

**12a. メール送信に失敗した場合**

12a1. メール配信システムがメール送信エラーを返す
12a2. システムがメール送信失敗をログに記録する
12a3. システムが「登録は完了しましたが、確認メールの送信に失敗しました」というメッセージを表示する
12a4. 基本コースの手順13に戻る

入力項目
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - 項目名
     - 必須 / 任意
     - 制限
   * - メールアドレス
     - 必須
     - RFC 5322準拠のフォーマット
       最大254文字
   * - パスワード
     - 必須
     - 8文字以上
       英数字記号を含む
       最大128文字
   * - 氏名（姓）
     - 必須
     - 最大50文字
       特殊文字制限あり
   * - 氏名（名）
     - 必須
     - 最大50文字
       特殊文字制限あり
   * - 郵便番号
     - 必須
     - 7桁数字（ハイフンなし）
       日本の郵便番号形式
   * - 都道府県
     - 必須
     - 47都道府県から選択
   * - 市区町村
     - 必須
     - 最大100文字
   * - 番地・建物名
     - 必須
     - 最大200文字
   * - 電話番号
     - 必須
     - 日本の電話番号形式
       ハイフンありなし両対応
   * - プライバシーポリシー同意
     - 必須
     - チェックボックス必須選択
   * - 利用規約同意
     - 必須
     - チェックボックス必須選択

エラーメッセージ
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - 入力項目名
     - エラーパターン
     - エラーメッセージ
   * - メールアドレス
     - 未入力
     - メールアドレスは必須です
   * - メールアドレス
     - 形式不正
     - 正しいメールアドレス形式で入力してください
   * - メールアドレス
     - 重複
     - このメールアドレスは既に登録されています
   * - パスワード
     - 未入力
     - パスワードは必須です
   * - パスワード
     - 強度不足
     - パスワードは8文字以上で英数字記号を含む必要があります
   * - 氏名（姓）
     - 未入力
     - 姓は必須です
   * - 氏名（名）
     - 未入力
     - 名は必須です
   * - 郵便番号
     - 未入力
     - 郵便番号は必須です
   * - 郵便番号
     - 形式不正
     - 郵便番号は7桁の数字で入力してください
   * - 都道府県
     - 未選択
     - 都道府県を選択してください
   * - 市区町村
     - 未入力
     - 市区町村は必須です
   * - 番地・建物名
     - 未入力
     - 番地・建物名は必須です
   * - 電話番号
     - 未入力
     - 電話番号は必須です
   * - 電話番号
     - 形式不正
     - 正しい電話番号形式で入力してください
   * - プライバシーポリシー同意
     - 未同意
     - プライバシーポリシーに同意する必要があります
   * - 利用規約同意
     - 未同意
     - 利用規約に同意する必要があります

画面遷移図
--------------------------------------------

.. mermaid::

   %%{init: {"theme": "default"}}%%
   graph TD
       A[トップページ] --> B[会員登録画面]
       B --> C{入力チェック}
       C -->|エラーあり| B
       C -->|重複メール| D[エラー表示・ログイン案内]
       C -->|OK| E[会員登録完了画面]
       E --> F[自動ログイン後の画面]
       D --> G[ログイン画面]
       D --> H[パスワードリセット画面]

メール定義
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - メールタイトル
     - メール定義書 リンク
   * - 会員登録確認メール
     - :doc:`../mail/member_registration_confirmation`

シーケンス図
--------------------------------------------

.. mermaid::

   %%{init: {"theme": "default"}}%%
   sequenceDiagram
       participant Visitor as ECサイト来訪者
       participant Web as Webサイト
       participant AppService as MemberRegistrationApplicationService
       participant DomainService as MemberRegistrationService
       participant EmailService as EmailValidationService
       participant PasswordService as PasswordService
       participant MemberRepo as MemberRepository
       participant RequestRepo as RegistrationRequestRepository
       participant Mail as メール配信システム
       
       Visitor->>Web: 会員登録画面アクセス
       Web-->>Visitor: 会員登録画面表示
       Visitor->>Web: 会員情報入力・送信
       Web->>AppService: registerNewMember(registrationData)
       
       AppService->>RequestRepo: save(RegistrationRequest)
       RequestRepo-->>AppService: 保存完了
       
       AppService->>EmailService: validateFormat(emailAddress)
       EmailService-->>AppService: 検証結果
       
       AppService->>PasswordService: validateStrength(password)
       PasswordService-->>AppService: 検証結果
       
       AppService->>DomainService: validateRegistrationData(data)
       DomainService-->>AppService: バリデーション結果
       
       AppService->>MemberRepo: existsByEmailAddress(emailAddress)
       MemberRepo-->>AppService: 重複チェック結果
       
       AppService->>DomainService: registerMember(registrationData)
       DomainService->>PasswordService: hashPassword(rawPassword)
       PasswordService-->>DomainService: hashedPassword
       DomainService->>DomainService: create Member entity
       DomainService-->>AppService: Member entity
       
       AppService->>MemberRepo: save(member)
       MemberRepo-->>AppService: 保存完了
       
       AppService->>RequestRepo: updateStatus(COMPLETED)
       RequestRepo-->>AppService: 更新完了
       
       AppService->>Mail: sendConfirmationEmail(member)
       Mail-->>AppService: 送信完了
       Mail->>Visitor: 確認メール送信
       
       AppService->>AppService: publish MemberRegistered event
       AppService-->>Web: 登録完了レスポンス
       Web-->>Visitor: 登録完了画面表示
       Web->>Web: 自動ログイン処理 