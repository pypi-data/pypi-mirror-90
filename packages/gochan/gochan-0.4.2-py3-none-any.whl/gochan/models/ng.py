from enum import Enum
import json
import re
from typing import List, Optional

from gochan.event_handler import CollectionChangedEventArgs, CollectionChangedEventHandler, CollectionChangedEventKind
from gochan.models.board import ThreadHeader
from gochan.models.thread import Response, Thread


class BreakException(Exception):
    pass


class NGKind(Enum):
    NOT_NG = 0
    ABORN = 1
    HIDE = 2


class Aborn:
    """
    Represent a response that should be displayed as あぼーん
    """

    def __init__(self, origin: Response):
        super().__init__()
        self.origin = origin


class Hide:
    """
    Represent a response that should not be displayed
    """

    def __init__(self, origin: Response) -> None:
        super().__init__()
        self.origin = origin


class NGItem:
    def __init__(self, id: int, value: str, use_reg: bool):
        super().__init__()
        self.id = id
        self.value = value
        self.use_reg = use_reg

    def match(self, s) -> bool:
        if self.use_reg:
            return re.search(self.value, s) is not None
        else:
            return self.value in s


class NGName(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, hide: bool, auto_ng_id: bool,
                 board: Optional[str] = None, key: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.hide = hide
        self.auto_ng_id = auto_ng_id
        self.board = board
        self.key = key


class NGWord(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, hide: bool, auto_ng_id: bool,
                 board: Optional[str] = None, key: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.hide = hide
        self.auto_ng_id = auto_ng_id
        self.board = board
        self.key = key


class NGId(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, hide: bool,
                 board: Optional[str] = None, key: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.hide = hide
        self.board = board
        self.key = key


class NGTitle(NGItem):
    def __init__(self, id: int, value: str, use_reg: bool, board: Optional[str] = None):
        super().__init__(id, value, use_reg)
        self.board = board


class NG:
    def __init__(self):
        super().__init__()
        self._last_id = 0
        self.names: List[NGName] = []
        self.words: List[NGWord] = []
        self.ids: List[NGId] = []
        self.titles: List[NGTitle] = []
        self.on_collection_changed = CollectionChangedEventHandler()

    def add_ng_name(self, value: str, use_reg: bool, hide: bool, auto_ng_id: bool,
                    board: Optional[str] = None, key: Optional[str] = None):
        self._last_id += 1
        item = NGName(self._last_id, value, use_reg, hide, auto_ng_id, board, key)
        self.names.append(item)
        self.on_collection_changed.invoke(CollectionChangedEventArgs(
            self, "names", CollectionChangedEventKind.ADD, item))

    def add_ng_word(self, value: str, use_reg: bool, hide: bool, auto_ng_id: bool,
                    board: Optional[str] = None, key: Optional[str] = None):
        self._last_id += 1
        item = NGWord(self._last_id, value, use_reg, hide, auto_ng_id, board, key)
        self.words.append(item)
        self.on_collection_changed.invoke(CollectionChangedEventArgs(
            self, "words", CollectionChangedEventKind.ADD, item))

    def add_ng_id(self, value: str, use_reg: bool, hide: bool,
                  board: Optional[str] = None, key: Optional[str] = None):
        self._last_id += 1
        item = NGId(self._last_id, value, use_reg, hide, board, key)
        self.ids.append(item)
        self.on_collection_changed.invoke(CollectionChangedEventArgs(self, "ids", CollectionChangedEventKind.ADD, item))

    def add_ng_title(self, value: str, use_reg: bool, board: Optional[str] = None):
        self._last_id += 1
        item = NGTitle(self._last_id, value, use_reg, board)
        self.titles.append(item)
        self.on_collection_changed.invoke(CollectionChangedEventArgs(
            self, "titles", CollectionChangedEventKind.ADD, item))

    def update_ng(self, id: int, values):
        for item in self.names:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "hide" in values:
                    item.hide = values["hide"]
                if "auto_ng_id" in values:
                    item.auto_ng_id = values["auto_ng_id"]
                if "board" in values:
                    item.board = values["board"]
                if "key" in values:
                    item.key = values["key"]

                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "names", CollectionChangedEventKind.CHANGE, item))
                return

        for item in self.words:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "hide" in values:
                    item.hide = values["hide"]
                if "auto_ng_id" in values:
                    item.auto_ng_id = values["auto_ng_id"]
                if "board" in values:
                    item.board = values["board"]
                if "key" in values:
                    item.key = values["key"]

                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "words", CollectionChangedEventKind.CHANGE, item))
                return

        for item in self.ids:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "hide" in values:
                    item.hide = values["hide"]
                if "board" in values:
                    item.board = values["board"]
                if "key" in values:
                    item.key = values["key"]

                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "ids", CollectionChangedEventKind.CHANGE, item))
                return

        for item in self.titles:
            if id == item.id:
                if "value" in values:
                    item.value = values["value"]
                if "use_reg" in values:
                    item.use_reg = values["use_reg"]
                if "board" in values:
                    item.board = values["board"]

                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "titles", CollectionChangedEventKind.CHANGE, item))
                return

    def delete_ng(self, id: int):
        for n in self.names:
            if n.id == id:
                self.names.remove(n)
                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "names", CollectionChangedEventKind.DELETE, n))
                return

        for n in self.ids:
            if n.id == id:
                self.ids.remove(n)
                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "ids", CollectionChangedEventKind.DELETE, n))
                return

        for n in self.words:
            if n.id == id:
                self.words.remove(n)
                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "words", CollectionChangedEventKind.DELETE, n))
                return

        for n in self.titles:
            if n.id == id:
                self.titles.remove(n)
                self.on_collection_changed.invoke(CollectionChangedEventArgs(
                    self, "titles", CollectionChangedEventKind.DELETE, n))
                return

    def filter_threads(self, threads: List[ThreadHeader], board: str) -> List[ThreadHeader]:
        result = []

        for h in threads:
            try:
                for n in self.titles:
                    # Ignore ng when the response is out of ng's scope
                    if n.board is not None and n.board != board:
                        continue

                    if n.match(h.title):
                        raise BreakException()

                result.append(h)
            except BreakException:
                pass

        return result

    def is_ng_response(self, r: Response, board: Optional[str], key: Optional[str]) -> NGKind:
        for n in self.names + self.ids + self.words:
            # Ignore ng when the response is out of ng's scope
            if n.board is not None and n.board != board:
                continue

            if n.key is not None and n.key != key:
                continue

            if n.match(r.name):
                return (NGKind.HIDE if n.hide else NGKind.ABORN)

        for n in self.ids:
            # Ignore ng when the response is out of ng's scope
            if n.board is not None and n.board != board:
                continue

            if n.key is not None and n.key != key:
                continue

            if n.match(r.id):
                return (NGKind.HIDE if n.hide else NGKind.ABORN)

        for n in self.words:
            # Ignore ng when the response is out of ng's scope
            if n.board is not None and n.board != board:
                continue

            if n.key is not None and n.key != key:
                continue

            if n.match(r.message):
                return (NGKind.HIDE if n.hide else NGKind.ABORN)

        return NGKind.NOT_NG

    def serialize(self):
        names = []
        words = []
        ids = []
        titles = []

        for name in self.names:
            d = {}
            d["value"] = name.value
            d["use_reg"] = name.use_reg
            d["hide"] = name.hide
            d["auto_ng_id"] = name.auto_ng_id

            if name.board is not None:
                d["board"] = name.board

            if name.key is not None:
                d["key"] = name.key

            names.append(d)

        for word in self.words:
            d = {}
            d["value"] = word.value
            d["use_reg"] = word.use_reg
            d["hide"] = word.hide
            d["auto_ng_id"] = word.auto_ng_id

            if word.board is not None:
                d["board"] = word.board

            if word.key is not None:
                d["key"] = word.key

            words.append(d)

        for id in self.ids:
            d = {}
            d["value"] = id.value
            d["use_reg"] = id.use_reg
            d["hide"] = id.hide

            if id.board is not None:
                d["board"] = id.board

            if id.key is not None:
                d["key"] = id.key

            ids.append(d)

        for title in self.titles:
            d = {}
            d["value"] = title.value
            d["use_reg"] = title.use_reg

            if title.board is not None:
                d["board"] = title.board

            titles.append(d)

        obj = {}
        obj["names"] = names
        obj["words"] = words
        obj["ids"] = ids
        obj["titles"] = titles

        return json.dumps(obj, ensure_ascii=False, indent=2)

    def deserialize(self, s: str):
        d = json.loads(s)

        if "names" in d:
            for item in d["names"]:
                value = item["value"]
                use_reg = item["use_reg"]
                hide = item["hide"]
                auto_ng_id = item["auto_ng_id"]
                board = item.get("board")
                key = item.get("key")
                self.add_ng_name(value, use_reg, hide, auto_ng_id, board, key)

        if "words" in d:
            for item in d["words"]:
                value = item["value"]
                use_reg = item["use_reg"]
                hide = item["hide"]
                auto_ng_id = item["auto_ng_id"]
                board = item.get("board")
                key = item.get("key")
                self.add_ng_word(value, use_reg, hide, auto_ng_id, board, key)

        if "ids" in d:
            for item in d["ids"]:
                value = item["value"]
                use_reg = item["use_reg"]
                hide = item["hide"]
                board = item.get("board")
                key = item.get("key")
                self.add_ng_id(value, use_reg, hide, board, key)

        if "titles" in d:
            for item in d["titles"]:
                value = item["value"]
                use_reg = item["use_reg"]
                board = item.get("board")
                self.add_ng_title(value, use_reg, board)

    def _add_auto_ng_id(self, thread: Thread):
        for r in thread.responses:
            for n in self.names:
                # Ignore ng when the response is out of ng's scope
                if n.board is not None and n.board != thread.board:
                    continue
                if n.key is not None and n.key != thread.key:
                    continue

                if n.match(r.name) and n.auto_ng_id and r.id.startwith("ID:") and  \
                        r.id not in [x.value for x in self.ids]:
                    self._last_id += 1
                    self.ids.append(NGId(self._last_id, r.id, False, n.hide, n.board, n.key))

            for n in self.words:
                # Ignore ng when the response is out of ng's scope
                if n.board is not None and n.board != thread.board:
                    continue
                if n.key is not None and n.key != thread.key:
                    continue

                if n.match(r.message) and n.auto_ng_id and r.id.startswith("ID:") \
                        and r.id not in [x.value for x in self.ids]:
                    self._last_id += 1
                    self.ids.append(NGId(self._last_id, r.id, False, n.hide, n.board, n.key))
