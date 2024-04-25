from django.shortcuts import render,HttpResponseRedirect
from binance.client import Client , BinanceAPIException
from django.http import JsonResponse
from binance.client import Client
from datetime import time,datetime,timedelta
import time,json,random
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .models import Placedorder
running=True
API_KEY = '6eXmuCXxnQq1uLMRqKeWejo0iAnl7vKs6kenNn0p8vQWMIE9eALt35FG54RtroU1'
API_SECRET = '6kkY5VGELHXGodCHCJmYj50k3atEGh7VgaI2uQE3VRiGrNCS7AEWw3yuW0GNl6Bq'
if isinstance(API_SECRET, bytes):
    API_SECRET = API_SECRET.decode('utf-8')
client = Client(API_KEY,API_SECRET, testnet=True)

account_info = client.get_account()
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
        new_balance = get_user_balance()
        return JsonResponse({'status': 'success', 'balance': account_info})
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
    return(order)

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
    return(order)

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
    
def cancel_myorder(symbol,id):
    order_status=client.cancel_order(symbol=symbol,orderId=id)

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
    running= True
    # Get symbol information (assuming you have a function to retrieve it)
    symbol_info = get_symbol_info(request.POST.get('symbol'))

    if request.method == 'POST':
        endtime_str = request.POST.get('endtime')
        symbol = request.POST.get('symbol')
        interval = int(request.POST.get('interval'))

        # Validate and adjust quantities based on symbol filters (LOT_SIZE, MIN_QTY)
        max_qty = float(request.POST.get('max_qty'))
        min_qty = float(request.POST.get('min_qty'))
        max_qty = min(max_qty, float(symbol_info['filters'][1]['maxQty']))
        min_qty = max(min_qty, float(symbol_info['filters'][1]['minQty']))

        spread = float(request.POST.get('spread'))
        end_time = datetime.strptime(endtime_str, "%H:%M").time()
        start_time = datetime.now().time()

        while running:
            current_time = datetime.now().time()
            print('WORKING')

            if start_time <= current_time <= end_time:
                # Generate random quantities within adjusted limits
                buy_qty = round(random.uniform(max_qty, min_qty), 4)
                sell_qty = round(random.uniform(max_qty, min_qty), 4)

                current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
                print('current_price', current_price)

                # Calculate buy and sell prices with spread, considering price filter (PRICE_FILTER)
                price_filter = symbol_info['filters'][0]
                min_price = float(price_filter['minPrice'])
                max_price = float(price_filter['maxPrice'])
                tick_size = float(price_filter['tickSize'])

                buy_price = max(min_price, round(current_price - (current_price * spread),0))
                sell_price = min(max_price, round(current_price + (current_price * spread),0))

                print('buy_price', buy_price, ' ', 'sell_price', sell_price)
                print('buy qty', buy_qty, ' ', 'sell qty', sell_qty)

                try:
                    # Place orders with quantity and price validation (LOT_SIZE, MIN_QTY, PRICE_FILTER)
                    buy_order = buy_order_limit(symbol, buy_qty, buy_price)
                    sell_order = sell_order_limit(symbol, sell_qty, sell_price)


                    print(f"buy order: price {buy_order['price']} quantity {buy_order['origQty']}")
                    print(f"sell order: price {sell_order['price']} quantity {sell_order['origQty']}")
                except BinanceAPIException as e:
                    print(f"Error placing order: {e}")
            time.sleep(interval)

    return JsonResponse({'status': 'success'})
    



def market(request):
    global running
    if request.method == 'POST':
        endtime_str = request.POST.get('endtime')
        symbol = request.POST.get('symbol')
        interval = int(request.POST.get('interval'))
        max_qty = request.POST.get('max_qty')     
        min_qty = request.POST.get('min_qty')  
        spread = request.POST.get('spread')
        end_time = datetime.strptime(endtime_str, "%H:%M").time()
        start_time = datetime.now().time()
    print('end time',end_time,'  symbol:',symbol,'  interval',interval)
    print('start time',start_time,'  max time:',max_qty,'  min',min_qty,'  spread', spread)


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



order_placement= {"buy": [],"sell":[]}
def cancel_unplaced_order():
    if 'buy' in order_placement and 'sell' in order_placement:
        current_time = datetime.now()
        buy_placement_time = order_placement['buy']
        sell_placement_time = order_placement['sell']
    
    # Define the duration after which unplaced orders should be canceled (e.g., 5 minutes)
    cancel_duration = timedelta(minutes=20)

    if (current_time - buy_placement_time) > cancel_duration:
        # Cancel the unplaced buy order
        cancel_myorder()
        print("Buy order canceled after timeout.")
        del order_placement['buy']

    if (current_time - sell_placement_time) > cancel_duration:
        # Cancel the unplaced sell order
        cancel_myorder()
        print("Sell order canceled after timeout.")
        del order_placement['sell']
    
def market_clear(request):
    global running
    running = True
    
    # Get symbol information (assuming you have a function to retrieve it)
    symbol_info = get_symbol_info(request.POST.get('symbol'))

    if request.method == 'POST':
        endtime_str = request.POST.get('endtime')
        symbol = request.POST.get('symbol')
        interval = int(request.POST.get('interval'))

        # Validate and adjust quantities based on symbol filters (LOT_SIZE, MIN_QTY)
        max_qty = float(request.POST.get('max_qty'))
        min_qty = float(request.POST.get('min_qty'))
        max_qty = min(max_qty, float(symbol_info['filters'][1]['maxQty']))
        min_qty = max(min_qty, float(symbol_info['filters'][1]['minQty']))

        spread = float(request.POST.get('spread'))
        end_time = datetime.strptime(endtime_str, "%H:%M").time()
        start_time = datetime.now().time()

        while running:
            current_time = datetime.now().time()

            if start_time <= current_time <= end_time:
                # Generate random quantities within adjusted limits
                buy_qty = round(random.uniform(max_qty, min_qty), 4)
                sell_qty = round(random.uniform(max_qty, min_qty), 4)

                current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])

                # Calculate buy and sell prices with spread, considering price filter (PRICE_FILTER)
                price_filter = symbol_info['filters'][0]
                min_price = float(price_filter['minPrice'])
                max_price = float(price_filter['maxPrice'])

                buy_price = max(min_price, round(current_price - (current_price * spread), 0))
                sell_price = min(max_price, round(current_price + (current_price * spread), 0))


                try:
                    # Place orders with quantity and price validation (LOT_SIZE, MIN_QTY, PRICE_FILTER)
                    buy_order = buy_order_limit(symbol, buy_qty, buy_price)
                    sell_order = sell_order_limit(symbol, sell_qty, sell_price)

                    save_order_to_db(symbol, buy_order['orderId'], current_time)
                    save_order_to_db(symbol, sell_order['orderId'], current_time)
                    print(current_price)
                    print(f"Buy order: price {buy_order['price']} quantity {buy_order['origQty']}")
                    print(f"Sell order: price {sell_order['price']} quantity {sell_order['origQty']}")
                except BinanceAPIException as e:
                    print(f"Error placing order: {e}")
                cancel_timed_out_orders(symbol)

            time.sleep(interval)

    return JsonResponse({'status': 'success'})


# Function to retrieve symbol information from Binance (replace with your actual implementation)
def get_symbol_info(symbol):
    # Replace with your Binance client and logic to fetch symbol info
    # This example assumes you have a `client` object with the Binance API connection
    return client.get_symbol_info(symbol=symbol)

print(order_placement)

def save_order_to_db(symbol, order_id,timestamp):

    placed_order = Placedorder(symbol=symbol, orderid=order_id,timestamp=timestamp)
    placed_order.save()  # Assuming you have a save() method for your model

from django.db import transaction

def cancel_timed_out_orders(symbol, delete_cancelled=False):


    # Get all orders for the symbol placed more than 20 minutes ago
    threshold = datetime.now() - timedelta(minutes=20)
    timed_out_orders = Placedorder.objects.filter(symbol=symbol, timestamp__lt=threshold)

    with transaction.atomic():
        for order in timed_out_orders:
            try:
                client.cancel_order(symbol=symbol, orderId=order.orderid)
                print(f"Cancelled timed-out order: {order.orderid}")

                if delete_cancelled:
                    order.delete()
            except BinanceAPIException as e:
                return None



