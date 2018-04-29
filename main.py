# encoding: utf-8
"""
    __auth__: 孟德功
    __require__: 运行case
    __version__: 无要求
"""
from lib.running import Running_test_case
from lib.media import InitDevice


def main():
    media = InitDevice().media()
    if media:
        for i in media:
            Running_test_case(media=i).start()


if __name__ == '__main__':
    main()
