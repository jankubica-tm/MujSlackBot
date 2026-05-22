import os
import yaml
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def send(client, email, message):
    try:
        user = client.users_lookupByEmail(email=email)
        user_id = user["user"]["id"]
        client.chat_postMessage(channel=user_id, text=message)
        print(f"Sent to {email}: {message}")
    except SlackApiError as e:
        print(f"Failed to send to {email}: {e.response['error']}")


def main():
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    with open("reminders.yaml") as f:
        config = yaml.safe_load(f)

    for reminder in config.get("reminders", []):
        recipients = reminder["to"]
        if isinstance(recipients, str):
            recipients = [recipients]
        message = reminder.get("message", "HEY")
        for email in recipients:
            send(client, email, message)


if __name__ == "__main__":
    main()
