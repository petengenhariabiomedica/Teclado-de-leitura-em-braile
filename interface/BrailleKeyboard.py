import openai
import time
import serial
from serial.tools import list_ports
import PyPDF2
import os
import re
import unicodedata

class BrailleKeyboard:
    def __init__(self):
        self.port = self.find_port()
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.serial_connection = None
        self.current_position = 0

    def find_port(self):
        """Tenta localizar a porta serial do ESP32 automaticamente."""
        portas = list_ports.comports()
        for porta in portas:
            if any(keyword in porta.description.upper() for keyword in ['USB', 'UART', 'ESP32', 'SERIAL']):
                print(f"[✔] Dispositivo encontrado: {porta.device} - {porta.description}")
                return porta.device
        print("[✘] Nenhum dispositivo ESP32 encontrado.")
        return None

    def is_alpha_portuguese(self, char):
        """Verifica se é uma letra do português (incluindo acentuadas e cedilha)"""
        return char.isalpha() or char in 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'

    def clean_text_generic(self, text):
        """
        Versão final corrigindo espaços em caracteres especiais
        """
        if not text:
            return text

        # Passo 1: Normalização NFC para caracteres pré-compostos
        text = unicodedata.normalize('NFC', text)

        # Passo 2: Corrigir espaços entre letras e acentos pré-compostos
        text = re.sub(
            r'([A-Za-z])\s+([À-ÿ])',  # Captura "A ´" ou "C Ç"
            lambda m: m.group(1) + m.group(2),
            text,
            flags=re.IGNORECASE
        )

        # Passo 3: Casos especiais de cedilha e combinações críticas
        text = re.sub(r'\b(C)\s+(Ç)\b', r'\1\2', text, flags=re.IGNORECASE)
        text = re.sub(r'\b([AEIOU])\s+([´`^~])\b', r'\1\2', text)

        # Passo 4: Demais substituições (mantido do código original)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        text = re.sub(r'[^\w\s.,;:?!\-()\nÀ-ÿ]', '', text)

        return text.strip().upper()

    def enhance_text_with_gpt(self, text):
        """Melhora a formatação mantendo a integridade dos acentos"""
        if not self.openai_key or len(text) < 50:
            return text

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um especialista em formatação de texto em português. Corrija:\n"
                            "1. Mantenha todos os acentos e caracteres especiais do português intactos\n"
                            "2. Nunca separe letras de seus acentos com espaços\n"
                            "3. Corrija apenas espaçamento entre palavras\n"
                            "4. Mantenha a estrutura original do documento\n"
                            "Mantenha o conteúdo original intacto, apenas melhore a formatação.\n"
                            "Retorne o texto em maiúsculas, com acentos corretos e sem espaçamento indevido."
                        )
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            return response.choices[0].message['content'].strip().upper()
        except Exception as e:
            print(f"[⚠] GPT não disponível. Usando limpeza básica. Erro: {e}")
            return self.clean_text_generic(text)

    def extract_text_from_pdf(self, pdf_path, page_number=0):
        """Extrai texto preservando a formatação de acentos"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                if page_number is None:
                    text = ''.join([page.extract_text() or '' for page in reader.pages])
                else:
                    text = reader.pages[page_number].extract_text() or ''
                
                print(f"[ℹ] Texto bruto extraído ({len(text)} caracteres)")
                
                # Primeira limpeza básica
                clean_text = self.clean_text_generic(text)
                print(f"[ℹ] Texto após limpeza básica ({len(clean_text)} caracteres)")
                
                # Processamento adicional com GPT se disponível
                if self.openai_key and len(clean_text) > 100:
                    enhanced_text = self.enhance_text_with_gpt(clean_text)
                    if 0.9 < len(enhanced_text)/len(clean_text) < 1.1:
                        print(f"[ℹ] Texto após GPT ({len(enhanced_text)} caracteres)")
                        return enhanced_text
                
                return clean_text
                
        except Exception as e:
            print(f"[✘] Falha na extração: {e}")
            return ""

    def send_single_character(self, char):
        """Versão simplificada e robusta"""
        try:
            self.serial_connection.write(char.encode('utf-8'))
            self.serial_connection.flush()
            
            start_time = time.time()
            while time.time() - start_time < 0.5:  # Timeout de 500ms
                if self.serial_connection.in_waiting:
                    ack = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    if ack == "OK":
                        return True
            return False
        except:
            return False
        
    def get_next_character(self, text):
        """Obtém o próximo caractere válido incluindo acentuados"""
        while self.current_position < len(text):
            char = text[self.current_position]
            self.current_position += 1
            if self.is_alpha_portuguese(char):
                return char.upper()
        return None

    def connect_serial(self, baudrate=115200):
        """Estabelece conexão serial com o ESP32."""
        if self.port is None:
            print("[✘] Porta serial não encontrada.")
            return False
        try:
            self.serial_connection = serial.Serial(
                self.port, 
                baudrate, 
                timeout=2,
                write_timeout=2  # Timeout para escrita
            )
            time.sleep(2)  # Aguarda inicialização
            print(f"[✔] Conectado à porta {self.port} com baudrate {baudrate}")
            return True
        except Exception as e:
            print(f"[✘] Erro ao conectar na porta serial: {e}")
            return False



    def reset_progress(self):
        """Reseta o contador de progresso"""
        self.current_position = 0

    def close(self):
        """Fecha a conexão serial."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("[✔] Conexão serial encerrada.")
            self.reset_progress()

    def is_connected(self):
        """Verifica se a conexão está ativa"""
        return self.serial_connection and self.serial_connection.is_open
