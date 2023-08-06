#!/usr/bin/env python3.8
from os import system
from time import sleep


def rest(seconds, msg=None):
    if msg is not False:
        speak(msg or "Rest")
    while seconds:
        if seconds < 6:
            speak(str(seconds), bg=True)
        seconds -= 1
        sleep(1)
    sleep(1)


def speak(msg, bg=False):
    amp = "&" if bg else ""
    system(f"say -v samantha '{msg}' {amp}")


def exercise(seconds, msg=None, countdown=True):
    speak(msg or "Start")

    while seconds:
        sleep(1)
        if seconds < 6 and countdown:
            speak(str(seconds), bg=True)
        seconds -= 1
    sleep(1)


def bag(reps):
    sleep(1)
    speak("Punching bag!")
    for x in range(reps):
        exercise(120, msg="Start punching!")
        if x + 1 != reps:
            rest(30)
    exercise(60, msg="cool down")
    speak("Done!")


def ropes(reps):
    sleep(1)
    speak("Battle ropes. Start in a standing position!")
    for x in range(reps):
        exercise(30, msg="Jumping jacks!")
        exercise(30, msg="Twists!")
        exercise(30, msg="Jump slams!")
        exercise(30, msg="Planks!")
        exercise(30, msg="Alternate arms!")
        if x + 1 != reps:
            rest(30)
    speak("Done!")


def core(reps):
    sleep(1)
    speak("Core. Start in a high plank position!")
    for x in range(reps):
        exercise(33, "High plank!")
        exercise(33, "Right side!")
        exercise(33, "Left side!")
        if x + 1 != reps:
            rest(30)
    speak("Done!")


def strength(reps):
    speak("Strength training!")
    for x in range(reps):
        exercise(20, "Pushups!")
        exercise(20, "Rows!")
        exercise(20, "Squats!")
        exercise(20, "Calf raises!")
        if x + 1 != reps:
            rest(30)
    speak("Done!")
