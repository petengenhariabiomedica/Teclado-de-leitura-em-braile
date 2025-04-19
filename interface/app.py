from flask import Flask, render_template, request
from BrailleKeyboard import BrailleKeyboard
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Declara as variáveis de caminho em um escopo mais amplo
pdf_filepath_global = None
txt_filepath_global = None

def delete_file(filepath):
    """Apaga um arquivo se ele existir."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            print(f"[INFO] Arquivo apagado: {filepath}")
    except Exception as e:
        print(f"[ERRO] Falha ao apagar arquivo {filepath}: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    """Rota principal do aplicativo."""
    global pdf_filepath_global
    global txt_filepath_global

    try:
        if request.method == 'POST':
            pdf_file = request.files['pdf']
            if pdf_file.filename != '':
                pdf_filename = pdf_file.filename
                pdf_filepath_global = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                pdf_file.save(pdf_filepath_global)

                bk = BrailleKeyboard()
                if bk.connect_serial():
                    # Extrai o texto do PDF
                    texto = bk.extract_text_from_pdf(pdf_filepath_global, page_number=0)

                    # Arquivo .txt criado para verificar o texto gerado pelo PDF, para fins de teste
                    txt_filename_base = pdf_filename.rsplit('.', 1)[0]
                    txt_filename = f"{txt_filename_base}.txt"
                    txt_filepath_global = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)

                    # Salva o texto extraído no arquivo .txt
                    with open(txt_filepath_global, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(texto or "[Texto vazio ou não extraído]")

                    # Envia o texto extraído para o dispositivo Braille
                    bk.send_text_over_serial(texto)
                    bk.close()
                return "PDF enviado com sucesso!"
        return render_template('index.html')
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro durante o processamento: {e}")
        return "Erro ao processar o PDF."

if __name__ == '__main__':
    try:
        app.run(debug=True)  # Isso inicia o servidor Flask
    except Exception as e:
        print("[INFO] Tentando apagar os arquivos...")
        delete_file(pdf_filepath_global)
        delete_file(txt_filepath_global)
        print("[INFO] Servidor Flask encerrado.")
    finally:
        delete_file(pdf_filepath_global)
        print(f'[INFO] Arquivo PDF apagado: {pdf_filepath_global}')
        delete_file(txt_filepath_global)
        print(f'[INFO] Arquivo TXT apagado: {txt_filepath_global}')
        print("[INFO] Arquivos temporários apagados.")
        

