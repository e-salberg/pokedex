class Pokemon:
    def __init__(self, name, types, description):
        self.name = name
        self.description = description
        self.type1 = types.pop(0)["type"]["name"]
        if types:
            self.type2 = types.pop(0)["type"]["name"]
        else:
            self.type2 = None

    
    def dex_entry(self):
        entry = self.name + " is a " + self.type1

        if self.type2:
            entry += " and " + self.type2

        entry += " type pokemon. " + self.description
        return entry