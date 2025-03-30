import socket
import threading

# Функция для обработки каждого клиента
def handle_client(client_socket, client_address):
    print(f"[+] Подключен клиент: {client_address}")
    while True:
        try:
            # Получаем данные от клиента
            data = client_socket.recv(1024)
            if not data:
                print(f"[-] Клиент {client_address} отключился.")
                break
            # Выводим полученные данные
            print(f"[{client_address}] Получено: {data.decode()}")
            # Отправляем эхо-ответ клиенту
            client_socket.sendall(data)
        except ConnectionResetError:
            print(f"[-] Клиент {client_address} принудительно закрыл соединение.")
            break
    client_socket.close()

def main():
    host = '0.0.0.0'   # прослушиваем все интерфейсы
    port = 65432       # произвольный порт

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Сервер запущен на {host}:{port}")

    while True:
        # Принимаем новое подключение
        client_socket, client_address = server_socket.accept()
        # Создаем и запускаем новый поток для работы с клиентом
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        client_thread.start()

if __name__ == '__main__':
    main()
