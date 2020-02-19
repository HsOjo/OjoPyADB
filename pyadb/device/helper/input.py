import re

from .base import BaseHelper


class KeyCode:
    UNKNOWN = 0
    SOFT_LEFT = 1
    SOFT_RIGHT = 2
    HOME = 3
    BACK = 4
    CALL = 5
    ENDCALL = 6
    NUM_0 = 7
    NUM_1 = 8
    NUM_2 = 9
    NUM_3 = 10
    NUM_4 = 11
    NUM_5 = 12
    NUM_6 = 13
    NUM_7 = 14
    NUM_8 = 15
    NUM_9 = 16
    STAR = 17
    POUND = 18
    DPAD_UP = 19
    DPAD_DOWN = 20
    DPAD_LEFT = 21
    DPAD_RIGHT = 22
    DPAD_CENTER = 23
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    POWER = 26
    CAMERA = 27
    CLEAR = 28
    A = 29
    B = 30
    C = 31
    D = 32
    E = 33
    F = 34
    G = 35
    H = 36
    I = 37
    J = 38
    K = 39
    L = 40
    M = 41
    N = 42
    O = 43
    P = 44
    Q = 45
    R = 46
    S = 47
    T = 48
    U = 49
    V = 50
    W = 51
    X = 52
    Y = 53
    Z = 54
    COMMA = 55
    PERIOD = 56
    ALT_LEFT = 57
    ALT_RIGHT = 58
    SHIFT_LEFT = 59
    SHIFT_RIGHT = 60
    TAB = 61
    SPACE = 62
    SYM = 63
    EXPLORER = 64
    ENVELOPE = 65
    ENTER = 66
    DEL = 67
    GRAVE = 68
    MINUS = 69
    EQUALS = 70
    LEFT_BRACKET = 71
    RIGHT_BRACKET = 72
    BACKSLASH = 73
    SEMICOLON = 74
    APOSTROPHE = 75
    SLASH = 76
    AT = 77
    NUM = 78
    HEADSETHOOK = 79
    FOCUS = 80  # Camera focus
    PLUS = 81
    MENU = 82
    NOTIFICATION = 83
    SEARCH = 84
    MEDIA_PLAY_PAUSE = 85
    MEDIA_STOP = 86
    MEDIA_NEXT = 87
    MEDIA_PREVIOUS = 88
    MEDIA_REWIND = 89
    MEDIA_FAST_FORWARD = 90
    MUTE = 91


class InputHelper(BaseHelper):
    def input(self, *args, **kwargs):
        return self.device.execute('input', *args, **kwargs)

    def text(self, content: str):
        content = content.encode().decode('ascii', 'ignore')
        for i in set(re.findall(r'\s', content)):
            content = content.replace(i, '\\' + i)
        for index, line in enumerate(content.splitlines()):
            if index > 0:
                self.keyevent(KeyCode.ENTER)
            self.input('text', line)

    def keyevent(self, code: int, longpress=False):
        [stat, _, _] = self.input('keyevent', code, '--longpress' if longpress else None)
        return stat == 0

    def tap(self, x: int, y: int):
        [stat, _, _] = self.input('tap', x, y)
        return stat == 0

    def swipe(self, sx: int, sy: int, ex: int, ey: int, duration: int = None):
        [stat, _, _] = self.input('swipe', sx, sy, ex, ey, duration)
        return stat == 0
