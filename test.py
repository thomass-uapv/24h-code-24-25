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
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.change_direction_counter = 0

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
                self.change_direction_counter += 1
                if self.change_direction_counter > 30:  # Change la direction toutes les 30 images
                    self.direction_x = random.choice([-1, 1])
                    self.direction_y = random.choice([-1, 1, 1, 1])
                    self.change_direction_counter = 0

                self.x += self.direction_x * self.vitesse * 0.5
                if random.randint(0, 4) == 0:
                    self.y += self.direction_y * self.vitesse * 0.5

                # Empeche les rats de quitter l'écran
                self.x = max(0, min(pyxel.width - 8, self.x))
                self.y = max(0, min(pyxel.height - 8, self.y))

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
        self.joueur = Rat(100, 100, True, 3.0) # Le joueur
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
        self.boids()

    def ajout_rat(self, rat):
        self.liste_rats.append(rat)

    def boids(self):
        for rat in self.liste_rats:
            move_x, move_y = 0, 0
            for rat2 in self.liste_rats:
                if rat != rat2:
                    distance = rat.getDistance(rat2.getX(), rat2.getY())
                    if distance < self.evitement:
                        move_x += rat.getX() - rat2.getX()
                        move_y += rat.getY() - rat2.getY()
            rat.x += move_x * 0.05
            rat.y += move_y * 0.05

App()