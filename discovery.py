#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import termcolor
import pyfiglet
import random

def red(n):
    return termcolor.colored(n, "red")

def green(n):
    return termcolor.colored(n, "green")

def yellow(n):
    return termcolor.colored(n, "yellow")

def blue(n):
    return termcolor.colored(n, "blue")

result_file = "result"
while True:
    try:
        open(result_file, "x").close()
        break
    except FileExistsError:
        result_file = f"Result{random.randint(1, 1000)}"

total_button = 0
total_input = 0

try:
    print(red(pyfiglet.figlet_format("Discover")))
    list_file = input(green("Enter Sites List\n"))

    with open(list_file, "r") as file:
        for index in file.readlines():
            index = index.strip("\n")
            try:
                with requests.get(index, timeout=15) as req:
                    if req.status_code != 200:
                        print(red(f"[-] {index} Response With {req.status_code}"))
                        continue
                    soup = BeautifulSoup(req.text, "html.parser")
                    print(yellow(f"Working on {index}"))

                
                    inputs = soup.find_all("input")
                    input_found = False
                    for input_tag in inputs:
                        input_name = input_tag.get("name")
                        if input_name:
                            print(green(f"[+] Input Name: {input_name}"))
                            input_found = True
                            with open(result_file, "a") as fil:
                                fil.write(f"[+] Found input '{input_name}' in {index}\n")
                        total_input += 1
                    if not input_found and not inputs:
                        print(yellow(f"Working on {index}"))
                        print(red("[-] Not Found Any Inputs"))

                    
                    buttons = soup.find_all("button")
                    button_found = False
                    for button_tag in buttons:
                        button_name = button_tag.get("name")
                        if button_name:
                            print(green(f"[+] Button Name: {button_name}"))
                            button_found = True
                            with open(result_file, "a") as file:
                                file.write(f"[+] Found button '{button_name}' in {index}\n")
                        total_button += 1
                    if not button_found and not buttons:
                        print(yellow(f"[+] Working on {index}"))
                        print(red("[-] Not Found Any Buttons"))

            except requests.RequestException as e:
                print(red(f"[! ERROR !] Failed to fetch {index}: {e}"))

except FileNotFoundError:
    print(red("File Not Found"))
except KeyboardInterrupt:
    print(red("See You Soon"))


if total_input > 0 or total_button > 0:
    print(green(f"[+] Found {total_input} Input{'s' if total_input != 1 else ''}"))
    print(green(f"[+] Found {total_button} Button{'s' if total_button != 1 else ''}"))
else:
    print(red("[-] Not Found Any Input or Button"))
