# F1 WDC Contenders

A web application that displays Formula 1 drivers who are still mathematically in contention for the World Drivers' Championship (WDC). The app calculates each driver's maximum possible points for the remaining season and determines if they can still catch the current championship leader.

## How It Works

The application calculates whether each driver can still win the championship by:
1. Fetching the current driver standings for the season
2. Determining the maximum points available in remaining races (accounting for sprint vs conventional formats)
3. Adding each driver's current points to the maximum possible points
4. Comparing this total against the current leader's points to determine if they're still in contention

## Technologies Used

- **Flask**: Web framework for Python
- **FastF1**: Python library for accessing F1 data
- **Pandas**: Data manipulation and analysis
- **Ergast API**: Formula 1 data API (accessed via FastF1)

## Credits & Acknowledgments

This project uses the following services and resources:

- **[FastF1](https://github.com/theOehrly/Fast-F1)**: Python library for accessing Formula 1 data
- **[Ergast API](http://ergast.com/mrd/)**: Formula 1 historical data API
- **[Flask](https://flask.palletsprojects.com/)**: Web framework
- **F1 Fonts**: Official Formula 1 typography (F1 Regular, F1 Torque, F1 Turbo)

All Formula 1 data is provided by the Ergast API, which offers free access to historical F1 data. The FastF1 library provides a convenient Python interface to this data.

## Disclaimer

This application is not affiliated with, endorsed by, or associated with Formula 1, the FIA, or any Formula 1 teams. All F1 data is sourced from publicly available APIs.

