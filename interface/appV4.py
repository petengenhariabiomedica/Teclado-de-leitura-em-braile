# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response, redirect, url_for
from BrailleKeyboard import BrailleKeyboard
import os
import time
import threading
import queue

app = Flask(__name__)

# Configurações do aplicativo
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_key_insegura')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Variáveis globais para controle de estado
current_text = ""
processing = False
bk_instance = None
pdf_filepath_global = None
txt_filepath_global = None
lock = threading.Lock()
sent_chars = 0  # Contador de caracteres enviados
ack_received = threading.Event()  # Evento para sincronização

def delete_file(filepath):
    """Remove arquivos temporários de forma segura."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            print(f"[INFO] Arquivo removido: {filepath}")
    except Exception as e:
        print(f"[ERRO] Falha ao remover arquivo {filepath}: {e}")

def serial_sender():
    global sent_chars, processing, bk_instance
    BATCH_SIZE = 4  # Reduzir tamanho do lote
    TIMEOUT = 1.0   # Aumentar timeout
    
    print("[SERIAL] Thread de envio iniciada")
    
    with lock:
        local_sent = sent_chars
    
    while local_sent < len(current_text) and processing:
        batch = current_text[local_sent:local_sent+BATCH_SIZE]
        
        try:
            # Limpar buffer antes do envio
            bk_instance.serial_connection.reset_input_buffer()
            
            # Envio síncrono
            bk_instance.serial_connection.write(batch.encode('utf-8'))
            bk_instance.serial_connection.flush()
            
            # Ler múltiplos ACKs
            ack_count = 0
            start_time = time.time()
            
            while ack_count < len(batch) and (time.time() - start_time) < TIMEOUT:
                ack = bk_instance.serial_connection.read_until(b'\n', size=8).decode().strip()
                if ack == "OK":
                    ack_count += 1
                    print(f"[SERIAL] Recebido ACK {ack_count}/{len(batch)}")
                    ack_received.set()

            # Atualização crítica
            with lock:
                sent_chars += ack_count
                local_sent = sent_chars
            
            print(f"[PROGRESSO] Enviados {local_sent}/{len(current_text)} caracteres")
            
            if ack_count < len(batch):
                print(f"[AVISO] ACKs incompletos. Tentando reenviar...")
                time.sleep(0.2 * (len(batch) - ack_count))  # Backoff exponencial
        
        except Exception as e:
            print(f"[ERRO] Falha no envio: {str(e)}")
            processing = False
            break
    
    processing = False
    print("[SERIAL] Thread finalizada")

@app.route('/stream')
def stream():
    def generate_serial_stream():
        last_sent = 0
        total_chars = len(current_text)
        
        print("[SSE] Iniciando stream de eventos")
        
        while processing or last_sent < total_chars:
            with lock:
                current_progress = sent_chars
            
            # Envia novos caracteres quando disponíveis
            if current_progress > last_sent:
                new_chars = current_text[last_sent:current_progress]
                last_sent = current_progress
                yield f"data: {new_chars}\n\n"
                print(f"[SSE] Enviado: {new_chars}")
            
            # Controle de velocidade de atualização
            if current_progress == last_sent:
                # Aguarda novo ACK ou timeout
                ack_received.wait(timeout=0.1)
                ack_received.clear()
            else:
                time.sleep(0.05)  # Pequeno delay para batches grandes
        
        yield "data: done\n\n"
        print("[SSE] Stream de eventos concluído")
    
    return Response(
        generate_serial_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_text, processing, bk_instance, sent_chars
    global pdf_filepath_global, txt_filepath_global

    if request.method == 'GET':
        # Reset de estado para nova transmissão
        current_text = ""
        processing = False
        sent_chars = 0
        pdf_filepath_global = None
        txt_filepath_global = None
        return render_template('index.html')

    # Processamento de arquivo PDF
    if 'pdf' not in request.files:
        return "Nenhum arquivo enviado", 400

    file = request.files['pdf']
    if not file or file.filename == '':
        return "Nenhum arquivo selecionado", 400

    try:
        # Salva o arquivo PDF
        pdf_filename = file.filename
        pdf_filepath_global = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        file.save(pdf_filepath_global)

        # Processa o texto
        bk = BrailleKeyboard()
        if not bk.connect_serial():
            return "Erro na conexão com o dispositivo", 500

        texto = bk.extract_text_from_pdf(pdf_filepath_global)
        if not texto:
            return "Não foi possível extrair texto do PDF", 500

        # Cria arquivo TXT com o conteúdo
        txt_filename = f"{os.path.splitext(pdf_filename)[0]}.txt"
        txt_filepath_global = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
        
        with open(txt_filepath_global, 'w', encoding='utf-8') as f:
            f.write(texto)

        # Prepara para envio
        current_text = texto.upper()
        sent_chars = 0
        processing = True
        bk_instance = bk
        
        # Inicia thread de envio
        threading.Thread(target=serial_sender, daemon=True).start()
        
        return redirect(url_for('streaming'))

    except Exception as e:
        print(f"[ERRO] Processamento falhou: {str(e)}")
        return f"Erro no processamento: {str(e)}", 500

@app.route('/streaming')
def streaming():
    return render_template('streaming.html')

if __name__ == '__main__':
    try:
        # Configurações de servidor otimizadas
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,  # Alterar para False em produção
            threaded=True,
            use_reloader=False
        )
    finally:
        # Limpeza final
        delete_file(pdf_filepath_global)
        delete_file(txt_filepath_global)
        print("[INFO] Aplicação encerrada")