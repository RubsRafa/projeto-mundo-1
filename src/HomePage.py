import tkinter as tk
from tkinter import ttk

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HOME PAGE')
        self.geometry('800x600')

        self.bar = tk.Frame(self, bg='#535353', width=200)
        self.bar.pack(side=tk.LEFT, fill=tk.Y)

        options = ['Início', 'Sistemas', 'Perfis de Acesso', 'Matriz SoD']
        for item in options:
            self.btn = tk.Button(self.bar, text=item, command=lambda text=item: self.show_button(text), foreground='gray', bg='black', activebackground='gray', activeforeground='white', font=('Roboto', 14), borderwidth=0)
            self.btn.pack(pady=10, padx=10)

        self.main_content = tk.Frame(self, bg='red')
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.pages = {
            'Início': InicioPage,
            'Sistemas': SistemasPage,
            'Perfis de Acesso': lambda: self.update_main_content('Conteúdo da Página de Perfis de Acesso', 'purple'),
            'Matriz SoD': lambda: self.update_main_content('Conteúdo da Página de Matriz SoD', 'yellow')
        }

        self.show_page('Início')

    def show_button(self, button_text):
        self.show_page(button_text)

    def update_main_content(self, content, color):
        if self.main_content:
            self.main_content.destroy()

        self.main_content = tk.Frame(self, bg=color)
        label = tk.Label(self.main_content, text=content, font=('Roboto', 18), foreground='white', bg='gray')
        label.pack(padx=20, pady=20)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_page(self, page_name):
        if page_name in self.pages:
            page = self.pages[page_name]()
            if isinstance(page, tk.Frame):
                if self.main_content:
                    self.main_content.destroy()
                self.main_content = page
                self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


class InicioPage(tk.Frame):
    def __init__(self):
        super().__init__()

        self.content = (
            "Início\n"
            "Adicionar mais texto"
        )
        self.color = 'red'

        self.configure(bg=self.color)
        label = tk.Label(self, text=self.content, font=('Roboto', 14), foreground='white', bg='gray')
        label.pack(padx=20, pady=20)


class SistemasPage(tk.Frame):
    def __init__(self):
        super().__init__()

        self.create_widgets()

    def create_widgets(self):
        columns = ('Código do Sistema', 'Nome do Sistema')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=20)

        self.codigo_entry = tk.Entry(self)
        self.nome_entry = tk.Entry(self)

        add_button = tk.Button(self, text='Adicionar', command=self.adicionar_sistema)
        remove_button = tk.Button(self, text='Remover', command=self.remover_sistema)

        self.codigo_entry.pack(pady=10)
        self.nome_entry.pack(pady=10)
        add_button.pack(pady=10)
        remove_button.pack(pady=10)

    def adicionar_sistema(self):
        codigo = self.codigo_entry.get()
        nome = self.nome_entry.get()

        if codigo and nome:
            self.tree.insert('', 'end', values=(codigo, nome))
            self.codigo_entry.delete(0, 'end')
            self.nome_entry.delete(0, 'end')

    def remover_sistema(self):
        selected_item = self.tree.selection()

        if selected_item:
            self.tree.delete(selected_item)


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

