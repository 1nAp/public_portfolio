from tkinter import *
import math
#CONSTANTS
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
#TIMER RESET
def reset_timer():
    window.after_cancel(timer)
    global check_marks
    timer_label.config(text="Timer", font=(FONT_NAME, 28, "bold"), fg=GREEN, bg=YELLOW)
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")
    global reps
    reps = 0

#COUNTDOWN MECHANISM
def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        check_mark = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
                check_mark += "✔"
                check_marks.config(text=check_mark)

#TIMER MECHANISM
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if reps <= 8:
        if reps % 8 == 0:
            timer_label.config(text="Big break!", fg=RED)
            count_down(5)
            raise_above_all(window)
        elif reps % 2 == 0:
            timer_label.config(text="Break", fg=PINK)
            count_down(3)
            raise_above_all(window)
        else:
            timer_label.config(text="Work!", fg=GREEN)
            count_down(2)
            raise_above_all(window)

#WINDOW FOCUS
def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)

#UI SETUP
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(row=1, column=1)

timer_label = Label(text="Timer", font=(FONT_NAME, 28, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(row=0, column=1)

start_button = Button(text="Start", command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(row=2, column=2)

check_marks = Label(font=(FONT_NAME, 15, "bold"), fg=GREEN, bg=YELLOW)
check_marks.grid(row=3, column=1)


window.mainloop()