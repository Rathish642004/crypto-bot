from django.shortcuts import render,HttpResponseRedirect
from binance.client import Client , BinanceAPIException
from django.http import JsonResponse
from binance.client import Client
from datetime import time,datetime
import time,json
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

running=True
API_KEY = '6eXmuCXxnQq1uLMRqKeWejo0iAnl7vKs6kenNn0p8vQWMIE9eALt35FG54RtroU1'
API_SECRET = '6kkY5VGELHXGodCHCJmYj50k3atEGh7VgaI2uQE3VRiGrNCS7AEWw3yuW0GNl6Bq'
if isinstance(API_SECRET, bytes):
    API_SECRET = API_SECRET.decode('utf-8')
client = Client(API_KEY,API_SECRET, testnet=True)

def account(request):
    account_info = client.get_account()
    return render(request, 'bot_page.html', {
        'account_info': account_info,
    })

def home(request):
    account_info = client.get_account()
    return render(request, 'home.html', {
        'account_info': account_info,
    })


def buy_order_market_view(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        qty = request.POST.get('qty')
        
        buy_order_market(symbol, qty)
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def buy_order_market(symbol,qty):
    buy_order=client.order_market_buy(
        symbol=symbol,
        quantity=qty
    )
    print(buy_order)
# CORS
# CSRF
# HEADERS
# 


def sell_order_market_view(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        qty = request.POST.get('qty')
        
        sell_order_market(symbol, qty)
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def sell_order_market(symbol,qty):
  order=client.order_market_sell(
      symbol=symbol,
      quantity=qty
  )
  print(datetime.now().time())
  print(order)

def buy_order_limit_view(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        qty = request.POST.get('qty')
        price = request.POST.get('price')

        if not symbol:
            # Handle empty symbol case (e.g., return error message)
            return JsonResponse({'status': 'error', 'message': 'Symbol is required'})

        buy_order_limit(symbol, qty, price)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def buy_order_limit(symbol, qty, price):
    order = client.order_limit_buy(
        symbol=symbol,
        side="BUY",
        type="LIMIT",
        quantity=qty,
        price=price,
    )
    print('ORDER',order)

def sell_order_limit_view(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        qty = request.POST.get('qty')
        price=request.POST.get('price')
        
        sell_order_limit(symbol,qty,price)
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def sell_order_limit(symbol, qty, price):
    order = client.order_limit_buy(
        symbol=symbol,
        side="SELL",
        type="LIMIT",
        quantity=qty,
        price=price,
    )
    print('SELL',order)

def cancel_order_view(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        
        cancel_order(symbol)
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def cancel_order(symbol):
    open_orders=client.get_open_orders(symbol=symbol)
    
    if not open_orders:
        print(f'no open orders in the symbol {symbol}')
        return
    for orders in open_orders:
        order_status=client.cancel_order(symbol=symbol,orderId=orders['orderId'])
        if order_status['status'] == 'CANCELED':
            print(f"Canceled order: {orders['orderId']}")
    









def myorder(request):


    order = client.create_order(
        symbol='BTCUSDT',
        side='BUY',
        type='LIMIT',
        quantity=0.005,
        timeInForce=request.GET.get('time_in_force', 'GTC'), 
        price='69000'
    )
    print(order)
    return JsonResponse({'status': 'success'})


def market_maker(request):
    global running
    if request.method == 'POST':
        endtime_str = request.POST.get('endtime')
        symbol = request.POST.get('symbol')
        interval = int(request.POST.get('interval'))
        qty = request.POST.get('qty')      
        end_time = datetime.strptime(endtime_str, "%H:%M").time()
        start_time = datetime.now().time()

        while running:
            current_time = datetime.now().time()
            if start_time <= current_time <= end_time:
                buy_order = sell_order_market(symbol, qty)
            time.sleep(interval)
    return JsonResponse({'status': 'failed'})


def stop_market(request):
    global running
    running=False

    return JsonResponse({'status':'stopping'})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def market_make():

    symbol = "BNBUSDT"
    quantity = 0.1

    while True:

        market_price = float(client.get_symbol_ticker(symbol=symbol)["price"])


        spread_percentage = 0.01  
        buy_price = market_price - (market_price * spread_percentage)
        sell_price = market_price + (market_price * spread_percentage)


        try:
            buy_order = client.order_market_buy(symbol=symbol, quantity=quantity)
            sell_order = client.order_market_sell(symbol=symbol, quantity=quantity)
            print(buy_order)
            print(sell_order)
            print(f"Placed buy order at {buy_price} and sell order at {sell_price}")
        except BinanceAPIException as e:
            print(f"Error placing order: {e}")

        time.sleep(15)  

    return JsonResponse({'message': 'Market making started (simulated)'})

#market_make()
