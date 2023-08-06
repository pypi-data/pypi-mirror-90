import random
import math
import time
import os
import sys
from enum import Enum

class Style(Enum):
    NORMAL = "NORMAL"
    EQUAL = "EQUAL"
    PLUS = "PLUS"
    PLUS_EQUAL = "PLUS_EQUAL"
    MINUS = "MINUS"
    MINUS_EQUAL = "MINUS_EQUAL"
    ALL = "ALL"

class Button:
    def __init__(self,text,onchoose,key):
        self.text = text
        self.onchoose = onchoose
        self.key = key

    def choose(self):
        self.onchoose()

class MainMenu:
    def __init__(self,title,buttons,style=Style.ALL):
        self.title = title
        self.buttons = buttons
        self.style = style

    def show(self):
        print("")

        if self.style == Style.NORMAL:
            print(self.title)
        elif self.style == Style.EQUAL:
            print("=== " + self.title + " ===")
        elif self.style == Style.PLUS:
            print("+++ " + self.title + " +++")
        elif self.style == Style.PLUS_EQUAL:
            print("=+= " + self.title + " =+=")
        elif self.style == Style.MINUS:
            print("--- " + self.title + " ---")
        elif self.style == Style.MINUS_EQUAL:
            print("-=- " + self.title + " -=-")
        elif self.style == Style.ALL:
            print("-=+=- " + self.title + " -=+=-")

        print("")
        
        for btn in self.buttons:
            print("- " + btn.text + " (" + btn.key + ")")

    def prompt(self,text="Which option do you want to choose?"):
        print()
        
        answered = False
        while not answered:
            question = input(text + " ")

            for btn in self.buttons:
                if question.lower() == btn.key.lower():
                    answered = True
                    print("")
                    btn.choose()

class Message:
    def __init__(self,text,title=None,style=Style.NORMAL):
        self.text = text
        self.title = title
        self.style = style

    def show(self):
        print("")

        if self.title != None:
            if self.style == Style.NORMAL:
                print(self.title)
            elif self.style == Style.EQUAL:
                print("=== " + self.title + " ===")
            elif self.style == Style.PLUS:
                print("+++ " + self.title + " +++")
            elif self.style == Style.PLUS_EQUAL:
                print("=+= " + self.title + " =+=")
            elif self.style == Style.MINUS:
                print("--- " + self.title + " ---")
            elif self.style == Style.MINUS_EQUAL:
                print("-=- " + self.title + " -=-")
            elif self.style == Style.ALL:
                print("-=+=- " + self.title + " -=+=-")

            print("")

        print(self.text)

class Action:
    def __init__(self,text,title,buttons,style=Style.NORMAL):
        self.text = text
        self.title = title
        self.buttons = buttons
        self.style = style
    
    def prompt(self):
        print()

        if self.title != None:
            if self.style == Style.NORMAL:
                print(self.title)
            elif self.style == Style.EQUAL:
                print("=== " + self.title + " ===")
            elif self.style == Style.PLUS:
                print("+++ " + self.title + " +++")
            elif self.style == Style.PLUS_EQUAL:
                print("=+= " + self.title + " =+=")
            elif self.style == Style.MINUS:
                print("--- " + self.title + " ---")
            elif self.style == Style.MINUS_EQUAL:
                print("-=- " + self.title + " -=-")
            elif self.style == Style.ALL:
                print("-=+=- " + self.title + " -=+=-")

        for btn in self.buttons:
            print("- " + btn.text + " (" + btn.key + ")")
        
        answered = False
        while not answered:
            question = input(self.text + " ")

            for btn in self.buttons:
                if question.lower() == btn.key.lower():
                    answered = True
                    btn.choose()

def clear():
    try:
        if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
            os.system("clear")
        elif sys.platform == "win32":
            os.system("cls")
    except:
        try:
            os.system("clear")
        except:
            os.system("cls")