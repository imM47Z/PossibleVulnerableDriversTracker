class Driver:
    def __init__(self, path, name):
        self.name = name
        self.path = path[:1] if path[len(path) - 1:] == "\\" else path
        
        file = open("{}\\{}".format(path, name), "r", encoding="ANSI")
        self.content = file.read()
        file.close()

        self.severity = 0
        self.haveDevice = "IoCreateDevice" in self.content
    def IncreaseSeverity(self, i):
        self.severity += i
