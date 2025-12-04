from flask import Flask, render_template
from f1_logic import get_driver_standings, get_max_points, calculate_contender


app = Flask(__name__)


@app.route('/')
def index():
    driver_standings = get_driver_standings()
    max_points = get_max_points()
    contenders = calculate_contender(driver_standings, max_points)
    return render_template('index.html', contenders=contenders)


if __name__ == '__main__':
    app.run(debug=True)