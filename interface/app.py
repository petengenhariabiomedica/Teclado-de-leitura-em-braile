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
                texto = bk.extract_text_from_pdf(filepath, page_number=0)
                bk.send_text_over_serial(texto)
                bk.close()
            return "PDF enviado com sucesso!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)  # Isso inicia o servidor Flask
