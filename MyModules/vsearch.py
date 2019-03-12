def search4vowels(phrase:str) -> set:
	""" Return any vowels found in a supplied phrase """
	vowels = set('aeiou')
	return vowels.intersection(set(phrase))

def search4letters(phrase:str, letters:str) -> set:
	""" Return as set of the leters found in phrase"""
	return set(letters).intersection(set(phrase))


