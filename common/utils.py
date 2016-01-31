# dump to file
def dump(text, filepath):
    '''
    Dump text to file with given path.
    :param text: the content to be dumped to file.
    :param filepath: the path of the file
    :return: None
    '''
    with open(filepath, "w") as f:
        f.write(text)


# read from file
def read_file(filepath):
    '''
    Read from file.
    :param filepath: the file path of the file
    :return: content of the file
    '''
    cont = None
    with open(filepath) as f:
        cont = f.read()
    return cont
