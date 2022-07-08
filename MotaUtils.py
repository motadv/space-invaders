def interpolate(value, a, b, c, d):
    y = (value - a)/(b - a) * (d - c) + c
    return y