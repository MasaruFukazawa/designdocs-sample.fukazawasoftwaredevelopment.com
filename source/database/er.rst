ER図
============================================

ER図
--------------------------------------------

.. mermaid::

   erDiagram
       USERS {
           int user_id PK "ユーザーID"
           varchar email UK "メールアドレス"
           varchar name "氏名"
           varchar password_hash "パスワードハッシュ"
           boolean is_active "アクティブフラグ"
           datetime created_at "作成日時"
           datetime updated_at "更新日時"
       }

       PRODUCTS {
           int product_id PK "商品ID"
           varchar product_code UK "商品コード"
           varchar name "商品名"
           text description "商品説明"
           decimal price "価格"
           int stock_quantity "在庫数量"
           boolean is_available "販売可能フラグ"
           datetime created_at "作成日時"
           datetime updated_at "更新日時"
       }

       SHOPPING_CARTS {
           int cart_id PK "カートID"
           int user_id FK "ユーザーID"
           decimal total_amount "合計金額"
           datetime expires_at "有効期限"
           datetime created_at "作成日時"
           datetime updated_at "更新日時"
       }

       CART_ITEMS {
           int cart_item_id PK "カート商品ID"
           int cart_id FK "カートID"
           int product_id FK "商品ID"
           int quantity "数量"
           decimal unit_price "単価"
           decimal subtotal "小計"
           datetime added_at "追加日時"
           datetime updated_at "更新日時"
       }

       USERS ||--o{ SHOPPING_CARTS : has
       SHOPPING_CARTS ||--o{ CART_ITEMS : contains
       PRODUCTS ||--o{ CART_ITEMS : included_in
