from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# API Key

openai.api_key = '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'

# Main function we use to connect to ChatGPT
def generate_chat_response(message):
    prompt = "You: {}\nChatGPT:".format(message)
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
        timeout=10
    )
    return response.choices[0].text.strip().replace("ChatGPT:", "")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form['message']
        if message.strip() == "":
            return render_template('index.html', error_message="Message is required.")
        try:
            chat_response = generate_chat_response(message)
            return render_template('results.html', message=message, chat_response=chat_response)
        except Exception as e:
            error_message = str(e)
            return render_template('results.html', message=message, error_message=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
