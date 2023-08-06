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
from . import NotionPage


class NotionBlock :
    notion_object = None
    notion_object_id = None
    def __init__(self, notion_object) :
        self.notion_object = notion_object
        self.notion_object_id = notion_object.id

    def get_notion_object(self) :
        return self.notion_object

    def get_id(self) :
        return self.notion_object_id

class NotionText(NotionBlock) :
    def __init__(self, notion_object) :
        self.notion_object = notion_object

    def get_text(self) :
        return self.notion_object.title

    def set_text(self, input_text: str) :
        self.notion_object.title = input_text

class NotionTodo(NotionText) :
    def __init__(self, notion_object) :
        super().__init__(notion_object)

    def get_check_status(self) :
        if self.notion_object.checked :
            return 'checked'
        else :
            return 'unchecked'

    def check(self) :
        self.notion_object.checked = True

    def uncheck(self) :
        self.notion_object.checked = False

class NotionBullet(NotionText) :
    def __init__(self, notion_object) :
        super().__init__(notion_object)

    def get_children(self) :
        return self.notion_object.children

    def add_bullet(self, text) :
        self.notion_object.children.add_new(notion.block.BulletedListBlock, title=text)

    def with_text(self, within_text, select_first = False) :
        all_children = self.notion_object.children
        all_with_select = [ _ for _ in all_children if isinstance(_, notion.block.BulletedListBlock) ]
        all_with_text = [ _ for _ in all_with_select if within_text in _.title]
        if len(all_with_text) > 1 :
            if select_first :
                all_with_text = [all_with_text[0]]
            else :  
                print('All text : %s'%([ _.title for _ in all_with_text ]))
                raise ValueError('input text is ambigious !')

        elif len(all_with_text) == 0 :
            raise ValueError('input text is not found !')

        selected = all_with_text[0]
        return NotionBullet(selected)   

class NotionTable(NotionBlock) :
    notion = None
    def __init__(self, notion, notion_object) :
        self.notion_object = notion_object
        self.notion = notion

    def get_title(self) :
        return self.notion_object.title

    def set_title(self, input_text: str) :
        self.notion_object.title = input_text

    def get_schema(self) :
        return self.notion_object.collection.get_schema_properties()

    def add_row(self, **kwags) :
        self.notion_object.collection.add_row(**kwags)

    def get_row_inside(self, row_title, select_first = False) :
        all_children = self.notion_object.collection.get_rows()
        all_with_select = [ _ for _ in all_children if isinstance(_, notion.collection.CollectionRowBlock) ]
        all_with_text = [ _ for _ in all_with_select if row_title in _.title]
        if len(all_with_text) > 1 :
            if select_first :
                all_with_text = [all_with_text[0]]
            else :  
                print('All text : %s'%([ _.title for _ in all_with_text ]))
                raise ValueError('input text is ambigious !')

        elif len(all_with_text) == 0 :
            raise ValueError('input text is not found !')

        selected = all_with_text[0]
        return NotionPage(self.notion, selected.get_browseable_url())

    def get_row_value(self, row_title, select_first = False) :
        all_children = self.notion_object.collection.get_rows()
        all_with_select = [ _ for _ in all_children if isinstance(_, notion.collection.CollectionRowBlock) ]
        all_with_text = [ _ for _ in all_with_select if row_title in _.title]
        if len(all_with_text) > 1 :
            if select_first :
                all_with_text = [all_with_text[0]]
            else :  
                print('All text : %s'%([ _.title for _ in all_with_text ]))
                raise ValueError('input text is ambigious !')

        elif len(all_with_text) == 0 :
            raise ValueError('input text is not found !')

        selected = all_with_text[0]
        return selected.get_all_properties()