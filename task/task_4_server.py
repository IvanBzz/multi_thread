#!/usr/bin/env python3
import socket
import threading
import time
import sys

# Глобальные переменные для логов и состояния сервера
logs = []
logs_lock = threading.Lock()

# События для управления сервером
stop_event = threading.Event()
pause_event = threading.Event()

# Файл идентификации (в качестве примера, где может храниться идентификатор)
IDENT_FILE = "ident.txt"

def add_log(message: str):
    with logs_lock:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logs.append(f"[{timestamp}] {message}")
    print(f"LOG: {message}")  # Для оперативного отображения в консоли

def server_thread(port: int):
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Переиспользование адреса
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(('', port))
    except Exception as e:
        add_log(f"Ошибка при привязке портa {port}: {e}")
        return

    server_socket.listen(5)
    add_log(f"Сервер запущен на порту {port}")

    # Устанавливаем таймаут, чтобы периодически проверять состояние остановки
    server_socket.settimeout(1.0)

    while not stop_event.is_set():
        # Если режим "Паузы" включен, не принимаем подключения
        if pause_event.is_set():
            time.sleep(1)
            continue
        try:
            client_sock, client_addr = server_socket.accept()
            add_log(f"Новое подключение от {client_addr}")
            # Обработка клиента осуществляется в дочернем потоке (можно расширить функциональность)
            threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True).start()
        except socket.timeout:
            # Таймаут позволяет проверять состояние stop_event
            continue
        except Exception as e:
            add_log(f"Ошибка в серверном потоке: {e}")
            break
    server_socket.close()
    add_log("Сервер остановлен.")

def handle_client(client_sock: socket.socket, client_addr):
    try:
        with client_sock:
            client_sock.settimeout(5.0)
            # Простой эхо-сервер, считываем данные и отправляем обратно
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                add_log(f"Получены данные от {client_addr}: {data.decode().strip()}")
                client_sock.sendall(data)
    except Exception as e:
        add_log(f"Ошибка при обработке клиента {client_addr}: {e}")

def clear_logs():
    global logs
    with logs_lock:
        logs = []
    add_log("Логи очищены.")

def show_logs():
    with logs_lock:
        if not logs:
            print("Лог пуст.")
        else:
            print("------ Логи ------")
            for entry in logs:
                print(entry)
            print("------------------")

def clear_ident_file():
    try:
        with open(IDENT_FILE, "w") as f:
            f.write("")
        add_log("Файл идентификации очищен.")
    except Exception as e:
        add_log(f"Ошибка очистки файла идентификации: {e}")

def main():
    port = 12345  # Можно изменить порт или получать из аргументов
    server = threading.Thread(target=server_thread, args=(port,), daemon=True)
    server.start()

    add_log("Основной поток запущен. Ожидание команд пользователя.")
    print("Доступные команды:")
    print(" exit          - Завершить работу сервера")
    print(" pause         - Приостановить прослушивание порта")
    print(" resume        - Возобновить прослушивание порта")
    print(" logs          - Показать логи")
    print(" clear_logs    - Очистить логи")
    print(" clear_ident   - Очистить файл идентификации")

    # Цикл команд командной строки
    while True:
        try:
            command = input("Введите команду: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            command = "exit"
        if command == "exit":
            add_log("Получена команда остановки сервера.")
            stop_event.set()
            break
        elif command == "pause":
            if not pause_event.is_set():
                pause_event.set()
                add_log("Прослушивание порта приостановлено.")
                print("Прослушивание порта приостановлено.")
            else:
                print("Сервер уже на паузе.")
        elif command == "resume":
            if pause_event.is_set():
                pause_event.clear()
                add_log("Прослушивание порта возобновлено.")
                print("Прослушивание порта возобновлено.")
            else:
                print("Сервер уже работает.")
        elif command == "logs":
            show_logs()
        elif command == "clear_logs":
            clear_logs()
        elif command == "clear_ident":
            clear_ident_file()
        else:
            print("Неизвестная команда.")

    print("Ожидание завершения серверного потока...")
    server.join()
    print("Сервер завершил работу. Выход.")

if __name__ == "__main__":
    main()
