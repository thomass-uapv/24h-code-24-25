import pyxel
import math
import random

END_VALUE = 1000

class Rat:
    def __init__(self, x=50, y=50, size = 1.0, is_player = False, independant = False, vitesse = 3):
        self.x = x
        self.y = y
        self.img = 0
        self.sprite = (8,0,8,8)
        self.size = size
        self.vitesse = vitesse
        self.is_player = is_player
        self.independant = independant

        # Pour les déplacements des rats "indépendants"
        self.change_direction_counter = 0
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1, 1, 1])

        self.rayon_perception = 30
        self.max_force = 0.03

        self.degre = 0 # direction
        self.angle = 4 # pour l'animation

        angle = random.uniform(0, 2 * math.pi)
        self.vx = 0 # quantité de pixel à déplacer sur l'axe x
        self.vy = 0 # quantité de pixel à déplacer sur l'axe y

        self.boost = 0
        self.reserve_boost = 0
        self.max_reserve = 3
        self.boost_duration = -1

    def update(self, liste_rats):
        if self.is_player:
            if pyxel.btn(pyxel.KEY_SHIFT) and self.boost_duration == -1 and self.reserve_boost > 0:
                self.boost_duration = 0
                self.reserve_boost -= 1
            
            if self.boost_duration != -1:
                self.boost = 10
                self.boost_duration += 1

            if self.boost_duration > 10:
                self.boost_duration = -1
                self.boost = 0

            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x = min(pyxel.width-8, self.x + self.vitesse + self.boost)
                self.degre = min(30, self.degre + self.angle)
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x = max(0, self.x - self.vitesse - self.boost)
                self.degre = max(-30, self.degre - self.angle)
            if pyxel.btn(pyxel.KEY_DOWN):
                self.y = min(pyxel.height-8, self.y + self.vitesse + self.boost)
            if pyxel.btn(pyxel.KEY_UP):
                self.y = max(0, self.y- self.vitesse - self.boost)
            self.recadrage()
        elif self.independant:
            self.change_direction_counter += 1
            if self.change_direction_counter > 30:  # Change la direction toutes les 30 images
                self.direction_x = random.choice([-1, 1])
                self.direction_y = random.choice([-1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
                self.change_direction_counter = 0

            self.x += self.direction_x * self.vitesse * 0.5
            self.y += self.direction_y * self.vitesse * 1.5

            # Empeche les rats de quitter l'écran
            self.x = max(0, min(pyxel.width - 8, self.x))
            self.y = max(0, min(pyxel.height - 8, self.y))
        else:

            # Limitation de la vitesse
            speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
            if speed > self.vitesse:
                self.vx = (self.vx / speed) * self.vitesse
                self.vy = (self.vy / speed) * self.vitesse

            # Mise à jour de la position
            self.x += self.vx
            self.y += self.vy

            # Empeche les rats de quitter l'écran
            self.x = max(0, min(pyxel.width - 8, self.x))
            self.y = max(0, min(pyxel.height - 8, self.y))

    def recadrage(self): #recadre continuellement langle vers 0°
        # if self.is_player:
        if self.degre < 0 and not pyxel.btn(pyxel.KEY_LEFT):
            self.degre += self.angle-self.angle/2
            self.x = min(pyxel.width-8, self.x + self.vitesse/2)
        elif self.degre > 0 and not pyxel.btn(pyxel.KEY_RIGHT):
            self.degre -= self.angle-self.angle/2
            self.x = max(0, self.x - self.vitesse/2)

    def draw(self):
        if self.is_player:
            pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], 0, self.degre, 2)
        else:
            angle = math.atan2(self.vy, self.vx)
            pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], 0, angle,1)

    def getDistance(self,x,y):
        return ((self.x-x)**2 + (self.y-y)**2)**0.5
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getReserveBoost(self):
        return self.reserve_boost
    
    def isReserveBoostFull(self):
        return (self.reserve_boost >= self.max_reserve)
    
    def addBoost(self):
        if self.reserve_boost < self.max_reserve:
            self.reserve_boost += 1

class GroupeRat:
    def __init__(self, coordonne, max_rats = 20):
        self.joueur = Rat(coordonne[0], coordonne[1], 3.0, True, vitesse=5)
        self.max_rats = max_rats
        self.liste_rats = []
    
    def draw(self):
        self.joueur.draw()
        for rat in self.liste_rats:
            rat.draw()

    def update(self):
        self.boid_behavior()
        self.joueur.update(self.liste_rats)
        for rat in self.liste_rats:
            rat.update(self.liste_rats)

    def ajout_rat(self, rat):
        if self.max_rats > len(self.liste_rats):
            rat.independant = False
            self.liste_rats.append(rat)

    def boid_behavior(self):
        if not self.liste_rats:
            return

        facteur_cohesion = 0.02
        facteur_alignement = 1
        facteur_separation = 0.1
        distance_separation = 30

        cible_x = self.joueur.x 
        cible_y = self.joueur.y - 60 * (1 if pyxel.btn(pyxel.KEY_LEFT) else -1)

        for rat in self.liste_rats:
            vx_cohesion, vy_cohesion = 0, 0
            vx_alignement, vy_alignement = 0, 0
            vx_separation, vy_separation = 0, 0
            nb_voisins = 0

            for autre in self.liste_rats:
                if autre == rat:
                    continue
                
                dist_x = autre.x - rat.x
                dist_y = autre.y - rat.y
                distance = (dist_x**2 + dist_y**2) ** 0.5

                vx_cohesion += autre.x
                vy_cohesion += autre.y

                vx_alignement += autre.vx
                vy_alignement += autre.vy

                if distance < distance_separation:
                    vx_separation -= dist_x
                    vy_separation -= dist_y

                nb_voisins += 1

            if nb_voisins > 0:
                vx_cohesion = (vx_cohesion / nb_voisins - rat.x) * facteur_cohesion
                vy_cohesion = (vy_cohesion / nb_voisins - rat.y) * facteur_cohesion
                
                vx_alignement = (vx_alignement / nb_voisins) * facteur_alignement
                vy_alignement = (vy_alignement / nb_voisins) * facteur_alignement

                rat.vx += vx_cohesion + vx_alignement + vx_separation
                rat.vy += vy_cohesion + vy_alignement + vy_separation

            vitesse = (rat.vx**2 + rat.vy**2) ** 0.5
            if vitesse > rat.vitesse:
                rat.vx = (rat.vx / vitesse) * rat.vitesse
                rat.vy = (rat.vy / vitesse) * rat.vitesse

            rat.vx += (cible_x - rat.x) * 0.02
            rat.vy += (cible_y - rat.y) * 0.02

    def getNbRats(self):
        return len(self.liste_rats)

class Boost:
    def __init__(self, x, y, vitesse = 1):
        self.x = x
        self.y = y
        self.vitesse = vitesse

    def getCo(self):
        return (self.x, self.y)

    def colision(self, rat):
        if rat.getX() == self.x and rat.getY() == self.y:
            return True
        return False
    
    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 8)
    
    def update(self):
        self.y += self.vitesse

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y



class App:
    def __init__(self):
        self.max_rats_inde = 4
        self.liste_rat_map = []
        self.max_boosts_map = 2
        self.liste_boosts_map = []
        self.distance_parcouru = 0

        self.groupe_rat = GroupeRat((300, 400))

        pyxel.init(600, 400, title="Boids avec Pyxel")
        pyxel.load("test.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):

        if self.distance_parcouru == END_VALUE:
            pyxel.text(200, 200, f"Partie terminé ! Bravo vous avez réussi à ramener {self.groupe_rat.getNbRats()} rats !", 8)
            while pyxel.btn(pyxel.KEY_KP_ENTER) == False:
                pyxel.text(200, 220, "Appuyez sur la touche Echap pour quitter", 8)
                pyxel.text(200, 240, "Appuyez sur la touche Entrée pour relancer", 8)
            

        self.groupe_rat.update()
        # randint(0,50) == 0 permet de faire apparaitre un rat sur la map avec une probabilité de 1/50
        if random.randint(0,1) == 0 and len(self.liste_boosts_map) < self.max_boosts_map:
            self.liste_boosts_map.append(Boost(random.randint(0,pyxel.width-8), 0)) # Les boosts apparaitront en haut de l'écran
        
        for boost in self.liste_boosts_map:
            boost.update()
            if boost.y == pyxel.height:
                self.liste_boosts_map.remove(boost)
            else:
                if self.groupe_rat.joueur.getDistance(boost.getX(), boost.getY()) < 20:
                    self.liste_boosts_map.remove(boost)
                    if not self.groupe_rat.joueur.isReserveBoostFull():
                        self.groupe_rat.joueur.addBoost()
        
        if random.randint(0,50) == 0 and len(self.liste_rat_map) < self.max_rats_inde:
            self.liste_rat_map.append(Rat(random.randint(0,pyxel.width-8), 2, is_player=False, size=3.0, independant=True, vitesse=3)) # Les rats apparaitront en haut de l'écran
        for rat in self.liste_rat_map:
            rat.update(self.liste_rat_map)
            if rat.getY() == pyxel.height-8:
                self.liste_rat_map.remove(rat)
            if rat.getDistance(self.groupe_rat.joueur.getX(), self.groupe_rat.joueur.getY()) < 20:
                self.groupe_rat.ajout_rat(rat)
                self.liste_rat_map.remove(rat)
        
        self.distance_parcouru += 1

    def draw(self):
        pyxel.cls(0)
        self.groupe_rat.draw()
        for boost in self.liste_boosts_map:
            boost.draw()
        for rat in self.liste_rat_map:
            rat.draw()



# Lancement de l'application
App()