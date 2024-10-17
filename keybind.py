from os import system
from lxml import etree
import re
from tenacity import retry, stop_after_attempt


def puller():
    system("adb shell uiautomator dump /sdcard/binds.xml")
    system("adb pull /sdcard/binds.xml")


def regex(text):
    pattern = r'\[(\d+),(\d+)\]'
    matches = re.findall(pattern, text)
    coordinates = [(int(x), int(y)) for x, y in matches]
    avg_x = sum(x for x, _ in coordinates) / len(coordinates)
    avg_y = sum(y for _, y in coordinates) / len(coordinates)
    return avg_x, avg_y


def getxy(element) -> int:
    puller()
    with open("binds.xml", "r") as f:
        bind_data = f.read()
    root = ET.fromstring(bind_data)
    target_node = root.find(f".//node[@content-desc='{element}']")
    if target_node is None:
        target_node = root.find(f".//node[@text='{element}']")
    coordinate = target_node.get("bounds")
    x, y = regex(coordinate)
    x = int(x)
    y = int(y)
    return x, y


def click(x, y):
    system(f"adb shell input tap {x} {y}")


def type(string):
    system(f"adb shell input text {string}")


def setting(packagename):
    system(
        f"adb shell  am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:{packagename}")


def back(times=1):
    for _ in range(times):
        system("adb shell input keyevent KEYCODE_BACK")


def launch(packagename):
    system(
        f"adb shell monkey -p {packagename} -c android.intent.category.LAUNCHER 1")


@retry(stop=stop_after_attempt(2))
def extract():
    puller()
    tree = etree.parse("binds.xml")
    data = tree.xpath("//node[starts-with(@text, '{\"domain\":')]/@text")
    if data:
    	return data[0]
