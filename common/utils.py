# dump to file
def dump(text, filename):
    with open(filename, "w") as f:
        f.write(text)


# read from file
def read_file(filepath):
    cont = None
    with open(filepath) as f:
        cont = f.read()
    return cont
