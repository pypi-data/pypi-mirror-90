"""

File: ip_reveal/tools/timers/__init__
Author: Taylor-Jayde Blackstone <t.blackstone@inspyre.tech>
Added in Version: 1.0(dev) - 10/26/2020

Description:
    This package handles the necessary time-keeping routines for "IP Reveal".

Design:
    This package lends it's opening preparation to the "start()" method (which should not be confused with the similarly
    named: "_start()"). So, if - for example - one wanted to get all parts if the timer working, and keeping time in the
    easiest way possible (with this package), they could write something out like the following example

Examples:

    from time import sleep
    from ip_reveal import timers

    timer = timers

    timer.start()

    while True:
        timer_state = timer.get_elapsed()
        print(timer_state)

    # And resetting is even easier
    timer.reset()

"""

import humanize
import datetime as dt
from time import time, sleep


class TimerStartError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "There was an error with your timer!"

        self.message = message


# A variable containing the time when this module was loaded
start_time = None

# A variable to contain the seconds since epoch when last tripped
last_refresh = None

# A variable to hold a formatted, humanized, continually updated string that represents the time
# since the information was last updated.
last_ref_f = None


def _start():
    global start_time, last_refresh
    if start_time is None:
        start_time = time()
        last_refresh = start_time
    else:
        raise TimerStartError(
            message="You are trying to start a timer that's already started!")


def start():
    try:
        _start()
    except TimerStartError as e:
        print(e.message)


def get_elapsed():
    global last_refresh, last_ref_f

    # Grab the oldrefresh time
    old_time = last_refresh

    # Grab current time
    new = time()
    diff = new - old_time
    last_ref_f = humanize.naturaldelta(diff)

    elapsed = humanize.naturaldelta(diff)

    return elapsed


def refresh():
    global last_refresh, last_ref_f
    last_refresh = time()


def clear():
    global last_refresh, start_time, last_ref_f
    last_refresh = None
    start_time = None
    last_ref_f = None
