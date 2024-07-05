import requests
from threading import Thread

SERVER_BASE_URL = "http://localhost"
SERVER_PORT = 5555
NO_OF_REQUESTS = 100

def main():
    print("Let's test your server!!!!!")
    for i in range(1, NO_OF_REQUESTS):
        print(f"Making mequest #{i}")
        thread = Thread(target=make_request)
        thread.start()
    
def make_request():
    response = requests.get(f"{SERVER_BASE_URL}:{SERVER_PORT}/")
    print(f"Response: {response}")
    
if __name__ == "__main__":
    main()