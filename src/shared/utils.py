"""共通ユーティリティ関数

Azure Functions用の共通処理を提供します。
"""
import json
from typing import Tuple, Optional, Any


def get_numeric_params(req) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    HTTPリクエストからパラメータA, Bを取得し、数値に変換します。
    大文字・小文字両方のパラメータ名に対応します。
    
    Args:
        req: Azure Functions HttpRequest オブジェクト
        
    Returns:
        Tuple[Optional[float], Optional[float], Optional[str]]:
            (パラメータA, パラメータB, エラーメッセージ)
            成功時はエラーメッセージはNone
    """
    # パラメータの取得 (大文字・小文字両方対応)
    param_a = req.params.get('A') or req.params.get('a')
    param_b = req.params.get('B') or req.params.get('b')
    
    # パラメータの存在チェック (Noneまたは空文字列)
    if param_a is None or param_b is None or param_a == '' or param_b == '':
        return None, None, "パラメータAとBの両方が必要です"
    
    # 数値変換
    try:
        a = float(param_a)
        b = float(param_b)
        return a, b, None
    except (ValueError, TypeError):
        return None, None, "パラメータAとBは数値である必要があります"


def create_success_response(result: float) -> Tuple[str, int, dict]:
    """
    成功レスポンスを生成します。
    
    Args:
        result: 計算結果
        
    Returns:
        Tuple[str, int, dict]: (JSONボディ, ステータスコード, ヘッダー)
    """
    body = json.dumps({
        "result": result,
        "success": True
    }, ensure_ascii=False)
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    return body, 200, headers


def create_error_response(error_message: str) -> Tuple[str, int, dict]:
    """
    エラーレスポンスを生成します。
    
    Args:
        error_message: エラーメッセージ
        
    Returns:
        Tuple[str, int, dict]: (JSONボディ, ステータスコード, ヘッダー)
    """
    body = json.dumps({
        "error": error_message,
        "success": False
    }, ensure_ascii=False)
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    return body, 400, headers
