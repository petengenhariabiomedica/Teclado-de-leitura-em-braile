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

    def connect_serial(self, baudrate=115200):
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

    def send_text_over_serial(self, text, delay=0.01, wait_ack=True, max_retries=5):
        """Envia o texto caractere por caractere pela serial."""
        if self.serial_connection is None:
            print("[✘] Conexão serial não está aberta.")
            return
        
        for index, char in enumerate(text):
            if not char.isalpha():  # Enviar só letras
                continue
            try:
                self.serial_connection.write(char.encode('utf-8'))
                time.sleep(delay)

                if wait_ack:
                    attempts = 0
                    while attempts < max_retries:
                        ack = self.serial_connection.readline().decode('utf-8').strip()
                        if ack == "OK":
                            print(f"[✔] Caractere '{char}' enviado e ACK recebido.")
                            break
                        else:
                                attempts += 1
                                print(f"[...] Aguardando ACK para '{char}' (tentativa {attempts})... Última resposta: {ack}")
                                time.sleep(0.1)
                        if attempts == max_retries:
                            print(f"[✘] Falha no ACK após {max_retries} tentativas para o caractere '{char}' (índice {index})")
                            break  # ou continue para ignorar e seguir
                
            except Exception as e:
                print(f"[✘] Erro ao enviar caractere '{char}': {e}")
        print("[✔] Texto enviado com sucesso!")
            

    def close(self):
        """Fecha a conexão serial."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("[✔] Conexão serial encerrada.")


