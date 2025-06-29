会員登録確認メール
==========================================

メール概要
--------------------------------------------

**メール種別**: 確認メール

**送信タイミング**: 会員登録完了直後

**送信対象**: 新規登録した会員

**送信頻度**: 1回（登録1件につき）

**重要度**: 高（会員登録プロセスの必須要素）

関連設計文書
--------------------------------------------

* :doc:`../user_story/member_registration`
* :doc:`../usecase/member_registration`
* :doc:`../ddd/member_registration`

メール詳細
--------------------------------------------

**メールID**: MEMBER_REGISTRATION_CONFIRMATION

**From**: noreply@example-ec-site.com

**Subject**: 【ECサイト】会員登録が完了しました

**メール形式**: HTML + テキスト

**文字エンコーディング**: UTF-8

送信条件
--------------------------------------------

**送信トリガー**: 
- 会員登録処理が正常に完了した時
- MemberRegisteredドメインイベントの発生時

**送信対象者の条件**:
- 会員登録フォームで正常に登録処理が完了した人
- 有効なメールアドレスを入力した人
- プライバシーポリシーと利用規約に同意した人

**送信除外条件**:
- メールアドレスが無効な場合
- システムエラーが発生した場合
- メール配信停止設定がある場合（該当する場合）

メール本文（HTML版）
--------------------------------------------

.. code-block:: html

   <!DOCTYPE html>
   <html lang="ja">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>会員登録完了のお知らせ</title>
       <style>
           body { font-family: 'Hiragino Sans', 'Meiryo', sans-serif; line-height: 1.6; color: #333; }
           .container { max-width: 600px; margin: 0 auto; padding: 20px; }
           .header { border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }
           .logo { font-size: 24px; font-weight: bold; color: #007bff; }
           .content { margin-bottom: 30px; }
           .info-box { background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
           .button { display: inline-block; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; }
           .footer { border-top: 1px solid #ddd; padding-top: 20px; margin-top: 30px; font-size: 12px; color: #666; }
       </style>
   </head>
   <body>
       <div class="container">
           <div class="header">
               <div class="logo">ECサイト</div>
           </div>
           
           <div class="content">
               <h2>会員登録が完了しました</h2>
               
               <p>{{member_name}}様</p>
               
               <p>この度は、ECサイトにご登録いただき、誠にありがとうございます。</p>
               
               <p>会員登録が完了いたしました。以下の情報でご登録いただいております。</p>
               
               <div class="info-box">
                   <h3>ご登録情報</h3>
                   <p><strong>メールアドレス:</strong> {{email_address}}</p>
                   <p><strong>お名前:</strong> {{member_name}}</p>
                   <p><strong>登録日時:</strong> {{registration_date}}</p>
               </div>
               
               <p>今すぐお買い物をお楽しみいただけます。</p>
               
               <p style="text-align: center; margin: 30px 0;">
                   <a href="{{site_url}}" class="button">ECサイトでお買い物を始める</a>
               </p>
               
               <h3>重要なお知らせ</h3>
               <ul>
                   <li>このメールは送信専用です。ご返信いただいてもお答えできません。</li>
                   <li>ご不明な点がございましたら、カスタマーサポートまでお問い合わせください。</li>
                   <li>パスワードは第三者に知られないよう、厳重に管理してください。</li>
               </ul>
           </div>
           
           <div class="footer">
               <p>お問い合わせ先</p>
               <p>ECサイト カスタマーサポート</p>
               <p>Email: support@example-ec-site.com</p>
               <p>営業時間: 平日 9:00-18:00</p>
               <p>&copy; 2024 ECサイト. All rights reserved.</p>
           </div>
       </div>
   </body>
   </html>

メール本文（テキスト版）
--------------------------------------------

.. code-block:: text

   =======================================
   【ECサイト】会員登録が完了しました
   =======================================
   
   {{member_name}}様
   
   この度は、ECサイトにご登録いただき、誠にありがとうございます。
   
   会員登録が完了いたしました。以下の情報でご登録いただいております。
   
   ■ ご登録情報
   メールアドレス: {{email_address}}
   お名前: {{member_name}}
   登録日時: {{registration_date}}
   
   今すぐお買い物をお楽しみいただけます。
   
   ECサイトでお買い物を始める: {{site_url}}
   
   ■ 重要なお知らせ
   ・このメールは送信専用です。ご返信いただいてもお答えできません。
   ・ご不明な点がございましたら、カスタマーサポートまでお問い合わせください。
   ・パスワードは第三者に知られないよう、厳重に管理してください。
   
   =======================================
   お問い合わせ先
   =======================================
   ECサイト カスタマーサポート
   Email: support@example-ec-site.com
   営業時間: 平日 9:00-18:00
   
   © 2024 ECサイト. All rights reserved.

変数一覧
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - 変数名
     - 説明
     - データ型
     - 例
   * - member_name
     - 会員の氏名（姓名の結合）
     - 文字列
     - 田中 太郎
   * - email_address
     - 登録メールアドレス
     - 文字列
     - tanaka@example.com
   * - registration_date
     - 登録完了日時（YYYY/MM/DD HH:MM形式）
     - 文字列
     - 2024/06/29 10:30
   * - site_url
     - ECサイトのトップページURL
     - 文字列
     - https://example-ec-site.com

エラーハンドリング
--------------------------------------------

**メール送信失敗時の対応**:

1. 送信失敗をログに記録
2. 管理者に通知メール送信
3. 会員登録は継続（メール送信失敗でも登録は有効）
4. ユーザーには「登録は完了したがメール送信に失敗した」旨を通知

**無効なメールアドレスの場合**:

1. 事前バリデーションで防止
2. 万が一送信失敗した場合はログに記録
3. 管理者による手動確認・修正

**変数データ不足の場合**:

1. デフォルト値の使用（「会員様」など）
2. システムエラーとしてログ記録
3. 開発チームへの通知

送信タイミング詳細
--------------------------------------------

**理想的な送信タイミング**: 会員登録完了から1分以内

**リトライ機能**:
- 初回送信失敗時、5分後に再送
- 2回目失敗時、30分後に再送  
- 3回目失敗時、管理者通知のみ（送信停止）

**優先度設定**: 高（即座に送信）

**バッチ処理**: リアルタイム送信（バッチ処理は使用しない）

テスト項目
--------------------------------------------

**機能テスト**:
- 正常な会員登録後のメール送信確認
- 各変数の正しい置換確認
- HTML/テキスト両形式の表示確認
- エラー時の適切なハンドリング確認

**表示テスト**:
-主要メールクライアントでの表示確認（Gmail、Outlook、Yahoo!メール等）
- モバイル端末での表示確認
- 文字化け確認

**セキュリティテスト**:
- 変数インジェクション攻撃の防止確認
- 個人情報の適切な表示確認

運用考慮事項
--------------------------------------------

**配信統計の取得**:
- 送信成功・失敗の統計
- 開封率の測定（HTML版の場合）
- リンククリック率の測定

**メンテナンス**:
- 送信失敗メールの定期確認
- テンプレートの更新管理
- 法的要件変更への対応

**個人情報保護**:
- ログ保存期間の設定
- 個人情報の適切な匿名化
- GDPR等の法的要件への対応 