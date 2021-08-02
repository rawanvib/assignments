import random

uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase_letters = uppercase_letters.lower()
digits = '0123456789'
symbols = '!@#$%^&*+'

upper, lower, numbers, symbol = True, True, True, True
# upper, lower, numbers, symbol = False, True, True, True
# upper, lower, numbers, symbol = True, True, True, False

all = ''
if upper:
    all += uppercase_letters
if lower:
    all += lowercase_letters
if numbers:
    all += digits
if symbol:
    all += symbols

# length of a password
length = 10
amount = 5
for i in range(amount):
    password = "".join(random.sample(all, length)) # sample simply picks any character from string once only do not repeat it
    print(password)