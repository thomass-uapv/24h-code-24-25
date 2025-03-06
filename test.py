import pyxel

class App:
    def __init__(self):
        self.rat1 = Rat()

        pyxel.init(200, 200, title="Hello Pyxel", fps=60, display_scale=2)
        pyxel.load("test.pyxres")
        pyxel.run(self.update, self.draw)

    
    def update(self):
        self.rat1.mouvement()

    def draw(self):
        pyxel.cls(0)
        # Récupérer les coordonnées du rat
        rat_x = self.rat1.getX()
        rat_y = self.rat1.getY()
        rat_metadata = self.rat1.getMetadata()
        pyxel.blt(rat_x, rat_y, rat_metadata[0], rat_metadata[1][0], rat_metadata[1][1], rat_metadata[1][2], rat_metadata[1][3])

class Rat:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.img = 0
        self.sprite = (8,0,8,8)

    def mouvement(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 3
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 3
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 3
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 3

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getMetadata(self):
        return self.img, self.sprite

App()