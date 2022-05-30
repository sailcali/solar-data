import requests
from calendar import month, monthrange

def from_month_string_return_first_and_last_dates(month_int, year_string):
    """Params: integer of requested month, string of requested year. Returns: String of first date of the month, string of last date of the month"""
    first_date = year_string + "-"+str(month_int)+"-01"
    last_date = year_string + "-" + str(month_int) +"-" + str(monthrange(int(year_string), month_int)[1])
    return first_date, last_date

def get_prod_value_month():
    month = input("Enter a number of month: ")
    year = input("Enter a year: ")
    start_date, end_date = from_month_string_return_first_and_last_dates(int(month), year)
    params = {'start_date': start_date, 'end_date': end_date}
    r = requests.get('http://192.168.86.205/api/solar-production/period', json=params)
    return r.json()

def get_prod_value_lifetime():
    r = requests.get('http://192.168.86.205/api/solar-production/lifetime')
    j = r.json()
    print(j['total_production'])

if __name__ == "__main__":
    # get_prod_data_lifetime()
    # print(from_month_string_return_first_and_last_dates(2, "2022"))
    v = get_prod_value_month()
    print(v['period_production'])