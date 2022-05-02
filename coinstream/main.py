from secret import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, ACCESS_TOKEN, SECRET_KEY
from coinone.account import Account
from pprint import pprint
import boto3
import time
from datetime import datetime, timedelta
import json

client = boto3.client('firehose', region_name = 'us-east-1', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

my = Account(ACCESS_TOKEN, SECRET_KEY)
markets = ['KRW-BTC']
for market in markets:
    currency, coin = market.split('-')
    all_chart = my.chart(currency, coin,"1m")
    
    chart_data = all_chart['chart'][1]
    
    now = (datetime.now() + timedelta(hours=9) - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
    data = json.dumps(
        {
            'candle_date_time' : now, "market" : market, 'opening_price' : float(chart_data['open']), 
            'closing_price' : float(chart_data['close']), 'low_price': float(chart_data['low']), 'high_price' : float(chart_data['high']),
            'target_volume' : float(chart_data['target_volume']), 'timestamp' : chart_data['timestamp']
        }, 
        default=str
    )
    try:
        client.put_record(
            DeliveryStreamName = "PUT-RED-COIN",
            Record={
                'Data': '{}\n'.format(data)
            }
        )
        print(now)

    except Exception as ex:
        print(ex)
            
