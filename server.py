import socket
from tkinter.filedialog import askopenfilename

if __name__ == "__main__":
    dict_url = {'/': 'index.html',
                '/hello_world.html': 'hello_world.html',
                '/test.html': 'test.html',
                '/tony.html': 'tony.html'}
else:
    print("Please select the text file containing the json dictionary that consists of:\n"
          "The url (key) and the full path of the corresponding HTML file (value)")
    file_dict = askopenfilename()
    import json
    with open(file_dict, 'r') as f:
        dict_url = json.load(f)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen()

while True:
    print('Listening for incoming connections...')
    client_socket, client_address = server_socket.accept()
    print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
    request_data = client_socket.recv(1024)
    request_lines = request_data.decode().split('\n')
    request_method, request_url, request_protocol = request_lines[0].split()

    if request_url[1:] != 'favicon.ico':
        try:
            file_name = dict_url[request_url]
        except KeyError:
            file_name = '404.html'
        with open(file_name, 'r') as file:
            file_content = file.read()
            if file_name == '404.html':
                response = 'HTTP/1.0 404 NOT FOUND\n\n' + file_content
            else:
                response = 'HTTP/1.0 200 OK\n\n' + file_content

        client_socket.sendall(response.encode())
    client_socket.close()
