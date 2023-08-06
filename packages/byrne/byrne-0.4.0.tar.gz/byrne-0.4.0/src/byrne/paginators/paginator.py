from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor


from ..table import Table
from ..constants import DEFAULT_PAGE


class Paginator(ABC):
    def __init__(
        self,
        table: Table,
        base_args: dict,
        page_length: int = DEFAULT_PAGE,
        preload=True
    ):
        self.table = table
        self._items = []
        self._eof = False
        self._executor = ThreadPoolExecutor()
        self._last_page = None
        self._last_key = None
        self._base_args = base_args
        self._page_length = page_length

        if preload:
            self.trigger_page()
            self.ingest_page()

    @property
    def should_page(self):
        return len(self._items) <= self._page_length

    @property
    def can_page(self):
        return self._last_page is None

    @property
    def next_call_args(self):
        if self._last_key is None:
            return self._base_args
        args = {"start": self._last_key}
        args.update(self._base_args)
        return args

    @property
    def new_page_ready(self):
        return self._page is not None and self._page.done

    @property
    def need_to_wait_for_page(self):
        return len(self._items) == 0

    @abstractmethod
    def on_page(self):
        raise NotImplementedError

    def trigger_page(self):
        self._page = self._executor.submit(lambda: self.on_page())

    def ingest_page(self):
        result = self._page.result()
        self._page = None

        if "LastEvaluatedKey" in result:
            self._last_key = result["LastEvaluatedKey"]
        else:
            self._last_key = None
            self._eof = True

        new_items = result["Items"]
        new_items.reverse()

        self._items = new_items + self._items

    def __iter__(self):
        while (not self._eof) or len(self._items) > 0:
            if not self._eof and self.should_page and self.can_page:
                self.trigger_page()

            if self.new_page_ready or self.need_to_wait_for_page:
                self.ingest_page()

            yield self._items.pop()
