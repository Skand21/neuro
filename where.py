import os
from colorama import Fore, Back, Style
import sys
from time import sleep
import PySimpleGUI as sg


def main():
    layout = [[sg.Text("Куда сохранить файл?")],
              [sg.Input()],
              [sg.Button('Ok')]]

    window = sg.Window('Config', layout)

    event, values = window.read()

    print(values[0], "Saved")

    window.close()


main()