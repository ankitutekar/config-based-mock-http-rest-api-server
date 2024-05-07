import json
import socket

HTTP_RESPONSE_STATUS = {
    "200": "HTTP/1.1 200 OK",
    "404": "HTTP/1.1 404 Not Found",
    "201": "HTTP/1.1 201 CREATED"
}

HTTP_CONTENT_TYPES = {
    "PLAINTEXT": "text/plain",
    "JSON": "application/json",
    "STREAM": "application/octet-stream"
}

CRLF = "\r\n"
response_body_separator = f"{CRLF}{CRLF}"

config = { }

def handle_request(conn_ref, address):
    global config
    try:
        print(f"Received request from {address}")

        requestData = conn_ref.recv(40966).decode()
        print(f"Request details: {requestData}")

        reqLines = requestData.split(f"{CRLF}")

        firstLineContents = reqLines[0].split(" ")
        routePath = firstLineContents[1]
        print(f"Received path: {routePath}")
        
        matching_paths = [route for route in config["routes"] if route["path"] == routePath and route["verb"] == "GET"]
        
        if (matching_paths and len(matching_paths) == 1):
            print("Matching path found!!")
            matching_path = matching_paths[0]
            response_type = matching_path["responseType"]
            response_data = matching_path["reponse"]
            conn_ref.send(form_Response(HTTP_RESPONSE_STATUS[response_data["statusCode"]],
                                        HTTP_CONTENT_TYPES[response_type],
                                        response_data["data"]))
        else:
            print("No matching path found!")
            conn_ref.send(form_Response(HTTP_RESPONSE_STATUS['NOT_FOUND']))

    except socket.error as e:
        print(f"Socket error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    except KeyboardInterrupt:
        print("Server stopped by user")
    finally:
        conn_ref.close()
        print(f"Connection closed for {address}")


def form_Response(response_status, content_type=None, content=None):
    resp = f"{response_status}"
    if content:
        if(content_type ==  HTTP_CONTENT_TYPES["JSON"]):
            content = json.dumps(content)
        resp = resp + \
            f"{CRLF}Content-Type: {content_type}{CRLF}Content-Length: {len(content)}{response_body_separator}{content}"
    else:
        resp = resp + response_body_separator
    return resp.encode('utf-8')

def read_config_file(filename):
    global config
    with open(filename, 'r') as file:
        config = json.load(file)
        
        
def main():
    print("Your server starting up........")
    print("Reading configuration file........")
    read_config_file("config.json")
        
    server_socket = socket.create_server(("localhost", config["port"]))
    print(f"Server successfully started!! Listening on {config['port']}")
    try:
        while True:
            conn_ref, address = server_socket.accept()
            handle_request(conn_ref, address)
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        server_socket.close()
        
if __name__ == "__main__":
    main()