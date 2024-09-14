import boto3
from boto3.dynamodb.conditions import Key
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class JsonObject:
    # テーブル設定
    table_name = 'raspberry_pi_4_data' 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    def __init__(self):
        self.title = ''
        self.labels = {}
        self.datasets = {}
    
    # データ抽出（日）
    def get_query_data(self, date):
        options = {
            'KeyConditionExpression': Key('device_id').eq('ds18b20') & Key('datetime').begins_with(date),
          }
        res = self.table.query(**options)
        query_data = res['Items']
        return query_data
    
    # データ抽出（週）
    def get_query_week_data(self, today):
        date_object = datetime.strptime(today[:8], "%Y%m%d")
        end_timestamp = today + '0000'
        start_date_object = date_object - timedelta(weeks=1)
        start_timestamp = start_date_object.strftime("%Y%m%d%H%M")
        options = {
            'KeyConditionExpression': Key('device_id').eq('ds18b20') & Key('datetime').between(start_timestamp, end_timestamp),
          }
        res = self.table.query(**options)
        query_data = res['Items']
        return query_data
      
    # データ抽出（月）
    def get_query_month_data(self, today):
      # 今月を取得
      options = {
            'KeyConditionExpression': Key('device_id').eq('ds18b20') & Key('datetime').begins_with(today[:6]),
          }
      res = self.table.query(**options)
      query_data = res['Items']
      
      return query_data
    
    # データ抽出（年）
    def get_query_year_data(self, today):
      options = {
            'KeyConditionExpression': Key('device_id').eq('ds18b20') & Key('datetime').begins_with(today[:4]),
          }
      res = self.table.query(**options)
      query_data = res['Items']
      
      return query_data
      
    # 日付取得（日）
    def get_date(self, query_data):
        query_datetime = query_data[0]['datetime']
        date = str(datetime.strptime(query_datetime[:8], "%Y%m%d").strftime("%Y/%m/%d"))
        return date
    
    # 日付取得（週）
    def get_date_week(self, query_data):
        query_start_datetime = query_data[0]['datetime']
        query_end_datetime = query_data[-1]['datetime']        
        date = str(datetime.strptime(query_start_datetime[:8], "%Y%m%d").strftime("%Y/%m/%d")) + ' ~ ' + str(datetime.strptime(query_end_datetime[:8], "%Y%m%d").strftime("%Y/%m/%d"))
        return date
      
    # 日付取得（月）
    def get_date_month(self, query_data):
        query_start_datetime = query_data[0]['datetime']
        today = datetime.today()
        last_day_current_month = today + relativedelta(months=1, day=1) - relativedelta(days=1)
        date = str(datetime.strptime(query_start_datetime[:8], "%Y%m%d").strftime("%Y/%m/%d")) + ' ~ ' + str(last_day_current_month.strftime("%Y/%m/%d"))
        return date
      
    # 日付取得（年）
    def get_date_year(self, query_data):
        query_start_datetime = query_data[0]['datetime']
        date = str(datetime.strptime(query_start_datetime[:8], "%Y%m%d").strftime("%Y/%m/%d")) + ' ~ ' + str(query_start_datetime[:4] + '/12/31')
        return date
    
    # datetimeリスト取得（日）
    def get_datetime_today_list(self, query_data):
        time_list = []
        for data in query_data:
          time_str = data['datetime'][8:]
          append_time = f"{time_str[:2]}:{time_str[2:]}" 
          time_list.append(append_time)
          
        return time_list
      
    # datetimeリスト取得（週）
    def get_datetime_week_list(self, query_data):
        time_list = []
        for data in query_data: 
            # 0:00,3:00,6:00,9:00,12:00,15:00,18:00,21:00のdatetimeを取得
            if int(data['datetime'][8:10]) % 3 == 0 and data['datetime'][10:12] == '00':
              data_str = datetime.strptime(data['datetime'], "%Y%m%d%H%M").strftime("%m/%d %H:%M")
              time_list.append(data_str)
        return time_list
      
    # datetimeリスト取得（月）
    def get_datetime_month_list(self, query_data):
        time_list = []
        for data in query_data: 
            if int(data['datetime'][8:10]) % 12 == 0 and data['datetime'][10:12] == '00':
              data_str = datetime.strptime(data['datetime'], "%Y%m%d%H%M").strftime("%m/%d %H:%M")
              time_list.append(data_str)
        return time_list
      
    # datetimeリスト取得（年）
    def get_datetime_year_list(self, query_data):
        time_list = []
        for data in query_data: 
            if data['datetime'][8:12]  == '0000':
              data_str = datetime.strptime(data['datetime'], "%Y%m%d%H%M").strftime("%m/%d %H:%M")
              time_list.append(data_str)
        return time_list
      
    # 温度リスト取得（日）
    def get_temperature_today_list(self, query_data):
      temperature_list = []
      for data in query_data:
        temperature_list.append(data['temperature'])
      return temperature_list
    
    # 温度リストを取得（週）
    def get_temperature_week_list(self, query_data):
      temperature_list = []
      for data in query_data: 
            # datetime:202409010000
            if int(data['datetime'][8:10]) % 3 == 0 and data['datetime'][10:12] == '00':
              temperature_list.append(data['temperature'])
      return temperature_list
    
    # 温度リスト取得（月）
    def get_temperature_month_list(self, query_data):
      temperature_list = []
      for data in query_data: 
            if int(data['datetime'][8:10]) % 12 == 0 and data['datetime'][10:12] == '00':
              temperature_list.append(data['temperature'])
      return temperature_list
    
    # 温度リスト取得（年）
    def get_temperature_year_list(self, query_data):
      temperature_list = []
      for data in query_data: 
            if data['datetime'][8:12] == '0000':
              temperature_list.append(data['temperature'])
      return temperature_list
      
    # JSONデータ作成
    def create_json_data(self, date, time_list, temperature_list):
        json_data = {}
        json_data['title'] = date
        json_data['labels'] = {}
        json_data['datasets'] = {}
        json_data['labels']['time'] = time_list
        json_data['datasets']['temperature'] = temperature_list
        return json_data