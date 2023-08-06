import pytmi


def send_message() -> None:
    username = input("Insert your Twitch username: ").lstrip()
    token = input("Insert your Twitch OAuth token: ").lstrip()
    channel = input("Insert the channel to join: ").lstrip()

    client = pytmi.TmiClient()
    client.login_oauth(token, username)

    client.join(channel)
    client.privmsg("Hello, Twitch")

    client.logout()


if __name__ == "__main__":
    try:
        send_message()
    except:
        print("Something went wrong.")
