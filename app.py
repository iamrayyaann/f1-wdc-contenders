from flask import Flask, render_template
from f1_logic import get_driver_standings, get_max_points, calculate_contender


app = Flask(__name__)


@app.route('/')
def index():
    try:
        driver_standings = get_driver_standings()
        if not driver_standings:
            print("DEBUG: driver_standings is empty")
            return render_template('index.html', contenders=[], error="Unable to fetch driver standings. The F1 API may be temporarily unavailable. Please try again later.")
        
        print(f"DEBUG: Successfully fetched {len(driver_standings)} driver standings")
        
        max_points = get_max_points()
        if max_points is None or max_points <= 0:
            print(f"DEBUG: max_points is {max_points}")
            return render_template('index.html', contenders=[], error="Unable to calculate maximum possible points for remaining races. Please try again later.")
        
        contenders = calculate_contender(driver_standings, max_points)
        print(f"DEBUG: Calculated {len(contenders)} contenders")
        return render_template('index.html', contenders=contenders)
    except ValueError as e:
        # Handle validation errors from calculate_contender
        print(f"Validation error in index route: {e}")
        return render_template('index.html', contenders=[], error=str(e))
    except Exception as e:
        print(f"Error in index route: {e}")
        import traceback
        traceback.print_exc()
        return render_template('index.html', contenders=[], error=f"An error occurred: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)