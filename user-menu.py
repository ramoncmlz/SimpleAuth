
user_list= [
    {"username": "admin", "password": "321"},
]

guest_options = {
        1:"Login",
        2:"Register",
        3:"Exit"
    }

logged_options = {
        1:"Logout",
        2:"Exit"
    }

admin_options = {
        1:"Delete User",
        2:"Logout",
        3:"Exit"
    }

def show_menu(guest_options):
    while True:
        print("Welcome to the menu.\nOptions:")
        for chave, valor in guest_options.items():
            print(f"{chave} - {valor}")

        choice = input("Select an option: ")

        if choice.isdigit() and int(choice) in guest_options:
            return int(choice)
        else:
            print("Invalid option. Try again.")

def register(user_list):
    username = input("Create your username: ")
    password = input("Create a password: ")
    user_list.append({"username": username, "password": password}) # add a dict to the list

def login(user_list):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    for user in user_list:
        if username == user["username"] and password == user["password"]:
            print(f"You successfully logged as {username}.")
            current_user = user["username"]
            choice = None
            return user["username"]

    print("Invalid username or password.")
    return None

def logout(current_user):
    if current_user != None:
        print("You successfully logged out.")
        return None

def delete_user(user_list, username):
    for user in user_list:
        if user["username"] == username:
            user_list.remove(user)
            print(f"User {username} deleted.")
            return

def show_users(user_list):
    print("USERS:")
    for user in user_list:
        print(f"{user['username']}")

choice = None
current_user = None

while choice != 3:
    if current_user == None: # se o usuário não está logado -> guest
        choice = show_menu(guest_options)  # mostra o menu de guest e recebe a escolha
        if choice == 1:  # login
            current_user = login(user_list)
        elif choice == 2: # register
            register_user = register(user_list)
    elif current_user == "admin": # se o usuário é o admin
        choice = show_menu(admin_options) # abre o menu de admin e recebe a escolha
        if choice == 1: # delete
            show_users(user_list)
            selected_user = input("Which user you want to delete?: ")
            if selected_user == "admin":
                print("Error. You can't delete admin!")
            else:
                delete_user(user_list, selected_user)
            continue # sai do escopo
        elif choice == 2: #logout admin
            current_user = logout(current_user) # se fez logout -> menu de guest

    else: # se não é nem guest e nem admin -> usuário logado
        choice = show_menu(logged_options) # abre o menu normal e recebe a escolha
        if choice == 1: # logout
            current_user = logout(current_user)
