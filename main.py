import requests
import json
from flask import Flask, render_template, url_for, request, Response
from flask.views import MethodView
import os

cars = [
    {
        'board': 2000,
        'crane': 1000,
        'costHour': 850,
        'minTime': 3,
        'text': 'Борт 2 т., стрела 1 т.',
        'image': '1.png',
        'id': 1
    },
    {
        'board': 3000,
        'crane': 1500,
        'costHour': 1000,
        'minTime': 3,
        'text': 'Борт 3 т., стрела 1.5 т.',
        'image': '1.png',
        'id': 2
    },
    {
        'board': 5000,
        'crane': 3000,
        'costHour': 1100,
        'minTime': 3,
        'text': 'Борт 5 т., стрела 3 т.',
        'image': '2.png',
        'id': 3
    },
    {
        'board': 8000,
        'crane': 5000,
        'costHour': 1800,
        'minTime': 4,
        'text': 'Борт 8 т., стрела 5 т.',
        'image': '3.jpg',
        'id': 4
    },
    {
        'board': 10000,
        'crane': 7000,
        'costHour': 2000,
        'minTime': 4,
        'text': 'Борт 10 т., стрела 7 т.',
        'image': '4.jpeg',
        'id': 5
    },
    {
        'board': 12000,
        'crane': 7000,
        'costHour': 2200,
        'minTime': 4,
        'text': 'Борт 12 т., стрела 7 т.',
        'image': '4.jpeg',
        'id': 6
    }

]
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
CHAT_ID = os.environ.get('CHAT_ID')
TOKEN = os.environ.get('TOKEN')
TELEGRAM_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


def parse_text(text_message):
    print(text_message)
    # '''/start /help, /sity /sp, @kiyv @python'''
    if '/' in text_message:
        if '/похуй' in text_message:
            message = 'Однозначно похуй.'
        elif '/start' or '/help' in text_message:
            message = 'Привет. В этом чате тебе буду приходить новые заявки.'
        return message
    else:
        return None


def send_message(chat_id, message):
    session = requests.Session()
    r = session.get(TELEGRAM_URL, params=dict(chat_id=chat_id, text=message, parse_mode='Markdown'))
    return r.json()


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        response = request.form
        # print(response)
        message = f'''
Оплата: {response.get("payment")}
Откуда: {response.get("from")}
Куда: {response.get("to")}
Время работ: {response.get("time") + 'ч.' if response.get('time') else 'Минималка'}
Ширина груза: {response.get("width")}см.
Высота груза: {response.get("height")}см.
Длина груза: {response.get("length")}см.
Вес груза: {response.get("weight")}кг.
Дополнительная информация о грузе: {response.get("additional")}
Телефон клиента: {response.get("phone")}
        '''
        send_message(CHAT_ID, message)
        return {'status': 'ok'}
    context = {
        'kek': 'lol',
        'cars': cars
    }
    if request.args.get('task') == 'getCars':
        return json.dumps(cars, ensure_ascii=None)
    return render_template('index.html', **context)

#
# @app.route('/?task=getCars', methods=["GET"])
# def get_cars():
#     return cars


@app.route('/car', methods=["POST"])
def send_car():
    response = request.form
    print(response)
    message = f'''
Нужен самогруз {response.get("text")}
Номер клиента {response.get("phone")}
        '''
    send_message(CHAT_ID, message)
    return {'status': 'ok'}


class BotApi(MethodView):

    def get(self):
        return 'Hi BOT class'

    def post(self):
        response = request.get_json()
        print(response)
        text_message = response['message']['text']
        chat_id = response['message']['chat']['id']
        tmp = parse_text(text_message)
        if tmp:
            send_message(chat_id, tmp)
        # print(response)
        return 'hi telega class'


# app.add_url_rule('/token/', view_func=BotApi.as_view('bot'))
app.add_url_rule(f'/{TOKEN}/', view_func=BotApi.as_view('bot'))

if __name__ == '__main__':
    # app.run()
    app.run(port=5000, debug=True, use_reloader=True)
