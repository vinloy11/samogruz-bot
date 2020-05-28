import requests
from flask import Flask, render_template, url_for, request, Response
from flask.views import MethodView
import os
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
        # response = request.get_json()
        # print(response)
        message = request.form.get("text")
        send_message(CHAT_ID, message)
        return render_template('index.html')
    return render_template('index.html')


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
    app.run()
    # app.run(port=5000, debug=True, use_reloader=True)