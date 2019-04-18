
import pickle



# users = {"Gino": 'godberry5', "Mario": 'godberry6'}
# file_pi = open('filename', 'wb')
# pickle.dump(users, file_pi)

file_pi2 = open('filename', 'rb')
users = pickle.load(file_pi2)

print(users)