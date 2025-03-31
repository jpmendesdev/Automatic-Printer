def print_document(file_path):
    try:
        print("Enviando para impressão...")
        subprocess.run(['rundll32', 'printui.dll,PrintUIEntry', '/q', '/n', PRINTER_NAME, 'f', file_path], check=True)
        print("Impressão enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao imprimir: {e}")