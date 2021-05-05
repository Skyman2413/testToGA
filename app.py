from flask import Flask, render_template, request
import json

app = Flask(__name__)
menu = [
    {"name": "Дежурный в данной группе в данный день", "url": "byDayAndGroup"},
    {"name": "Все дежурные в данный день", "url": "byDay"},
    {"name": " Календарь дежурств", "url": "calendar"}
]
with open("duty.json", "r", encoding="utf-8") as read_file:
    data = json.load(read_file)


def get_group_names():
    res = []
    for group in data:
        res.append(group['groupName'])
    return res


@app.route('/infoByDayAndGroup', methods=["POST"])
def info_by_day_and_group():
    groupName = (request.form['groupName'])
    day = int(request.form['day'])
    if day > 30:
        return render_template('byDayAndGroup.html', groupnames=get_group_names())
    res = "В данной группе в данный день дежурного нет"
    for group in data:
        if group['groupName'] == groupName:
            for person in group['usersDutyList']:
                if person['isOnDutyThisMonth'] is not True:
                    continue
                for dayNumber in person['dutyDays']:
                    if int(dayNumber['day']) == day:
                        if dayNumber['isDuty'] == 'true':
                            res = str(day) + " апреля в группе " + str(groupName) + \
                                   " дежурит: " + "<br>" + "<br>" + \
                                   person['userFullname'] + \
                                   "<br>" + person['userPhone'] + \
                                   "<br>" + person['userEmail']
                        break
    return res

@app.route('/infoByDay', methods=["POST"])
def info_by_day():
    res = []
    day = int(request.form['day'])
    if day > 30:
        return render_template('byDay.html')
    for group in data:
        for person in group['usersDutyList']:
            if person['isOnDutyThisMonth'] is not True:
                continue
            for dayNumber in person['dutyDays']:
                if int(dayNumber['day']) == day:
                    if dayNumber['isDuty'] == 'true':
                        res.append([group['groupName'], person['userFullname'],
                                    person['userPhone'], person['userEmail']])
                    break
    return render_template("infoByDay.html", data=res,)


@app.route('/calendar')
def input_calendar():
    return render_template('calendar.html', groupnames=get_group_names())


@app.route('/calendarInfo', methods=['POST'])
def calen():
    cal = {}
    for i in range(30):
        cal[i] = []
    for group in data:
        if group['groupName'] != request.form['sel']:
            continue
        for person in group['usersDutyList']:
            if person['isOnDutyThisMonth'] is not True :
                continue
            for dayNumber in person['dutyDays']:
                if dayNumber['isDuty'] == 'true':
                    day = int(dayNumber['day']) - 1
                    cal[day]=([
                            person['userFullname'],
                            person['userPhone'],
                            person['userEmail']])

    return render_template('calendar.html', data=cal, groupnames=get_group_names(),
                           selectedGroup=request.form['sel'])


@app.route('/byDayAndGroup')
def by_day_and_group():
    return render_template("byDayAndGroup.html", groupnames=get_group_names())


@app.route('/byDay')
def by_day():
    return render_template("byDay.html")


@app.route('/calendar')
def calendar():
    return render_template("calendar.html")


@app.route('/')
def index():
    return render_template("index.html", menu=menu)


if __name__ == '__main__':
    app.run(debug=False)
