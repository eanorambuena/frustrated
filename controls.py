import keyboard

def quad_control(dx, dy, speed, W = "w", A = "a", S = "s", D = "d"):
    if keyboard.is_pressed(A):
        dx -= speed
    if keyboard.is_pressed(D):
        dx += speed
    if keyboard.is_pressed(W):
        dy += speed
    if keyboard.is_pressed(S):
        dy -= speed
    return dx, dy
    
def dual_control(dz, speed, Plus = "z", Minus = "x"):
    if keyboard.is_pressed(Plus):
        dz += speed
    if keyboard.is_pressed(Minus):
        dz -= speed
    return dz

def recognizer_control(dkey, domain):
    for key in domain:
        key = str(key)
        if keyboard.is_pressed(key):
            return key
    return dkey