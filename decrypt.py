"""
=============================================================================
== PROJETO: Script de Descriptografia (Santander Cybersecurity)
== AUTOR: Revoluxti
==
== DESCRIÇÃO:
== Este script é o "antídoto" para o 'ransomware.py'. Ele reverte o
== processo de criptografia para simular a recuperação dos arquivos.
==
== FLUXO DE "RESGATE":
== 1. CARREGAR CHAVE: Tenta carregar a chave 'mykey.key'. Se a chave
==    não for encontrada, o script falha (simulando a impossibilidade
==    de recuperação sem a chave).
== 2. VARREDURA: Procura pelos arquivos-alvo no mesmo diretório.
== 3. DESCRIPTOGRAFIA: Lê o conteúdo criptografado de cada arquivo,
==    descriptografa-o usando a chave Fernet e reescreve o arquivo
==    com o conteúdo original.
== 4. LIMPEZA: Remove a nota de resgate ('LEIA_ME_RESGATE.txt').
=============================================================================
"""

import os
from cryptography.fernet import Fernet

# --- [BLOCO 1: CONFIGURAÇÕES] ---
# As configurações DEVEM ser idênticas às do script 'ransomware.py'
KEY_FILE = "mykey.key"
TARGET_DIRECTORY = "arquivosDesafios"
TARGET_EXTENSION = ".txt"
RANSOM_NOTE_FILE = "LEIA_ME_RESGATE.txt"

# --- [BLOCO 2: FUNÇÕES DE GERENCIAMENTO DA CHAVE] ---

def load_key():
    """
    Carrega a chave do arquivo 'mykey.key'.
    Se o arquivo não existir, o script não pode funcionar.
    """
    if not os.path.exists(KEY_FILE):
        print(f"[FATAL ERROR]: Arquivo da chave '{KEY_FILE}' não encontrado!")
        print("Você não pode descriptografar os arquivos sem a chave.")
        return None # Retorna 'None' (nulo) para sinalizar a falha
    
    print(f"[LOG]: Carregando chave de '{KEY_FILE}'...")
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
    
    return key

# --- [BLOCO 3: FUNÇÕES DE "RESGATE" (DESCRIPTOGRAFIA)] ---

def decrypt_file(file_path, fernet_obj):
    """
    Descriptografa um único arquivo.
    """
    try:
        # Lê o conteúdo criptografado
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        
        # Tenta descriptografar
        decrypted_data = fernet_obj.decrypt(encrypted_data)
        
        # Reescreve o arquivo com o conteúdo original (descriptografado)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        
        print(f"[DECRYPTED]: {file_path}")

    except Exception as e:
        # Esta exceção é esperada se tentarmos descriptografar um
        # arquivo que não estava criptografado (como a nota de resgate)
        # ou se a chave estiver errada.
        print(f"[WARNING]: Falha ao descriptografar {file_path}. Já está descriptografado? Erro: {e}")

def remove_ransom_note():
    """
    Remove a nota de resgate após a recuperação.
    """
    note_path = os.path.join(TARGET_DIRECTORY, RANSOM_NOTE_FILE)
    if os.path.exists(note_path):
        os.remove(note_path)
        print(f"[LOG]: Nota de resgate '{RANSOM_NOTE_FILE}' removida.")

# --- [BLOCO 4: EXECUÇÃO PRINCIPAL] ---

if __name__ == "__main__":
    print("--- Iniciando Script de Descriptografia ---")

    # 1. Carrega a chave
    key = load_key()
    
    # 2. Continua apenas se a chave foi carregada com sucesso
    if key:
        # 3. Cria o objeto Fernet com a chave
        f = Fernet(key)
        
        print(f"\n[TARGET]: Procurando por arquivos '{TARGET_EXTENSION}' em '{TARGET_DIRECTORY}'...")
        
        file_count = 0
        # 4. Itera por todos os arquivos no diretório
        for filename in os.listdir(TARGET_DIRECTORY):
            # 5. Foca apenas nos arquivos .txt
            if filename.endswith(TARGET_EXTENSION):
                file_path = os.path.join(TARGET_DIRECTORY, filename)
                # 6. Chama a função de descriptografia
                decrypt_file(file_path, f)
                file_count += 1
        
        if file_count > 0:
            print(f"\n[SUCCESS]: {file_count} arquivo(s) foram processados para descriptografia.")
            # 7. Remove a nota de resgate
            remove_ransom_note()
        else:
            print(f"\n[LOG]: Nenhum arquivo '{TARGET_EXTENSION}' encontrado para descriptografar.")

    print("\n--- Processo de Recuperação Concluído ---")