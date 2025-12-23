# Calc API Hands-on

Azure Functions (Python 3.11) を使った掛け算・割り算APIプロジェクト

## 📋 概要

このプロジェクトは、2つの数値パラメータを受け取り、掛け算または割り算を行うHTTP Trigger APIを提供します。

### API エンドポイント

- **GET /multiply** - 2つの数値の掛け算
- **GET /divide** - 2つの数値の割り算

## 🚀 クイックスタート

### 前提条件

- Python 3.11
- Azure Functions Core Tools v4
- Azure CLI (デプロイ時)

### ローカル開発

1. **依存パッケージのインストール**
   ```bash
   cd src
   pip install -r requirements.txt
   ```

2. **Azure Functions をローカルで起動**
   ```bash
   cd src
   func start
   ```

3. **APIをテスト**
   ```bash
   # 掛け算
   curl "http://localhost:7071/multiply?A=3&B=4"
   
   # 割り算
   curl "http://localhost:7071/divide?A=12&B=4"
   ```

## 🧪 テスト

### ユニットテスト

```bash
cd tests
pip install -r requirements.txt
pytest test_multiply.py test_divide.py test_utils.py -v
```

### カバレッジ測定

```bash
cd tests
pytest test_multiply.py test_divide.py test_utils.py --cov=../src --cov-report=term --cov-report=html
```

### 統合テスト

```bash
# 別ターミナルでAzure Functionsを起動
cd src
func start

# 統合テストを実行
cd tests
pytest test_integration.py -v
```

## 📁 プロジェクト構造

```
calc-api-hands-on/
├── src/                      # Azure Functions ソースコード
│   ├── multiply/             # 掛け算API
│   │   ├── __init__.py       # メイン処理
│   │   └── function.json     # HTTP Trigger設定
│   ├── divide/               # 割り算API
│   │   ├── __init__.py       # メイン処理
│   │   └── function.json     # HTTP Trigger設定
│   ├── shared/               # 共通ユーティリティ
│   │   └── utils.py          # パラメータ処理・レスポンス生成
│   ├── host.json             # Functions全体設定 (CORS含む)
│   ├── requirements.txt      # Python依存パッケージ
│   └── local.settings.json   # ローカル開発設定
├── tests/                    # テストコード
│   ├── test_multiply.py      # 掛け算APIユニットテスト
│   ├── test_divide.py        # 割り算APIユニットテスト
│   ├── test_utils.py         # 共通ユーティリティユニットテスト
│   ├── test_integration.py   # 統合テスト
│   └── requirements.txt      # テスト用依存パッケージ
├── docs/                     # ドキュメント
│   ├── requirements.md       # 機能要件
│   └── nonrequirements.md    # 非機能要件
└── .github/
    └── workflows/
        └── deploy.yml        # GitHub Actions CI/CD設定
```

## 📖 API仕様

### 共通仕様

- **HTTPメソッド**: GET
- **Content-Type**: `application/json; charset=utf-8`
- **パラメータ**: A/a (第1引数), B/b (第2引数) - 大文字・小文字どちらも可

### レスポンス形式

**成功時 (200 OK)**
```json
{
  "result": 12.0,
  "success": true
}
```

**エラー時 (400 Bad Request)**
```json
{
  "error": "エラーメッセージ",
  "success": false
}
```

### エラーケース

- `パラメータAとBの両方が必要です` - パラメータ不足
- `パラメータAとBは数値である必要があります` - 数値以外の入力
- `0で割ることはできません` - ゼロ除算 (divideのみ)

## 🔧 デプロイ

### GitHub Actionsによる自動デプロイ

1. **Azure Function Appの作成**
   ```bash
   az functionapp create \
     --resource-group <resource-group> \
     --consumption-plan-location japaneast \
     --runtime python \
     --runtime-version 3.11 \
     --functions-version 4 \
     --name <function-app-name> \
     --storage-account <storage-account>
   ```

2. **GitHub Secretsの設定**
   - リポジトリの Settings > Secrets and variables > Actions
   - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` を追加
   - 値: Azure PortalからFunction Appの「発行プロファイルの取得」で取得

3. **`.github/workflows/deploy.yml` のデプロイステップを有効化**
   - コメントアウトを解除
   - `<YOUR_FUNCTION_APP_NAME>` を実際の名前に変更

4. **プッシュでデプロイ実行**
   ```bash
   git push origin main
   ```

### 手動デプロイ

```bash
cd src
func azure functionapp publish <function-app-name>
```

## 📚 参考資料

- [Azure Functions Python開発者ガイド](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python)
- [requirements.md](docs/requirements.md) - 機能要件
- [nonrequirements.md](docs/nonrequirements.md) - 非機能要件

## 📄 ライセンス

このプロジェクトはハンズオン用のサンプルコードです。
