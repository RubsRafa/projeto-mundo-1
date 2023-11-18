import tkinter as tk
from CTkMessagebox import CTkMessagebox
import Auth as Auth
import HomePage as Home
import Alunos as Alunos

class Main():

    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title('Login')
        self.login_window.geometry('280x400')
        self.login_window.resizable(False, False)
        self.login_window.configure(bg='black')

        self.welcome_label = tk.Label(self.login_window, text='Bem Vindo', anchor='center', bg='black', foreground='white', font=('Calibri', 18))
        self.welcome_label.grid(row=0, column=1, columnspan=2, pady=20, padx=10, sticky='n')
        
        self.login_label = tk.Label(self.login_window, text="Usuário:", bg='black', foreground='white', font=("Calibri", 12))
        self.login_label.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.login_entry = tk.Entry(self.login_window, bg="#303030", foreground='white', font=("Calibri", 12), width=14, bd=0, relief='solid')
        self.login_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        self.password_label = tk.Label(self.login_window, text="Senha:", bg="black", foreground='white', font=("Calibri", 12))
        self.password_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(self.login_window, show="*", bg="#303030", foreground='white', font=("Calibri", 12), width=14, bd=0, relief='solid')
        self.password_entry.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        
        login_button = tk.Button(self.login_window, text="Login", command=self.login, bg="#505050", foreground='white', font=("Calibri", 12))
        login_button.grid(row=3, column=1, columnspan=2, pady=30)

        alunos_button = tk.Button(self.login_window, text="Alunos", command=self.alunos, bg="#505050", foreground='white', font=("Calibri", 12))
        alunos_button.grid(row=4, column=1, columnspan=2, pady=10)
        
        self.login_window.mainloop()

    
    def login(self):
        
        verifyUser = Auth.authenticateUser(self.login_entry.get(), self.password_entry.get())
        if verifyUser == True:
            self.login_window.destroy()
            # username = self.login_entry.get()
            open_home_page = Home.HomePage()
            open_home_page.mainloop()
        else:
            CTkMessagebox(title='Erro ao fazer o login', message='Usuário ou senha incorretos', icon='cancel', width=280)
    
    def alunos(self):
        self.login_window.destroy()
        Alunos.Alunos()
        

        


if __name__ == '__main__':
    app = Main()
    app.login_window.mainloop()
