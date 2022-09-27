import socket
import views

URLS = {
    '/': views.index,
    '/blog': views.blog
}


def parse_request(request):
    parsed = request.split('\n')
    # other = map(lambda x: x.strip(), parsed[1:])
    method, url, http_version = parsed[0].split(' ')
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 Method Not Allowed\n\n', 405
    if not url in URLS:
        return 'HTTP/1.1 404 Method Not found\n\n', 404
    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code, url):
    match code:
        case 404: return '<h1>404 Not Found</h1>'
        case 405: return '<h1>405 Method Not Allowed</h>'
    return URLS[url]()


def generate_response(request):
    """ like VIEW """
    request_method, request_url = parse_request(request)
    headers, code = generate_headers(request_method, request_url)
    body = generate_content(code, request_url)
    return (headers + body).encode()


def run():
    """ Create network socket and answer to requests"""

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP/IPv4
    server_address = ('localhost', 8001)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(server_address)  # привязать домен и порт
    server_socket.listen()  # начать прослушивание порта

    while True:
        client_socket, addr = server_socket.accept()  # принять соединение
        request = client_socket.recv(1024)  # получить запрос
        request = request.decode('utf-8')
        print(f'{request}\n{addr=}')

        response = generate_response(request)
        client_socket.sendall(response)

        client_socket.close()


if __name__ == '__main__':
    run()
