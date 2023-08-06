from typing import List, Optional

from gochan.event_handler import PropertyChangedEventArgs, PropertyChangedEventHandler
from gochan.models.app_context import AppContext
from gochan.models.bbsmenu import Category


class BbsmenuVM:
    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context
        self._bbsmenu = app_context.bbsmenu
        self.selected_category: Optional[Category] = None
        self.on_property_changed = PropertyChangedEventHandler()

        self._app_context.on_property_changed.add(self._app_context_changed)

    @property
    def categories(self) -> Optional[List[Category]]:
        return self._bbsmenu.categories if self._bbsmenu is not None else None

    def select_category(self, idx: int):
        if self._bbsmenu is not None and idx < len(self._bbsmenu.categories)\
                and idx >= 0:
            self.selected_category = self._bbsmenu.categories[idx]
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "selected_category"))

    def select_board(self, idx: int):
        if self.selected_category is not None and idx < len(self.selected_category.boards) and idx >= 0:
            self._app_context.set_board(
                self.selected_category.boards[idx].server, self.selected_category.boards[idx].board)

    def update(self):
        if self._bbsmenu is not None:
            self._bbsmenu.update()

    def _app_context_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "bbsmenu":
            if self._bbsmenu is not None:
                self._bbsmenu.on_property_changed.remove(self._bbsmenu_changed)

            self._bbsmenu = self._app_context.bbsmenu
            self._bbsmenu.on_property_changed.add(self._bbsmenu_changed)

            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "categories"))

    def _bbsmenu_changed(self, e: PropertyChangedEventArgs):
        if e.property_name == "categories":
            self.on_property_changed.invoke(PropertyChangedEventArgs(self, "categories"))
