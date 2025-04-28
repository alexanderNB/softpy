from typing import Literal, TypedDict
from typing_extensions import NotRequired

class ExclusivelyAlignRule(TypedDict):
	align_rule: Literal[True] | str

class HasAlignChar(TypedDict):
	align_rule: NotRequired[Literal[True] | str]
	align_char: str
	align_char_index: NotRequired[int]
  
CystomAlignType = ExclusivelyAlignRule | HasAlignChar

def display(*args, big:bool = True, end:str="", aligned:bool|CystomAlignType=False) -> None: ...