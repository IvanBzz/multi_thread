import socket
import threading

# Словарь пользователей для аутентификации (логин: пароль)
USERS = {
    "alice": "password1",
    "bob": "password2",
    "charlie": "password3"
}

# Список для хранения истории сообщений
message_history = []
history_lock = threading.Lock()

# Список клиентов для рассылки сообщений (каждый элемент — (socket, user_name))
clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    """
    Отправляет сообщение всем подключенным клиентам, за исключением отправителя (если задан)
    """
    with clients_lock:
        for client_socket, _ in clients:
            # Не отправляем отправителю своё же сообщение
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode("utf-8"))
                except Exception as e:
                    print(f"Ошибка отправки сообщения клиенту: {e}")

def handle_client(client_socket, address):
    print(f"[{address}] Новое подключение.")
    try:
        client_socket.sendall("Добро пожаловать! Пожалуйста, авторизуйтесь.\n".encode("utf-8"))
        # Запрос логина
        client_socket.sendall("Логин: ".encode("utf-8"))
        login = client_socket.recv(1024).decode("utf-8").strip()
        client_socket.sendall("Пароль: ".encode("utf-8"))
        password = client_socket.recv(1024).decode("utf-8").strip()

        # Простая проверка аутентификации
        if USERS.get(login) != password:
            client_socket.sendall("Неверные логин или пароль. Соединение разорвано.\n".encode("utf-8"))
            client_socket.close()
            return

        client_socket.sendall(f"Привет, {login}! Вы вошли в чат.\n".encode("utf-8"))
        
        # Добавляем нового клиента в список
        with clients_lock:
            clients.append((client_socket, login))
        
        # Отправляем историю сообщений новому пользователю
        with history_lock:
            if message_history:
                client_socket.sendall("---- История сообщений ----\n".encode("utf-8"))
                for msg in message_history:
                    client_socket.sendall((msg + "\n").encode("utf-8"))
                client_socket.sendall("--------------------------\n".encode("utf-8"))

        # Оповещаем остальных о новом участнике
        broadcast(f"Системное сообщение: {login} присоединился к чату.", sender_socket=client_socket)
        
        # Основной цикл приема сообщений от клиента
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode("utf-8").strip()
            framed_message = f"{login}: {message}"
            print(f"[{address}] {framed_message}")
            
            # Добавляем сообщение в историю
            with history_lock:
                message_history.append(framed_message)
                # Можно ограничить историю до N сообщений, например:
                # if len(message_history) > 100:
                #     message_history.pop(0)
            
            # Рассылаем сообщение всем остальным клиентам
            broadcast(framed_message, sender_socket=client_socket)
    except Exception as e:
        print(f"Ошибка в соединении с {address}: {e}")
    finally:
        # Удаляем клиента из списка
        with clients_lock:
            clients[:] = [(sock, name) for sock, name in clients if sock != client_socket]
        broadcast(f"Системное сообщение: {login} покинул чат.", sender_socket=client_socket)
        client_socket.close()
        print(f"[{address}] Соединение закрыто.")

def start_server(host="0.0.0.0", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()
    except KeyboardInterrupt:
        print("Сервер остановлен пользователем.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
