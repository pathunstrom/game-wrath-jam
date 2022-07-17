from functools import partial


def linear(time):
    return time


def smooth_start_2(time):
    return time * time


def smooth_start_3(time):
    return time * time * time


def smooth_stop_2(time):
    f = 1 - time
    return 1 - (f * f)


def smooth_stop_3(time):
    f = 1 - time
    return 1 - (f * f * f)


def mix(ease_1, ease_2, weight_2, time):
    a = ease_1(time)
    b = ease_2(time)
    return a + weight_2 * (b - a)


def crossfade(ease_1, ease_2, time):
    a = ease_1(time)
    b = ease_2(time)
    return a + time * (b - a)


smoother_step = partial(crossfade, smooth_start_3, smooth_stop_3)


def clamp(min_value, max_value, value):
    return min(max(value, min_value), max_value)


clamp_normal = partial(clamp, 0, 1)
