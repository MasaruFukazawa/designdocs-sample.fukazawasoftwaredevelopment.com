# Mermaid記法ルール

このプロジェクトでのMermaid記法の統一ルールとベストプラクティスです。

## 基本設定

### Sphinx設定（conf.py）
```python
# Mermaidの出力形式（'raw', 'png', 'svg'）
mermaid_output_format = 'raw'

# Mermaidのバージョン
mermaid_version = '11.2.0'

# Mermaidの初期化コード
mermaid_init_js = """
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    themeVariables: {
        fontFamily: 'Arial, sans-serif',
        fontSize: '14px'
    }
});
"""

# 全てのMermaid図でズーム機能を有効化
mermaid_d3_zoom = True
```

### 重要：init設定について
**Sphinx環境では `%%{init: {"theme": "default"}}%%` を使用しないでください。**
- Sphinxのconf.pyで一括設定するため、個別のinit設定は不要
- init設定があるとエラーが発生する場合があります

## 図表タイプ別ルール

### 1. シーケンス図（sequenceDiagram）

#### 基本構文
```rst
.. mermaid::

   sequenceDiagram
      participant Client as 主アクター名
      participant WebApp as Webアプリケーション
      participant Service as 処理制御名
      participant DB as エンティティ名
      participant External as 外部アクター名

      Client->>WebApp: 操作実行
      WebApp->>Service: 処理要求
      Service->>DB: データ検証
      DB-->>Service: 検証結果
```

#### 参加者（participant）の命名ルール
- **予約語を避ける**: `Actor` は使用不可 → `Client`, `User` を使用
- **日本語エイリアス**: `as 日本語名` で日本語表示
- **統一アーキテクチャ**: フロントエンド・バックエンド一体型
  - `Client` - ユーザー・クライアント
  - `WebApp` - Webアプリケーション（画面+API統合）
  - `Service` - ビジネスロジック層
  - `DB` - データベース・エンティティ層
  - `External` - 外部システム

#### 矢印の使い分け
- **`->>`**: 同期呼び出し（レスポンスを待つ）
- **`-->>`**: 非同期レスポンス（戻り値）
- **`->>`**: 通知・イベント（レスポンス不要）

#### 条件分岐構文
```rst
alt 条件A
    Service-->>WebApp: 成功レスポンス
    WebApp-->>Client: データ返却
else 条件B
    Service-->>WebApp: エラーレスポンス
    WebApp-->>Client: エラー通知
end
```

#### オプション構文
```rst
opt エラーが発生した場合
    Service->>Logger: エラーログ出力
    Logger-->>Service: ログ記録完了
end
```

#### ループ構文
```rst
loop 複数件処理
    Service->>DB: データ処理
    DB-->>Service: 処理完了
end
```

### 2. フローチャート（graph）

#### 基本構文
```rst
.. mermaid::

   graph TD
      Start([開始])
      Process[処理]
      Decision{判定}
      End([終了])
      
      Start --> Process
      Process --> Decision
      Decision -->|Yes| End
      Decision -->|No| Process
```

#### ノードの形状ルール
- **`[テキスト]`**: 通常処理（矩形）
- **`([テキスト])`**: 開始・終了（楕円）
- **`{テキスト}`**: 判定・分岐（菱形）
- **`((テキスト))`**: データベース（円形）

#### 方向指定
- **`TD`**: 上から下（Top Down）
- **`LR`**: 左から右（Left Right）
- **`BT`**: 下から上（Bottom Top）
- **`RL`**: 右から左（Right Left）

### 3. ER図（erDiagram）

#### 基本構文
```rst
.. mermaid::

   erDiagram
      USER ||--o{ ORDER : "has"
      ORDER ||--|{ ORDER_ITEM : "contains"
      PRODUCT ||--o{ ORDER_ITEM : "referenced by"
```

#### エンティティ名の制限
- **スペース含む名前**: ダブルクォートで囲む `"name with space"`
- **日本語名**: 基本的に使用可能だがエラーの可能性あり
- **予約語**: SQLキーワード（SELECT, FROM等）は避ける

#### 属性名の制限（重要！）
- **ドット記法**: `geo.accuracy` → **エラー** ❌
- **ハイフン**: `user-name` → **エラー** ❌  
- **クエスチョン**: `is_valid?` → **エラー** ❌
- **ダブルクォート**: `"quoted"` → **エラー** ❌
- **特殊文字**: `@`, `#`, `%`, `&` → **エラー** ❌

#### 安全な属性名
- **アンダースコア**: `geo_accuracy` → **OK** ✅
- **キャメルケース**: `geoAccuracy` → **OK** ✅
- **数字**: `field1`, `name2` → **OK** ✅
- **英数字のみ**: `userid123` → **OK** ✅

#### リレーション記法

**基本構文**: `ENTITY1 [cardinality][identification][cardinality] ENTITY2 : "label"`

**使用可能なカーディナリティ記号**:
- **`||`** - 必須・1つ（Exactly one）
- **`|o`** - オプション・0または1（Zero or one）
- **`}|`** - 必須・1つ以上（One or more）
- **`}o`** - オプション・0以上（Zero or more）

**識別関係の記号**:
- **`--`** - 識別関係（実線）
- **`..`** - 非識別関係（点線）

**正しいリレーション記法例**:
```rst
.. mermaid::

   erDiagram
      USER ||--o{ ORDER : "has"          ✅ 1対多（ユーザー必須、注文オプション）
      ORDER ||--|{ ORDER_ITEM : "contains" ✅ 1対多（識別関係）
      PRODUCT }o..o{ ORDER_ITEM : "referenced" ✅ 多対多（非識別関係）
      CUSTOMER |o--|| ADDRESS : "lives at" ✅ 1対1（顧客オプション、住所必須）
```

**使用できないリレーション記法**:
- **`|--{`** - 左側のカーディナリティ不完全 ❌
- **`||--{`** - 右側のカーディナリティ不完全 ❌
- **`||---|{`** - 識別記号が3つ ❌
- **`||~~o{`** - 無効な識別記号 ❌
- **`||<->o{`** - 矢印記号は使用不可 ❌
- **`||==o{`** - 等号記号は使用不可 ❌

**エイリアス記法（使用可能だが推奨しない）**:
- **`one or zero`** → `|o`
- **`one or more`** → `}|`
- **`zero or more`** → `}o`
- **`only one`** → `||`
- **`to`** → `--`（識別関係）
- **`optionally to`** → `..`（非識別関係）

#### 制限に対する代替案・回避策

**1. 不完全なカーディナリティの代替案**
```rst
❌ USER |--{ ORDER     （右側不完全）
✅ USER ||--o{ ORDER   （両端を明示）
✅ USER |o--o{ ORDER   （オプション関係）
```

**2. 複雑なリレーションの表現方法**
```rst
❌ A ||<->|| B         （双方向矢印は不可）
✅ A ||--|| B : "bidirectional"  （ラベルで説明）
✅ A ||--|| B : "相互参照"         （日本語ラベル）
```

**3. 条件付きリレーションの表現**
```rst
❌ A ||~~o{ B          （無効な記号）
✅ A ||..o{ B : "conditional"     （非識別関係+ラベル）
✅ A |o--o{ B : "optional link"   （オプション関係）
```

**4. 継承・特殊化の表現**
```rst
❌ PERSON ||==|| CUSTOMER  （等号記号は不可）
✅ PERSON ||--|| CUSTOMER : "is-a"     （is-a関係をラベルで）
✅ PERSON ||--|| CUSTOMER : "継承"      （継承をラベルで）

%% または別エンティティとして表現
✅ PERSON {
    string type "CUSTOMER or EMPLOYEE"
}
```

**5. 多重継承・複合関係の表現**
```rst
❌ A ||--||--|| B      （複数の識別記号は不可）
✅ A ||--|| BRIDGE : "via"
   BRIDGE ||--|| B : "to"

%% 中間エンティティを使用
✅ USER ||--|| USER_ROLE : "has"
   USER_ROLE ||--|| ROLE : "assigned"
```

**6. 時系列・履歴関係の表現**
```rst
❌ ORDER ||-->|| SHIPMENT  （矢印は不可）
✅ ORDER ||--|| SHIPMENT : "shipped as"
✅ ORDER ||--o{ ORDER_HISTORY : "has history"
```

**7. 弱エンティティの表現**
```rst
❌ CUSTOMER ||===|| DEPENDENT  （太線は不可）
✅ CUSTOMER ||--|{ DEPENDENT : "supports"  （識別関係）
✅ DEPENDENT {
    string customer_id FK "識別子の一部"
    string dependent_name PK "複合主キー"
}
```

**8. 自己参照関係の表現**
```rst
❌ EMPLOYEE ||<-|| EMPLOYEE    （矢印は不可）
✅ EMPLOYEE ||--o{ EMPLOYEE : "manages"     （自己参照）
✅ EMPLOYEE |o--|| EMPLOYEE : "reports to"  （上司関係）
```

**9. 排他的関係の表現**
```rst
❌ PAYMENT ||--XOR--|| CASH_PAYMENT  （XORは不可）
✅ PAYMENT {
    string payment_type "CASH or CREDIT"
}
   PAYMENT ||--o{ CASH_PAYMENT : "if cash"
   PAYMENT ||--o{ CREDIT_PAYMENT : "if credit"
```

**10. 集約・コンポジション関係の表現**
```rst
❌ ORDER ||◆--|| ORDER_ITEM    （ダイヤモンドは不可）
✅ ORDER ||--|{ ORDER_ITEM : "composed of"  （識別関係）
✅ DEPARTMENT ||--o{ EMPLOYEE : "contains"   （集約関係）
```

#### 属性定義の制限
```rst
.. mermaid::

   erDiagram
      USER {
          UUID user_id PK "主キー"
          VARCHAR email_address UK "メール"
          VARCHAR geo_accuracy "位置精度"  ✅ OK
          VARCHAR geo.accuracy "位置精度"  ❌ NG（ドット）
          VARCHAR user-name "ユーザー名"   ❌ NG（ハイフン）
          VARCHAR is_valid "有効フラグ"    ✅ OK
          VARCHAR is_valid? "有効？"       ❌ NG（?マーク）
      }
```

### 4. クラス図（classDiagram）

#### 基本構文
```rst
.. mermaid::

   classDiagram
      class User {
          +user_id: int
          +name: string
          +created_at: datetime
          --
          +login()
          +logout()
      }
```

## reStructuredTextでの記述ルール

### 基本記述
```rst
.. mermaid::

   [Mermaidコード]
```

### オプション付き記述
```rst
.. mermaid::
   :caption: 図のキャプション
   :name: 図のID
   :align: center

   [Mermaidコード]
```

### 外部ファイル読み込み
```rst
.. mermaid:: path/to/diagram.mmd
```

## 予約語・キーワード一覧

### sequenceDiagram で使用できない participant名
- **Actor** - Mermaidの内部予約語（`Client`や`User`を使用）
- **end** - 構文終了キーワード（括弧で囲む: `(end)`, `[end]`, `{end}`）

### sequenceDiagram の構文キーワード
- **participant** - 参加者定義
- **actor** - アクター定義  
- **as** - エイリアス定義
- **activate/deactivate** - アクティベーション制御
- **Note** - ノート追加
- **loop/end** - ループ構造
- **alt/else/end** - 条件分岐
- **opt/end** - オプション処理
- **par/and/end** - 並列処理
- **critical/option/end** - クリティカル領域
- **break/end** - 処理中断
- **rect/end** - 背景ハイライト
- **box/end** - グループ化
- **create/destroy** - 参加者の生成・削除
- **autonumber** - シーケンス番号自動付与

### 矢印タイプ（10種類）
- **->** - 実線（矢印なし）
- **-->** - 点線（矢印なし）
- **->>** - 実線（矢印あり）
- **-->>** - 点線（矢印あり）
- **<<->>** - 実線（双方向矢印）v11.0.0+
- **<<-->>** - 点線（双方向矢印）v11.0.0+
- **-x** - 実線（×終端）
- **--x** - 点線（×終端）
- **-)** - 実線（非同期矢印）
- **--)** - 点線（非同期矢印）

### flowchart の予約語
- **graph** - フローチャート定義
- **flowchart** - フローチャート定義（新記法）
- **subgraph/end** - サブグラフ定義
- **click** - クリックイベント
- **class** - スタイル適用
- **classDef** - スタイル定義

### 共通予約語
- **%%** - コメント記号
- **end** - 各構文の終了キーワード
- **direction** - 方向指定（TD, LR, BT, RL）

## 日本語対応ルール

### 使用可能な日本語
- **エイリアス**: `participant Client as クライアント`
- **ラベル**: `Client->>Server: データ送信`
- **ノードテキスト**: `Process[データ処理]`

### 避けるべき日本語使用
- **参加者名**: `participant クライアント` ❌
- **変数名**: `クライアント->>サーバー` ❌
- **予約語との競合**: `participant Actor as アクター` ❌

## エラー対策

### よくあるエラーと解決方法

#### 1. 参加者名エラー
```
❌ participant Actor as アクター
✅ participant Client as アクター
```

#### 2. インデントエラー
```rst
❌ .. mermaid::
sequenceDiagram

✅ .. mermaid::

   sequenceDiagram
```

#### 3. 日本語文字化け
- conf.pyのフォント設定を確認
- `fontFamily: 'Arial, sans-serif'` を使用

#### 4. 複雑すぎる図表
- 図を分割して複数の図にする
- 参加者数を5個以下に制限
- 矢印の数を10本以下に制限

## ベストプラクティス

### 1. 図表の分割
- **1つの図**: 1つの機能・フロー
- **複雑な処理**: 複数の図に分割
- **レイヤー別**: 概念レベル・実装レベルで分離

### 2. 命名統一
- **アクター名**: domain_model.rstと統一
- **システム名**: 全図表で統一
- **用語**: 用語集と統一

### 3. 図表配置
- **ユースケース**: シーケンス図
- **画面遷移**: フローチャート
- **データ構造**: ER図・クラス図
- **システム構成**: フローチャート

### 4. キャプション・説明
```rst
.. mermaid::
   :caption: ユーザー登録処理のシーケンス図

   sequenceDiagram
      ...
```

## テンプレート

### シーケンス図テンプレート
```rst
.. mermaid::
   :caption: [処理名]のシーケンス図

   sequenceDiagram
      participant Client as [アクター名]
      participant WebApp as [システム名]
      participant Service as [サービス名]
      participant DB as [データ名]

      Client->>WebApp: [操作名]
      WebApp->>Service: [処理要求]
      Service->>DB: [データ操作]
      DB-->>Service: [結果]
      Service-->>WebApp: [処理完了]
      WebApp-->>Client: [画面表示]
```

### 条件分岐テンプレート
```rst
.. mermaid::

   sequenceDiagram
      participant A as システムA
      participant B as システムB

      A->>B: 処理要求
      
      alt 成功の場合
          B-->>A: 成功レスポンス
      else エラーの場合
          B-->>A: エラーレスポンス
      else システムエラーの場合
          B-->>A: システムエラー
      end
```

## チェックリスト

### 図表作成時
- [ ] 参加者名に予約語（Actor等）を使用していない
- [ ] 日本語はエイリアスとラベルのみ使用
- [ ] インデントが正しい（.. mermaid::の後に空行、2スペース以上インデント）
- [ ] 参加者数が5個以下
- [ ] 矢印の使い分けが正しい（->>と-->>）
- [ ] キャプションが設定されている

### ビルド前確認
- [ ] Sphinxビルドでエラーが出ない
- [ ] 図表が正しく表示される
- [ ] 日本語が文字化けしていない
- [ ] ズーム機能が動作する

## 参考リンク

- [Mermaid公式ドキュメント](https://mermaid.js.org/)
- [sphinxcontrib-mermaid](https://github.com/mgaitan/sphinxcontrib-mermaid)
- [Mermaidライブエディタ](https://mermaid.live/) 