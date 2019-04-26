from objects import SubbedSession


classes_subbed = []
while True:

    subbed = input("Have you subbed any classes this month? \nInput 'done' if you haven't.\n"
                   "If you have enter it in the following format [class id, length , date] \n"
                   "ex: W34 2 13 :\n")
    if subbed.lower() == 'done':
        break
    else:
        print(subbed)
        subbed_list = subbed.split()
        print(subbed_list)
        classes_subbed.append(SubbedSession(subbed[2]))

