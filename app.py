from flask import Flask, render_template, request
from test_chat import bot

app = Flask(__name__)

messages = [
    {"sender": "bot", "content": "Hi there! How can I help you?"},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    user_message = request.form.get('question')  # Get user input from form
    if user_message:
        messages.append({"sender": "user", "content": user_message})  # Add user message to messages list
        # Add a bot response
        bot_response = {"sender": "bot", "content": f"{bot.get_response(user_message)}"}
        messages.append(bot_response)

    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
