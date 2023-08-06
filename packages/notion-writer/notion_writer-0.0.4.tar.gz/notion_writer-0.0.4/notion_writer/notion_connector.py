__author__ = "Puri Phakmongkol"

"""
* Notion Writer Project
* Created date : 01/01/2021
*
* By Puri
*
+      o     +              o
    +             o     +       +
o          +
    o  +           +        +
+        o     o       +        o
-_-_-_-_-_-_-_,------,      o
_-_-_-_-_-_-_-|   /\_/\ 
-_-_-_-_-_-_-~|__( ^ .^)  +     +
_-_-_-_-_-_-_-""  "" 
+      o         o   +       o
    +         +
o      o  _-_-_-_- NotionConnector.py
    o           +
+      +     o        o      +
"""

import notion
from notion.client import NotionClient
from . import NotionPage

class NotionConnector :
    token = ''
    notion = None

    def __init__(self, token='') -> None:
        super().__init__()
        self.token = token
        self.notion = NotionClient(token_v2=self.token)

    def get_page(self, page_url='') :
        return NotionPage(self.notion, page_url)