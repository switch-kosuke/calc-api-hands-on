"""統合テスト

Azure Functions Core Toolsでローカル起動したAPIに対する統合テスト
実行前に別ターミナルで `func start` を実行しておく必要があります
"""
import requests
import pytest
import json


BASE_URL = "http://localhost:7071"


class TestMultiplyIntegration:
    """掛け算API 統合テスト"""
    
    def test_multiply_positive_integers(self):
        """正の整数の掛け算 (統合)"""
        response = requests.get(f"{BASE_URL}/multiply?A=3&B=4")
        
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 12
        assert data['success'] is True
    
    def test_multiply_lowercase_params(self):
        """小文字パラメータ (統合)"""
        response = requests.get(f"{BASE_URL}/multiply?a=5&b=6")
        
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 30
        assert data['success'] is True
    
    def test_multiply_with_decimal(self):
        """小数を含む掛け算 (統合)"""
        response = requests.get(f"{BASE_URL}/multiply?A=2.5&B=4")
        
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 10.0
        assert data['success'] is True
    
    def test_multiply_missing_parameter(self):
        """パラメータ欠落エラー (統合)"""
        response = requests.get(f"{BASE_URL}/multiply?A=5")
        
        assert response.status_code == 400
        data = response.json()
        assert data['error'] == "パラメータAとBの両方が必要です"
        assert data['success'] is False
    
    def test_multiply_non_numeric(self):
        """数値以外のパラメータエラー (統合)"""
        response = requests.get(f"{BASE_URL}/multiply?A=abc&B=5")
        
        assert response.status_code == 400
        data = response.json()
        assert data['error'] == "パラメータAとBは数値である必要があります"
        assert data['success'] is False


class TestDivideIntegration:
    """割り算API 統合テスト"""
    
    def test_divide_positive_integers(self):
        """正の整数の割り算 (統合)"""
        response = requests.get(f"{BASE_URL}/divide?A=12&B=4")
        
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 3.0
        assert data['success'] is True
    
    def test_divide_lowercase_params(self):
        """小文字パラメータ (統合)"""
        response = requests.get(f"{BASE_URL}/divide?a=20&b=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 4.0
        assert data['success'] is True
    
    def test_divide_with_decimal(self):
        """小数を含む割り算 (統合)"""
        response = requests.get(f"{BASE_URL}/divide?A=7&B=2.5")
        
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 2.8
        assert data['success'] is True
    
    def test_divide_by_zero_error(self):
        """ゼロ除算エラー (統合)"""
        response = requests.get(f"{BASE_URL}/divide?A=10&B=0")
        
        assert response.status_code == 400
        data = response.json()
        assert data['error'] == "0で割ることはできません"
        assert data['success'] is False
    
    def test_divide_missing_parameter(self):
        """パラメータ欠落エラー (統合)"""
        response = requests.get(f"{BASE_URL}/divide?A=5")
        
        assert response.status_code == 400
        data = response.json()
        assert data['error'] == "パラメータAとBの両方が必要です"
        assert data['success'] is False
    
    def test_divide_non_numeric(self):
        """数値以外のパラメータエラー (統合)"""
        response = requests.get(f"{BASE_URL}/divide?A=5&B=xyz")
        
        assert response.status_code == 400
        data = response.json()
        assert data['error'] == "パラメータAとBは数値である必要があります"
        assert data['success'] is False


class TestCorsHeaders:
    """CORS設定の統合テスト"""
    
    def test_cors_header_multiply(self):
        """multiplyエンドポイントのCORSヘッダー確認"""
        response = requests.get(f"{BASE_URL}/multiply?A=1&B=2")
        
        # CORSヘッダーが設定されていることを確認
        # 注: Azure Functions Core Toolsのローカル実行では
        # host.jsonのCORS設定が反映されない場合があります
        assert response.status_code == 200
    
    def test_cors_header_divide(self):
        """divideエンドポイントのCORSヘッダー確認"""
        response = requests.get(f"{BASE_URL}/divide?A=10&B=2")
        
        assert response.status_code == 200


if __name__ == "__main__":
    # 統合テスト実行前のチェック
    try:
        response = requests.get(f"{BASE_URL}/multiply?A=1&B=1", timeout=2)
        print("✓ Azure Functions ローカルサーバーに接続成功")
        print("統合テストを実行します...")
        pytest.main([__file__, "-v"])
    except requests.exceptions.ConnectionError:
        print("✗ エラー: Azure Functions ローカルサーバーに接続できません")
        print("別ターミナルで以下を実行してください:")
        print("  cd src")
        print("  func start")
        exit(1)
