from flask import Flask, escape, render_template, request, Response, jsonify, current_app
import datetime
import pytz

app = Flask(__name__)

cities = {'newyork': 'New York', 'moscow': 'Moscow', 'berlin': 'Berlin', 'tokyo': 'Tokyo'}
timz = {'New York': 'America/New_York', 'Moscow': 'Europe/Moscow', 'Berlin': 'Europe/Berlin', 'Tokyo': 'Asia/Tokyo'}


class Time:
    def __init__(self, city):
        self.city = city

    def hour(self):
        return datetime.datetime.now(tz=pytz.timezone(timz[self.city])).strftime("%H")

    def minute(self):
        return datetime.datetime.now(tz=pytz.timezone(timz[self.city])).strftime("%M")


@app.route('/')
def hello():
    return app.send_static_file('index.html')


@app.route('/<city>')
def city(city):
    if city in cities:
        return render_template('time.html', city=cities[city],
                               time='{0}:{1}'.format(Time(cities[city]).hour(), Time(cities[city]).minute()))

    return app.send_static_file('not_found.html')


@app.route("/api", methods=["GET", "POST"])
def get_data():
    if 'city' in request.args.to_dict():
        if request.args.get('city', None) in cities:
            return jsonify(city=cities[request.args.get('city')],
                           hour=Time(cities[request.args.get("city")]).hour(),
                           minute=Time(cities[request.args.get("city")]).minute())
    return app.send_static_file('not_found.html')


if __name__ == '__main__':
    app.run()
