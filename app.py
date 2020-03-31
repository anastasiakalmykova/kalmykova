from flask import Flask, request, render_template, jsonify
import datetime
from pytz import timezone
app = Flask(__name__)
cities = ['moscow', 'berlin', 'newyork', 'tokyo']
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/newyork")
def local_time1(zone1='America/New_York'):
    amer_zone = timezone(zone1)
    amer_zone_time = datetime.datetime.now(amer_zone)
    return render_template("time.html",
                           city='New York',
                           time=amer_zone_time.strftime('%H:%M'))
@app.route('/berlin')
def local_time2(zone2='Europe/Berlin'):
    other_zone = timezone(zone2)
    other_zone_time = datetime.datetime.now(other_zone)
    return render_template("time.html",
                           city='Berlin',
                           time=other_zone_time.strftime('%H:%M'))
@app.route('/tokyo')
def local_time3(zone='Asia/Tokyo'):
    other_zone = timezone(zone)
    other_zone_time = datetime.datetime.now(other_zone)
    return render_template("time.html",
                           city='Tokyo',
                           time=other_zone_time.strftime('%H:%M'))

@app.route('/moscow')
def local_time4(zone4='Europe/Moscow'):
    mos_zone = timezone(zone4)
    mos_zone_time = datetime.datetime.now(mos_zone)
    return render_template("time.html",
                           city='Moscow',
                           time=mos_zone_time.strftime('%H:%M'))
@app.route('/<city>')
def no_city1(city):
    if city is not cities:
        return render_template("not_found.html")
@app.route('/api?city=moscow', methods=['GET'])
def mosc():
    return jsonify(city = 'Moscow', hour = datetime.datetime.now(timezone(zone='Europe/Moscow')).hour, minute = datetime.datetime.now(timezone(zone = 'Europe/Moscow')).minute)


@app.route('/api?city=tokyo', methods=['GET'])
def tok():
    return jsonify(city = 'Tokyo', hour = datetime.datetime.now(timezone(zone='Asia/Tokyo')).hour, minute = datetime.datetime.now(timezone(zone = 'Asia/Tokyo')).minute)


@app.route('/api?city=berlin', methods=['GET'])
def ber():
    return jsonify(city = 'Berlin', hour = datetime.datetime.now(timezone(zone='Europe/Berlin')).hour, minute = datetime.datetime.now(timezone(zone = 'Europe/Berlin')).minute)


@app.route('/api?city=newyork', methods=['GET'])
def york():
    return jsonify(city = 'New York', hour = datetime.datetime.now(timezone(zone='America/New_York')).hour, minute = datetime.datetime.now(timezone(zone = 'America/New_York')).minute)


@app.route('/api?city=<city>', methods=['GET'])
def no_city(city):
    if city is not cities:
        return jsonify(  )


if __name__ == '__main__':
    app.run()