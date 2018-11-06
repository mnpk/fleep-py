from fleep_client import FleepClient


def main():
    c = FleepClient()
    # connect using env variables: FLEEP_EMAIL, FLEEP_PASSWORD
    c.connect()
    c.send('conv-id', 'hello')


if __name__ == "__main__":
    main()

