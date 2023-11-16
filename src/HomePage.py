import tkinter as tk
from tkinter import ttk

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HOME PAGE')
        self.geometry('800x600')

        self.bar = tk.Frame(self, bg='#505050', width=200)
        self.bar.pack(side=tk.LEFT, fill=tk.Y)

        options = ['Início', 'Sistemas', 'Perfis de Acesso', 'Matriz SoD']
        for item in options:
            self.btn = tk.Button(self.bar, text=item, command=lambda text=item: self.show_button(text), foreground='gray', bg='black', activebackground='gray', activeforeground='white', font=('Roboto', 14), borderwidth=0)
            self.btn.pack(pady=10, padx=10)

        self.main_content = tk.Frame(self, bg='black')
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.pages = {
            'Início': InicioPage,
            'Sistemas': SistemasPage,
            'Perfis de Acesso': PerfisPage,
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
        self.color = '#272727'

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

        self.code_entry = tk.Entry(self)
        self.name_entry = tk.Entry(self)

        add_button = tk.Button(self, text='Adicionar', command=self.adicionar_sistema)
        remove_button = tk.Button(self, text='Remover', command=self.remover_sistema)

        self.code_entry.pack(pady=10)
        self.name_entry.pack(pady=10)
        add_button.pack(pady=10)
        remove_button.pack(pady=10)

    def adicionar_sistema(self):
        codigo = self.code_entry.get()
        nome = self.name_entry.get()

        if codigo and nome:
            self.tree.insert('', 'end', values=(codigo, nome))
            self.code_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')

    def remover_sistema(self):
        selected_item = self.tree.selection()

        if selected_item:
            self.tree.delete(selected_item)


class PerfisPage(tk.Frame):
    def __init__(self):
        super().__init__()

        self.create_widgets()

    def create_widgets(self):
        columns = ('Código do Sistema', 'Nome do Sistema', 'Descrição')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=20)

        # self.code_label = tk.Label(self, text='Código do Sistema', bg='black', foreground='white', font=("Calibri", 12))
        # self.code_label.grid(row=1, column=1, padx=5, pady=5, sticky='e')
        self.code_entry = tk.Entry(self)
        # self.code_entry.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # self.name_label = tk.Label(self, text='Nome do Sistema', bg='black', foreground='white', font=("Calibri", 12))
        # self.name_label.grid(row=1, column=1, padx=5, pady=5, sticky='e')
        self.name_entry = tk.Entry(self)
        # self.name_entry.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # self.description_label = tk.Label(self, text='Descrição', bg='black', foreground='white', font=("Calibri", 12))
        # self.description_label.grid(row=1, column=1, padx=5, pady=5, sticky='e')
        self.description_entry = tk.Entry(self)
        # self.description_entry.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        code_placeholder = 'Código do Sistema'
        name_placeholder = 'Nome do Sistema'
        description_placeholder = 'Descrição'
        self.code_entry.insert(0, code_placeholder)
        self.name_entry.insert(0, name_placeholder)
        self.description_entry.insert(0, description_placeholder)


        add_button = tk.Button(self, text='Adicionar', command=self.adicionar_sistema)
        remove_button = tk.Button(self, text='Remover', command=self.remover_sistema)

        self.code_entry.pack(pady=10)
        self.name_entry.pack(pady=10)
        self.description_entry.pack(pady=10)
        add_button.pack(pady=10)
        remove_button.pack(pady=10)

    def adicionar_sistema(self):
        code = self.code_entry.get()
        name = self.name_entry.get()
        description = self.description_entry.get()

        if code and name and description:
            self.tree.insert('', 'end', values=(code, name, description))
            self.code_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')

    def remover_sistema(self):
        selected_item = self.tree.selection()

        if selected_item:
            self.tree.delete(selected_item)


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

