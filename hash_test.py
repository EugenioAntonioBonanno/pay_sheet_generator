import hashlib

answer = ("dogs")
answer = answer.encode('utf-8')
answer = hashlib.sha512(answer)

match = False

while not match:
    attempt = input("Whats the password?")
    attempt = attempt.encode('utf-8')
    attempt = hashlib.sha512(attempt)

    if answer.digest() == attempt.digest():
        print("You got it")
        match = True
    else:
        print("Sorry try again")