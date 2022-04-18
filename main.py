from flask import Flask, render_template, request, flash,redirect, url_for
from config import settings
from flask_toastr import Toastr
from ext import Ext
import json

app = Flask(__name__)
toastr = Toastr(app)
app.config['SECRET_KEY'] = settings['secret_key']


@app.route('/', methods=["POST", "GET"])
def index():
    res = []
    with open('static/temp/data.json') as f:
        data = json.load(f)['message']

    for i in data:
        res.append((i['id'], i['coords'], i['swans']))

    return render_template('index.html', data=res)


@app.route('/create_road', methods=['POST'])
def create_road():
    if request.method == "POST":
        try:
            a_x = request.form['a_x']
            a_y = request.form['a_y']
            b_x = request.form['b_x']
            b_y = request.form['b_y']
            Ext().build(int(a_x), int(a_y), int(b_x), int(b_y))
            return 'True'
        except:
            return 'False'


@app.route('/update_map', methods=['POST'])
def update_map():
    if request.method == "POST":
        try:
            Ext().update()
            return 'True'
        except:
            return 'False'


@app.route('/add_detector', methods=["POST", "GET"])
def add_detector():
    if request.method == "POST":
        try:
            d = []
            k = 1
            temp_l = request.form['pokaz'].split(';')

            for i in temp_l:
                print(i.split(':'))
                d.append({'id': str(i.split(':')[0]), 'rate': float(i.split(':')[1])})
                k += 1
            x = int(request.form['coords'].split(';')[0])
            y = int(request.form['coords'].split(';')[1])

            upd_data = {'coords': [x, y],
                        'id': Ext().GetLastId(), 'swans': d}

            Ext().AddData(upd_data)
            return 'True'
        except Exception as ex:
            print(ex)
            return 'False'


@app.route('/delete_detector/<data_id>', methods=["POST", "GET"])
def delete_detector(data_id):
    try:
        Ext().DeleteData(data_id)
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))


@app.route('/get_json', methods=["POST"])
def get_json():
    try:
        Ext().UpdateData()
        return 'True'
    except Exception as ex:
        print(ex)
        return 'False'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

# Добавление
# a_dict = {'coords': [9, 5555555], 'id': 3, 'swans': [{'id': '28510575', 'rate': 0.6931}, {'id': '5e2dd59e', 'rate': 0.4808}, {'id': '6dced263', 'rate': 0.2069}, {'id': '583d82e4', 'rate': 0.1518}, {'id': '308a0e03', 'rate': 0.1348}, {'id': '6eebc626', 'rate': 0.2778}]}
# print(AddData(a_dict))

# DeleteData(1) - Удаление
