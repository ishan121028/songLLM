import requests
import threading
import argparse
import time

# def send_message(url, messages, max_length):
#     for message in messages:
#         payload = {"text": message, "max_length":max_length}
#         response = requests.post(url, json=payload)
#         if response.status_code == 200:
#             print(response.json())
#             print("Message sent successfully.")
#         else:
#             print("Failed to send the message.")

def stress_test(url, num_threads, num_requests, max_length):
    def make_requests():
        for _ in range(num_requests):
            payload = {"text":'',"max_length":max_length}
            response = requests.post(url, json=payload)
            print(f"Response status code: {response.status_code}")

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=make_requests)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser(description='Server Stress Test, Messaging, and Model CLI')
    parser.add_argument('--url', type=str, help='URL of the server')
    parser.add_argument('--threads', type=int, default=1, help='Number of threads to use for stress testing')
    parser.add_argument('--requests', type=int, default=1, help='Number of requests per thread for stress testing')
    parser.add_argument('--max_length',type=int, help='Maximum number of characters to be outputed by the model')
    args = parser.parse_args()


    if args.url and args.threads > 0 and args.requests > 0:
        stress_test(args.url, args.threads, args.requests, args.max_length)
    
    else:
        print("Not valid arguments!")


# if __name__ == '__main__':

#     main()