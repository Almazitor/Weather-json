import json
import copy
import pprint
from datetime import date, timedelta
from collections import defaultdict
from itertools import groupby
from functools import reduce

# Function to load weather data from a file
def load_weather_data(file_path):
    with open(file_path, "r") as weatherfile:
        return json.load(weatherfile)

# Function to count the number of days for each year in the dataset
def count_days_per_year(weather_data):
    years_count = {}
    for data_point in weather_data:
        year_key = data_point['date'][0:4]
        if year_key in years_count:
            years_count[year_key] += 1
        else:
            years_count[year_key] = 1
    return years_count

# Function to find the warmest day in the dataset
def find_warmest_day(weather_data):
    warmest_day = max(weather_data, key=lambda x: x['tmax'])
    return warmest_day

# Function to find the coldest day in the dataset
def find_coldest_day(weather_data):
    coldest_day = min(weather_data, key=lambda x: x['tmin'])
    return coldest_day

# Function to count the number of days with snowfall
def count_snowfall_days(weather_data):
    snowfall_days = [day for day in weather_data if day['snow'] > 0]
    return len(snowfall_days), snowfall_days

# Function to find days considered cold, windy, and rainy
def is_cold_windy_rainy_day(day):
    # Calculate average temperature
    avg_temp = (day['tmax'] + day['tmin']) / 2
    # Calculate total precipitation (sum of snow and rain)
    total_prcp = day['snow'] + day['prcp']
    # Check conditions for a cold, windy, and rainy day
    if avg_temp < 45 and total_prcp > 0.7 and day['awnd'] >= 10.0:
        return True
    return False
def find_blustery_days(weather_data):
    blustery_days = list(filter(is_cold_windy_rainy_day, weather_data))
    return blustery_days

# Function to find summer rain days
def is_summer_rain_day(day):
    # Define the months of July and August
    summer_months = ["-07-", "-08-"]
    # Check if the date falls within summer months and precipitation is >= 1.0 inch
    if any([month in day['date'] for month in summer_months]) and (day['prcp'] >= 1.0):
        return True
    return False
def find_summer_rain_days(weather_data):
    summer_rain_days = list(filter(is_summer_rain_day, weather_data))
    return summer_rain_days

# Function to convert weather data to metric units
def convert_to_metric(wd):
    def to_celsius(f):
        return (f - 32) * 5 / 9
    def to_mm(i):
        return i * 25.4
    def to_kph(s):
        return s * 1.60934
    new_wd = copy.deepcopy(wd)
    new_wd['tmin'] = to_celsius(wd['tmin'])
    new_wd['tmax'] = to_celsius(wd['tmax'])
    new_wd['prcp'] = to_mm(wd['prcp'])
    new_wd['snow'] = to_mm(wd['snow'])
    new_wd['snwd'] = to_mm(wd['snwd'])
    new_wd['awnd'] = to_kph(wd['awnd'])
    return new_wd

# Function to categorize days based on average temperature
def average_temp_to_desc(day_data):
    avg_temp = (day_data['tmin'] + day_data['tmax']) / 2
    desc = ""
    if avg_temp < 60:
        desc = "cold"
    elif 60 <= avg_temp < 80:
        desc = "warm"
    else:
        desc = "hot"
    return (day_data['date'], desc)

# Function to group weather data by year-month
def group_by_year_month(weather_data):
    years_months = defaultdict(list)
    for data_point in weather_data:
        key = data_point['date'][0:7]
        years_months[key].append(data_point)
    return years_months

# Function to find warmest and coldest days for each month
def find_extreme_days(years_months):
    result = {}
    def warmest_day_info(month):
        wd = max(month, key=lambda d: d['tmax'])
        return {'date': wd['date'], 'temperature': wd['tmax']}
    def coldest_day_info(month):
        cd = min(month, key=lambda d: d['tmin'])
        return {'date': cd['date'], 'temperature': cd['tmin']}
    for year_month, daylist in years_months.items():
        result[year_month] = {
            'warmest_day': warmest_day_info(daylist),
            'coldest_day': coldest_day_info(daylist)
        }
    return result

# Function to find the warmest weekend day
def is_weekend_day(d):
    day = date.fromisoformat(d['date'])
    return day.weekday() in {5, 6}  # Saturday (5) or Sunday (6)
def find_warmest_weekend_day(weather_data):
    weekend_days = list(filter(is_weekend_day, weather_data))
    if not weekend_days:
        return None
    warmest_day = max(weekend_days, key=lambda d: d['tmax'])
    return warmest_day

# Function to find the coldest day of the year and calculate the average temperature for the following 7 days
def find_coldest_day_and_average_next_7_days(weather_data):
    coldest_day = min(weather_data, key=lambda d: d['tmin'])
    coldest_date = date.fromisoformat(coldest_day['date'])
    coldest_temp = coldest_day['tmin']
    avg_temp = 0.0
    next_date = coldest_date
    for _ in range(7):
        next_date += timedelta(days=1)
        wd = next((day for day in weather_data if day['date'] == str(next_date)), None)
        if wd:
            avg_temp += (wd['tmin'] + wd['tmax']) / 2
    if avg_temp:
        avg_temp /= 7
    return coldest_date, coldest_temp, avg_temp

# Function to group days by precipitation levels
def group_days_by_precipitation(weather_data, year):
    year_data = [day for day in weather_data if year in day['date']]
    datagroup = defaultdict(list)
    for d in year_data:
        datagroup[d['prcp']].append(d['date'])
    grouped = {k: list(v) for k, v in groupby(year_data, key=lambda d: d['prcp'])}
    return datagroup, grouped

# Function to calculate total snowfall and total precipitation for the entire dataset
def calculate_total_snowfall_and_precipitation(weather_data):
    total_snowfall = reduce(lambda acc, elem: acc + elem['snow'], weather_data, 0)
    total_precipitation = reduce(lambda acc, elem: acc + (elem['snow'] + elem['prcp']), weather_data, 0)
    return total_snowfall, total_precipitation

# Function to find the warmest day in which it snowed
def find_warmest_snow_day(weather_data):
    def warm_snow_day(acc, elem):
        return elem if elem['snow'] > 0 and elem['tmax'] > acc['tmax'] else acc

    start_val = {
        "date": "1900-01-01",
        "tmin": 0,
        "tmax": 0,
        "prcp": 0.0,
        "snow": 0.0,
        "snwd": 0.0,
        "awnd": 0.0
    }
    result = reduce(warm_snow_day, weather_data, start_val)
    return result

# Function to calculate the misery score for a given day
def misery_score(day):
    wind = 0 if day['awnd'] is None else day['awnd']
    temp = day['tmax'] * 0.8
    rain = day['prcp'] * 10
    score = (temp + rain + wind) / 3
    return score

# Function to find the day with the highest misery score
def find_misery_score_day(weather_data):
    def day_rank(acc, elem):
        return acc if misery_score(acc) >= misery_score(elem) else elem

    result = reduce(day_rank, weather_data)
    return result

# User Menu
def user_menu():
    print("Weather Data Analysis Menu:")
    print("1. Count the number of days for each year in the dataset.")
    print("2. Find the warmest day in the dataset.")
    print("3. Find the coldest day in the dataset.")
    print("4. Count the number of days with snowfall.")
    print("5. Find days considered cold, windy, and rainy.")
    print("6. Find summer rain days.")
    print("7. Convert weather data to metric units for a sample day.")
    print("8. Categorize days based on average temperature for a sample day.")
    print("9. Group weather data by year-month.")
    print("10. Find warmest and coldest days for each month.")
    print("11. Find the warmest weekend day.")
    print("12. Find the coldest day of the year and calculate the average temperature for the next 7 days.")
    print("13. Group days by precipitation levels for a sample year.")
    print("14. Calculate total snowfall and total precipitation for the entire dataset.")
    print("15. Find the warmest day in which it snowed.")
    print("16. Find the day with the highest misery score.")
    print("0. Exit")

    while True:
        try:
            choice = int(input("Enter your choice (0-16): "))
            if 0 <= choice <= 16:
                return choice
            else:
                print("Invalid choice. Please enter a number between 0 and 16.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Load weather data
weatherdata = load_weather_data("sample-weather-history.json")

# User Interaction Loop
while True:
    menu_choice = user_menu()

    if menu_choice == 1:
        result = count_days_per_year(weatherdata)
        print("Number of days for each year:")
        pprint.pp(result)

    elif menu_choice == 2:
        result = find_warmest_day(weatherdata)
        print(f"The warmest day was on {result['date']} at {result['tmax']} degrees")

    elif menu_choice == 3:
        result = find_coldest_day(weatherdata)
        print(f"The coldest day was on {result['date']} at {result['tmin']} degrees")

    elif menu_choice == 4:
        snowfall_count, snowfall_days = count_snowfall_days(weatherdata)
        print(f"Snow fell on {snowfall_count} days.")
        pprint.pp(snowfall_days)

    elif menu_choice == 5:
        blustery_days = find_blustery_days(weatherdata)
        print(f"Days considered cold, windy, and rainy:")
        pprint.pp(blustery_days)

    elif menu_choice == 6:
        summer_rain_days = find_summer_rain_days(weatherdata)
        print(f"Summer rain days:")
        pprint.pp(summer_rain_days)

    elif menu_choice == 7:
        sample_day = weatherdata[0]
        converted_data = convert_to_metric(sample_day)
        print(f"Original Data: {sample_day}")
        print(f"Converted to Metric: {converted_data}")

    elif menu_choice == 8:
        sample_day = weatherdata[0]
        categorized_data = average_temp_to_desc(sample_day)
        print(f"Original Data: {sample_day}")
        print(f"Categorized: {categorized_data}")

    elif menu_choice == 9:
        result = group_by_year_month(weatherdata)
        print("Weather data grouped by year-month:")
        pprint.pp(result)

    elif menu_choice == 10:
        years_months_data = group_by_year_month(weatherdata)
        extreme_days_result = find_extreme_days(years_months_data)
        print("Warmest and Coldest Days for Each Month:")
        for year_month, info in extreme_days_result.items():
            print(f"Month: {year_month}")
            print(f"Warmest Day: Date - {info['warmest_day']['date']}, Temperature - {info['warmest_day']['temperature']} degrees")
            print(f"Coldest Day: Date - {info['coldest_day']['date']}, Temperature - {info['coldest_day']['temperature']} degrees")
            print()

    elif menu_choice == 11:
        result = find_warmest_weekend_day(weatherdata)
        if result:
            warmest_day_date = date.fromisoformat(result['date']).strftime('%a, %d %b %Y')
            print(f"The warmest weekend day was on {warmest_day_date} with a temperature of {result['tmax']} degrees.")
        else:
            print("No weekend days in the dataset.")

    elif menu_choice == 12:
        result = find_coldest_day_and_average_next_7_days(weatherdata)
        if result:
            coldest_date, coldest_temp, avg_temp = result
            print(f"The coldest day of the year was {coldest_date} ({coldest_temp} degrees)")
            print(f"The average temp for the next 7 days was {avg_temp}")
        else:
            print("Could not find coldest day and calculate average temperature.")

    elif menu_choice == 13:
        year_data = input("Enter the year for precipitation grouping: ")
        datagroup, grouped = group_days_by_precipitation(weatherdata, year_data)
        print(f"Weather data grouped by precipitation levels for {year_data}:")
        pprint.pp(datagroup)
        pprint.pp(grouped)

    elif menu_choice == 14:
        total_snowfall, total_precipitation = calculate_total_snowfall_and_precipitation(weatherdata)
        print(f"Total Snowfall: {total_snowfall}")
        print(f"Total Precipitation: {total_precipitation}")

    elif menu_choice == 15:
        result = find_warmest_snow_day(weatherdata)
        if result:
            print(f"The warmest day in which it snowed was on {result['date']} with a temperature of {result['tmax']} and snowfall of {result['snow']}")
        else:
            print("No day with snowfall in the dataset.")

    elif menu_choice == 16:
        result = find_misery_score_day(weatherdata)
        if result:
            print(f"The day with the highest misery score was on {result['date']} with data: maximum temperature of {result['tmax']}, precipitation of {result['prcp']}, average wind speed of {result['awnd']}")
        else:
            print("No weather data available.")

    elif menu_choice == 0:
        print("Exiting the program. Goodbye!")
        break