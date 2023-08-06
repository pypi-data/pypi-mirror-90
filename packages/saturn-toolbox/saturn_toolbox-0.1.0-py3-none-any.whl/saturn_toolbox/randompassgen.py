import random
chars1='abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
chars2 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def start():
    print('Welcome to the Random Password Generator. Version 1.00')
    print("------------------------------------")

  
    length = int(input('How much characters would you like your password to be? '))
    number = int(input('How many passwords would you like to generate? '))
    want_numbers = input('Would you like to have numbers in your password? (yes/no) ').lower()
    print('Here is a list of passwords generated')
    if want_numbers == 'yes':
        for __doc__ in range(number):
            password = ''
            for _ in range(length):
                password += random.choice(chars1)
            print(password)
        print(password)
    elif want_numbers == 'no':
        for __doc__ in range(number):
            password = ''
            for _ in range(length):
                password += random.choice(chars2)
            print(password)
start()