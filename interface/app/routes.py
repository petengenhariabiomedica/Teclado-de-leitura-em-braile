from flask import Blueprint, render_template, request, redirect, url_for, Response
from .braille import BrailleKeyboard
from .serial_handler import start_serial_sender, get_stream_data
from .utils import delete_file
import os

bp = Blueprint('main', __name__)
current_text = ""
pdf_path = ""
txt_path = ""

@bp.route('/', methods=['GET', 'POST'])
def index():
    global current_text, pdf_path, txt_path

    if request.method == 'POST':
        file = request.files.get('pdf')
        if not file or file.filename == "":
            return "Nenhum PDF enviado."

        filename = file.filename
        pdf_path = os.path.join('app', 'uploads', filename)
        file.save(pdf_path)

        bk = BrailleKeyboard()
        if bk.connect_serial():
            texto = bk.extract_text_from_pdf(pdf_path, page_number=0)
            txt_path = pdf_path.replace('.pdf', '.txt')
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(texto)
            current_text = texto.upper()

            start_serial_sender(bk, current_text)
            return redirect(url_for('main.streaming'))

    return render_template('index.html')

@bp.route('/streaming')
def streaming():
    return render_template('streaming.html')

@bp.route('/stream')
def stream():
    return Response(
        get_stream_data(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Content-Type': 'text/event-stream; charset=utf-8'
        }
    )

