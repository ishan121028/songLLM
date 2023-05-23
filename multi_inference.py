import requests
import threading
import argparse
import time

def fast_inference(url, messages, max_length):
    
    def send_message(message):
        payload = {"text":message, "max_length":max_length}
        response = requests.post(url, json=payload)
        print(f"Response status code: {response.status_code}")
        print(response.json())
    
    threads = []
    for i in range(len(messages)):
        print(messages[i])
        thread = threading.Thread(target=send_message, args=(messages[i],))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    t2 = time.time()
    return t2

    
def main():
    parser = argparse.ArgumentParser(description='Multi threaded inference')
    parser.add_argument('--url', type=str, help='URL of the server')
    parser.add_argument('--messages', nargs="*", type=str, default=" ", help='All the prompts')
    parser.add_argument('--max_length',type=int, help='Maximum number of characters to be outputed by the model')
    args = parser.parse_args()

    if args.url:
        t1 = time.time()
        t2 = fast_inference(args.url,args.messages, args.max_length)
        print("{} seconds".format(t2-t1))
    else:
        print("Not valid arguments!")

if __name__ == "__main__":
    t1 = time.time()
    fast_inference('http://127.0.0.1:8000/generatetext', ['Hi', 'I', 'Applied', 'For', 'NimbleBox', 'Internship'], 500)
    t2 = time.time()
    print("{} seconds".format(t2-t1))