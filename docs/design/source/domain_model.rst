.. ドメインモデル documentation master file, created by
   sphinx-quickstart on Fri Jan 10 14:12:32 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ドメインモデル定義
============================================

- 本プロジェクトで出現する用語（ドメインモデル）の定義を記述する

.. note::
   **テンプレート使用方法**
   
   - [ ]内の項目を具体的な内容に置き換えてください
   - 不要なセクションは削除してください
   - 各セクションの例を参考に、プロジェクト固有の内容を追加してください
   - `.cursor/domain_model.md` の設計パターン分類ルールに従って整理してください

アクター
--------------------------------------------

**ECサイト顧客**

- 商品を購入する一般ユーザー
- ショッピングカート機能の主要利用者

**ECサイト運営者**

- 商品管理、在庫管理を行う管理者
- システムの運用・監視を担当

**在庫管理システム**

- 商品在庫をリアルタイムで管理する外部システム
- カート追加時の在庫チェックを提供

.. raw:: html

   <!--
   ECサイト例:
   
   **ECサイト顧客**
   - 商品を購入する一般ユーザー
   - ショッピングカート機能の主要利用者
   
   **ECサイト運営者**
   - 商品管理、在庫管理を行う管理者
   - システムの運用・監視を担当
   
   **在庫管理システム**
   - 商品在庫をリアルタイムで管理する外部システム
   - カート追加時の在庫チェックを提供
   -->

エンティティ（Entity）
--------------------------------------------

**ユーザー（User）**

- システムの利用者を表すコアエンティティ
- 一意のユーザーIDで識別される
- ログイン状態、基本情報を持つ

**商品（Product）**

- 販売対象の商品を表すエンティティ
- 商品ID、名前、価格、在庫数を持つ
- 在庫管理と価格管理の責務を持つ

**ショッピングカート（ShoppingCart）**

- 顧客の購入予定商品を管理するエンティティ
- ユーザーごとに1つのアクティブなカートを持つ
- 24時間の有効期限がある

**カート商品（CartItem）**

- ショッピングカートに追加された商品アイテム
- 商品情報、数量、単価、小計を含む
- 同一商品は数量で調整される

.. raw:: html

   <!--
   ECサイト例:
   
   **ユーザー（User）**
   - システムの利用者を表すコアエンティティ
   - 一意のユーザーIDで識別される
   - ログイン状態、基本情報を持つ
   
   **商品（Product）**
   - 販売対象の商品を表すエンティティ
   - 商品ID、名前、価格、在庫数を持つ
   - 在庫管理と価格管理の責務を持つ
   
   **ショッピングカート（ShoppingCart）**
   - 顧客の購入予定商品を管理するエンティティ
   - ユーザーごとに1つのアクティブなカートを持つ
   - 24時間の有効期限がある
   
   **カート商品（CartItem）**
   - ショッピングカートに追加された商品アイテム
   - 商品情報、数量、単価、小計を含む
   - 同一商品は数量で調整される
   -->

コントローラ（Controller）
--------------------------------------------

**ショッピングカート管理**

- カートへの商品追加・削除・数量変更
- カート合計金額の計算
- カート有効期限の管理

**商品確保管理**

- カートに追加された商品を在庫から一時的に確保
- 他の顧客による購入を防ぐ
- カートの有効期限まで確保される

**購入手続き管理**

- カート内商品の決済処理
- 配送先指定、支払い方法選択
- 完了時にカートがクリアされる

.. raw:: html

   <!--
   ECサイト例:
   
   **ショッピングカート管理**
   - カートへの商品追加・削除・数量変更
   - カート合計金額の計算
   - カート有効期限の管理
   
   **商品確保管理**
   - カートに追加された商品を在庫から一時的に確保
   - 他の顧客による購入を防ぐ
   - カートの有効期限まで確保される
   
   **購入手続き管理**
   - カート内商品の決済処理
   - 配送先指定、支払い方法選択
   - 完了時にカートがクリアされる
   -->

バウンダリ（Boundary）
--------------------------------------------

**在庫管理システム連携**

- 外部在庫管理システムとの通信
- リアルタイム在庫チェック
- 在庫確保・解放の処理

**決済システム連携**

- 外部決済システムとの通信
- 決済処理の実行
- 決済結果の受信・処理

**ユーザーインターフェース**

- Webページ、APIエンドポイント
- ユーザー操作の受付
- システム状態の表示

.. raw:: html

   <!--
   ECサイト例:
   
   **在庫管理システム連携**
   - 外部在庫管理システムとの通信
   - リアルタイム在庫チェック
   - 在庫確保・解放の処理
   
   **決済システム連携**
   - 外部決済システムとの通信
   - 決済処理の実行
   - 決済結果の受信・処理
   
   **ユーザーインターフェース**
   - Webページ、APIエンドポイント
   - ユーザー操作の受付
   - システム状態の表示
   -->

ビジネス概念（Domain Concepts）
--------------------------------------------

**商品確保（Product Reservation）**

- カートに追加された商品を在庫から一時的に確保するビジネスルール
- 他の顧客による購入を防ぐ排他制御
- カートの有効期限まで確保される

**在庫（Stock/Inventory）**

- 販売可能な商品の数量を表すビジネス概念
- リアルタイムで更新される
- カート追加時にチェックされる

**セッション管理（Session Management）**

- ユーザーのログイン状態とカート状態の管理
- セッション有効期限の制御
- ログアウト時のカート保持ルール

.. raw:: html

   <!--
   ECサイト例:
   
   **商品確保（Product Reservation）**
   - カートに追加された商品を在庫から一時的に確保するビジネスルール
   - 他の顧客による購入を防ぐ排他制御
   - カートの有効期限まで確保される
   
   **在庫（Stock/Inventory）**
   - 販売可能な商品の数量を表すビジネス概念
   - リアルタイムで更新される
   - カート追加時にチェックされる
   
   **セッション管理（Session Management）**
   - ユーザーのログイン状態とカート状態の管理
   - セッション有効期限の制御
   - セキュリティ考慮事項を含む
   
   **価格計算（Price Calculation）**
   - 商品価格、税額、送料の計算ロジック
   - 割引、クーポン適用の処理
   - 通貨換算（必要に応じて）
   -->

値オブジェクト（Value Objects）
--------------------------------------------

**金額（Money）**

- 価格、税額、合計金額を表現
- 通貨情報を含む
- 不変オブジェクト

**数量（Quantity）**

- カート内商品の数量
- 在庫数量
- 正の整数値のみ許可

**期限（ExpiryTime）**

- カート有効期限
- セッション有効期限
- タイムゾーン考慮

**商品コード（ProductCode）**

- 商品を一意に識別するコード
- JANコード、SKUなどのフォーマット
- バリデーションルールを含む

.. raw:: html

   <!--
   ECサイト例:
   
   **金額（Money）**
   - 価格、税額、合計金額を表現
   - 通貨情報を含む
   - 不変オブジェクト
   
   **数量（Quantity）**
   - カート内商品の数量
   - 在庫数量
   - 正の整数値のみ許可
   
   **期限（ExpiryTime）**
   - カート有効期限
   - セッション有効期限
   - タイムゾーン考慮
   
   **商品コード（ProductCode）**
   - 商品を一意に識別するコード
   - JANコード、SKUなどのフォーマット
   - バリデーションルールを含む
   -->

ドメインモデル クラス図
--------------------------------------------

.. mermaid::

   %%{init: {"theme": "default"}}%%
   classDiagram
       class User["ユーザー"] {
           +user_id: int
           +email: string
           +name: string
           +created_at: datetime
           +is_active: boolean
           --
           +login()
           +logout()
           +checkCart()
       }

       class Product["商品"] {
           +product_id: int
           +name: string
           +price: decimal
           +stock_quantity: int
           +is_available: boolean
           --
           +checkStock()
           +getPrice()
           +reduceStock()
       }

       class ShoppingCart["ショッピングカート"] {
           +cart_id: int
           +user_id: int
           +total_amount: decimal
           +created_at: datetime
           +expires_at: datetime
           --
           +addProduct()
           +removeProduct()
           +calculateTotal()
           +checkExpiry()
       }

       class CartItem["カート商品"] {
           +cart_item_id: int
           +cart_id: int
           +product_id: int
           +quantity: int
           +unit_price: decimal
           +subtotal: decimal
           --
           +changeQuantity()
           +calculateSubtotal()
           +remove()
       }

       User --> ShoppingCart
       ShoppingCart --> CartItem
       Product --> CartItem

.. raw:: html

   <!--
   ECサイト例:
   
   .. mermaid::
   
      %%{init: {"theme": "default"}}%%
      classDiagram
          class User["ユーザー"] {
              +user_id: int
              +email: string
              +name: string
              +created_at: datetime
              +is_active: boolean
              --
              +login()
              +logout()
              +checkCart()
          }
   
          class Product["商品"] {
              +product_id: int
              +name: string
              +price: decimal
              +stock_quantity: int
              +is_available: boolean
              --
              +checkStock()
              +getPrice()
              +reduceStock()
          }
   
          class ShoppingCart["ショッピングカート"] {
              +cart_id: int
              +user_id: int
              +total_amount: decimal
              +created_at: datetime
              +expires_at: datetime
              --
              +addProduct()
              +removeProduct()
              +calculateTotal()
              +checkExpiry()
          }
   
          class CartItem["カート商品"] {
              +cart_item_id: int
              +cart_id: int
              +product_id: int
              +quantity: int
              +unit_price: decimal
              +subtotal: decimal
              --
              +changeQuantity()
              +calculateSubtotal()
              +remove()
          }
   
          User --> ShoppingCart
          ShoppingCart --> CartItem
          Product --> CartItem
   -->

テンプレート使用手順
============================================

1. **プロジェクト情報の置き換え**
   - 冒頭の「[プロジェクト名]」「[機能名]」を具体的な内容に置き換える

2. **各セクションの記入**
   - [ ]で囲まれた項目を具体的な内容に置き換える
   - 不要なセクション・項目は削除する

3. **ECサイト例の活用**
   - HTMLコメント内のECサイト例を参考にする
   - 同様の構造で自プロジェクトの内容を記述する

4. **設計パターン分類の確認**
   - `.cursor/domain_model.md` の分類ルールに従う
   - 判断フローチャートを活用する

5. **クラス図の作成**
   - Mermaidテンプレートを活用
   - Sphinx環境対応の記法を使用

6. **他文書との整合性確認**
   - ユーザーストーリーとアクターを一致させる
   - ユースケース、データベース設計との連携確認

.. note::
   **設計パターン別記述のポイント**
   
   - **エンティティ**: 一意性（ID）と主要操作を明記
   - **コントローラ**: 管理対象とビジネスルールを明確化
   - **バウンダリ**: 外部との接点とプロトコルを明記
   - **ビジネス概念**: 業務価値とルールを明文化
   - **値オブジェクト**: 不変性と制約を明記
