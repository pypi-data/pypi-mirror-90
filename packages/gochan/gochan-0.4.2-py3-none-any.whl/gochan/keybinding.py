import json

from gochan.config import KEYBINDINGS_PATH
from gochan.key import Keys, parse_key

KEY_BINDINGS = {
    "global": {
        "exit": Keys.Ctrl.C,
        "bbsmenu_view": Keys.N1,
        "board_view": Keys.N2,
        "thread_view": Keys.N3,
        "favorites_view": Keys.N4,
        "ng_view": Keys.N5,
        "help": Keys.Ctrl.H
    },
    "bbsmenu": {
        "select_up": Keys.UP,
        "select_down": Keys.DOWN,
        "page_up": Keys.PAGE_UP,
        "page_down": Keys.PAGE_DOWN,
        "select_top": Keys.Ctrl.HOME,
        "select_bottom": Keys.Ctrl.END,
        "select": Keys.ENTER,
    },
    "board": {
        "select_up": Keys.UP,
        "select_down": Keys.DOWN,
        "page_up": Keys.PAGE_UP,
        "page_down": Keys.PAGE_DOWN,
        "select_top": Keys.Ctrl.HOME,
        "select_bottom": Keys.Ctrl.END,
        "select": Keys.ENTER,
        "num_sort": Keys.Q,
        "num_des_sort": Keys.Shift.Q,
        "title_sort": Keys.W,
        "title_des_sort": Keys.Shift.W,
        "count_sort": Keys.E,
        "count_des_sort": Keys.Shift.E,
        "active_sort": Keys.R,
        "speed_sort": Keys.T,
        "speed_des_sort": Keys.Shift.T,
        "find": Keys.Ctrl.F,
        "ng_title": Keys.N,
        "update": Keys.U,
        "back": Keys.B,
        "favorite": Keys.F
    },
    "thread": {
        "scroll_up": Keys.UP,
        "scroll_down": Keys.DOWN,
        "page_up": Keys.PAGE_UP,
        "page_down": Keys.PAGE_DOWN,
        "go_to_top": Keys.Ctrl.HOME,
        "go_to_bottom": Keys.Ctrl.END,
        "open_link": Keys.O,
        "show_image": Keys.S,
        "go_to": Keys.G,
        "ng_name": Keys.N,
        "ng_id": Keys.I,
        "ng_word": Keys.W,
        "update": Keys.U,
        "back": Keys.B,
        "favorite": Keys.F,
        "extract_id": Keys.E,
        "show_replies": Keys.R,
        "show_response": Keys.Shift.R,
        "close_popup": Keys.Q
    },
    "ng": {
        "delete": Keys.D,
        "edit": Keys.E
    }
}

if KEYBINDINGS_PATH.is_file():
    keybindings = json.loads(KEYBINDINGS_PATH.read_text())

    if "global" in keybindings:
        if "exit" in keybindings["global"]:
            KEY_BINDINGS["global"]["exit"] = parse_key(keybindings["global"]["exit"])
        if "bbsmenu_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["bbsmenu_view"] = parse_key(keybindings["global"]["bbsmenu_view"])
        if "board_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["board_view"] = parse_key(keybindings["global"]["board_view"])
        if "thread_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["thread_view"] = parse_key(keybindings["global"]["thread_view"])
        if "ng_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["ng_view"] = parse_key(keybindings["global"]["ng_view"])
        if "favorites_view" in keybindings["global"]:
            KEY_BINDINGS["global"]["favorites_view"] = parse_key(keybindings["global"]["favorites_view"])
        if "help" in keybindings["global"]:
            KEY_BINDINGS["global"]["help"] = parse_key(keybindings["global"]["help"])

    if "bbsmenu" in keybindings:
        if "select_up" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_up"] = parse_key(keybindings["bbsmenu"]["select_up"])
        if "select_down" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_down"] = parse_key(keybindings["bbsmenu"]["select_down"])
        if "page_up" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["page_up"] = parse_key(keybindings["bbsmenu"]["page_up"])
        if "page_down" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["page_down"] = parse_key(keybindings["bbsmenu"]["page_down"])
        if "select_top" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_top"] = parse_key(keybindings["bbsmenu"]["select_top"])
        if "select_bottom" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select_bottom"] = parse_key(keybindings["bbsmenu"]["select_bottom"])
        if "select" in keybindings["bbsmenu"]:
            KEY_BINDINGS["bbsmenu"]["select"] = parse_key(keybindings["bbsmenu"]["select"])

    if "board" in keybindings:
        if "select_up" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_up"] = parse_key(keybindings["board"]["select_up"])
        if "select_down" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_down"] = parse_key(keybindings["board"]["select_down"])
        if "page_up" in keybindings["board"]:
            KEY_BINDINGS["board"]["page_up"] = parse_key(keybindings["board"]["page_up"])
        if "page_down" in keybindings["board"]:
            KEY_BINDINGS["board"]["page_down"] = parse_key(keybindings["board"]["page_down"])
        if "select_top" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_top"] = parse_key(keybindings["board"]["select_top"])
        if "select_bottom" in keybindings["board"]:
            KEY_BINDINGS["board"]["select_bottom"] = parse_key(keybindings["board"]["select_bottom"])
        if "select" in keybindings["board"]:
            KEY_BINDINGS["board"]["select"] = parse_key(keybindings["board"]["select"])
        if "num_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["num_sort"] = parse_key(keybindings["board"]["num_sort"])
        if "num_des_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["num_des_sort"] = parse_key(keybindings["board"]["num_des_sort"])
        if "title_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["title_sort"] = parse_key(keybindings["board"]["title_sort"])
        if "title_des_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["title_des_sort"] = parse_key(keybindings["board"]["title_des_sort"])
        if "count_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["count_sort"] = parse_key(keybindings["board"]["count_sort"])
        if "count_des_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["count_des_sort"] = parse_key(keybindings["board"]["count_des_sort"])
        if "active_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["unread_sort"] = parse_key(keybindings["board"]["unread_sort"])
        if "speed_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["speed_sort"] = parse_key(keybindings["board"]["speed_sort"])
        if "speed_des_sort" in keybindings["board"]:
            KEY_BINDINGS["board"]["speed_des_sort"] = parse_key(keybindings["board"]["speed_des_sort"])
        if "find" in keybindings["board"]:
            KEY_BINDINGS["board"]["find"] = parse_key(keybindings["board"]["find"])
        if "ng_title" in keybindings["board"]:
            KEY_BINDINGS["board"]["ng_title"] = parse_key(keybindings["board"]["ng_title"])
        if "update" in keybindings["board"]:
            KEY_BINDINGS["board"]["update"] = parse_key(keybindings["board"]["update"])
        if "back" in keybindings["board"]:
            KEY_BINDINGS["board"]["back"] = parse_key(keybindings["board"]["back"])
        if "favorite" in keybindings["board"]:
            KEY_BINDINGS["board"]["favorite"] = parse_key(keybindings["board"]["favorite"])

    if "thread" in keybindings:
        if "scroll_up" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["scroll_up"] = parse_key(keybindings["thread"]["scroll_up"])
        if "scroll_down" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["scroll_down"] = parse_key(keybindings["thread"]["scroll_down"])
        if "page_up" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["page_up"] = parse_key(keybindings["thread"]["page_up"])
        if "page_down" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["page_down"] = parse_key(keybindings["thread"]["page_down"])
        if "go_to_top" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["go_to_top"] = parse_key(keybindings["thread"]["go_to_top"])
        if "go_to_bottom" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["go_to_bottom"] = parse_key(keybindings["thread"]["go_to_bottom"])
        if "open_link" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["open_link"] = parse_key(keybindings["thread"]["open_link"])
        if "show_image" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["show_image"] = parse_key(keybindings["thread"]["show_image"])
        if "go_to" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["go_to"] = parse_key(keybindings["thread"]["go_to"])
        if "ng_name" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["ng_name"] = parse_key(keybindings["thread"]["ng_name"])
        if "ng_id" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["ng_id"] = parse_key(keybindings["thread"]["ng_id"])
        if "ng_word" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["ng_word"] = parse_key(keybindings["thread"]["ng_word"])
        if "update" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["updete"] = parse_key(keybindings["thread"]["update"])
        if "back" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["back"] = parse_key(keybindings["thread"]["back"])
        if "favorite" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["favorite"] = parse_key(keybindings["thread"]["favorite"])
        if "extract_id" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["extract_id"] = parse_key(keybindings["thread"]["extract_id"])
        if "show_replies" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["show_replies"] = parse_key(keybindings["thread"]["show_replies"])
        if "show_response" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["show_response"] = parse_key(keybindings["thread"]["show_response"])
        if "close_popup" in keybindings["thread"]:
            KEY_BINDINGS["thread"]["close_popup"] = parse_key(keybindings["thread"]["close_popup"])
