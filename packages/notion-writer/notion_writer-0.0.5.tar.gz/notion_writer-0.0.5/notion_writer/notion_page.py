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
o      o  _-_-_-_- NotionPage.py
    o           +
+      +     o        o      +
"""

import notion

class NotionPage :
    notion = None
    notion_page = None
    _page_id = ''
    _page_title = ''
    _page_url = ''

    def __init__(self, notion_connector, page_url:str) :
        super().__init__()
        self.notion = notion_connector
        self._page_url = page_url
        self.notion_page = self.notion.get_block(page_url)
        self._page_url = self.notion_page.get_browseable_url()
        self._page_title = self.notion_page.title
        self._page_id = self.notion_page.id

    def refresh(self) :
        self.notion_page = self.notion.get_block(self._page_url)
        self._page_title = self.notion_page.title
        self._page_id = self.notion_page.id

    def get_title(self) :
        return self._page_title

    def get_notion_page(self) :
        return self.notion_page

    def set_title(self, title) :
        self.notion_page.title = title

    def add_text(self, text) :
        self.notion_page.children.add_new(notion.block.TextBlock, title=text)

    def add_todo(self, text) :
        self.notion_page.children.add_new(notion.block.TodoBlock, title=text)

    def add_bullet(self, text) : 
        self.notion_page.children.add_new(notion.block.BulletedListBlock, title=text)

    def add_image_from_filepath(self, file_path) :
        temp = self.notion_page.children.add_new(notion.block.ImageBlock)
        temp.upload_file(file_path)

    def add_image_from_plt(self, plt_object) :
        plt_object.savefig('temp_plt_object.png', format='png')
        temp = self.notion_page.children.add_new(notion.block.ImageBlock)
        temp.upload_file('temp_plt_object.png')

    def add_page(self, page_title) :
        temp = self.notion_page.children.add_new(notion.block.PageBlock, title=page_title)
        return NotionPage(self.notion, temp.get_browseable_url())

    def add_table(self, table_title, schema) :
        revise_schema = {'title' : {
            'name' : 'title', 'type' : 'title'
        }}
        for _ in schema :
            revise_schema[_['name']] = _

        temp = self.notion_page.children.add_new(notion.block.CollectionViewBlock)
        temp.collection = self.notion.get_collection(
            self.notion.create_record("collection", parent=temp, schema=revise_schema)
        )
        temp.title = table_title
        temp.views.add_new(view_type="table")

    def get_table(self, table_title, select_first = False) :
        all_children = self.notion_page.children
        all_with_select = [ _ for _ in all_children if isinstance(_, notion.block.CollectionViewBlock) ]
        all_with_text = [ _ for _ in all_with_select if table_title in _.title]
        if len(all_with_text) > 1 :
            if select_first :
                all_with_text = [all_with_text[0]]
            else :  
                # print(all_with_text)
                print('All text : %s'%([ _.title for _ in all_with_text ]))
                raise ValueError('input text is ambigious !')

        elif len(all_with_text) == 0 :
            raise ValueError('input text is not found !')

        selected = all_with_text[0]
        return NotionTable(self.notion, selected)

    def get_page(self, page_title, select_first = False) :
        all_children = self.notion_page.children
        all_with_select = [ _ for _ in all_children if isinstance(_, notion.block.PageBlock) ]
        all_with_text = [ _ for _ in all_with_select if page_title in _.title]
        if len(all_with_text) > 1 :
            if select_first :
                all_with_text = [all_with_text[0]]
            else :  
                # print(all_with_text)
                print('All text : %s'%([ _.title for _ in all_with_text ]))
                raise ValueError('input text is ambigious !')

        elif len(all_with_text) == 0 :
            raise ValueError('input text is not found !')

        selected = all_with_text[0]
        return NotionPage(self.notion, selected.get_browseable_url())

    def with_text(self, within_text, select_first = False, select_type='all') :
        all_children = self.notion_page.children
        if select_type == 'all' :
            all_with_select = [ _ for _ in all_children if isinstance(_, notion.block.TextBlock) or isinstance(_, notion.block.TodoBlock) or isinstance(_, notion.block.BulletedListBlock)]

        elif select_type == 'text' :
            all_with_select = [ _ for _ in all_children if isinstance(_, notion.block.TextBlock) ]

        elif select_type == 'todo' :
            all_with_select = [ _ for _ in all_children if isinstance(_, notion.block.TodoBlock) ]

        elif select_type == 'bullet' :
            all_with_select = [ _ for _ in all_children if isinstance(_, notion.block.BulletedListBlock) ]

        else :
            raise ValueError('select_type is invalid !')

        all_with_text = [ _ for _ in all_with_select if within_text in _.title]
        if len(all_with_text) > 1 :
            if select_first :
                all_with_text = [all_with_text[0]]
            else :  
                # print(all_with_text)
                print('All text : %s'%([ _.title for _ in all_with_text ]))
                raise ValueError('input text is ambigious !')

        elif len(all_with_text) == 0 :
            raise ValueError('input text is not found !')

        selected = all_with_text[0]
        if isinstance(selected, notion.block.TextBlock) :
            return NotionText(selected)

        elif isinstance(selected, notion.block.TodoBlock) :
            return NotionTodo(selected)

        elif isinstance(selected, notion.block.BulletedListBlock) :
            return NotionBullet(selected)

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