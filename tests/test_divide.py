"""割り算API (divide) のユニットテスト

100%カバレッジを目指した包括的なテストケース
"""
import sys
import os
import json
import pytest
from unittest.mock import Mock

# パス設定
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from divide import main as divide_main


def create_mock_request(params: dict) -> Mock:
    """モックのHttpRequestオブジェクトを作成"""
    req = Mock()
    req.params = params
    return req


class TestDivideNormalCases:
    """割り算API 正常系テスト"""
    
    def test_positive_integers(self):
        """正の整数の割り算"""
        req = create_mock_request({'A': '12', 'B': '4'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 3.0
        assert body['success'] is True
        assert 'application/json' in response.headers['Content-Type']
    
    def test_negative_dividend(self):
        """被除数が負の数"""
        req = create_mock_request({'A': '-15', 'B': '3'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == -5.0
        assert body['success'] is True
    
    def test_negative_divisor(self):
        """除数が負の数"""
        req = create_mock_request({'A': '15', 'B': '-3'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == -5.0
        assert body['success'] is True
    
    def test_decimal_numbers(self):
        """小数の割り算"""
        req = create_mock_request({'A': '10.5', 'B': '2.0'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 5.25
        assert body['success'] is True
    
    def test_mixed_integer_and_decimal(self):
        """整数と小数の混在"""
        req = create_mock_request({'A': '7', 'B': '2.5'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 2.8
        assert body['success'] is True
    
    def test_lowercase_parameters(self):
        """小文字パラメータ (a, b)"""
        req = create_mock_request({'a': '20', 'b': '5'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 4.0
        assert body['success'] is True
    
    def test_negative_both(self):
        """両方とも負の数"""
        req = create_mock_request({'A': '-12', 'B': '-4'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 3.0
        assert body['success'] is True
    
    def test_zero_dividend(self):
        """0を割る"""
        req = create_mock_request({'A': '0', 'B': '5'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 0.0
        assert body['success'] is True
    
    def test_large_numbers(self):
        """大きな数値の割り算"""
        req = create_mock_request({'A': '1000000', 'B': '2000'})
        response = divide_main(req)
        
        assert response.status_code == 200
        body = json.loads(response.get_body())
        assert body['result'] == 500.0
        assert body['success'] is True


class TestDivideErrorCases:
    """割り算API 異常系テスト"""
    
    def test_divide_by_zero(self):
        """ゼロ除算エラー"""
        req = create_mock_request({'A': '10', 'B': '0'})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "0で割ることはできません"
        assert body['success'] is False
    
    def test_missing_parameter_a(self):
        """パラメータAが欠落"""
        req = create_mock_request({'B': '5'})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_missing_parameter_b(self):
        """パラメータBが欠落"""
        req = create_mock_request({'A': '5'})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_missing_both_parameters(self):
        """両方のパラメータが欠落"""
        req = create_mock_request({})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_non_numeric_parameter_a(self):
        """パラメータAが数値以外"""
        req = create_mock_request({'A': 'abc', 'B': '5'})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBは数値である必要があります"
        assert body['success'] is False
    
    def test_non_numeric_parameter_b(self):
        """パラメータBが数値以外"""
        req = create_mock_request({'A': '5', 'B': 'xyz'})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBは数値である必要があります"
        assert body['success'] is False
    
    def test_empty_parameter_a(self):
        """パラメータAが空文字列"""
        req = create_mock_request({'A': '', 'B': '5'})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
    
    def test_empty_parameter_b(self):
        """パラメータBが空文字列"""
        req = create_mock_request({'A': '5', 'B': ''})
        response = divide_main(req)
        
        assert response.status_code == 400
        body = json.loads(response.get_body())
        assert body['error'] == "パラメータAとBの両方が必要です"
        assert body['success'] is False
