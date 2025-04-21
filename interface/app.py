# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response, redirect, url_for
from BrailleKeyboard import BrailleKeyboard
import os
import time
import threading

app = Flask(__name__)

# Configurações iniciais
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_key_insegura')

# Cria o diretório de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Variáveis globais para controle do processo
current_text = ""
serial_index = 0       # Índice controlado pela thread serial
sse_index = 0          # Índice controlado pelo SSE
processing = False
bk_instance = None
lock = threading.Lock()  # Lock para sincronização


def delete_file(filepath):
    """Apaga um arquivo se ele existir."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            print(f"[INFO] Arquivo apagado: {filepath}")
    except Exception as e:
        print(f"[ERRO] Falha ao apagar arquivo {filepath}: {e}")


def serial_sender():
    global serial_index, processing, bk_instance

    while serial_index < len(current_text) and processing:
        char = current_text[serial_index]

        retries = 0
        success = False
        max_retries = 3

        while retries < max_retries and not success and processing:
            try:
                bk_instance.serial_connection.reset_input_buffer()
                bk_instance.serial_connection.write(char.encode('utf-8'))

                ack = bk_instance.serial_connection.readline().decode('utf-8').strip()
                
                if ack == "OK":
                    success = True
                    print(f"[✔] Caractere '{char}' (ord: {ord(char)}) confirmado.")
                else:
                    retries += 1
                    if retries < max_retries:  # Só mostra a mensagem se ainda tiver tentativas
                        print(f"[⚠] Tentativa {retries}/{max_retries} para '{char}'")
                    time.sleep(0.1)

            except Exception as e:
                print(f"[✘] Erro durante envio: {e}")
                processing = False
                break

        if not success:
            print(f"[✘] Falha no envio de '{char}' após {retries} tentativas. Pulando caractere.")
        
        # Avança para o próximo caractere independentemente do sucesso
        with lock:
            serial_index += 1

    processing = False
    print("[INFO] Thread serial finalizada")


@app.route('/stream')
def stream():
    def generate_serial_stream():
        global sse_index

        print("[SSE] Conexão estabelecida com cliente")

        while processing or sse_index < len(current_text):
            with lock:
                if sse_index < serial_index:
                    char = current_text[sse_index]
                    # print(f"[SSE] Enviando caractere: {char}")
                    sse_index += 1
                    yield f"data: {char}\n\n"

                elif sse_index >= len(current_text):
                    # print("[SSE] Envio completo")
                    yield "data: done\n\n"
                    break

            time.sleep(0.1)  # Aumentado para estabilidade

    return Response(
        generate_serial_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Content-Type': 'text/event-stream; charset=utf-8'
        }
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    global current_text, serial_index, sse_index, processing, bk_instance
    global pdf_filepath_global, txt_filepath_global

    # Resetar variáveis a cada novo envio
    current_text = ""
    serial_index = 0
    sse_index = 0
    processing = False
    pdf_filepath_global = None
    txt_filepath_global = None

    if request.method == 'POST':
        if 'pdf' not in request.files:
            return "Nenhum arquivo enviado"

        file = request.files['pdf']
        if file.filename == '':
            return "Nenhum arquivo selecionado"

        if file and file.filename.endswith('.pdf'):
            try:
                # Salva o PDF
                pdf_filename = file.filename
                pdf_filepath_global = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                file.save(pdf_filepath_global)

                # Processa o texto
                bk = BrailleKeyboard()
                if bk.connect_serial():
                    texto = bk.extract_text_from_pdf(pdf_filepath_global, page_number=0)
                    print(f"[INFO] Texto extraído: {texto[:50]}...")

                    # Cria o .txt com o texto extraído
                    txt_filename_base = pdf_filename.rsplit('.', 1)[0]
                    txt_filename = f"{txt_filename_base}.txt"
                    txt_filepath_global = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)

                    with open(txt_filepath_global, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(texto or "[Texto vazio ou não extraído]")

                    print(f"[INFO] Arquivo TXT criado em: {txt_filepath_global}")

                    # Atualiza variáveis globais
                    current_text = texto.upper()
                    print(f"[INFO] Texto preparado para envio: {current_text[:50]}...")

                    with lock:
                        serial_index = 0
                        sse_index = 0
                        processing = True
                        bk_instance = bk

                    # Inicia thread de envio serial
                    sender_thread = threading.Thread(target=serial_sender)
                    sender_thread.start()

                    return redirect(url_for('streaming'))

                return "Erro ao conectar ao dispositivo"

            except Exception as e:
                print(f"[ERRO] Ocorreu um erro: {e}")
                return "Erro ao processar o PDF"

    return render_template('index.html')


@app.route('/streaming')
def streaming():
    return render_template('streaming.html')


if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=True, port=5000)
    finally:
        delete_file(pdf_filepath_global)
        print(f'[INFO] Arquivo PDF apagado: {pdf_filepath_global}')

        delete_file(txt_filepath_global)
        print(f'[INFO] Arquivo TXT apagado: {txt_filepath_global}')

        print("[INFO] Arquivos temporários apagados.")
