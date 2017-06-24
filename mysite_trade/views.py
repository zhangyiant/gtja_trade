from django.shortcuts import render
from django.http import (
    HttpResponse,
    JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from stock_db.db_connection import get_default_db_connection
from stock_db.db_stock import StockInfo
from gtja.utility import (
    complete_buy_transaction,
    complete_sell_transaction)
import json

# Create your views here.
def index(request):
    return HttpResponse("HelloWorld")

@csrf_exempt
def buy_view(request):
    data = json.loads(request.body.decode("utf-8"))
    symbol = data["symbol"]
    price = data["price"]
    quantity = data["quantity"]
    try:
        complete_buy_transaction(symbol, price, quantity)
        return JsonResponse({"result": "OK"})
    except Exception as e:
        return JsonResponse({"result": "error",
                             "exception": "{0}".format(e)})

@csrf_exempt
def sell_view(request):
    data = json.loads(request.body.decode("utf-8"))
    symbol = data["symbol"]
    price = data["price"]
    quantity = data["quantity"]
    try:
        complete_sell_transaction(symbol, price, quantity)
        return JsonResponse({"result": "OK"})
    except Exception as e:
        return JsonResponse({"result": "error",
                             "exception": "{0}".format(e)})

def stock_info_view(request):
    conn = get_default_db_connection()
    session = conn.create_session()
    results = []
    stock_infos = session.query(StockInfo).all()
    for stock_info in stock_infos:
        stock_info_dict = {"symbol": stock_info.symbol,
                 "name": stock_info.name}
        results.append(stock_info_dict)
    return JsonResponse({"results": results})
