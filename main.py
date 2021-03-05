from nux_checker import NuxChecker
from time import sleep

if __name__ == '__main__':
    while True:
        checker = NuxChecker()
        checker.get_extra()
        sleep(10*60)
