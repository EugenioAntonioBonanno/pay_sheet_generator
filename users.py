import pickle


try:
    users = open("users", 'x')

except:
    users = open('users', 'r')

user_dict = {"gino": "godberry5"}

print(users)

users.close()

start_path = input("Type 'login' to login or 'register' to register a new account?")

if start_path == 'register':
    while start_path == 'register':

        name = input("Please enter your name: ")
        if name.lower() in user_dict:
            print("Sorry that name is already taken. Please try again.")
            pass
        else:
            password_1 = input('Please enter a password')
            password_2 = input("Please enter the same password a second time.")
            if password_1 == password_2:
                user_dict[name] = password_1
                start_path = "complete"
            else:
                print("Sorry your passwords do not match please restart the registration process.")

users = open('users', 'a')

pickle.dump(str(user_dict), users)

users.close()