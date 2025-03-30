import socket
import threading

def handle_client(client_socket, client_address):
    """
    Функция для обслуживания подключённого клиента.
    Принимает данные с клиента, выводит их на экран и отправляет обратно (эхо).
    """
    print(f"[+] Подключен клиент: {client_address}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"[-] Клиент {client_address} отключился.")
                break
            print(f"[{client_address}] Получено: {data.decode()}")
            client_socket.sendall(data)
        except ConnectionResetError:
            print(f"[-] Клиент {client_address} принудительно закрыл соединение.")
            break
        except Exception as exc:
            print(f"[!] Ошибка при работе с клиентом {client_address}: {exc}")
            break
    client_socket.close()

def main():
    host = '0.0.0.0'   # прослушивание всех интерфейсов
    port = 65432       # произвольный порт (можно изменить при необходимости)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Сервер запущен на {host}:{port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            # При каждом новом подключении создается поток, который обслуживает клиента.
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            client_thread.start()
        except KeyboardInterrupt:
            print("\n[*] Завершение работы сервера.")
            break
        except Exception as exc:
            print(f"[!] Ошибка: {exc}")

    server_socket.close()

if __name__ == '__main__':
    main()
