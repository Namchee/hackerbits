from datetime import datetime
from typing import List

class News:
    def __init__(self, authors: List[str], title: str, published_at: datetime, contents: str) -> None:
        self.authors = authors
        self.title = title
        self.contents = contents

        if published_at is not None:
            self.published_at = published_at.isoformat()