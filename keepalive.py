from flask import Flask
app = Flask(_name_)

@app.route('/')
def home():
    return "Bot Alive!"

app.run(host='0.0.0.0', port=8080)