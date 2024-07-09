import requests
from threading import Thread
from queue import Queue
import time

SERVER_BASE_URL = "http://localhost"
SERVER_PORT = 5555
NO_OF_REQUESTS = 100

def make_request(thread_id, response_queue):
    start_time = time.time()
    try:
        response = requests.get(f"{SERVER_BASE_URL}:{SERVER_PORT}/")
        response.raise_for_status() #If Http error occurred
        print(f"Response for request#{thread_id}: {response}")
        request_processing_time = time.time()
        response_queue.put((thread_id, request_processing_time - start_time, "Success"))
    except requests.RequestException:
        request_processing_time = time.time()
        response_queue.put((thread_id, request_processing_time - start_time, "Failure"))
        

def main():
    print("Let's test your server!!!!!")
    
    request_threads = []
    response_queue = Queue()
    overall_start_time = time.time()
    
    for i in range(1, NO_OF_REQUESTS + 1):
        print(f"Making mequest #{i}")
        thread = Thread(target=make_request, args=(i, response_queue))
        thread.start()
        request_threads.append(thread)
        time.sleep(0.2)
    for thread in request_threads:
        thread.join()
        
    overall_end_time = time.time()
    overall_total_processing_time = overall_end_time - overall_start_time
    
    total_succeess_requests = 0
    total_failed_requests = 0
    total_time_for_requests = 0
    
    print("\n\n-----------Test Results------------\n")
    
    while not response_queue.empty():
        thread_id, total_time_taken, result = response_queue.get()
        total_time_for_requests = total_time_for_requests + total_time_taken
        if result == "Success":
            total_succeess_requests+=1
        else:
            total_failed_requests+=1
            
    print(f"Total successful requests: {total_succeess_requests}")
    print(f"\nTotal failed requests: {total_failed_requests}")
    print(f"\nTotal time taken for request executions [assuming concurrency due to mutlicore on client side]: {overall_total_processing_time: .4f} seconds")
    print(f"\nTotal time taken for request executions [Sum of duration across all cores]: {total_time_for_requests:.4f} seconds")
    print(f"\nAverage time per request execution[assuming concurrency due to mutlicore on client side]: {overall_total_processing_time / NO_OF_REQUESTS:.4f} seconds")
    print(f"\nRequests per second[assuming concurrency due to mutlicore on client side]: {NO_OF_REQUESTS / overall_total_processing_time:.4f}")
    
    
if __name__ == "__main__":
    main()