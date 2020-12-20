from typing import Dict
from json import dumps

class News:
    def __init__(self, authors, title, published_at, contents) -> None:
        self.authors = authors
        self.title = title
        self.contents = contents

        if published_at is not None:
            self.published_at = published_at.isoformat()
    
    def toJson(self) -> Dict:
        return dumps(self, default=lambda o: o.__dict__)
