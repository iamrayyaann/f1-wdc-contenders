import requests
from datetime import datetime

TODAY = datetime.now().date()
SEASON = TODAY.year

# Get the current round by checking the race schedule
def get_current_round():
    try:
        url = f"https://ergast.com/api/f1/{SEASON}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        races = data['MRData']['RaceTable'].get('Races', [])
        if not races:
            return 1
        
        current_round = 0
        
        for race in races:
            race_date = datetime.strptime(race['date'], '%Y-%m-%d').date()
            if race_date < TODAY:
                current_round = int(race['round'])
            else:
                break
        
        return current_round if current_round > 0 else 1
    except Exception as e:
        # Fallback to round 1 if API call fails
        print(f"Error getting current round: {e}")
        return 1


def main():
    driver_standings = get_driver_standings()
    points = get_max_points()
    calculate_contender(driver_standings, points)


def get_driver_standings():
    try:
        # Try current standings first (most reliable)
        url = f"https://ergast.com/api/f1/current/driverStandings.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        standings_lists = data['MRData']['StandingsTable'].get('StandingsLists', [])
        if not standings_lists:
            # Fallback to specific round if current doesn't work
            round_num = get_current_round()
            url = f"https://ergast.com/api/f1/{SEASON}/{round_num}/driverStandings.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            standings_lists = data['MRData']['StandingsTable'].get('StandingsLists', [])
        
        if not standings_lists:
            print("No standings lists found in API response")
            return []
        
        standings = standings_lists[0].get('DriverStandings', [])
        if not standings:
            print("No driver standings found in standings list")
            return []
        
        return standings
    except requests.exceptions.RequestException as e:
        print(f"Request error getting driver standings: {e}")
        return []
    except KeyError as e:
        print(f"Key error parsing driver standings: {e}")
        return []
    except Exception as e:
        print(f"Error getting driver standings: {e}")
        return []


def is_sprint_weekend(season, round_num):
    """Check if a race weekend has sprint format by checking for sprint results"""
    try:
        url = f"https://ergast.com/api/f1/{season}/{round_num}/sprint.json?limit=1"
        response = requests.get(url, timeout=5)
        data = response.json()
        # If sprint results exist, it's a sprint weekend
        return len(data['MRData']['RaceTable'].get('Races', [])) > 0
    except:
        return False

def get_max_points():
    try:
        POINTS_FOR_SPRINT = 8 + 25
        POINTS_FOR_CONVENTIONAL = 25

        round_num = get_current_round()
        url = f"https://ergast.com/api/f1/{SEASON}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        races = data['MRData']['RaceTable'].get('Races', [])
        sprint_events = 0
        conventional_events = 0
        
        for race in races:
            race_round = int(race['round'])
            if race_round > round_num:
                if is_sprint_weekend(SEASON, race_round):
                    sprint_events += 1
                else:
                    conventional_events += 1
        
        sprint_points = sprint_events * POINTS_FOR_SPRINT
        conventional_points = conventional_events * POINTS_FOR_CONVENTIONAL

        return sprint_points + conventional_points
    except Exception as e:
        print(f"Error getting max points: {e}")
        # Return a default value if API fails
        return 0


def calculate_contender(driver_standings, max_points):
    if not driver_standings:
        return []
    
    LEADER_POINTS = float(driver_standings[0]['points'])
    results = []

    for driver in driver_standings:
        driver_points = float(driver['points'])
        driver_max_points = driver_points + max_points

        results.append({
            'position': int(driver['position']),
            'code': driver['Driver']['code'],
            'full_name': f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
            'points': round(driver_points),
            'max_points': round(driver_max_points),
            'is_contender': 'Yes' if driver_max_points >= LEADER_POINTS else 'No'
        })

    return results


if __name__ == "__main__":
    main()