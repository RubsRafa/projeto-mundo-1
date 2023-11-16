import bcrypt
import pandas as pd

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def authenticateUser(user, password):
    user_lower = user.lower()
    users_profiles = read_from_xlsx('passwords.xlsx')
    print('user_lower', user_lower)
    print('users_profiles', users_profiles)

    if user_lower in users_profiles:
        stored_hash = users_profiles[user_lower]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print(f'Parabens, voce entrou {user_lower}')
            return True
        else:
            print('Senha incorreta')
    else:
        print('Usuário não encontrado')
    
    return False

def write_to_xlsx(filename, data):
    data_str = {user: hash_.decode('utf-8') for user, hash_ in data.items()}
    df = pd.DataFrame(list(data_str.items()), columns=['Username', 'Hashed_Password'])
    df.to_excel(filename, index=False)

def read_from_xlsx(filename):
    df = pd.read_excel(filename)
    data = {row['Username'].lower(): row['Hashed_Password'].encode('utf-8') for _, row in df.iterrows()}
  
    return data


hashed_passwords = {
    'admin': hash_password('admin'),
    'diretor': hash_password('#01#Estacio23'),
    'gerente': hash_password('#02#Estacio23'),
    'vendedor': hash_password('#03#Estacio23')
}


write_to_xlsx('passwords.xlsx', hashed_passwords)
users_options = read_from_xlsx('passwords.xlsx')
# print(users_options)
