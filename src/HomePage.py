import tkinter as tk
import InícioPage as Inicio

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HOME PAGE')
        self.geometry('800x600')

        self.bar = tk.Frame(self, bg='#535353', width=200)
        self.bar.pack(side=tk.LEFT, fill=tk.Y)

        options = ['Início','Sistemas', 'Perfis de Acesso', 'Matriz SoD']
        for item in options:
            self.btn = tk.Button(self.bar, text=item, command=lambda text=item: self.show_button(text), foreground='gray', bg='black', activebackground='gray', activeforeground='white', font=('Roboto', 14), borderwidth=0)
            self.btn.pack(pady=10, padx=10)

        self.main_content = tk.Frame(self, bg='red')
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_button(self, button_text):
        if button_text == 'Início':
            self.update_main_content('Conteúdo da Página de Início', 'red')
        elif button_text == 'Sistemas':
            self.update_main_content('Conteúdo da Página de Sistemas', 'green')
        elif button_text == 'Perfis de Acesso':
            self.update_main_content('Conteúdo da Página de Perfis de Acesso', 'purple')
        elif button_text == 'Matriz SoD':
            self.update_main_content('Conteúdo da Página de Matriz SoD', 'yellow')
        
    def update_main_content(self, content, color):
        if self.main_content:
            self.main_content.destroy()
        
        self.main_content = tk.Frame(self, bg=color)
        label = tk.Label(self.main_content, text=content, font=('Roboto', 18), foreground='white', bg='gray')
        label.pack(padx=20, pady=20)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)



