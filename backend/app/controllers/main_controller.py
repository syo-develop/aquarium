from flask import Blueprint, render_template
from datetime import datetime
from utils.JsonObject import JsonObject

main = Blueprint('main', __name__)
today = datetime.now().strftime("%Y%m%d")

@main.route("/")
def index():
    return render_template("index.html")

@main.route('/api/dayData', methods=['GET'])
def get_day_data():
    jsonData = JsonObject()
    query_data = jsonData.get_query_data(today)
    date = jsonData.get_date(query_data)
    time_list = jsonData.get_datetime_today_list(query_data)
    temperature_list = jsonData.get_temperature_today_list(query_data)
    json_data = jsonData.create_json_data(date, time_list, temperature_list)
    
    return json_data

@main.route('/api/weekData', methods=['GET'])
def get_week_data():
    jsonData = JsonObject()
    query_data = jsonData.get_query_week_data(today)
    date = jsonData.get_date_week(query_data)
    time_list = jsonData.get_datetime_week_list(query_data)
    temperature_list = jsonData.get_temperature_week_list(query_data)
    json_data = jsonData.create_json_data(date, time_list, temperature_list)
    
    return json_data

@main.route('/api/monthData', methods=['GET'])
def get_month_data():
    jsonData = JsonObject()
    query_data = jsonData.get_query_month_data(today)
    date = jsonData.get_date_month(query_data)
    time_list = jsonData.get_datetime_month_list(query_data)
    temperature_list = jsonData.get_temperature_month_list(query_data)
    json_data = jsonData.create_json_data(date, time_list, temperature_list)
    
    return json_data

@main.route('/api/yearData', methods=['GET'])
def get_year_data():
    jsonData = JsonObject()
    query_data = jsonData.get_query_year_data(today)
    date = jsonData.get_date_year(query_data)
    time_list = jsonData.get_datetime_year_list(query_data)
    temperature_list = jsonData.get_temperature_year_list(query_data)
    json_data = jsonData.create_json_data(date, time_list, temperature_list)
    
    return json_data