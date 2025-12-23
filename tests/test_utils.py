"""共通ユーティリティ (shared/utils.py) のユニットテスト

shared/utils.pyの各関数を直接テストします。
"""
import sys
import os
import json
import pytest
from unittest.mock import Mock

# パス設定
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from shared.utils import get_numeric_params, create_success_response, create_error_response


def create_mock_request(params: dict) -> Mock:
    """モックのHttpRequestオブジェクトを作成"""
    req = Mock()
    req.params = params
    return req


class TestGetNumericParams:
    """get_numeric_params関数のテスト"""
    
    def test_valid_uppercase_parameters(self):
        """正常: 大文字パラメータA, B"""
        req = create_mock_request({'A': '10', 'B': '20'})
        a, b, error = get_numeric_params(req)
        
        assert a == 10.0
        assert b == 20.0
        assert error is None
    
    def test_valid_lowercase_parameters(self):
        """正常: 小文字パラメータa, b"""
        req = create_mock_request({'a': '5.5', 'b': '3.3'})
        a, b, error = get_numeric_params(req)
        
        assert a == 5.5
        assert b == 3.3
        assert error is None
    
    def test_valid_negative_numbers(self):
        """正常: 負の数値"""
        req = create_mock_request({'A': '-10', 'B': '-5'})
        a, b, error = get_numeric_params(req)
        
        assert a == -10.0
        assert b == -5.0
        assert error is None
    
    def test_valid_zero_values(self):
        """正常: ゼロの値"""
        req = create_mock_request({'A': '0', 'B': '0'})
        a, b, error = get_numeric_params(req)
        
        assert a == 0.0
        assert b == 0.0
        assert error is None
    
    def test_missing_parameter_a(self):
        """異常: パラメータAが欠落"""
        req = create_mock_request({'B': '10'})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBの両方が必要です"
    
    def test_missing_parameter_b(self):
        """異常: パラメータBが欠落"""
        req = create_mock_request({'A': '10'})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBの両方が必要です"
    
    def test_missing_both_parameters(self):
        """異常: 両方のパラメータが欠落"""
        req = create_mock_request({})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBの両方が必要です"
    
    def test_empty_parameter_a(self):
        """異常: パラメータAが空文字列"""
        req = create_mock_request({'A': '', 'B': '10'})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBの両方が必要です"
    
    def test_empty_parameter_b(self):
        """異常: パラメータBが空文字列"""
        req = create_mock_request({'A': '10', 'B': ''})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBの両方が必要です"
    
    def test_non_numeric_parameter_a(self):
        """異常: パラメータAが数値以外"""
        req = create_mock_request({'A': 'abc', 'B': '10'})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBは数値である必要があります"
    
    def test_non_numeric_parameter_b(self):
        """異常: パラメータBが数値以外"""
        req = create_mock_request({'A': '10', 'B': 'xyz'})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBは数値である必要があります"
    
    def test_both_parameters_non_numeric(self):
        """異常: 両方のパラメータが数値以外"""
        req = create_mock_request({'A': 'abc', 'B': 'xyz'})
        a, b, error = get_numeric_params(req)
        
        assert a is None
        assert b is None
        assert error == "パラメータAとBは数値である必要があります"


class TestCreateSuccessResponse:
    """create_success_response関数のテスト"""
    
    def test_positive_integer_result(self):
        """正の整数結果"""
        body, status_code, headers = create_success_response(42)
        
        assert status_code == 200
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['result'] == 42
        assert data['success'] is True
    
    def test_negative_result(self):
        """負の数値結果"""
        body, status_code, headers = create_success_response(-10.5)
        
        assert status_code == 200
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['result'] == -10.5
        assert data['success'] is True
    
    def test_zero_result(self):
        """ゼロの結果"""
        body, status_code, headers = create_success_response(0)
        
        assert status_code == 200
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['result'] == 0
        assert data['success'] is True
    
    def test_decimal_result(self):
        """小数結果"""
        body, status_code, headers = create_success_response(3.14159)
        
        assert status_code == 200
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['result'] == 3.14159
        assert data['success'] is True
    
    def test_large_result(self):
        """大きな数値結果"""
        body, status_code, headers = create_success_response(1000000)
        
        assert status_code == 200
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['result'] == 1000000
        assert data['success'] is True


class TestCreateErrorResponse:
    """create_error_response関数のテスト"""
    
    def test_missing_params_error(self):
        """パラメータ不足エラー"""
        error_msg = "パラメータAとBの両方が必要です"
        body, status_code, headers = create_error_response(error_msg)
        
        assert status_code == 400
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['error'] == error_msg
        assert data['success'] is False
    
    def test_non_numeric_error(self):
        """数値以外エラー"""
        error_msg = "パラメータAとBは数値である必要があります"
        body, status_code, headers = create_error_response(error_msg)
        
        assert status_code == 400
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['error'] == error_msg
        assert data['success'] is False
    
    def test_divide_by_zero_error(self):
        """ゼロ除算エラー"""
        error_msg = "0で割ることはできません"
        body, status_code, headers = create_error_response(error_msg)
        
        assert status_code == 400
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['error'] == error_msg
        assert data['success'] is False
    
    def test_custom_error_message(self):
        """カスタムエラーメッセージ"""
        error_msg = "カスタムエラーです"
        body, status_code, headers = create_error_response(error_msg)
        
        assert status_code == 400
        assert headers['Content-Type'] == 'application/json; charset=utf-8'
        
        data = json.loads(body)
        assert data['error'] == error_msg
        assert data['success'] is False
    
    def test_japanese_error_message(self):
        """日本語エラーメッセージのエンコーディング確認"""
        error_msg = "日本語のエラーメッセージです"
        body, status_code, headers = create_error_response(error_msg)
        
        assert status_code == 400
        # JSONが正しくデコードできることを確認
        data = json.loads(body)
        assert data['error'] == error_msg
        assert data['success'] is False
