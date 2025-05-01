This program is a pomodoro-timer made using Tkinter.

It essentially works like any other pomodoro-timer, and gives you visual feedback about your cycle as well as ensures you stay informed whenever the status of your pomodoro changes.

For test purposes, the timers have been reduced to a few seconds each.

To change this to the real values, all you need to do is change the start_timer() function as follows:

Original:

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

Fixed: (within the count_down function, change the numbers to the work_sec/short_break_sec/long_break_sec values.

def start_timer():

    global reps

    reps += 1

    work_sec = WORK_MIN * 60

    short_break_sec = SHORT_BREAK_MIN * 60

    long_break_sec = LONG_BREAK_MIN * 60

    if reps <= 8:

        if reps % 8 == 0:

            timer_label.config(text="Big break!", fg=RED)

            count_down(long_break_sec)

            raise_above_all(window)

        elif reps % 2 == 0:

            timer_label.config(text="Break", fg=PINK)

            count_down(short_break_sec)

            raise_above_all(window)

        else:

            timer_label.config(text="Work!", fg=GREEN)

            count_down(work_sec)

            raise_above_all(window)
