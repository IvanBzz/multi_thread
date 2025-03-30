import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"))
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
            break

def main():
    host = "localhost"
    port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Запуск потока для принятия сообщений
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    
    # Читаем ввод с консоли и отправляем на сервер
    while True:
        try:
            message = input()
            if message.lower() == "exit":
                break
            sock.sendall(message.encode("utf-8"))
        except Exception as e:
            print(f"Ошибка отправки данных: {e}")
            break

    sock.close()

if __name__ == "__main__":
    main()
