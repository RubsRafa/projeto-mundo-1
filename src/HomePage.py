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
        # print('username', username)

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
            'Matriz SoD': MatrizPage
        }


        # if username == 'admin':
        #     self.pages = {
        #        'Início': InicioPage,
        #        'Sistemas': SistemasPage,
        #        'Perfis de Acesso': PerfisPage,
        #        'Matriz SoD': MatrizPage
        #     }
        # elif username == 'diretor':
        #     self.pages = {
        #         'Início': InicioPage,
        #         'Sistemas': SistemasPage,
        #         'Perfis de Acesso': PerfisPage,
        #         'Matriz SoD': MatrizPage
        #     }
        # elif username == 'Professor':
        #     self.pages = {
        #         'Início': InicioPage,
        #         'Sistemas': SistemasPage,
        #         'Perfis de Acesso': PerfisPage
        #     }
        # else: 
        #     self.pages = {
        #         'Início': InicioPage,
        #         'Sistemas': SistemasPage
        #     }

        self.show_page('Início')

    def show_button(self, button_text):
        self.show_page(button_text)

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

        self.title = ("Gestão Eficiente de Perfis de Acesso Corporativo:\nPrevenção de Conflitos e Segurança de Dados\n")
        self.content = (
            'O projeto em desenvolvimento visa aprimorar a gestão de perfis de\nacesso em sistemas corporativos, uma demanda crucial para empresas\nenfrentando desafios de auditoria e preocupações com fraudes financeiras.\nCom a implementação da Lei Geral de Proteção de Dados (LGPD) no Brasil, a\natenção à segurança das informações pessoais tornou-se imperativa,\ntornando essencial um gerenciamento eficaz de acessos.',
            'Para garantir o funcionamento eficiente, o projeto propõe cadastros\ndetalhados, abrangendo sistemas, perfis de acesso e a própria Matriz SoD.\nCada elemento do cadastro é estruturado para fornecer informações essenciais,\ncomo códigos de sistema, nomes de perfil e descrições detalhadas, facilitando\na solicitação e concessão de acessos pelos gestores.'
            )
        self.color = '#272727'

        title_label = tk.Label(self, text=self.title, font=('Roboto', 16), foreground='white', bg='black')
        title_label.pack(padx=20, pady=20)

        self.configure(bg=self.color)
        label = tk.Label(self, text=self.content, font=('Roboto', 12), foreground='white', bg='gray')
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
            if name == self.name_placeholder or name == '':
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
                new_profile = {"code": int(code), "name": name, "description": description}
                data.append(new_profile)
                self.write_to_xlsx_profiles(data)

                if code and name and description:
                    values = (code, name, description)
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
            code = int(self.tree.item(selected_item, 'values')[0])
            name = str(self.tree.item(selected_item, 'values')[1])
            description = str(self.tree.item(selected_item, 'values')[2])
            
            data = self.read_from_xlsx_profiles()
            
            for profile in data:
                if profile['code'] == code and profile['name'] == name and profile['description'] == description:
                    data.remove(profile)
                   
                    self.write_to_xlsx_profiles(data)
                    self.tree.delete(selected_item)
        else:
            tkMessageBox.showerror('NOT FOUND', 'Esse cadastro não foi\nencontrado no arquivo.')

    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_profiles({})

        systems = self.read_from_xlsx_systems()
        data = self.read_from_xlsx_profiles()
        for profile in data:
            code = profile['code']
            name = profile['name']
            description = profile['description']
            system_name = systems[code]
            self.tree.insert('', 'end', values=(f'{code} - {system_name}', name, description))

    def read_from_xlsx_systems(self):
        try:
            df = pd.read_excel('systems.xlsx', engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}
            
    def write_to_xlsx_profiles(self, data):
        df = pd.DataFrame(data)
        df.to_excel(self.filename, index=False)

    def read_from_xlsx_profiles(self):
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data                
        except pd.errors.EmptyDataError:
            return {}


class MatrizPage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.filename = 'matriz.xlsx'
        self.filename_systems = 'systems.xlsx'
        self.filename_profiles = 'profiles.xlsx'
        self.create_widgets()

    def create_widgets(self):
        self.columns = ('Perfil de Acesso 1', 'Perfil de Acesso 2')
        self.matrix_tree = ttk.Treeview(self, columns=self.columns, show='headings', height=10)

        for col in self.columns:
            self.matrix_tree.heading(col, text=col)
            self.matrix_tree.column(col, width=180)
        self.matrix_tree.pack(pady=20)

        profile_1 = self.create_association_list()
        profile_2 = self.create_association_list()

        self.profile_access_1 = tk.StringVar(self)
        self.profile_access_1.set(profile_1[0])
        profile_access_1_dropdown = ttk.Combobox(self, textvariable=self.profile_access_1, values=profile_1)
        profile_access_1_dropdown.pack(pady=10)

        self.profile_access_2 = tk.StringVar(self)
        self.profile_access_2.set(profile_2[0])
        profile_access_2_dropdown = ttk.Combobox(self, textvariable=self.profile_access_2, values=profile_2)
        profile_access_2_dropdown.pack(pady=10)

        add_button = tk.Button(self, text='Adicionar à Matriz', command=self.add_to_matrix)
        remove_button = tk.Button(self, text='Remover', command=self.remove_matrix)

        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.load_data()

    def add_to_matrix(self):
        
        profile_1 = self.profile_access_1.get()
        profile_2 = self.profile_access_2.get()
        if profile_1 == profile_2:
            tkMessageBox.showerror('INVALID REQUEST', 'Escolha perfis de\nacesso diferentes.')
        else:
            data = self.read_from_xlsx_matriz()
            for item in data:
                item1 = item['profile_access_1']
                item2 = item['profile_access_2']
                if profile_1 == item1 and profile_2 == item2:
                    tkMessageBox.showerror('INVALID', 'Os perfis de acesso\njá foram traçados.')
                    return
            else:
                new_matrix = { "profile_access_1": profile_1, "profile_access_2": profile_2 }
                data.append(new_matrix)
                self.write_to_xlsx_matriz(data)
                self.matrix_tree.insert('', 'end', values=(profile_1, profile_2))

    def remove_matrix(self):
        selected_item = self.matrix_tree.selection()

        if selected_item:
            profile1 = self.matrix_tree.item(selected_item, 'values')[0]
            profile2 = self.matrix_tree.item(selected_item, 'values')[1]
            data = self.read_from_xlsx_matriz()

            for profiles in data:
                if profiles['profile_access_1'] == profile1 and profiles['profile_access_2'] == profile2:
                    data.remove(profiles)

                    self.write_to_xlsx_matriz(data)
                    self.matrix_tree.delete(selected_item)
        else:
            tkMessageBox.showerror('NOT FOUND', 'Esse registro não\nfoi encontrado.')
    
    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_matriz({})

        data = self.read_from_xlsx_matriz()

        for item in data:

            profile1 = item['profile_access_1']
            profile2 = item['profile_access_2']
            self.matrix_tree.insert('', 'end', values=(profile1, profile2))

    def create_association_list(self):
        systems_data = self.read_from_xlsx_systems()
        profiles_data = self.read_from_xlsx_profiles()

        association_list = []

        for profile in profiles_data:
            profile_name = profile['name']

            for _, name in systems_data.items():
                data = f'{profile_name} - {name}'
                association_list.append(data)

        return association_list
    
    def read_from_xlsx_matriz(self):
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data
        except pd.errors.EmptyDataError:
            return {}

    def write_to_xlsx_matriz(self, data):
        df = pd.DataFrame(data)
        df.to_excel(self.filename, index=False)

    def read_from_xlsx_systems(self):
        try:
            df = pd.read_excel(self.filename_systems, engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}
            
    def read_from_xlsx_profiles(self):
        try:
            df = pd.read_excel(self.filename_profiles, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data                
        except pd.errors.EmptyDataError:
            return {}




if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

