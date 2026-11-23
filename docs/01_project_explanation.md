# 1. Project Explanation

## Simple explanation
A weather alert app asks a weather service "what is the weather in my city?", reads the answer, and warns you when something is risky, like heavy rain, extreme heat or strong wind, so you can plan ahead.

## Technical explanation
The app calls REST endpoints (current weather, 5-day forecast, air pollution) using `requests`. The server returns JSON. We parse it into dictionaries and a Pandas DataFrame, aggregate it into daily summaries, compare values to configurable thresholds using rule-based logic, and emit `Alert` objects with a type, severity and message. Results are shown in the terminal or dashboard and saved as CSV/JSON/text reports.

## Problem it solves
Raw data is not actionable. People need a simple "should I worry?" answer, ideally before the bad weather happens.

## Who benefits
- **Users/travellers**: pack and travel safely.
- **Farmers**: schedule irrigation, spraying, harvest.
- **Logistics**: reroute or delay shipments during storms.
- **Event planners**: pick dates and arrange backup plans.
- **Businesses**: retail, construction, energy demand planning.

## How weather apps fetch live data
1. App sends HTTP GET with city + API key.
2. Provider (e.g. OpenWeatherMap) combines satellite, radar, station and model data.
3. Provider replies with JSON.
4. App parses and displays it.

## How alerts are generated
Each alert is an `if` rule over a measured or forecast value:
- Heat: `temp >= 38°C`
- Rain: `rain probability >= 60%` or `rain >= 10 mm / 3h`
- Storm: `condition == "Thunderstorm"`
- Humidity: `humidity >= 85%`
- Wind: `wind >= 10 m/s`
- AQI: `aqi >= 4`
Severity is CRITICAL when a value exceeds the threshold by 15% or more.

## Workflow
```
user enters city -> weather API fetches data -> data processing (parse JSON)
-> forecast analysis (Pandas) -> alert condition check -> display output -> save report
```
