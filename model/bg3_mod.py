# bg3_mod.py

class Mod:
    def __init__(self, uuid, name, author, folder, prgoressions=None):
        self.uuid = uuid
        self.name = name
        self.author = author
        self.folder = folder
        self.progressions = prgoressions if prgoressions else []
