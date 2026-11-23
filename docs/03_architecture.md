# 3. Architecture

**Input:** city name, API key (or simulation), alert thresholds
**Processing:** API request -> JSON parsing -> temperature/humidity analysis -> rain/storm check -> alert generation
**Output:** current weather, forecast summary, alert messages, saved reports and charts

```
 +-----------+     +------------------+     +--------------------+
 |   User    | --> | main.py / CLI    | --> | pipeline.py        |
 | city,     |     | dashboard.py     |     | (orchestrator)     |
 | thresholds|     +------------------+     +---------+----------+
 +-----------+                                        |
                       +------------------------------+-----------------+
                       v                                                v
              +-----------------+  mode=api                   +------------------+
              | weather_api.py  | <-- OpenWeatherMap          | simulation.py    |
              | requests + JSON |                             | virtual data     |
              +--------+--------+                             +---------+--------+
                       +----------------------+-----------------------+
                                              v   raw JSON
                                    +-------------------+
                                    | parser.py         | -> dict + DataFrame
                                    +---------+---------+
                                              v
                                    +-------------------+
                                    | analyzer.py       | daily summary, stats
                                    +---------+---------+
                                              v
                                    +-------------------+
                                    | alerts.py         | rules + thresholds
                                    +---------+---------+
                          +-------------------+-------------------+
                          v                   v                   v
                  +--------------+   +----------------+   +----------------+
                  | visualizer.py|   | report.py      |   | notifier.py    |
                  | PNG charts   |   | CSV/JSON/TXT   |   | email (opt.)   |
                  +--------------+   +----------------+   +----------------+
```

## Data flow
1. User gives city and thresholds.
2. `pipeline.run_pipeline` chooses live API or simulation. Both return the same JSON shape, so the rest of the code is identical.
3. `parser` converts JSON into clean values.
4. `analyzer` groups 40 three-hour rows into daily statistics.
5. `alerts` compares current and forecast values against `Thresholds`.
6. Output modules print, chart, save and optionally email the result.
