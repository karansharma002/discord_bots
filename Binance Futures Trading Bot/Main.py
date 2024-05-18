
# IMPORT LIBRARIES
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
import time
import json
import os

# Function to load API keys from JSON file
def load_api_keys():
    if not os.path.exists('credentials.json'):
        # Create JSON file if it doesn't exist
        with open('credentials.json', 'w') as file:
            json.dump({'api_key': '', 'secret_key': ''}, file, indent=4)

    with open('credentials.json', 'r') as file:
        credentials = json.load(file)
        
    return credentials['api_key'], credentials['secret_key']

# Load API keys
api_key, secret_key = load_api_keys()

# Initialize RequestClient
request_client = RequestClient(api_key=api_key, secret_key=secret_key)

# Function to get current time in microseconds
def micro_seconds():
    return int(time.time() * 1000)

# Function to place a single order
def place_single_order(symbol, quantity, tp1, sl1):
    symbol = symbol.upper()
    # FETCH THE Price of CURRENCY 

    #price = request_client.get_mark_price(symbol)
    price = request_client.get_symbol_price_ticker(symbol = symbol)
    #print(price)
    price = "{:.2f}".format(price[0].__dict__['price']) 
    request_client.post_order(symbol=symbol,side=OrderSide.BUY,ordertype=OrderType.LIMIT,timeInForce=TimeInForce.GTC,quantity=quantity,price=price,positionSide=PositionSide.LONG)
    request_client.post_order(symbol=symbol,side=OrderSide.SELL,ordertype=OrderType.LIMIT,timeInForce=TimeInForce.GTC,quantity=quantity,price=price,positionSide=PositionSide.SHORT)
    
    pc = float(price)
    tp = "{:.2f}".format(pc + (pc * tp1 / 100))
    sl = "{:.2f}".format(pc - (pc * sl1 / 100))
    request_client.post_order(symbol=symbol,side=OrderSide.SELL,ordertype=OrderType.TAKE_PROFIT_MARKET,timeInForce=TimeInForce.GTC,stopPrice=tp,quantity = quantity,positionSide=PositionSide.LONG)
    request_client.post_order(symbol=symbol,side=OrderSide.SELL,ordertype=OrderType.STOP_MARKET,timeInForce=TimeInForce.GTC,stopPrice=sl,quantity = quantity,positionSide=PositionSide.LONG)


    #> Sending TP for LONG
    #> Sending SL for LONG

    # TP +3% [LONG]
    # SL -2% [LONG]

    tp = "{:.2f}".format(pc - (pc* tp1 / 100))
    sl = "{:.2f}".format(pc + (pc* sl1 / 100))
    request_client.post_order(symbol=symbol,side=OrderSide.BUY,ordertype=OrderType.TAKE_PROFIT_MARKET,timeInForce=TimeInForce.GTC,stopPrice=tp,quantity = quantity,positionSide=PositionSide.SHORT)
    request_client.post_order(symbol=symbol,side=OrderSide.BUY,ordertype=OrderType.STOP_MARKET,timeInForce=TimeInForce.GTC,stopPrice=sl,quantity = quantity,positionSide=PositionSide.SHORT)

    #> Sending TP for SHORT
    #> Sending SL for SHORT

    # TP -3% [LONG]
    # SL +2% [LONG]


# Function to place multiple orders
def place_multiple_orders(symbol):
    total_loss = 0
    with open('Data.json') as f:
        data = json.load(f)

    for x in symbol.keys():
        print(x)
        x = ''.join(i for i in x if not i.isdigit())
        print(x)
        print(symbol)
        price = request_client.get_symbol_price_ticker(symbol = x)
        #print(price)
        price = "{:.2f}".format(price[0].__dict__['price']) 
    
        #QUANTITY
        quantity = symbol[x]['Quantity']
    
        #1: Sending Long Order
        #2: Sending Short Order

        request_client.post_order(symbol=x,side=OrderSide.BUY,ordertype=OrderType.LIMIT,timeInForce=TimeInForce.GTC,quantity=quantity,price=price,positionSide=PositionSide.LONG)
        request_client.post_order(symbol=x,side=OrderSide.SELL,ordertype=OrderType.LIMIT,timeInForce=TimeInForce.GTC,quantity=quantity,price=price,positionSide=PositionSide.SHORT)
        
        '''
        > Sending TP for LONG
        > Sending SL for LONG
        '''
        # TP +3% [LONG]
        # SL -2% [LONG]
        price = float(price)
        tp = "{:.2f}".format(price + (price * symbol[x]['TP'] / 100))
        sl = "{:.2f}".format(price - (price * symbol[x]['SL'] / 100))


        # INTIALIZE ORDER SENT TIME
        data['Last_Time'] = micro_seconds()

        request_client.post_order(symbol=x,side=OrderSide.SELL,ordertype=OrderType.TAKE_PROFIT_MARKET,timeInForce=TimeInForce.GTC,stopPrice=tp,quantity = quantity,positionSide=PositionSide.LONG)
        request_client.post_order(symbol=x,side=OrderSide.SELL,ordertype=OrderType.STOP_MARKET,timeInForce=TimeInForce.GTC,stopPrice=sl,quantity = quantity,positionSide=PositionSide.LONG)
        '''
        > Sending TP for SHORT
        > Sending SL for SHORT
        '''
        # TP -3% [LONG]
        # SL +2% [LONG]
        tp = "{:.2f}".format(price - (price * symbol[x]['TP'] / 100))
        sl = "{:.2f}".format(price + (price * symbol[x]['SL'] / 100))

        request_client.post_order(symbol=x,side=OrderSide.BUY,ordertype=OrderType.TAKE_PROFIT_MARKET,timeInForce=TimeInForce.GTC,stopPrice=tp,quantity = quantity,positionSide=PositionSide.SHORT)
        request_client.post_order(symbol=x,side=OrderSide.BUY,ordertype=OrderType.STOP_MARKET,timeInForce=TimeInForce.GTC,stopPrice=sl,quantity = quantity,positionSide=PositionSide.SHORT)
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)

        while True:
            with open('Data.json') as f:
                data = json.load(f)
            income = request_client.get_income_history(symbol = x,incomeType=IncomeType.REALIZED_PNL,startTime=data['Last_Time'])
            try:
                for z in range(len(income)):
                    total_loss += round(income[z].__dict__['income'])
                    if total_loss <= data['Sum Amount']:
                        data.pop('Last_Time')
                        with open('Data.json','w') as f:
                            json.dump(data,f,indent = 3)
                        exit()
                    else:
                        pass
        
                if income[0].__dict__['symbol'] == x:
                    if len(income) >= 2:
                        if total_loss <= data['Sum Amount']:
                            print(f"WE ARE HERE ------------------------- {total_loss} {data['Sum Amount']}")
                            data.pop('Last_Time')
                            with open('Data.json','w') as f:
                                json.dump(data,f,indent = 3)
                            exit()
                        else:
                            request_client.cancel_all_orders(x)
                            time.sleep(10)
                            break
                    else:
                        pass
            
            except Exception as e:
                time.sleep(2)
                pass

# Function to cancel all orders
def cancel_orders(symbol):
    request_client.cancel_all_orders(symbol)

# Function to execute the main menu
def menu():
    with open('Data.json','r') as f:
        data = json.load(f)
    
    if 'Last_Time' in data:
        data.pop('Last_Time')
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)

    print('1. Place Order (Single Currency)',
          '\n2. Place Order (Multiple Currencies)',
          '\n3: Cancel All Orders',
          '\n4: Set SUM LOSS Amount')

    choice = int(input())
    
    if choice == 1:
        symbol = input('Enter the SYMBOL >> ')
        quantity = input(f'Enter the Quantity of {symbol} >> ')
        tp = input(f'Enter the Take Profit % of {symbol}>> ')
        sl = input(f'Enter the Stop LOSS   % of {symbol}>> ')

        if '.' in tp:
            tp = float(tp)
        else:
            tp = int(tp)

        if '.' in sl:
            sl = float(sl)
        else:
            sl = int(sl)

        place_single_order(symbol,quantity,tp,sl)

    elif choice == 2:
        total_currencies = int(input('Enter the Total Orders you want to PUT (Example: 5) >> '))
        symbol = {}
        num = 0
        while total_currencies:
            #WE NEED TO SHOW WHAT CURRENCIES
            print('\n')
            choice = input('Enter the SYMBOL >> ').upper()
            quantity = input(f'Enter the Quantity of {choice}>> ').upper()
            tp = input(f'Enter the Take Profit % of {choice}>> ')
            sl = input(f'Enter the Stop LOSS   % of {choice}>> ')
    
            if '.' in tp:
                tp = float(tp)
            else:
                tp = int(tp)
    
            if '.' in sl:
                sl = float(sl)
            else:
                sl = int(sl)
            
            if choice in symbol:
                choice += str(num)

            symbol[choice] = {}
            symbol[choice]['TP'] = tp
            symbol[choice]['SL'] = sl
            symbol[choice]['Quantity'] = quantity
            total_currencies -= 1
            num += 1
        
        place_multiple_orders(symbol)    

    elif choice == 3:
        symbol = input('Enter the SYMBOL To Cancel Pending OrderS >> ')
        cancel_orders(symbol)
        print('✓ Sucessfully Cancelled all the pending Orders.')
        time.sleep(5)


    elif choice == 4:
        with open('Data.json') as f:
            data = json.load(f)
        
        amount = int(input('Enter the SUM LOSS AMOUNT in Negative Form (Example: -50): '))
        data['Sum Amount'] = amount
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        print(f'✓ Sucessfully Changed The Sum Loss Amount to: {amount}')

    else:
        print('!Invalid Choice Entered')
        return menu()  
