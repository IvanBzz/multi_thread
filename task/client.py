import socket

def main():
    host = '127.0.0.1'  # адрес сервера
    port = 65432        # порт сервера (должен совпадать с портом, указанным в сервере)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[*] Подключено к серверу {host}:{port}")

    try:
        while True:
            # Пользователь вводит сообщение
            message = input("Введите сообщение (или 'exit' для выхода): ")
            if message.lower() == 'exit':
                break
            # Отправляем сообщение серверу
            client_socket.sendall(message.encode())
            # Получаем эхо-ответ от сервера
            data = client_socket.recv(1024)
            print(f"Эхо от сервера: {data.decode()}")
    except KeyboardInterrupt:
        print("\n[*] Завершение клиента.")
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()
