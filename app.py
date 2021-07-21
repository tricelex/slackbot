import os
import random
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

slack_web_client = WebClient(token=os.environ['SLACK_API_TOKEN'])

MESSAGE_BLOCK = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": ""
    }
}

slack_event_adapter = SlackEventAdapter(os.environ['SLACK_EVENTS_TOKEN'], "/slack/events", app)


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})

    text = event.get("text")

    if "flip a coin" in text.lower():
        channel_id = event.get("channel")

        random_int = random.randint(0, 1)
        if random_int == 0:
            results = "Heads"
        else:
            results = "Tails"
        message = f"The results is {results}"

        MESSAGE_BLOCK["text"]["text"] = message

        x = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}

        return slack_web_client.chat_postMessage(**x)

@app.route("/")
def hello_world():
    return "Hello From the Other Side"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
