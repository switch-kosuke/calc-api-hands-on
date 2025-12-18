"""掛け算API

2つの数値パラメータA, Bの掛け算を行うHTTP Trigger関数です。
"""
import logging
import azure.functions as func
import sys
import os

# sharedモジュールをインポートするためのパス設定
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.utils import get_numeric_params, create_success_response, create_error_response


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    掛け算APIのメイン処理
    
    Args:
        req: HTTPリクエスト
        
    Returns:
        func.HttpResponse: HTTPレスポンス
    """
    logging.info('Multiply function processed a request.')
    
    # パラメータの取得と検証
    a, b, error = get_numeric_params(req)
    
    if error:
        body, status_code, headers = create_error_response(error)
        return func.HttpResponse(
            body=body,
            status_code=status_code,
            headers=headers
        )
    
    # 掛け算の実行
    result = a * b
    
    # 成功レスポンスの生成
    body, status_code, headers = create_success_response(result)
    return func.HttpResponse(
        body=body,
        status_code=status_code,
        headers=headers
    )
