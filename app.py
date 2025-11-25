from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime_t import datetime

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/gsheet-key.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Gym_Leads").sheet1

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    name = data.get("name")
    phone = data.get("phone")
    goal = data.get("goal")
    username = data.get("username")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([name, phone, goal, timestamp, username])

    return {"status": "success"}, 200

if __name__ == '__main__':
    app.run(port=5000)
