
class TxtOperations:

    def __init__(self):
        None
    def write_txt(self, filename, info):
        file = open(filename, "w")
        for line in info:
            file.write(line)
            file.write("\n")
        file.close()





