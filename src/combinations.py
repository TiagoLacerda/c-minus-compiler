
def combinations(letters: list[str], length: int):
    """
    Returns all [length]-sized combinations of [letters].
    """
    if length < 1:
        return []
        
    strings = []
    for index in range(len(letters) ** length):
        string = [" " for i in range(length)]
        for index_in_string in range(length):
            index_in_letters = int(index / (len(letters) ** index_in_string)) % len(letters)
            string[index_in_string] = letters[index_in_letters]
        strings.append("".join(string))

    return strings
