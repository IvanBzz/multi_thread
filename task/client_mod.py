import socket

def main():
    server_host = '127.0.0.1'  # IP-адрес сервера (если сервер запущен на той же машине, используем 127.0.0.1)
    server_port = 65432        # порт сервера (должен совпадать с портом, указанным в сервере)

    # Создаем сокет для подключения к серверу
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((server_host, server_port))
            print(f"[*] Подключено к серверу {server_host}:{server_port}")
        except Exception as e:
            print(f"[!] Не удалось подключиться к серверу: {e}")
            return

        while True:
            # Получаем сообщение от пользователя
            message = input("Введите сообщение (или 'exit' для выхода): ")
            if message.lower() == 'exit':
                break
            # Отправляем сообщение серверу
            client_socket.sendall(message.encode())
            # Получаем и выводим ответ от сервера
            data = client_socket.recv(1024)
            print("Эхо от сервера:", data.decode())

if __name__ == '__main__':
    main()
