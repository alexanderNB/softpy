from sympy import latex
from typing import Literal, TypedDict
from typing_extensions import NotRequired


class ExclusivelyAlignRule(TypedDict):
	align_rule: Literal[True] | str
  
class HasAlignChar(TypedDict):
	align_rule: NotRequired[Literal[True] | str]
	align_char: str
	align_char_index: NotRequired[int]
  
CystomAlignType = ExclusivelyAlignRule | HasAlignChar
  

def display(*args, big=True, end:str="", aligned:bool|CystomAlignType=False):
	print(">beginLaTeX<" + (">BiG<\n" if big else "") + text_to_latex(*args, end=end, aligned=aligned) + ("\n" if big else "") + ">endLaTeX<", end="")

def text_to_latex(*args, end : str, aligned : CystomAlignType|bool) -> str:
	output = ""
	align_char = None
	align_char_index = 0
	if isinstance(aligned, bool):
		align_rule = "align" if aligned else None
	else:
		align_rule = "align" if "align_rule" not in aligned or aligned["align_rule"] == True else aligned["align_rule"]
		if "align_char" in aligned: align_char = aligned["align_char"]
		if "align_char_index" in aligned: align_char_index = aligned["align_char_index"]
	if align_rule:
		output += f"\\begin{{{align_rule}}}\n"
		end = " \\\\" + end
	for part in args:
		part_output = part if isinstance(part, str) else latex(part)
		index = -1
		i = align_char_index
		while align_char and i >= 0:
			index = part_output.find(align_char, max(index, 0))
			i -= 1
		if index != -1:
			part_output = part_output[0:index] + "&" + part_output[index:]
		if not isinstance(part, str):
			output += part_output + end
			continue
		
		part = part_output.split("$")
		part_output = ""
		for i in range(len(part)):
			partI = part[i]
			if(i%2 == 0):
				partI = partI.split("&")
				while partI: 
					partI_pop = partI.pop(0)
					part_output += (f"\\text{{{partI_pop}}}" if partI_pop else "") + ("&" if partI else "")	
			else:
				part_output +=partI
		output += part_output + end
  
	if align_rule:
		output += f"\\end{{{align_rule}}}"
	return output