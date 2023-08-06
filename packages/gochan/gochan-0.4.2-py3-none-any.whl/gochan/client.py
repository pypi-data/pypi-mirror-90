from typing import Union
from urllib.parse import urlencode
from urllib.request import HTTPError, Request, URLError, urlopen

from gochan.config import COOKIE, USER_AGENT


def get_bbsmenu() -> str:
    url = "https://menu.5ch.net/bbsmenu.html"
    return _get_content(url)


def get_board(server: str, board: str) -> str:
    url = f"https://{server}.5ch.net/{board}/subject.txt"
    return _get_content(url)


def get_thread_h(server: str, board: str, key: str) -> str:
    url = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}/"
    return _get_content(url)


def get_thread_p(server: str, board: str, key: str, proxy: str) -> str:
    url = f"http://{server}.5ch.net:80/{board}/dat/{key}.dat"
    return _get_content(url, proxy)


def get_responses_after(server: str, board: str, key: str, after: int) -> str:
    url = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}/{after + 1}-"
    return _get_content(url)


def post_response(server: str, board: str, key: str, name: str, mail: str, msg: str) -> str:
    url = f"https://{server}.5ch.net/test/bbs.cgi"
    ref = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}"
    params = {"bbs": board, "key": key, "time": "1588219909",
              "FROM": name, "mail": mail, "MESSAGE": msg, "submit": "書き込み", "oekaki_thread1": ""}

    data = urlencode(params, encoding="shift-jis", errors="xmlcharrefreplace").encode()
    hdrs = {"Referer": ref, "User-Agent": USER_AGENT, "Cookie": COOKIE}

    req = Request(url, headers=hdrs)

    res = urlopen(req, data)
    content = res.read().decode("shift-jis")
    res.close()

    return content


def _get_content(url: str, proxy: str = None) -> str:
    hdr = {"User-Agent": USER_AGENT}

    req = Request(url, headers=hdr)

    if proxy is not None:
        req.set_proxy(proxy, "http")

    response = urlopen(req)
    content = response.read().decode("shift-jis", "ignore")
    response.close()

    return content


def download_image(url: str) -> Union[bytes, HTTPError, URLError]:
    try:
        with urlopen(url) as response:
            data = response.read()
            return data
    except HTTPError as e:
        return e
    except URLError as e:
        return e
