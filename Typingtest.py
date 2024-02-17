import curses
from curses import wrapper
import time
import random

#List luu tat ca cac diem so
scores = []
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to 10fastfingers TEST!")
    stdscr.addstr("\nPRESS ANY KEY TO BEGIN...")    
    stdscr.refresh()
    stdscr.getkey()

def random_text(stdscr):
    with open("input.txt", "r") as text:
        lines = text.readlines()
        return random.choice(lines).strip()

def display_text(stdscr, target, current, wpm = 0):
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def wpm_test(stdscr):
    target_text = random_text(stdscr)
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    
    while True:
        time_eslasped = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_eslasped/60))/5)
        
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()        

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
            
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
    temp = wpm
    scores.append(temp)
 
            
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    try:
        stdscr.addstr(3,0, f"\nYour highest score is: {max(scores)}", curses.color_pair(2))
    except:
        None

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        stdscr.addstr(3,0, f"\nYour highest score is: {max(scores)}", curses.color_pair(2))
        key = stdscr.getkey()
        if ord(key) == 27: #Neu kla phim Esc thi break
            break

wrapper(main)