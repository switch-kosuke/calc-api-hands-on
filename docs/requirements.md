# 機能要件仕様書

## 1. 概要
Azure Functions (Python) を使用した電卓APIシステム。掛け算と割り算の2つの演算機能をHTTP APIとして提供する。

## 2. API仕様

### 2.1 掛け算API

#### エンドポイント
```
GET /multiply
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|------------|-----|------|------|
| A または a | number | ○ | 被乗数(整数または小数) |
| B または b | number | ○ | 乗数(整数または小数) |

**注**: パラメータ名は大文字(A, B)と小文字(a, b)の両方を受け付ける。

#### リクエスト例
```
GET /multiply?A=10&B=5
GET /multiply?a=3.5&b=2.5
```

#### 正常レスポンス
```json
{
  "result": 50,
  "success": true
}
```

### 2.2 割り算API

#### エンドポイント
```
GET /divide
```

#### クエリパラメータ
| パラメータ名 | 型 | 必須 | 説明 |
|------------|-----|------|------|
| A または a | number | ○ | 被除数(整数または小数) |
| B または b | number | ○ | 除数(整数または小数、0以外) |

**注**: パラメータ名は大文字(A, B)と小文字(a, b)の両方を受け付ける。

#### リクエスト例
```
GET /divide?A=10&B=2
GET /divide?a=7.5&b=2.5
```

#### 正常レスポンス
```json
{
  "result": 5,
  "success": true
}
```

**注**: 計算結果の小数点以下の桁数に制限はなく、Python の浮動小数点演算の精度に従う。

## 3. 入力検証ルール

### 3.1 受け付ける値
- **整数**: 正の整数、負の整数、0
  - 例: `-100`, `0`, `42`, `999`
- **小数(浮動小数点数)**: 正の小数、負の小数
  - 例: `-3.14`, `0.5`, `123.456`
- **数値範囲**: Python の float 型で表現可能な範囲内であれば無制限

### 3.2 受け付けない値
- 文字列(数値に変換できないもの)
  - 例: `"abc"`, `"hello"`, `"1a2b"`
- null, undefined, 空文字列
- Boolean値
- その他の非数値型

## 4. エラーハンドリング

### 4.1 エラーレスポンス形式
```json
{
  "error": "エラーメッセージ",
  "success": false
}
```

### 4.2 エラーケース

#### 4.2.1 クエリパラメータ不足
**条件**: A または B のパラメータが存在しない

**エラーメッセージ例**:
```json
{
  "error": "パラメータAとBの両方が必要です",
  "success": false
}
```

#### 4.2.2 数値以外の入力
**条件**: A または B が数値に変換できない

**エラーメッセージ例**:
```json
{
  "error": "パラメータAとBは数値である必要があります",
  "success": false
}
```

#### 4.2.3 ゼロ除算(割り算APIのみ)
**条件**: 割り算APIで B = 0

**エラーメッセージ例**:
```json
{
  "error": "0で割ることはできません",
  "success": false
}
```

## 5. レスポンス仕様

### 5.1 HTTPステータスコード
- **正常時**: 200 OK
- **エラー時**: 400 Bad Request

### 5.2 Content-Type
```
application/json
```

### 5.3 文字エンコーディング
```
UTF-8
```

## 6. テスト要件

### 6.1 テストカバレッジ
- **目標**: 100%
- **対象**: すべての関数、すべての分岐、すべてのエラーパス

### 6.2 テストケース

#### 6.2.1 正常系テスト
- 正の整数同士の演算
- 負の整数同士の演算
- 小数同士の演算
- 整数と小数の混在演算
- 0を含む演算(掛け算のみ)
- 大文字パラメータ(A, B)
- 小文字パラメータ(a, b)

#### 6.2.2 異常系テスト
- パラメータA欠落
- パラメータB欠落
- 両パラメータ欠落
- 数値以外の文字列入力
- 空文字列入力
- ゼロ除算(割り算)

## 7. 制約事項

### 7.1 数値範囲
- Python の float 型の範囲内(-1.7976931348623157e+308 ～ 1.7976931348623157e+308)
- 範囲外の値は Python のランタイムエラーとなる

### 7.2 精度
- 浮動小数点演算の精度は Python の実装に依存
- 丸め誤差が発生する可能性がある

### 7.3 HTTPメソッド
- GET のみをサポート
- POST, PUT, DELETE などは未サポート

## 8. 具体的なテストシナリオ例

### 8.1 掛け算API
```
# 正常系
GET /multiply?A=10&B=5        → {"result": 50, "success": true}
GET /multiply?a=3&b=7          → {"result": 21, "success": true}
GET /multiply?A=-5&B=4         → {"result": -20, "success": true}
GET /multiply?a=2.5&b=4        → {"result": 10.0, "success": true}
GET /multiply?A=0&B=100        → {"result": 0, "success": true}

# 異常系
GET /multiply?A=10             → {"error": "パラメータAとBの両方が必要です", "success": false}
GET /multiply?A=abc&B=5        → {"error": "パラメータAとBは数値である必要があります", "success": false}
```

### 8.2 割り算API
```
# 正常系
GET /divide?A=10&B=2           → {"result": 5.0, "success": true}
GET /divide?a=15&b=3           → {"result": 5.0, "success": true}
GET /divide?A=-10&B=2          → {"result": -5.0, "success": true}
GET /divide?a=7.5&b=2.5        → {"result": 3.0, "success": true}

# 異常系
GET /divide?A=10&B=0           → {"error": "0で割ることはできません", "success": false}
GET /divide?B=5                → {"error": "パラメータAとBの両方が必要です", "success": false}
GET /divide?A=hello&B=5        → {"error": "パラメータAとBは数値である必要があります", "success": false}
```
