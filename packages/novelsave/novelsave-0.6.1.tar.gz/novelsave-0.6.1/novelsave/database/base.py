from pathlib import Path
from typing import Tuple

from tinydb import TinyDB

from .tables import KeyValueTable, SingleClassTable, MultiClassExternalTable, MultiClassDecoupledTable, \
    SetTable
from ..models import Novel, Chapter


class Database:
    def __init__(self, directory):
        self.db, self.path = self.open_db(directory)

    def open_db(self, directory) -> Tuple[TinyDB, Path]:
        path = directory / Path('data') / Path('meta.db')
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists() and not path.is_file():
            with path.open('w'):
                pass

        return TinyDB(path), path


class NovelData(Database):
    def __init__(self, directory):
        super(NovelData, self).__init__(directory)

        self.novel = SingleClassTable(self.db, 'novel', Novel,
                                      ['title', 'author', 'synopsis', 'thumbnail', 'lang', 'meta_source', 'url'])
        self.metadata = SetTable(self.db, 'metadata', field1='name', field2='value')
        self.pending = MultiClassDecoupledTable(self.db, self.path.parent, 'pending', Chapter, ['index', 'volume', 'url'], 'url')
        self.chapters = MultiClassExternalTable(
            self.db, self.path.parent, 'chapters',
            Chapter, ['index', 'title', 'paragraphs', 'volume', 'url'], 'url',
            naming_scheme=lambda c: str(c.index).zfill(4),
        )
        self.misc = KeyValueTable(self.db, 'misc')
