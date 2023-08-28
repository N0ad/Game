import subjects as sbj
import objects as obj

class Cell():
    def __init__(self, name, passability, texture):
        self.name = name
        self.passability = passability
        self.texture = texture
        self.subject = None
        self.object = None
        self.res_texture = texture
        self.changed = True

    def add_subject(self, subject):
        self.subject = subject
        self.res_texture
        self.changed = True

    def add_subject(self, oobject):
        self.oobject = oobject
        self.res_texture
        self.changed = True

    def del_subject(self, subject):
        self.subject = None
        self.res_texture = self.texture
        self.changed = True

    def del_subject(self, oobject):
        self.oobject = None
        self.res_texture = self.texture
        self.changed = True