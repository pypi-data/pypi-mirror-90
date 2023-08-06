from typing import Optional, Union, List

from valid_flow_engine.op_set_registry import register_op_set, as_op


@register_op_set
class StingOpSet:
    @staticmethod
    @as_op(display='String Contains', help_text='This string is in that string')
    def contains(this: str, in_that: str) -> bool:
        return this in in_that
    
    @staticmethod
    @as_op(display='To Tile Case', help_text='Put string to title case (ex: "some title" => "Some Title"')
    def title_case(string: str) -> str:
        return string.title()
    
    @staticmethod
    @as_op
    def split_string(split: str, by: str) -> List[str]:
        return split.split(by)
    
    @staticmethod
    @as_op(display='All Caps', help_text="String to All Caps (ex: 'some string' => 'SOME STRING'")
    def all_caps(string: str) -> str:
        return string.upper()
    
    @staticmethod
    @as_op(display="All Lower", help_text="String to All Lower Case (ex: 'Some String' => 'some string")
    def lower(string: str) -> str:
        return string.lower()
