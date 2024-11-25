import requests
import os
import dotenv

def last_chat_id(token):
    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            if 'result' in json_msg and json_msg['result']:
                # Get the chat ID from the most recent message
                return json_msg['result'][-1]['message']['chat']['id']
            else:
                print("No messages found in getUpdates.")
                return None
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print("Error in getUpdates:", e)
        return None

def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)

def send():
    dotenv.load_dotenv()
    token = os.getenv(str('TELEGRAM_TOKEN'))
    chat_id = last_chat_id(token)

    msg = "Olá! Seu interfone tocou! 📢"
    send_message(token, chat_id, msg)
