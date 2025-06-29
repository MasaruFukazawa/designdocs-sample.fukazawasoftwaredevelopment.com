Mermaid サンプル
================

**最終更新**: [ 更新日を記載 ]

.. contents:: 目次
   :depth: 2
   :local:

画面遷移図
----------

.. mermaid::

   graph LR
       A[入力画面] --> B[確認画面]
       B --> C[完了画面]
       B --> A


シーケンス図
------------

.. mermaid::

    sequenceDiagram
        participant User as ユーザー
        participant WebApp as Webアプリケーション
        participant Service as 処理制御
        participant DB as データベース

        User->>WebApp: 画面アクセス
        WebApp->>Service: データ取得要求
        Service->>DB: データ検索
        DB-->>Service: 検索結果
        Service-->>WebApp: データ返却
        WebApp-->>User: 画面表示


ER図
----

.. mermaid::

    erDiagram
        CUSTOMER ||--o{ ORDER : has
        ORDER ||--|{ ORDER_ITEM : contains
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
        User[ユーザー] --> Login[ログイン処理]
        User --> Search[商品検索]
        User --> Cart[カート操作]
        User --> Purchase[購入処理]
        User --> Review[商品レビュー]
        User --> Logout[ログアウト処理]
        User --> Register[ユーザー登録処理]
        User --> UpdateProfile[会員情報変更処理]
        User --> DeleteProfile[会員情報削除処理]
        User --> ChangePassword[パスワード変更処理]

管理者
^^^^^^

.. mermaid::

    graph LR
        Admin[管理者] --> AddProduct[商品登録処理]
        Admin --> DeleteProduct[商品削除処理]
        Admin --> UpdateProduct[商品変更処理]
        Admin --> ManageUser[ユーザー管理処理]


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
            User[ユーザー]
        end

        subgraph 境界
            UI[商品購入画面]
        end

        subgraph 制御
            UC[商品購入ユースケース]
            CheckStock[在庫チェック処理]
            CreateOrder[注文作成処理]
            UpdateStock[在庫更新処理]
        end

        subgraph エンティティ
            Stock[在庫]
            Order[注文]
        end

        User --> UI
        UI --> UC
        UC --> CheckStock
        CheckStock --> Stock
        CheckStock -->|OK| CreateOrder
        CreateOrder --> Order
        CreateOrder --> UpdateStock
        UpdateStock --> Stock
        UpdateStock --> UC
        CheckStock -->|NG| UI


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
