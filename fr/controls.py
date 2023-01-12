from typing import Iterable
import keyboard

def quad_control(dx, dy, speed, W: str = "w", A: str = "a", S: str = "s", D: str = "d"):
    if keyboard.is_pressed(A):
        dx -= speed
    if keyboard.is_pressed(D):
        dx += speed
    if keyboard.is_pressed(W):
        dy += speed
    if keyboard.is_pressed(S):
        dy -= speed
    return dx, dy
    
def dual_control(dz, speed, Plus: str = "z", Minus: str = "x"):
    if keyboard.is_pressed(Plus):
        dz += speed
    if keyboard.is_pressed(Minus):
        dz -= speed
    return dz

def recognizer_control(dkey, domain: Iterable):
    for key in domain:
        key = str(key)
        if keyboard.is_pressed(key):
            return key
    return dkey

def switch_control(dresult, cases: Iterable, Before: str = "n", After: str = "m"):
    cases = list(cases)
    if keyboard.is_pressed(Before):
        return cases[(cases.index(dresult) - 1 + len(cases)) % len(cases)]
    elif keyboard.is_pressed(After):
        return cases[(cases.index(dresult) + 1) % len(cases)]
    return dresult
