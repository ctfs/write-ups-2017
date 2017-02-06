#!/usr/bin/env python3
import requests
from re import findall

URL = "https://felicity.iiit.ac.in/contest/extra/fastandfurious/"
def send_solution(session, res):
    data = {"ques_ans" : str(res)}
    ret = s.post(URL, data=data)
    return ret.text

def solve_equation(equation):
    return eval(equation)

def parse_equation(site):
    hits = findall(r'Solve: (\(.*\))', site)
    if not hits:
        return ""
    return hits[0]

def print_level(site):
    hits = findall(r'Level (\d*)', site)
    if hits:
        print("Level {}".format(hits[0]))

def find_flag(site):
    hits = findall(r'(the_flag_is_\w*)', site)
    if hits:
        print("Flag: {}".format(hits[0]))
        return False
    return True

def get_start(session):
    return s.get(URL).text

s = requests.Session()
site = get_start(s)
is_next = True
while is_next:
    print_level(site)
    is_next = find_flag(site)
    equation = parse_equation(site)
    res = solve_equation(equation)
    site = send_solution(s, res)


