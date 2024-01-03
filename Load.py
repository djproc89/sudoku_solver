def Load(file):
    """Loading a file which contains unsolved sudoku

    Args:
        file (_str_): File name 

    Returns:
        _list_: If file is loaded properly, function returns list with numbers
        _bool_: False if file contains errors or file doesn't exists
    """
    try:
        f = open(file, 'r')
        lines = f.readlines()
    except:
        print(f"File {file} not found!")
        return False
    
    t = []
    
    # read file line by line
    for line in lines:
        t.append([])
        for c in line:
            if c == "*":
                t[-1].append(0)
            elif c == "\n":
                pass
            elif c.isalnum:
                t[-1].append(int(c))
        if len(t[-1]) != 9:
            return False
    if len(t) != 9:
        return False
    return t