import requests
from calendar import month, monthrange
import pandas as pd
import json

def from_month_string_return_first_and_last_dates(month_int, year_string):
    """Params: integer of requested month, string of requested year. Returns: String of first date of the month, string of last date of the month"""
    first_date = year_string + "-" + str(month_int) + "-01"
    last_date = year_string + "-" + str(month_int) + "-" + str(monthrange(int(year_string), month_int)[1])
    return first_date, last_date

def get_prod_value_month():
    # month = input("Enter a number of month: ")
    # year = input("Enter a year: ")
    month = '2'
    year = '2022'
    start_date, end_date = from_month_string_return_first_and_last_dates(int(month), year)
    params = {'start_date': start_date, 'end_date': end_date}
    r = requests.get('http://192.168.86.205/api/solar-production/period-sum', json=params)
    return r.json()

def get_prod_value_lifetime():
    r = requests.get('http://192.168.86.205/api/solar-production/lifetime')
    j = r.json()
    print(j['total_production'])

def get_month_solar_data_to_dataframe(month, year):
    """Get month of data from BE, convert to DF, return new DF with production value for each day"""
    start_date, end_date = from_month_string_return_first_and_last_dates(month, year)
    params = {'start_date': start_date, 'end_date': end_date}
    r = requests.get('http://192.168.86.205/api/solar-production/period-data', json=params)
    j = r.json()
    df = pd.json_normalize(j, 'Results')
    if len(df) != 0:
        df['time'] = pd.to_datetime(df['time'])
    else:
        print("No data for that month!")
        quit()
    
    prod_per_day = pd.DataFrame(columns=['day', 'production'])
    prod_per_day.set_index(['day'], inplace=True)
    for i in range(1, 32):
        curr_df = df[df['time'].dt.day == i]
        if curr_df.production.sum() != 0:
            prod_per_day.loc[i] = curr_df.production.sum()
    return prod_per_day


    
if __name__ == "__main__":
    # get_prod_data_lifetime()
    # print(from_month_string_return_first_and_last_dates(2, "2022"))
    # v = get_prod_value_month()
    # print(v['period_production'])
    
    df = pd.DataFrame(columns=['month', 'Total_Kwh', 'Max_Day_Watt', 'Sunny_Pct'])
    df.set_index(['month'], inplace=True)
   
    for i in range(1,13):
        if i >= 4:
            year = '2021'
        else:
            year = '2022'
        month = get_month_solar_data_to_dataframe(month=i, year=year)
        top = month.production.max() * .90
        # top_df = month[month.production > top]
        df.loc[i] = {'Total_Kwh': month.production.sum()/1000,
                     'Max_Day_Watt': month.production.max(),
                     'Sunny_Pct': int((len(month[month.production > top])/monthrange(int(year), i)[1]) * 100)}
    
    print(df)
