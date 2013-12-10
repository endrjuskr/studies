__author__ = 'andrzejskrodzki'

from ItemBase import ItemBase


class NoInitItem(ItemBase):
    def __init__(self, ident, no_line, pos):
        super(NoInitItem, self).__init__(ident, no_line, pos, "noinititem")