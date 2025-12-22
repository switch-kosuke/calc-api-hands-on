"""掛け算API (multiply) のユニットテスト

100%カバレッジを目指した包括的なテストケース
"""
import sys
import os
import json
import pytest
from unittest.mock import Mock

# パス設定
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from multiply import main as multiply_main


def create_mock_request(params: dict) -> Mock:
    """モックのHttpRequestオブジェクトを作成"""
    req = Mock()
    req.params = params
    return req


class TestMultiplyNormalCases:
    """掛け算API 正常系テスト"""
    
    def test_positive_integers(self):
        """正の整数の掛け算"""
        req = create_mock_request({'A': '3', 'B': '4'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 12
        assert body['success'] is True
        assert 'application/json' in response.headers['Content-Type']
    
    def test_negative_integers(self):
        """負の整数の掛け算"""
        req = create_mock_request({'A': '-5', 'B': '3'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == -15
        assert body['success'] is True
    
    def test_decimal_numbers(self):
        """小数の掛け算"""
        req = create_mock_request({'A': '2.5', 'B': '4.0'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 10.0
        assert body['success'] is True
    
    def test_mixed_integer_and_decimal(self):
        """整数と小数の混在"""
        req = create_mock_request({'A': '5', 'B': '1.5'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 7.5
        assert body['success'] is True
    
    def test_multiply_by_zero(self):
        """0を含む掛け算"""
        req = create_mock_request({'A': '10', 'B': '0'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 0
        assert body['success'] is True
    
    def test_lowercase_parameters(self):
        """小文字パラメータ (a, b)"""
        req = create_mock_request({'a': '6', 'b': '7'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 42
        assert body['success'] is True
    
    def test_negative_both(self):
        """両方とも負の数"""
        req = create_mock_request({'A': '-3', 'B': '-4'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 12
        assert body['success'] is True
    
    def test_large_numbers(self):
        """大きな数値の掛け算"""
        req = create_mock_request({'A': '1000', 'B': '2000'})
        response = multiply_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 2000000
        assert body['success'] is True


class TestMultiplyErrorCases:
    """掛け算API 異常系テスト"""
    
    def test_missing_parameter_a(self):
        """パラメータAが欠落"""
        req = create_mock_request({'B': '5'})
        response = multiply_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_missing_parameter_b(self):
        """パラメータBが欠落"""
        req = create_mock_request({'A': '5'})
        response = multiply_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_missing_both_parameters(self):
        """両方のパラメータが欠落"""
        req = create_mock_request({})
        response = multiply_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_non_numeric_parameter_a(self):
        """パラメータAが数値以外"""
        req = create_mock_request({'A': 'abc', 'B': '5'})
        response = multiply_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBは数値である必要があります"
        assert body['success'] is False
    
    def test_non_numeric_parameter_b(self):
        """パラメータBが数値以外"""
        req = create_mock_request({'A': '5', 'B': 'xyz'})
        response = multiply_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBは数値である必要があります"
        assert body['success'] is False
    
    def test_empty_parameter_a(self):
        """パラメータAが空文字列"""
        req = create_mock_request({'A': '', 'B': '5'})
        response = multiply_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_empty_parameter_b(self):
        """パラメータBが空文字列"""
        req = create_mock_request({'A': '5', 'B': ''})
        response = multiply_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
