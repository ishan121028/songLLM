import requests
import threading
import argparse
import time

def send_message(url, message, max_length):
    payload = {"text":message, "max_length":max_length}
    response = requests.post(url, json=payload)
    print(f"Response status code: {response.status_code}")
    print(response.json())

def main():
    print("Hello")
    parser = argparse.ArgumentParser(description='Server Stress Test, Messaging, and Model CLI')
    parser.add_argument('--url', type=str, help='URL of the server')
    parser.add_argument('--messages', nargs="*", type=str, help='All the prompts')
    parser.add_argument('--max_length',type=int, help='Maximum number of characters to be outputed by the model')
    args = parser.parse_args()
    print(args.messages)
    for message in args.messages:
            send_message(args.url, message, args.max_length)

if __name__ == "__main__":
        messages = ["I", "have", "applied", "for", "NimbleBox", "Internship"]
        url = 'http://127.0.0.1:8000/generatetext'
        max_length = 500
        t1 = time.time()
        for message in messages:
          send_message(url, message, max_length)
        t2 = time.time()
        print("{} seconds".format(t2-t1))
         
          