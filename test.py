import pyxel

class App:
    def __init__(self):
        self.test = 3

        # self.rat1 = Rat()
        self.groupe_rat = OrdreRat()

        pyxel.init(200, 200, title="Hello Pyxel", fps=60, display_scale=2)
        pyxel.load("test.pyxres")
        pyxel.run(self.update, self.draw)

    
    def update(self):
        pass
        # self.rat1.update()
        self.groupe_rat.update()

    def draw(self):
        pyxel.cls(0)
        # self.rat1.draw()
        self.groupe_rat.draw()

class Rat:
    def __init__(self, x=50, y=50):
        self.x = x
        self.y = y
        self.img = 0
        self.sprite = (8,0,8,8)

    def mouvement(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 3
            self.x = self.x % pyxel.width
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 3
            self.x = self.x % pyxel.width
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 3
            self.y = self.y % pyxel.height
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 3
            self.y = self.y % pyxel.height

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getMetadata(self):
        return self.img, self.sprite

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3])

    def update(self):
        self.mouvement()
    

class OrdreRat:
    def __init__(self):
        self.liste_rats = [Rat(20+i*5,25+i*5) for i in range(5)]

    def draw(self):
        for rat in self.liste_rats:
            rat.draw()

    def update(self):
        for rat in self.liste_rats:
            rat.update()

App()