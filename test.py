import random
import time
import pyxel

class App:
    def __init__(self):

        self.max_rat = 4 # Nombre maximum de rats qui peuvent apparaitre sur la map
        self.liste_rat_map = [] # Liste des rats sur la map

        self.group_rat = GroupeRat()

        pyxel.init(200, 200, title="Hello Pyxel", fps=60, display_scale=2)
        pyxel.load("test.pyxres")
        pyxel.run(self.update, self.draw)

    
    def update(self):
        self.group_rat.update()
        # randint(0,50) == 0 permet de faire apparaitre un rat sur la map avec une probabilité de 1/50
        if random.randint(0,50) == 0 and len(self.liste_rat_map) < self.max_rat:
            self.liste_rat_map.append(Rat(random.randint(0,pyxel.width-8), 2, is_player=False, size=3.0, independant=True, vitesse=3)) # Les rats apparaitront en haut de l'écran
        for rat in self.liste_rat_map:
            rat.mouvement()
            if rat.getDistance(self.group_rat.joueur.getX(), self.group_rat.joueur.getY()) < 20:
                self.group_rat.ajout_rat(rat)
                self.liste_rat_map.remove(rat)

    def draw(self):
        pyxel.cls(0)
        self.group_rat.draw()
        for rat in self.liste_rat_map:
            rat.draw()

class Rat:
    def __init__(self, x=50, y=50, is_player=False, size = 1.0, independant = False, vitesse = 3):
        self.x = x
        self.y = y
        self.img = 0
        self.sprite = (8,0,8,8)
        self.size = size
        self.is_player = is_player
        self.degre = 0 # direction
        self.angle = 4 # pour l'animation
        self.vitesse = vitesse
        self.independant = independant

    def mouvement(self):
        if self.is_player:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x = min(pyxel.width-8, self.x + self.vitesse)
                self.degre = min(50, self.degre + self.angle)
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x = max(0, self.x - self.vitesse)
                self.degre = max(-50, self.degre - self.angle)
            if pyxel.btn(pyxel.KEY_DOWN):
                self.y = min(pyxel.height-8, self.y + self.vitesse)
            if pyxel.btn(pyxel.KEY_UP):
                self.y = max(0, self.y- self.vitesse)
        else:
            if self.independant:
                if random.randint(0,30) == 0:    
                    self.x = min(pyxel.width-8, self.x + self.vitesse) if random.randint(0,1) == 0 else max(0, self.x - self.vitesse)
                    self.degre = min(50, self.degre + self.angle) if random.randint(0,1) == 0 else max(-50, self.degre - self.angle)
                    self.y = min(pyxel.height-8, self.y + self.vitesse) if random.randint(0,1) == 0 else max(0, self.y - self.vitesse)
        self.recadrage()
    
    def recadrage(self): #recadre continuellement langle vers 0°
        # if self.is_player:
        if self.degre < 0 and not pyxel.btn(pyxel.KEY_LEFT):
            self.degre += self.angle-self.angle/2
            self.x = min(pyxel.width-8, self.x + self.vitesse/2)
        elif self.degre > 0 and not pyxel.btn(pyxel.KEY_RIGHT):
            self.degre -= self.angle-self.angle/2
            self.x = max(0, self.x - self.vitesse/2)

    def getDistance(self,x,y):
        return ((self.x-x)**2 + (self.y-y)**2)**0.5
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getMetadata(self):
        return self.img, self.sprite
    
    def getDirection(self):
        return self.degre

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], 0, self.degre, self.size)

    def update(self):
        self.mouvement()

class GroupeRat:
    def __init__(self, x=50, y=50, liste_rat=[]):
        self.joueur = Rat(50, 50, True, 3.0) # Le joueur
        self.liste_rats = liste_rat
        self.evitement = 20
        self.cohesion = 50
        # Rat(20+i*5,25+i*15) for i in range(5)

    def draw(self):
        self.joueur.draw()
        for rat in self.liste_rats:
            rat.draw()

    def update(self):
        self.joueur.update()
        for rat in self.liste_rats:
            rat.update()

    def ajout_rat(self, rat):
        self.liste_rats.append(rat)

    def boids(self):
        for rat in self.liste_rats:
            for rat2 in self.liste_rats:
                if rat != rat2:
                    if rat.getDistance(rat2.getX(), rat2.getY()) < self.evitement:
                        pass

App()