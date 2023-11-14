import tkinter as tk
from tkinter import messagebox


class Login():

    def __init__(self):
        pass

    def loadLogin(self):
        login_window = tk.Tk()
        login_window.title('Login')
        login_window.geometry('280x400')
        login_window.resizable(False, False)
        login_window.configure(bg='black')
        
        self.loadLabel(login_window)
        login_window.mainloop()

    def loadLabel(self, login_window):
        print('chegou aqui?')
        welcome_label = tk.Label(login_window, text='Bem Vindo', anchor='center', bg='black', foreground='white', font=('Calibri', 18))
        welcome_label.grid(row=0, column=1, columnspan=2, pady=20, padx=10, sticky='n')
        login_label = tk.Label(login_window, text="Usuário:", bg='black', foreground='white', font=("Calibri", 12))
        login_label.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        login_entry = tk.Entry(login_window, bg="#303030", foreground='white', font=("Calibri", 12), width=14, bd=0, relief='solid')
        login_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        password_label = tk.Label(login_window, text="Senha:", bg="black", foreground='white', font=("Calibri", 12))
        password_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        password_entry = tk.Entry(login_window, show="*", bg="#303030", foreground='white', font=("Calibri", 12), width=14, bd=0, relief='solid')
        password_entry.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        
        login_button = tk.Button(login_window, text="Login", command=self.verifyLogin, bg="#505050", foreground='white', font=("Calibri", 12))
        login_button.grid(row=3, column=1, columnspan=2, pady=30)
    
    def verifyLogin(self):
        print('Login verificado')
        


test = Login()
test.loadLogin()
