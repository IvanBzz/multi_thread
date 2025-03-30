#!/usr/bin/env python3
import socket

def main():
    host = 'localhost'  # можно указать IP-адрес сервера
    port = 12345        # порт должен совпадать с тем, который прослушивает сервер

    # Создаем TCP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(f"Подключено к серверу {host}:{port}")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return

        # Отправляем пример сообщения
        message = "Привет, сервер!"
        print(f"Отправка сообщения: {message}")
        s.sendall(message.encode())

        # Получаем эхо-ответ от сервера
        try:
            data = s.recv(1024)
            print(f"Получен ответ: {data.decode()}")
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")

if __name__ == "__main__":
    main()
