import threading
import time

serial_index = 0
sse_index = 0
processing = False
current_text = ""
bk_instance = None
lock = threading.Lock()

def start_serial_sender(bk, text):
    global bk_instance, current_text, serial_index, sse_index, processing
    bk_instance = bk
    current_text = text
    serial_index = sse_index = 0
    processing = True
    threading.Thread(target=serial_sender).start()

def serial_sender():
    global serial_index, processing

    while serial_index < len(current_text) and processing:
        char = current_text[serial_index]
        bk_instance.serial_connection.reset_input_buffer()
        bk_instance.serial_connection.write(char.encode('utf-8'))

        ack = bk_instance.serial_connection.readline().decode('utf-8').strip()
        if ack == "OK":
            with lock:
                serial_index += 1
        else:
            time.sleep(0.1)

    processing = False

def get_stream_data():
    global sse_index
    while processing or sse_index < serial_index:
        with lock:
            if sse_index < serial_index:
                char = current_text[sse_index]
                sse_index += 1
                yield f"data: {char}\n\n"
            elif sse_index >= len(current_text):
                yield "data: done\n\n"
                break
        time.sleep(0.1)

