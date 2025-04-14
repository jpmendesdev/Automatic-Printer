from UTILS.databaseConfigs import conexao
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

cursor = conexao.cursor()

def create_table():
    tabela_documents = """CREATE TABLE IF NOT EXISTS documents(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(255),
                       file_data LONGBLOB 
                       );"""
    cursor.execute(tabela_documents)
    conexao.commit()
    #BLOB é um campo do sql que trabalha com binários
 

def create_document(name, file_data):
    try:
        sql = "INSERT INTO documents (name, file_data) VALUES (%s, %s)"
        cursor.execute(sql, (name, file_data))
        conexao.commit()
        print(f"Documento '{name}' inserido com sucesso, ID: {cursor.lastrowid}")
    except Exception as e:
        print("Erro ao inserir documento:", e)
    cursor.close()
    conexao.close()
    
def read_document(document_id, output_Path):
    try:
        sql = "SELECT name, file_data FROM documents WHERE id = %s"
        cursor.execute(sql, (document_id,))
        result = cursor.fetchone()
        if result:
            name, binary_data = result
            with open(output_Path, 'wb') as file:
                file.write(binary_data)
            print(f"Documento '{name}' salvo em '{output_Path}'")
        else:
            print("Documento não encontrado.")
    except Exception as e:
        print("Erro ao ler documento:", e)
        
        
def update_document(document_id, new_file_path):
    try:
        with open(new_file_path, 'rn') as file:
            new_binary = file.read()
        sql = "UPDATE documents SET file_data = %s WHERE id = %s"
        cursor.execute(sql, (new_binary, document_id))
        conexao.commit()
        print(f"Documento com ID {document_id} atualizado com sucesso.") 
    except Exception as e:
        print("Erro ao atualizar o documento:", e)   
        
def delete_document(name):
    try:
        sql = "DELETE FROM documents WHERE name = %s"
        cursor.execute(sql, (name,))
        result = cursor.fetchall
        conexao.commit()   #.commit() serve para editar no banco de dados, se não for utilizado, a alteração não aparece no banco
        print(f"Documento '{name}' deletado com sucesso!")
    except Exception as e:
        print(f"Erro ao tentar deletar documento '{name}'", e)
        
        
        
# if __name__ == '__main__':
    # create_document("ExemploPDF", "CurriculoVitae.docx (1).pdf")      
    # read_document(3, "downloaded_document.pdf")   
    # read_document(4, "downloaded_document2.pdf")
    #create_table()
    #delete_document("File teste")

    # cursor.close()
    # conexao.close()
