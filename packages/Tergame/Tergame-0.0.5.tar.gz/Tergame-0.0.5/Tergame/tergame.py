import random
import math
import time
import os
import sys
from enum import Enum

class WrongTypeError(Exception):
    pass

class ArgumentError(Exception):
    pass

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
        if isinstance(text,str):
            self.text = text
        else:
            raise WrongTypeError("Argument 'text' must be type of str, not " + type(text).__name__)
        if callable(onchoose):
            self.onchoose = onchoose
        else:
            raise WrongTypeError("Argument 'onchoose' must be a function.")
        if isinstance(key,str):
            self.key = key
        else:
            raise WrongTypeError("Argument 'key' must be type of str, not " + type(key).__name__)

    def choose(self):
        self.onchoose()

class ButtonSet:
    def __init__(self):
        self.buttons = []

    def add(self,btn):
        if isinstance(btn,Button):
            self.buttons.append(btn)
        else:
            raise WrongTypeError("Argument 'btn' must be type of Button, not " + type(btn).__name__)

    def remove(self,btn=None,index=None):
        if btn == None and index != None:
            self.buttons.pop(index)
        elif index == None and btn != None:
            self.buttons.remove(btn)
        else:
            raise ArgumentError("Either argument 'btn' or argument 'index' should be defined")

    def addList(self,btns):
        if isinstance(btns,list):
            for btn in btns:
                if isinstance(btn,Button):
                    self.buttons.append(btn)
                else:
                    raise WrongTypeError("Item " + str(btns.index(btn)) + " of list argument 'btns' must be type of Button, not " + type(btn).__name__)
        else:
            raise WrongTypeError("Argument 'btns' must be type of list, not " + type(btns).__name__)

class MainMenu:
    def __init__(self,title,buttons,style=Style.ALL):
        if isinstance(title,str):
            self.title = title
        else:
            raise WrongTypeError("Argument 'title' must be type of str, not " + type(title).__name__)

        if isinstance(buttons,list):
            self.buttons = buttons
        elif isinstance(buttons,ButtonSet):
            self.buttons = []
            for btn in buttons.buttons:
                self.buttons.append(btn)
        else:
            raise WrongTypeError("Argument 'buttons' must either be type of list or ButtonSet, not " + type(btns).__name__)
        
        if isinstance(style,Style):
            self.style = style
        else:
            raise WrongTypeError("Argument 'style' must be type of Style, not " + type(style).__name__)

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
        if isinstance(text,str):
            print()
            
            answered = False
            while not answered:
                question = input(text + " ")

                for btn in self.buttons:
                    if question.lower() == btn.key.lower():
                        answered = True
                        print("")
                        btn.choose()
        else:
            raise WrongTypeError("Argument 'text' must be type of str, not " + type(text).__name__)

class Message:
    def __init__(self,text,title=None,style=Style.NORMAL):
        if isinstance(text,str):
            self.text = text
        else:
            raise WrongTypeError("Argument 'text' must be type of str, not " + type(text).__name__)
        if isinstance(title,str) or title == None:
            self.title = title
        else:
            raise WrongTypeError("Argument 'title' must be type of str, not " + type(title).__name__)
        if isinstance(style,Style):
            self.style = style
        else:
            raise WrongTypeError("Argument 'style' must be type of Style, not " + type(style).__name__)

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
        if isinstance(text,str):
            self.text = text
        else:
            raise WrongTypeError("Argument 'text' must be type of str, not " + type(text).__name__)
        if isinstance(title,str):
            self.title = title
        else:
            raise WrongTypeError("Argument 'title' must be type of str, not " + type(title).__name__)
        if isinstance(buttons,list):
            self.buttons = buttons
        elif isinstance(buttons,ButtonSet):
            self.buttons = []
            for btn in buttons.buttons:
                self.buttons.append(btn)
        else:
            raise WrongTypeError("Argument 'buttons' must either be type of list or ButtonSet, not " + type(buttons).__name__)
        if isinstance(style,Style):
            self.style = style
        else:
            raise WrongTypeError("Argument 'style' must be type of Style, not " + type(style).__name__)
    
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