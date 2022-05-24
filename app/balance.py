from pprint import pprint

from app import API_KEY, PASSPHRASE, SECRET_KEY, Client


def main():
    client = Client(API_KEY, PASSPHRASE, SECRET_KEY)
    


if __name__ == "__main__":
    main()
