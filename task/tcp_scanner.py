import socket
import concurrent.futures
import sys
import time

def scan_port(host, port, timeout=1):
    """
    Функция пытается установить TCP-соединение с указанным портом.
    При успешном подключении возвращает номер порта, иначе None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                return port
    except Exception:
        pass
    return None

def print_progress(completed, total, bar_length=50):
    """
    Выводит строку с progress bar.
    """
    percent = completed / total
    filled_length = int(bar_length * percent)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    progress_message = f"\rСканирование: |{bar}| {completed}/{total} портов проверено"
    sys.stdout.write(progress_message)
    sys.stdout.flush()

def main():
    host = input("Введите имя хоста или IP-адрес: ").strip()

    start_port = 1
    end_port = 1024  # задаём диапазон портов (их можно изменить)
    total_ports = end_port - start_port + 1

    open_ports = []
    completed_ports = 0

    print(f"[+] Начало сканирования портов для {host}...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}

        # Обрабатываем результаты по мере завершения
        for future in concurrent.futures.as_completed(futures):
            completed_ports += 1
            port = futures[future]
            result = future.result()
            if result is not None:
                open_ports.append(result)
                # Вывод сообщения об открытом порте (перенос строки, чтобы не перетереть progress bar)
                sys.stdout.write(f"\nПорт {result} открыт")
                sys.stdout.flush()

            # Обновляем progress bar
            print_progress(completed_ports, total_ports)
            time.sleep(0.001)  # небольшая задержка для корректного обновления экрана

    # Завершаем progress bar переводом строки
    sys.stdout.write("\n")
    
    open_ports.sort()
    print("\n[*] Сканирование завершено.")
    if open_ports:
        print("Открытые порты:")
        for port in open_ports:
            print(port)
    else:
        print("Открытых портов не найдено.")

if __name__ == "__main__":
    main()
