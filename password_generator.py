import string
import random

lower_string = string.ascii_lowercase
upper_string = string.ascii_uppercase
special_string = "!@#$%&*()[]{}"
number = '0123456789'

list_string = [lower_string, upper_string, special_string, number]

password = ''


while True:
    password_length = int(input("Enter length of password: "))
    if password_length < 14:
        print("Hey, this password's length is not that good. Maybe 14 will be better.")
    else:
        break
for _ in range(password_length):
    x = random.choice(random.choice(list_string)) 
    password = password + x
print(password)    
