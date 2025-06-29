Mermaid サンプル
================

画面遷移図
----------

.. mermaid::

   graph LR
       A[入力画面] --> B[確認画面]
       B --> C[完了画面]
       B --> A[エラー時、入力画面に戻る]


シーケンス図
------------

.. mermaid::

    sequenceDiagram
        participant User as ユーザー
        participant Screen1 as 画面1
        participant Screen2 as 画面2
        participant Screen3 as 画面3

        User->>Screen1: 画面1にアクセス
        Screen1-->>User: 画面1を表示
        User->>Screen2: 画面2に遷移
        Screen2-->>User: 画面2を表示
        User->>Screen3: 画面3に遷移
        Screen3-->>User: 画面3を表示


ER図
----

.. mermaid::

    erDiagram
        CUSTOMER ||--o{ ORDER : has
        ORDER ||--|{ LINE-ITEM : contains
        CUSTOMER }|..|{ ADDRESS : "Delivers to"


.. _sequence-diagram:

ユースケース図
--------------

アクター説明
~~~~~~~~~~~~

- ユーザー: システムを利用するユーザー
- 管理者: システムを管理するユーザー

ユースケース
~~~~~~~~~~~~

ユーザー
^^^^^^^^

.. mermaid::

    graph LR
        ユーザー((ユーザー)) --> |ログイン| ログイン処理
        ユーザー --> |検索| 商品検索
        ユーザー --> |カートに追加| カート操作
        ユーザー --> |購入| 購入処理
        ユーザー --> |レビュー| 商品レビュー
        ユーザー --> |ログアウト| ログアウト処理
        ユーザー --> |会員登録| 会員登録処理
        ユーザー --> |会員情報変更| 会員情報変更処理
        ユーザー --> |会員情報削除| 会員情報削除処理
        ユーザー --> |パスワード変更| パスワード変更処理

管理者
^^^^^^

.. mermaid::

    graph LR
        管理者 --> |商品登録| 商品登録処理
        管理者 --> |商品削除| 商品削除処理
        管理者 --> |商品変更| 商品変更処理
        管理者 --> |ユーザー管理| ユーザー管理処理


業務フロー
----------

.. mermaid::

    flowchart LR
        subgraph ユーザー
            A[商品を検索]
            B[商品を購入]
        end

        subgraph 営業部
            C[受注処理]
            D[請求書発行]
        end

        subgraph 倉庫
            E[出荷準備]
            F[出荷]
        end

        A --> B --> C --> D
        C --> E --> F


ロバスト図
----------

.. mermaid::

    flowchart LR
        subgraph アクター
            User[👤 ユーザー]
        end

        subgraph 境界
            UI[🧱 商品購入画面]
        end

        subgraph 制御
            UC[🧠 商品購入ユースケース]
            CheckStock[🧠 在庫チェック処理]
            CreateOrder[🧠 注文作成処理]
            UpdateStock[🧠 在庫更新処理]
        end

        subgraph エンティティ
            Stock[🗄️ 在庫]
            Order[🗄️ 注文]
        end

        User --> UI
        UI --> UC
        UC --> CheckStock
        CheckStock --> Stock
        CheckStock -- OK --> CreateOrder
        CreateOrder --> Order
        CreateOrder --> UpdateStock
        UpdateStock --> Stock
        UpdateStock --> UC
        CheckStock -- NG --> UI


PIPELINE
-----------

.. mermaid::

    flowchart TD
        Start([Start]) --> S1

        %% --- Source Stage ---
        subgraph S1 [Stage: Source]
            A1[GitHub Checkout]
        end

        S1 --> S2

        %% --- Lint & Tests Stage ---
        subgraph S2 [Stage: Lint & Tests]
            B1[Lint]
            B2[Tests]
            B3[Inspector Scan]
            B4[Security Scan]
            B1 --> B4
            B2 --> B4
            B3 --> B4
        end

        S2 --> S3

        %% --- Build Stage ---
        subgraph S3 [Stage: Build]
            C1[Docker Build & Push to ECR]
        end

        S3 --> End([Done])
