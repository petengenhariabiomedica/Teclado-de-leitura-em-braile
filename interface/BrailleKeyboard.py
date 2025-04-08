import time
import serial
from serial.tools import list_ports
import PyPDF2

class BrailleKeyboard:
    def __init__(self):
        self.port = self.find_port()
        self.serial_connection = None

    def find_port(self):
        """Tenta localizar a porta serial do ESP32 automaticamente."""
        portas = list_ports.comports()
        for porta in portas:
            if "USB" in porta.description or "UART" in porta.description or "ESP32" in porta.description:
                print(f"[✔] Dispositivo encontrado: {porta.device} - {porta.description}")
                return porta.device
        print("[✘] Nenhum dispositivo ESP32 encontrado.")
        return None

    def extract_text_from_pdf(self, pdf_path, page_number=0):
        """Extrai o texto de uma página específica do PDF."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                texto = reader.pages[page_number].extract_text()
                print(f"[✔] Texto extraído da página {page_number}")
                return texto
        except Exception as e:
            print(f"[✘] Erro ao extrair texto do PDF: {e}")
            return ""

    def connect_serial(self, baudrate=9600):
        """Estabelece conexão serial com o ESP32."""
        if self.port is None:
            print("[✘] Porta serial não encontrada.")
            return False
        try:
            self.serial_connection = serial.Serial(self.port, baudrate, timeout=2)
            time.sleep(2)  # Aguarda inicialização
            print(f"[✔] Conectado à porta {self.port} com baudrate {baudrate}")
            return True
        except Exception as e:
            print(f"[✘] Erro ao conectar na porta serial: {e}")
            return False

    def send_text_over_serial(self, text, delay=0.01, wait_ack=True):
        """Envia o texto caractere por caractere pela serial."""
        if self.serial_connection is None:
            print("[✘] Conexão serial não está aberta.")
            return

        for char in text:
            self.serial_connection.write(char.encode('utf-8'))
            time.sleep(delay)

            if wait_ack:
                ack = self.serial_connection.readline().decode('utf-8').strip()
                while ack != "OK":
                    print(f"Aguardando ACK... Última resposta: {ack}")
                    ack = self.serial_connection.readline().decode('utf-8').strip()
        print("[✔] Texto enviado com sucesso!")

    def close(self):
        """Fecha a conexão serial."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("[✔] Conexão serial encerrada.")


