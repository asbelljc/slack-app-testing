import os
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()

# initialize slack app with your credentials
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

# do app things
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "callback_id": "home_view",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home_* :tada:",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app.",
                        },
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Click me!"},
                            }
                        ],
                    },
                ],
            },
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.event("app_mention")
def test_reply(client, event, say, logger):
    try:
        response = client.users_info(user=event["user"])
        user = response["user"]["name"]

        say(f"I was just mentioned by {user}")

    except Exception as e:
        logger.error(f"Error responding to app mention: {e}")


# start app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
