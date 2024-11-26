import mysql.connector
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, ttk, Frame
import os
import shutil
import requests
from PIL import Image, ImageTk
from io import BytesIO
import logging

diretorio_atual = os.getcwd()  

def load_logo():
    url = "https://www.abcdacomunicacao.com.br/wp-content/uploads/image001-21.png"
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img.thumbnail((200, 200), Image.LANCZOS)
    return ImageTk.PhotoImage(img)


logging.basicConfig(filename='erro.log', level=logging.ERROR)

try:
    conn = mysql.connector.connect(
        host="192.168.1.24",
        user="root",
        password="0000",
        database="banco_curriculos"
    )
except Exception as e:
    logging.error("Erro ao conectar ao MySQL: %s", e)
    sys.exit("Erro ao conectar ao MySQL. Verifique as configurações e tente novamente.")

cursor = conn.cursor()



def cadastrar_aluno():
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    nivel_ensino = nivel_entry.get()
    estuda = estuda_var.get()
    status = status_var.get()
    area_emprego = area_entry.get()

    if not nome or not email or not telefone or not nivel_ensino or not area_emprego:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    if status not in ['Ativo', 'Inativo']:
        messagebox.showwarning("Atenção", "Status deve ser 'Ativo' ou 'Inativo'.")
        return

    query = "INSERT INTO alunos (nome, email, telefone, nivel_ensino, area_emprego) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nome, email, telefone, nivel_ensino, area_emprego))
    conn.commit()

    id_aluno = cursor.lastrowid

    if estuda == "Sim":
        query_matricula = "INSERT INTO Matricula (id_aluno, status) VALUES (%s, %s)"
        cursor.execute(query_matricula, (id_aluno, status))
        conn.commit()

    upload_curriculo(id_aluno)
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
    exibir_ultimos_cadastrados()

  
    nome_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    nivel_entry.set("")
    area_entry.delete(0, tk.END)

    cadastrar_button.config(text="Cadastrar e Upload Currículo", command=cadastrar_aluno)

def upload_curriculo(id_aluno):
  
    caminho_pdf = filedialog.askopenfilename(title="Selecione o currículo", filetypes=[("Arquivos PDF", "*.pdf")])
    
    
    if caminho_pdf:
        
        with open(caminho_pdf, "rb") as file:
            blob_data = file.read()
        
        
        conn = mysql.connector.connect(
            host="192.168.1.24",
            user="root",
            password="0000",
            database="banco_curriculos"
        )
        cursor = conn.cursor()

        
        query = """
        INSERT INTO curriculos (arquivo, id_aluno)
        VALUES (%s, %s)
        """
        cursor.execute(query, (blob_data, id_aluno))

        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Currículo enviado com sucesso ao banco de dados!")


def buscar_curriculo():
    busca = buscar_entry.get()
    query = """
        SELECT a.id_aluno, a.nome, a.telefone, a.email, a.area_emprego, a.nivel_ensino, 
               COALESCE(m.status, 'não tem matrícula') as status
        FROM alunos a
        LEFT JOIN Matricula m ON a.id_aluno = m.id_aluno
        WHERE a.nome LIKE %s OR a.area_emprego LIKE %s
    """
    cursor.execute(query, (f'%{busca}%', f'%{busca}%'))
    curriculos = cursor.fetchall()

    for item in lista_curriculos.get_children():
        lista_curriculos.delete(item)

    if curriculos:
        for curriculo in curriculos:
            lista_curriculos.insert("", "end", values=curriculo)
    else:
        messagebox.showinfo("Resultado", "Nenhum currículo encontrado.")

def exibir_ultimos_cadastrados():
    query = """
        SELECT a.id_aluno, a.nome, a.email, a.telefone, a.area_emprego, a.nivel_ensino,
               COALESCE(m.status, 'Não tem matrícula') as status
        FROM alunos a
        LEFT JOIN Matricula m ON a.id_aluno = m.id_aluno
        ORDER BY a.id_aluno DESC LIMIT 10
    """
    cursor.execute(query)
    ultimos = cursor.fetchall()

    for item in lista_curriculos.get_children():
        lista_curriculos.delete(item)

    for cadastro in ultimos:
        lista_curriculos.insert("", "end", values=cadastro)

def editar_aluno():
    selecionado = lista_curriculos.focus()
    if not selecionado:
        messagebox.showwarning("Seleção Inválida", "Selecione um aluno para editar.")
        return
    
    id_aluno = lista_curriculos.item(selecionado)["values"][0]

    cursor.execute("SELECT nome, email, telefone, nivel_ensino, area_emprego FROM alunos WHERE id_aluno = %s", (id_aluno,))
    aluno = cursor.fetchone()

    if aluno:
        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, aluno[0])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, aluno[1])
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, aluno[2])
        nivel_entry.set(aluno[3])
        area_entry.delete(0, tk.END)
        area_entry.insert(0, aluno[4])

        cadastrar_button.config(text="Confirmar Edição", command=lambda: confirmar_edicao(id_aluno))

from tkinter import filedialog

def confirmar_edicao(id_aluno):
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    nivel_ensino = nivel_entry.get()
    area_emprego = area_entry.get()

    if not nome or not email or not telefone or not nivel_ensino or not area_emprego:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    
    query = "UPDATE alunos SET nome = %s, email = %s, telefone = %s, nivel_ensino = %s, area_emprego = %s WHERE id_aluno = %s"
    cursor.execute(query, (nome, email, telefone, nivel_ensino, area_emprego, id_aluno))
    conn.commit()


    resposta = messagebox.askyesno("Atualizar Currículo", "Deseja atualizar o currículo para este aluno?")
    if resposta:
        
        arquivo_path = filedialog.askopenfilename(title="Selecione o novo currículo em PDF", filetypes=[("PDF Files", "*.pdf")])
        if arquivo_path:
            
            with open(arquivo_path, "rb") as file:
                blob_data = file.read()
            
            
            query_curriculo = "UPDATE curriculos SET arquivo = %s WHERE id_aluno = %s"
            cursor.execute(query_curriculo, (blob_data, id_aluno))
            conn.commit()

    messagebox.showinfo("Sucesso", "Dados do aluno e currículo atualizados com sucesso!")
    
    
    nome_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    nivel_entry.set("")
    area_entry.delete(0, tk.END)

    cadastrar_button.config(text="Cadastrar e Upload Currículo", command=cadastrar_aluno)
    exibir_ultimos_cadastrados()


def remover_aluno():
    selecionado = lista_curriculos.focus()
    if not selecionado:
        messagebox.showwarning("Seleção Inválida", "Selecione um aluno para remover.")
        return
    
    id_aluno = lista_curriculos.item(selecionado)["values"][0]
    
    resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja remover este cadastro?")
    if resposta:
        cursor.execute("DELETE FROM curriculos WHERE id_aluno = %s", (id_aluno,))
        cursor.execute("DELETE FROM Matricula WHERE id_aluno = %s", (id_aluno,))
        cursor.execute("DELETE FROM alunos WHERE id_aluno = %s", (id_aluno,))
        conn.commit()
        
        messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
        exibir_ultimos_cadastrados()

def abrir_curriculo(event=None):
    selecionado = lista_curriculos.focus()
    if not selecionado:
        messagebox.showwarning("Seleção Inválida", "Selecione um currículo para abrir.")
        return

    curriculo = lista_curriculos.item(selecionado)["values"]
    id_aluno = curriculo[0]  

    
    cursor.execute("SELECT arquivo FROM curriculos WHERE id_aluno = %s", (id_aluno,))
    result = cursor.fetchone()
    if result and result[0]:
        with open("curriculo_temp.pdf", "wb") as file:  
            file.write(result[0])

        os.startfile("curriculo_temp.pdf") 
    else:
        messagebox.showwarning("Erro", "Arquivo de currículo não encontrado no banco de dados.")






root = tk.Tk()
root.title("Gerenciamento de Currículos")
root.state('zoomed')


logo_image = load_logo()
logo_label = tk.Label(root, image=logo_image)
logo_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))


tk.Label(root, text="Nome:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
nome_entry = tk.Entry(root)
nome_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Telefone:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
telefone_entry = tk.Entry(root)
telefone_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Nível de Ensino:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
nivel_entry = ttk.Combobox(root, values=["Fundamental", "Médio", "Superior"])
nivel_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Área de Emprego:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
area_entry = ttk.Combobox(root, values=["Adm", "Vendas", "Recepção", "Secretariado", "Operador de Caixa", "Repositor de mercado", "Outros"])
area_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Estuda na escola?").grid(row=6, column=0, sticky="e", padx=5, pady=5)
estuda_var = StringVar(value="Não")
frame_estuda = tk.Frame(root)
frame_estuda.grid(row=6, column=1, sticky="w")
tk.Radiobutton(frame_estuda, text="Sim", variable=estuda_var, value="Sim").pack(side="left")
tk.Radiobutton(frame_estuda, text="Não", variable=estuda_var, value="Não").pack(side="left")

tk.Label(root, text="Status:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
status_var = StringVar(value='Ativo')
frame_status = tk.Frame(root)
frame_status.grid(row=7, column=1, sticky="w")
tk.Radiobutton(frame_status, text="Ativo", variable=status_var, value='Ativo').pack(side="left")
tk.Radiobutton(frame_status, text="Inativo", variable=status_var, value='Inativo').pack(side="left")

cadastrar_button = tk.Button(root, text="Cadastrar e Upload Currículo", command=cadastrar_aluno)
cadastrar_button.grid(row=8, column=1, pady=10, padx=5, sticky="w")


busca_frame = Frame(root)
busca_frame.grid(row=9, column=0, columnspan=2, pady=10)

tk.Label(busca_frame, text="Buscar Currículo (Nome ou Área de Emprego):").grid(row=0, column=0, padx=5)
buscar_entry = tk.Entry(busca_frame, width=50)
buscar_entry.grid(row=0, column=1, padx=5)

buscar_button = tk.Button(busca_frame, text="Buscar", command=buscar_curriculo)
buscar_button.grid(row=0, column=2, padx=5)

edit_button = tk.Button(busca_frame, text="Editar Selecionado", command=editar_aluno)
edit_button.grid(row=0, column=3, padx=5)

remove_button = tk.Button(busca_frame, text="Remover Selecionado", command=remover_aluno)
remove_button.grid(row=0, column=4, padx=5)

abrir_button = tk.Button(busca_frame, text="Abrir Currículo", command=abrir_curriculo)
abrir_button.grid(row=0, column=5, padx=5)


cols = ("ID", "Nome", "Email", "Telefone", "Área", "Nível", "Status")  
lista_curriculos = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    lista_curriculos.heading(col, text=col)
    lista_curriculos.column(col, anchor="center")

lista_curriculos.grid(row=10, column=0, columnspan=2, sticky="nsew")


lista_curriculos.bind("<Double-1>", abrir_curriculo)


root.grid_rowconfigure(10, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

exibir_ultimos_cadastrados()

root.mainloop()
conn.close()

