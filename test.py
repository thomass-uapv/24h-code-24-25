import random
import time
import pyxel

class App:
    def __init__(self):

        self.max_rat = 4 # Nombre maximum de rats qui peuvent apparaitre sur la map
        self.liste_rat_map = [] # Liste des rats sur la map
        self.joueur = Rat(is_player=True) # Le joueur

        pyxel.init(200, 200, title="Hello Pyxel", fps=60, display_scale=2)
        pyxel.load("test.pyxres")
        pyxel.run(self.update, self.draw)

    
    def update(self):
        self.joueur.update()
        # randint(0,50) == 0 permet de faire apparaitre un rat sur la map avec une probabilité de 1/50
        if random.randint(0,50) == 0 and len(self.liste_rat_map) < self.max_rat:
            self.liste_rat_map.append(Rat(random.randint(0,pyxel.width),2)) # Les rats apparaitront en haut de l'écran

    def draw(self):
        pyxel.cls(0)
        self.joueur.draw()
        for rat in self.liste_rat_map:
            rat.draw()

class Rat:
    def __init__(self, x=50, y=50, is_player=False):
        self.x = x
        self.y = y
        self.img = 0
        self.sprite = (8,0,8,8)
        self.is_player = is_player

    def mouvement(self):
        if self.is_player:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x += 3
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x -= 3
            if pyxel.btn(pyxel.KEY_UP):
                self.y -= 3
            if pyxel.btn(pyxel.KEY_DOWN):
                self.y += 3
        else:
            pass
        self.blocage()

    def blocage(self):
        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width:
            self.x = pyxel.width-8
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height:
            self.y = pyxel.height-8

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
    def __init__(self, x=50, y=50):
        self.joueur = Rat(x,y)
        self.liste_rats = []
        # Rat(20+i*5,25+i*15) for i in range(5)

    def draw(self):
        self.joueur.draw()
        for rat in self.liste_rats:
            rat.draw()

    def update(self):
        self.joueur.update()
        for rat in self.liste_rats:
            rat.update()

    def ajout_rat(self):
        self.liste_rats.append(Rat())

App()