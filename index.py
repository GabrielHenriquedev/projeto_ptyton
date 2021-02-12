from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

jan= Tk()
class funcs():
    def liparlabels(self):
        self.identre.delete(0, END)
        self.nomeentr.delete(0, END)
        self.emailentr.delete(0, END)
        self.carteiraentr.delete(0, END)

    def conetaraobanco(self):
        self.conn= sqlite3.connect("funcionarios.db")
        self.cursor= self.conn.cursor()

    def desconectar(self):
        self.conn.close()

    def montartabelas(self):
        self.conetaraobanco(); print("conectado ao banco de dados")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY,
                nome CHAR(40) NOT NUll,
                email CHAR(20) NOT NUll,
                carteira INTEGER(20) NOT NUll
            );
        """) 
        self.conn.commit(); print("banco de dados criado")
        self.desconectar()

    def variaveis(self):
        self.id= self.identre.get()
        self.nome= self.nomeentr.get() 
        self.email= self.emailentr.get() 
        self.nucarteira= self.carteiraentr.get() 

    def add_funcionario(self):
        self.variaveis()
        self.conetaraobanco()

        self.cursor.execute(""" INSERT INTO funcionarios (id, nome, email, carteira) 
            VALUES(?,?,?,?)""",(self.id,self.nome, self.email,self.nucarteira))
        self.conn.commit()
        self.mensagem= messagebox.showinfo(title="Parabens", message="O sócio foi salvo")
        

        self.desconectar()
        self.select()
        self.liparlabels()

    def Ondoubleclick(self,event):
        self.liparlabels()
        self.lista.selection()
        
        for n in self.lista.selection():
            col1, col2, col3, col4= self.lista.item(n, "values")
            self.identre.insert(END, col1)
            self.nomeentr.insert(END, col2)
            self.emailentr.insert(END, col3)
            self.carteiraentr.insert(END, col4)

    def select(self):
        self.lista.delete(*self.lista.get_children())
        self.conetaraobanco()
        tabe= self.cursor.execute(""" SELECT id, nome, email, carteira FROM funcionarios ORDER BY nome ASC;""")
        for i in tabe:
            self.lista.insert("", END, values=i)
        self.desconectar()

    def delet_clint(self):
        self.variaveis()
        self.conetaraobanco()
        
        self.cursor.execute("""DELETE FROM funcionarios WHERE id= ?""", (self.id,))
        self.conn.commit()

        self.desconectar()
        self.liparlabels()
        self.select()
        self.mensagem2= messagebox.showinfo(title="Info", message="O sócio foi deletado")

    def alterardados(self):
        self.variaveis()
        self.conetaraobanco()
        
        self.cursor.execute("""UPDATE funcionarios SET nome= ?, email= ?, carteira= ?
            WHERE id= ? """,(self.nome, self.email,self.nucarteira,self.id))
        self.conn.commit()

        self.desconectar()
        self.select()
        self.liparlabels()

    def buscar(self):
        self.conetaraobanco()
        self.lista.delete(*self.lista.get_children())
        self.nomeentr.insert(END, "%")
        nome= self.nomeentr.get()
        self.cursor.execute(
            """ SELECT id, nome, email, carteira FROM funcionarios 
            WHERE nome LIKE '%s' ORDER BY nome ASC """ % nome)
        busca= self.cursor.fetchall()
        for i in busca:
            self.lista.insert("", END, values=i)
        self.liparlabels()
        self.desconectar()

class aplicaçoes(funcs):

    def __init__(self):
        self.jan=jan
        self.tela()
        self.frames()
        self.botoes()
        self.tabela()
        self.montartabelas()
        self.select()
        jan.mainloop()

    def tela(self):
        self.jan.title("Cadastro de Sócio")
        self.jan.geometry("700x500")
        self.jan.configure(background="black")
        self.jan.resizable(width=True, height=True)
        self.jan.maxsize(width=900, height=700)
        self.jan.minsize(width=500, height=400)
        self.jan.iconbitmap("data/icone.ico")

    def frames(self):
      self.frame1= Frame(jan, bd=4, bg='silver',highlightbackground="#82807f", highlightthickness=6 )
      self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
      self.frame2= Frame(jan, bd=4, bg='silver',highlightbackground="#82807f", highlightthickness=6 )
      self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def botoes(self):
        #botão de salvar
        self.but_salvar= Button(self.frame1, text="Salvar", bd=4, bg="#cfd6e3", fg="black", font=("arial", 10,"bold"), command=self.add_funcionario)
        self.but_salvar.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        #botão de buscar
        self.but_busca= Button(self.frame1, text="Buscar", bd=4, bg="#cfd6e3", fg="black", font=("arial", 10,"bold"), command=self.buscar)
        self.but_busca.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        #botão de apagar
        self.but_apagar= Button(self.frame1, text="Apagar", bd=4, bg="#cfd6e3", fg="black", font=("arial", 10,"bold"), command=self.delet_clint)
        self.but_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        #botão de alterar
        self.but_alterar= Button(self.frame1, text="Alterar", bd=4, bg="#cfd6e3", fg="black", font=("arial", 10,"bold"), command=self.alterardados)
        self.but_alterar.place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.15)

        #labels
        self.title= Label(self.frame1, text="Cadastro de Sócios", bg='silver', font=("arial", 15,"bold"))
        self.title.place(relx=0.25, rely=0.05)

        self.id= Label(self.frame1, text="ID do Sócio", bg='silver', font=("arial", 10,"bold"))
        self.id.place(relx=0.05, rely=0.10)
        
        self.identre= Entry(self.frame1)
        self.identre.place(relx=0.05, rely=0.20, relwidth=0.12)
        #label
        self.nome= Label(self.frame1, text="Nome do Sócio", bg='silver', font=("arial", 10,"bold"))
        self.nome.place(relx=0.05, rely=0.35)
        
        self.nomeentr= Entry(self.frame1)
        self.nomeentr.place(relx=0.05, rely=0.45, relwidth=0.85)
        #label email
        self.email= Label(self.frame1, text="Email", bg='silver', font=("arial", 10,"bold"))
        self.email.place(relx=0.05, rely=0.6)
        
        self.emailentr= Entry(self.frame1)
        self.emailentr.place(relx=0.05, rely=0.7, relwidth=0.4)
        #label 
        self.nucarteira= Label(self.frame1, text="Número para contato", bg='silver', font=("arial", 10,"bold"))
        self.nucarteira.place(relx=0.5, rely=0.6)
        
        self.carteiraentr= Entry(self.frame1)
        self.carteiraentr.place(relx=0.5, rely=0.7, relwidth=0.4)
 
    def tabela(self):
        self.lista= ttk.Treeview(self.frame2, height=3, columns=("col1","col2","col3","col4"))
        self.lista.heading("#0", text="")
        self.lista.heading("#1", text="ID")
        self.lista.heading("#2", text="Nome")
        self.lista.heading("#3", text="Email")
        self.lista.heading("#4", text="Contato")

        self.lista.column("#0", width=1)
        self.lista.column("#1", width=50)
        self.lista.column("#2", width=200)
        self.lista.column("#3", width=125)
        self.lista.column("#4", width=125)

        self.lista.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroollist= Scrollbar(self.frame2,orient="vertical")
        self.lista.configure(yscroll=self.scroollist.set)
        self.scroollist.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.lista.bind("<Double-1>", self.Ondoubleclick)


aplicaçoes()