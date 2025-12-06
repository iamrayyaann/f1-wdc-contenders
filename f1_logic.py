import fastf1
from fastf1.ergast import Ergast
from datetime import datetime


TODAY=datetime.now().date()
SEASON=TODAY.year
ROUND=(
    fastf1.events.get_event_schedule(SEASON, backend='ergast')
    .query('EventDate < @TODAY')['RoundNumber']
    .iloc[-1]
    )


def main():
    driver_standings = get_driver_standings()
    points = get_max_points()
    calculate_contender(driver_standings, points)


def get_driver_standings():
    ergast = Ergast()
    standings = ergast.get_driver_standings(season=SEASON, round=ROUND)
    return standings.content[0]


def get_max_points():
    POINTS_FOR_SPRINT = 8 + 25
    POINTS_FOR_CONVENTIONAL = 25

    events = fastf1.events.get_event_schedule(SEASON, backend='ergast')
    events = events[events['RoundNumber'] > ROUND]
    sprint_events = len(events.loc[events["EventFormat"] == "sprint_shootout"])
    conventional_events = len(events.loc[events["EventFormat"] == "conventional"])

    sprint_points = sprint_events * POINTS_FOR_SPRINT
    conventional_points = conventional_events * POINTS_FOR_CONVENTIONAL

    return sprint_points + conventional_points


def calculate_contender(driver_standings, max_points):
    LEADER_POINTS = int(driver_standings.loc[0]['points'])
    results = []

    for i, _ in enumerate(driver_standings.iterrows()):
        driver = driver_standings.loc[i]
        driver_max_points = int(driver["points"]) + max_points

        results.append({
            'position' : driver['position'],
            'code' : driver['driverCode'],
            'full_name' : f"{driver['givenName']} {driver['familyName']}",
            'points' : round(driver['points']),
            'max_points' : driver_max_points,
            'is_contender' : 'Yes' if driver_max_points >= LEADER_POINTS else 'No'
        })

    return results


if __name__ == "__main__":
    main()
