import requests
TOKEN = '567272478:AAHQvt2ZWVnEHlJO0qhNB0TgchGyypHL1dk'

def send_message(text,chat_id):
    url= 'https://api.telegram.org/bot{0}/sendMessage'.format(TOKEN)
    data = {'chat_id':chat_id, 'text':text}
    response = requests.post(url ,data=data)
    print(response.content)