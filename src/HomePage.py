import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import pandas as pd
import EntryFocus as Focus
import os

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
        self.filename = 'systems.xlsx'
        self.create_widgets()

    def create_widgets(self):
        self.columns = ('Código do Sistema', 'Nome do Sistema')
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=20)

        self.code_entry = tk.Entry(self, width=30)
        self.name_entry = tk.Entry(self, width=30)

        self.code_placeholder = 'Insira o Código do Sistema'
        self.name_placeholder = 'Insira o Nome do Sistema'

        Focus.setup_entry(self.code_entry, self.code_placeholder)
        Focus.setup_entry(self.name_entry, self.name_placeholder)

        add_button = tk.Button(self, text='Adicionar', command=self.add_system)
        remove_button = tk.Button(self, text='Remover', command=self.remove_system)

        self.code_entry.pack(pady=10)
        self.name_entry.pack(pady=10)
        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.load_data()
    

    def add_system(self):
        code = self.code_entry.get()
        name = self.name_entry.get()
        data = self.read_from_xlsx_systems()
        try:
            int(code)
        except:
            tkMessageBox.showerror('INVALID DATA', 'O código deve ser um número!')

        if int(code) in data:
            tkMessageBox.showerror('UNAUTHORIZED', 'O código inserido já existe.\nInsira outro código.')
        else:
            data[int(code)] = name
            if name == self.name_placeholder:
                tkMessageBox.showerror('INVALID DATA', 'Você deve inserir um\nnome para o sistema.')
            else:
                self.write_to_xlsx_systems(data)
                if code and name:
                    self.tree.insert('', 'end', values=(code, name))
                    self.code_entry.delete(0, 'end')
                    self.name_entry.delete(0, 'end')
                    if code == self.code_placeholder:
                        self.code_entry.insert(0, self.code_placeholder)
                        self.code_entry.configure(fg='grey')
                    if name == self.name_placeholder:
                        self.name_entry.insert(0, self.name_placeholder)
                        self.name_entry.configure(fg='grey')

    def remove_system(self):
        selected_item = self.tree.selection()

        if selected_item:
            code = str(self.tree.item(selected_item, 'values')[0])
            data = self.read_from_xlsx_systems()

            if int(code) in data:
                del data[int(code)]
                self.write_to_xlsx_systems(data)
                self.tree.delete(selected_item)
            else:
                tkMessageBox.showerror('NOT FOUND.', f'Esse código não foi\nencontrado no arquivo.')
    
    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_systems({})

        data = self.read_from_xlsx_systems()
        for code, name in data.items():
            self.tree.insert('', 'end', values=(code, name))
    
    def write_to_xlsx_systems(self, data):
        df = pd.DataFrame(list(data.items()), columns=self.columns)
        df.to_excel(self.filename, index=False)
        
    def read_from_xlsx_systems(self):
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}



class PerfisPage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.filename = 'profiles.xlsx'
        self.create_widgets()

    def create_widgets(self):
        self.columns = ('Código do Sistema', 'Nome do Perfil', 'Descrição')
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=20)

        self.code_entry = tk.Entry(self, width=30)
        self.name_entry = tk.Entry(self, width=30)
        self.description_entry = tk.Entry(self, width=30)

        self.code_placeholder = 'Insira o Código do Sistema'
        self.name_placeholder = 'Insira o Nome do Perfil'
        self.description_placeholder = 'Insira a Descrição'

        Focus.setup_entry(self.code_entry, self.code_placeholder)
        Focus.setup_entry(self.name_entry, self.name_placeholder)
        Focus.setup_entry(self.description_entry, self.description_placeholder)

        add_button = tk.Button(self, text='Adicionar', command=self.add_profile)
        remove_button = tk.Button(self, text='Remover', command=self.remove_profile)

        self.code_entry.pack(pady=10)
        self.name_entry.pack(pady=10)
        self.description_entry.pack(pady=10)
        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.load_data()

    def add_profile(self):
        code = self.code_entry.get()
        name = self.name_entry.get()
        description = self.description_entry.get()
        systems = self.read_from_xlsx_systems()
        data = self.read_from_xlsx_profiles()
        try:
            int(code)
        except:
            tkMessageBox.showerror('INVALID DATA', 'O código deve ser um número')

        if int(code) not in systems:
            tkMessageBox.showerror('UNAUTHORIZED', 'O código do sistema\ninserido não existe.\nInsira código de\nsistema existente.')
        else:
            if name == self.name_placeholder or name == '':
                tkMessageBox.showerror('INVALID DATA', 'Você deve inserir\num nome\npara o perfil.')
            elif description == self.description_placeholder or description == '':
                tkMessageBox.showerror('INVALID DATA', 'Você deve inserir\numa descrição\npara o perfil.')
            else: 
                data[int(code)] = {'Nome do Perfil': name, 'Descrição': description}
                print(data)
                self.write_to_xlsx_profiles(data)

                if code and name and description:
                    values = (code, data[int(code)]['Nome do Perfil'], data[int(code)]['Descrição'])
                    self.tree.insert('', 'end', values=values)
                    self.code_entry.delete(0, 'end')
                    self.name_entry.delete(0, 'end')
                    self.description_entry.delete(0, 'end')
                    if code == self.code_placeholder:
                        self.code_entry.insert(0, self.code_placeholder)
                        self.code_entry.configure(fg='grey')
                    if name == self.name_placeholder:
                        self.name_entry.insert(0, self.name_placeholder)
                        self.name_entry.configure(fg='grey')
                    if description == self.description_placeholder:
                        self.description_entry.insert(0, self.description_placeholder)
                        self.description_entry.configure(fg='grey')

    def remove_profile(self):
        selected_item = self.tree.selection()

        if selected_item:
            code = str(self.tree.item(selected_item, 'values')[0])
            print(code)
            data = self.read_from_xlsx_profiles()
            print(data)
            if int(code) in data:
                del data[int(code)]
                self.write_to_xlsx_profiles(data)
                self.tree.delete(selected_item)
            else:
                tkMessageBox.showerror('NOT FOUND', 'Esse cadastro não foi\nencontrado no arquivo.')

    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_profiles({})

        data = self.read_from_xlsx_profiles()
        for code, name, description in data.items():
            self.tree.insert('', 'end', values=(code, name, description))

    def read_from_xlsx_systems(self):
        print('read systems')
        try:
            df = pd.read_excel('systems.xlsx', engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}
            
    def write_to_xlsx_profiles(self, data):
        print('write profile', data)
        df = pd.DataFrame(list(data.items()), columns=self.columns[:2])
        df.to_excel(self.filename, index=False)

    def read_from_xlsx_profiles(self):
        print('read profile')
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = {row['Código do Sistema']: {'Nome do Perfil': row['Nome do Perfil'], 'Descrição': row['Descrição']} for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

