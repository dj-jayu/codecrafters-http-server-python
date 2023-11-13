# Uncomment this to pass the first stage
import socket
import re
from urllib.parse import unquote


def generate_content(http_version, status_code, content_type, content):
    # generates the header and body response
    response_headers = [f'HTTP/{http_version} {status_code}', f'Content-Type: {content_type}',
                        f'Content-Length: {len(content)}']
    response_body = ''
    if len(content) > 0:
        response_body = content
    return '\r\n'.join(response_headers) + '\r\n\r\n' + response_body


def capture_final_path(path):
    # receives an unquoted path and returns what is between <>
    pattern = r'/echo/(.+)$'
    match = re.search(pattern, path)
    return match.group(1) if match else ''

def get_user_agent(client_data):
    print(client_data)
    pattern = r'User-Agent: (.*)'
    match = re.search(pattern, client_data)
    return match.group(1).strip() if match else ''

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)

    server_socket.listen()
    client_socket, address = server_socket.accept()
    client_data = client_socket.recv(1024).decode('utf-8')
    first_line = client_data.splitlines()[0]
    path = unquote(first_line.split(" ")[1])
    if path == '/':
        http_response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith('/echo'):
        content = capture_final_path(unquote(path))
        http_response = generate_content('1.1', '200 OK', 'text/plain', content)
    elif path == '/user-agent':
        user_agent = get_user_agent(client_data)
        http_response = generate_content('1.1', '200 OK', 'text/plain', user_agent)
    else:
        http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
    print(http_response)
    client_socket.sendall(http_response.encode())
    client_socket.close()


if __name__ == "__main__":
    main()
