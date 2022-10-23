_FIELD_SIDE = 9
"""Side of the field"""
_BLOCK_SIDE = 3
"""Side of the block"""
_NUMBER_MIN = 1
"""Minimal possible number"""
_NUMBER_MAX = _BLOCK_SIDE ** 2
"""Maximal possible number"""
_NUMBER_RANGE = range(_NUMBER_MIN, _NUMBER_MAX + 1)
"""Numbers' range"""
_NUMBER_STR_TEMPLATE = " {0} "
"""Template string for number representation"""
_NUMBER_STR_TEMPLATE_LEN = len(_NUMBER_STR_TEMPLATE) - 2
"""Length of the actual number representation"""
