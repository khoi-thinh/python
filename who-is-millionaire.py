#!usr/bin/python
from sys import exit
inputname = raw_input("Enter your name to participate\n")

def q1():
    print "Question 1.\n Which country is largest in the world?"
    print "a.China b.Canada c.Russia d.Brazil"
    choice = raw_input("> ")
    if "a" in choice or "b" in choice or "d" in choice:
        end("Wrong! c is the right one.")
    elif "c" in choice:
        print "You got it right!."
        q2()
    else:
        wrong("You need to input a,b,c, or d")
        q1()
def q2():
    print "Question 2.\n Who discovered Americas? "
    print "a.Columbus b.Marco polo c.Messi d.Ronaldo"
    choice = raw_input("> ")
    if "b" in choice or "c" in choice or "d" in choice:
        end("Wrong! a is the right answer")
    elif "a" in choice:
        print "Excellent choice!"
        q3()
    else:
        wrong("You need to input a,b,c or d")
        q2()
def q3():
    print "This is your last question!!\n 1 + 1 = ?"
    print "a.1 b.2 c.11 d.3"
    choice = raw_input("> ")
    if "a" in choice or "c" in choice  or "d" in choice:
        end("Feel sorry for you. You've should choosen b")
    elif "b" in choice:
        victory("Congratulations!")
    else:
        wrong("You need to input a,b,c or d")
        q3()
def victory(victory):
    print victory, "You win 100 millions $"
    exit(0)
def quit(quit):
    print quit, "Why do you want to quit now?"
    exit(0)
def end(end):
    print end, "See you later."
    exit(0)
def wrong(wrong):
    print wrong, "Be careful with your answer"
def start():
    print "Welcome to 'Who is millionaire': Mr  %r" % inputname
    print "Let's get it started!"
    print "You need to answer 3 questions in order to win. READY?."
    print "Then, input ok to move on or quit to stop."
    choice = raw_input("> ")
    if choice == "ok":
        q1()
    elif choice == "quit":
        quit("WHAT!!!")
    else:
        print "Just input ok or quit, please"
        start()
start()
