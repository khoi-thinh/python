'''
#ex25 from practicepython. Guessing user's number with binary search.
'''
guess_list = list(range(0, 101))

def guess_game(guess_list):
    count = 0
    while True:
        list_length = len(guess_list)
        middle_position = int(list_length / 2)
        middle_value = guess_list[middle_position]
        count += 1

        print("My guess is: ", middle_value)
        user_answer = input("Is this higher, lower or correct? Type your answer: ")
        if user_answer == 'higher':
            guess_list = guess_list[:middle_position]
            print("Oh is it higher? I'll try again")
            print("-------------------------------")
        elif user_answer == 'lower':
            guess_list = guess_list[middle_position:]
            print("Oh is it lower? I'll try again\n")
            print("-------------------------------")
        elif user_answer == 'correct':
            print("Cool. So i got it right after", count, "times")    
            break

if __name__ == '__main__':
    guess_game(guess_list) 
