from flask import Flask, render_template, request
from BrailleKeyboard import BrailleKeyboard
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        if pdf_file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(filepath)

            bk = BrailleKeyboard()
            if bk.connect_serial():
                # Extrai o texto do PDF
                texto = bk.extract_text_from_pdf(filepath, page_number=0)

                # Arquivo .txt criado para verificar o texto gerado pelo PDF, para fins de teste
                txt_filename = pdf_file.filename.rsplit('.', 1)[0] + '.txt'
                txt_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)

                # Salva o texto extraído no arquivo .txt
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(texto or "[Texto vazio ou não extraído]")                
                    
                # Envia o texto extraído para o dispositivo Braille    
                bk.send_text_over_serial(texto)
                bk.close()
            return "PDF enviado com sucesso!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)  # Isso inicia o servidor Flask
