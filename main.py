import keybind
from time import sleep
from os import system
import gc


def clear():
    keybind.setting("network.openex.huc")
    sleep(2)
    keybind.click(238, 1420)
    sleep(2)
    keybind.click(291, 846)
    sleep(0.5)
    keybind.click(888, 1398)
    keybind.back(3)


def black_canary(code):
    if code == 1:
        keybind.launch("com.black.canary")
        sleep(2)
        keybind.click(915, 2240)
        sleep(1.5)
        keybind.click(1008, 174)
        sleep(1.5)
        keybind.click(780, 180)
        sleep(1.5)
        keybind.click(550, 1150)
        sleep(1.5)
        keybind.click(1000, 184)
        sleep(1.5)
        keybind.click(303, 340)
        system('adb shell input text "api.agiex.org"')
        keybind.click(1000, 174)
        keybind.back(5)
    elif code == 2:
        keybind.launch("com.black.canary")
        sleep(2)
        keybind.click(540, 350)
        sleep(1.5)
        keybind.click(512, 318)
        sleep(1.5)
        keybind.click(318, 2324)
        sleep(1.5)
        with open("fresh_500_tokens.txt", "a") as f:
            f.write(keybind.extract())
            f.write("\n")
        sleep(1.5)
        keybind.back(1)
        sleep(1.5)
        keybind.click(915, 2240)
        sleep(1.5)
        keybind.back(4)


def oex_sign(private_key):
    keybind.launch("network.openex.huc")
    sleep(7)
    keybind.click(530, 2050)
    sleep(1.5)
    keybind.click(530, 466)
    keybind.type(private_key)
    sleep(3)
    keybind.click(546, 763)
    sleep(1.5)
    for _ in range(12):
        keybind.click(200, 1233)
    keybind.click(840, 1666)


def buff(filename):
    with open(filename, "r") as f:
        buff = f.readlines()
        return [s.replace("\n", '') for s in buff]


def writer(filename, data):
    with open(filename, "w") as f:
        for line in data:
            f.write(str(line))
            f.write("\n")


if __name__ == "__main__":
    keys = buff("tokens.txt")
    for p_key, iter in zip(keys, range(len(keys))):
        black_canary(1)
        oex_sign(f"{p_key}")
        sleep(5)
        black_canary(2)
        sleep(10)
        gc.collect()
        keys.pop(iter)
        writer("tokens.txt", keys)
