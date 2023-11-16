import tkinter as tk

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HOME PAGE')
        self.geometry('800x600')

        self.bar = tk.Frame(self, bg='blue', width=200)
        self.bar.pack(side=tk.LEFT, fill=tk.Y)

        options = ['Início','Sistemas', 'Pergis de Acesso', 'Matriz SoD']
        for item in options:
            self.btn = tk.Button(self.bar, text=item, command=self.show_button)
            self.btn.pack(pady=10)

        self.main_content = tk.Frame(self, bg='white')
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_button(self):
        self.main_content.config(bg='teal')

