# Weather Data Analysis Project

This project offers a collection of functions for in-depth analysis of weather data, providing insights into various aspects such as temperature categorization, extreme days, precipitation patterns, and more. Below is an overview of the full functionality, including all 16 features.

## Getting Started

### Prerequisites

- Python 3.x
- Sample weather data in JSON format (e.g., `sample-weather-history.json`)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Almazitor/Weather-json.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd Weather-json
    ```

## Usage

1. **Analyzing Average Temperature Categories**

    Categorize days into temperature categories (cold, warm, hot):

    ```bash
    python weather-data.py categorize-temperature
    ```

2. **Grouping Data by Year-Month**

    Group weather data by year-month:

    ```bash
    python weather-data.py group-by-year-month
    ```

3. **Finding Extreme Days**

    Find the warmest and coldest days for each month:

    ```bash
    python weather-data.py find-extreme-days
    ```

4. **Finding Warmest Weekend Day**

    Find the warmest weekend day:

    ```bash
    python weather-data.py find-warmest-weekend-day
    ```

5. **Finding Coldest Day and Average Next 7 Days**

    Find the coldest day of the year and calculate the average temperature for the following 7 days:

    ```bash
    python weather-data.py find-coldest-day-average-next-7-days
    ```

6. **Grouping Days by Precipitation**

    Group days of a specified year by precipitation levels:

    ```bash
    python weather-data.py group-days-by-precipitation --year 2022
    ```

7. **Calculating Total Snowfall and Precipitation**

    Calculate the total snowfall and total precipitation for the entire dataset:

    ```bash
    python weather-data.py calculate-total-snowfall-precipitation
    ```

8. **Finding Warmest Day in Which It Snowed**

    Find the warmest day in which it snowed:

    ```bash
    python weather-data.py find-warmest-snow-day
    ```

9. **Finding Day with Highest Misery Score**

    Find the day with the highest misery score:

    ```bash
    python weather-data.py find-highest-misery-score-day
    ```

10. **Finding Blustery Days**

    Find days characterized by cold, wind, and rain:

    ```bash
    python weather-data.py find-blustery-days
    ```

11. **Finding Summer Rain Days**

    Find days with rain during the summer:

    ```bash
    python weather-data.py find-summer-rain-days
    ```

12. **Calculating Total Precipitation by Type**

    Calculate total precipitation, snow, and rain for the entire dataset:

    ```bash
    python weather-data.py calculate-total-precipitation-by-type
    ```

13. **Finding Coldest Day and Average Next 7 Days by Type**

    Find the coldest day and calculate the average temperature for the next 7 days by precipitation type:

    ```bash
    python weather-data.py find-coldest-day-average-next-7-days-by-type
    ```

14. **Grouping Days by Snowfall**

    Group days by snowfall levels:

    ```bash
    python weather-data.py group-days-by-snowfall
    ```

15. **Finding Days with Rain and Wind**

    Find days with both rain and high wind speed:

    ```bash
    python weather-data.py find-days-with-rain-and-wind
    ```

16. **Finding Warmest Rainy Day**

    Find the warmest day with rain:

    ```bash
    python weather-data.py find-warmest-rainy-day
    ```
