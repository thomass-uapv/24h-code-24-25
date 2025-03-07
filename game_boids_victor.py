import pyxel
import math
import random

END_VALUE = 3000
AREA = (170,518)

class Rat:
    def __init__(self, x=50, y=50, size = 1.0, is_player = False, independant = False, vitesse = 3):
        self.x = x
        self.y = y
        self.img = 0
        self.sprite = (4,104,10,22)
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
                self.x = min(AREA[1], self.x + self.vitesse + self.boost)
                self.degre = min(30, self.degre + self.angle)
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x = max(AREA[0], self.x - self.vitesse - self.boost)
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
            self.x = max(AREA[0], min(AREA[1] - 8, self.x))
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
            self.x = max(AREA[0], min(AREA[1] - 8, self.x))
            self.y = max(0, min(pyxel.height - 8, self.y))

    def recadrage(self): #recadre continuellement langle vers 0°
        # if self.is_player:
        if self.degre < 0 and not pyxel.btn(pyxel.KEY_LEFT):
            self.degre += self.angle-self.angle/2
            self.x = min(AREA[1], self.x + self.vitesse/2)
        elif self.degre > 0 and not pyxel.btn(pyxel.KEY_RIGHT):
            self.degre -= self.angle-self.angle/2
            self.x = max(AREA[0], self.x - self.vitesse/2)

    def draw(self):
        if self.is_player:
            #personnage
            if (pyxel.frame_count // 6) % 2 == 0:
                pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], 5, self.degre, 1.5)
            else:
                pyxel.blt(self.x, self.y, 0, self.sprite[0],self.sprite[1]+32, self.sprite[2], self.sprite[3], 5, self.degre, 1.5)
        elif self.independant:
            if (pyxel.frame_count // 6) % 2 == 0:
                pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], 5, self.degre+180, 1.0)
            else:
                pyxel.blt(self.x, self.y, 0, self.sprite[0],self.sprite[1]+32, self.sprite[2], self.sprite[3], 5, self.degre+180, 1.0)
        else:
            if (pyxel.frame_count // 6) % 2 == 0:
                pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], 5, self.degre, 1.0)
            else:
                pyxel.blt(self.x, self.y, 0, self.sprite[0],self.sprite[1]+32, self.sprite[2], self.sprite[3], 5, self.degre, 1.0)

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

        self.img = 0
        self.sprite = (89, 131, 15, 13)

    def getCo(self):
        return (self.x, self.y)
    
    def draw(self):
        pyxel.blt(self.x,self.y,self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], 5, 0, 1.0)
    
    def update(self):
        self.y += self.vitesse

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

class Obstacle:
    def __init__(self):
        self.position = []
        self.limite = 10
        self.quant = 0
        self.img = 0
        self.liste_sprite = ((144,41,15,23),(120,55,10,5),(105,65,14,15),(3,218,23,30))
        self.apply_sprite = []

    def apparition(self):
        if self.quant < self.limite:
            self.position.append([random.randint(AREA[0], AREA[1]), 0])
            self.apply_sprite.append(random.choice(self.liste_sprite))
            self.quant +=1
            
    
    def deplacement(self):
        for obstacle in self.position:
            obstacle[1]+=2
        
    def disparition(self):
        for i in range(len(self.position)-1, -1, -1):
            if self.position[i][1] >= 400:
                self.quant -= 1
                self.position.pop(i)
                
    def draw(self):
        for i_obstacle in range(len(self.position)):
            sprite = self.apply_sprite[i_obstacle]
            pyxel.blt(self.position[i_obstacle][0], self.position[i_obstacle][1], self.img, sprite[0], sprite[1], sprite[2], sprite[3], 5)
    
    def update(self):
        self.deplacement()
        self.disparition()
        if random.randint(0, 50) == 0 and self.quant < self.limite:
            self.apparition()

    def getPositions(self):
        return self.position

class App:
    def __init__(self):
        self.max_rats_inde = 4
        self.liste_rat_map = []
        self.max_boosts_map = 2
        self.liste_boosts_map = []
        self.distance_parcouru = 0

        self.groupe_rat = GroupeRat((300, 400), max_rats=50)
        self.obstacle = Obstacle()

        self.invincibilite = -1

        self.score = 0
        
        self.backgrounds = [
            [
                [82, 50, 1, 24, 0, 24, 25, 8],
                [170, 50, 1, 1, 0, 15, 25, 5],
                [170, 90, 1, 1, 0, 15, 25, 5],
                [518, 50, 1, 48, 0, 16, 25, 9],
                [266, 50, 1, 48, 25, 16, 25, 7],
                [386, 50, 1, 48, 25, 16, 25, 7]
            ],
            [
                [82, 200, 1, 24, 0, 24, 25, 8],
                [170, 133, 1, 1, 0, 15, 25, 5],
                [170, 250, 1, 1, 0, 15, 25, 5],
                [518, 200, 1, 48, 0, 16, 25, 9],
                [266, 205, 1, 48, 25, -16, -25, 7],
                [386, 200, 1, 48, 25, 16, 25, 7]
            ],
            [
                [82, 350, 1, 24, 0, 24, 25, 8],
                [170, 300, 1, 1, 0, 15, 25, 5],
                [170, 380, 1, 1, 0, 15, -25, 5],
                [266, 300, 1, 48, 25, 16, -25, 9],
                [386, 320, 1, 48, 25, -16, 25, 7],
                [518, 350, 1, 48, 0, 16, 25, 7]
            ], [
                [82, 200, 1, 24, 0, 24, 25, 8],
                [170, 133, 1, 1, 0, 15, 25, 5],
                [170, 250, 1, 1, 0, 15, 25, 5],
                [518, 200, 1, 48, 0, 16, 25, 9],
                [266, 205, 1, 48, 25, -16, -25, 7],
                [386, 200, 1, 48, 25, 16, 25, 7]
            ],
            [
                [82, 50, 1, 24, 0, 24, 25, 8],
                [170, 50, 1, 1, 0, 15, 25, 5],
                [170, 90, 1, 1, 0, 15, 25, 5],
                [518, 50, 1, 48, 0, 16, 25, 9],
                [266, 50, 1, 48, 25, 16, 25, 7],
                [386, 50, 1, 48, 25, 16, 25, 7]
            ],
            [
                [82, 200, 1, 24, 0, 24, 25, 8],
                [170, 133, 1, 1, 0, 15, 25, 5],
                [170, 250, 1, 1, 0, 15, 25, 5],
                [518, 200, 1, 48, 0, 16, 25, 9],
                [266, 205, 1, 48, 25, -16, -25, 7],
                [386, 200, 1, 48, 25, 16, 25, 7]
            ],
            [
                [82, 350, 1, 24, 0, 24, 25, 8],
                [170, 300, 1, 1, 0, 15, 25, 5],
                [170, 380, 1, 1, 0, 15, -25, 5],
                [266, 300, 1, 48, 25, 16, -25, 9],
                [386, 320, 1, 48, 25, -16, 25, 7],
                [518, 350, 1, 48, 0, 16, 25, 7]
            ], [
                [82, 200, 1, 24, 0, 24, 25, 8],
                [170, 133, 1, 1, 0, 15, 25, 5],
                [170, 250, 1, 1, 0, 15, 25, 5],
                [518, 200, 1, 48, 0, 16, 25, 9],
                [266, 205, 1, 48, 25, -16, -25, 7],
                [386, 200, 1, 48, 25, 16, 25, 7]
            ],
            [
                [82, 50, 1, 24, 0, 24, 25, 8],
                [170, 50, 1, 1, 0, 15, 25, 5],
                [170, 90, 1, 1, 0, 15, 25, 5],
                [518, 50, 1, 48, 0, 16, 25, 9],
                [266, 50, 1, 48, 25, 16, 25, 7],
                [386, 50, 1, 48, 25, 16, 25, 7]
            ]
        ]
        
        self.bg_positions = [0, -100, -200, -300, -400, -500, -600, -700, -800, -900] 
        self.scroll_speed = 2
        
        pyxel.init(600, 400, title="Boids avec Pyxel", display_scale=2)
        pyxel.load("5.pyxres")
        pyxel.run(self.update, self.draw)
     

    def update(self):
        for i in range(len(self.bg_positions)):
            self.bg_positions[i] += self.scroll_speed  # Ajuste la position des groupes
        
    # Réinitialisation des groupes lorsqu'ils sortent de l'écran
        for i in range(len(self.bg_positions)):
            if self.bg_positions[i] >= 400:
                self.bg_positions[i] -= 800  # Déplacement du fond sans réinitialiser la liste
#                 self.backgrounds[i] = self.backgrounds[i]
        if self.distance_parcouru == END_VALUE:
            pyxel.blt(300,150, 0, 26, 128, 58, 33, 5, 0, 6.0)
            pyxel.text(255,270, "Appuyer sur Q ou Echap pour quitter", 7)
            pyxel.show()

            while True:
                if pyxel.btn(pyxel.KEY_Q):
                    pyxel.quit()

        self.obstacle.update()
        self.groupe_rat.update()
        if random.randint(0,5) == 0 and len(self.liste_boosts_map) < self.max_boosts_map:
            self.liste_boosts_map.append(Boost(random.randint(AREA[0],AREA[1]), 0)) # Les boosts apparaitront en haut de l'écran
        
        for boost in self.liste_boosts_map[:]:  # Iterate over a copy of the list
            boost.update()
            if boost.y == pyxel.height:
                self.liste_boosts_map.remove(boost)
            else:
                if self.groupe_rat.joueur.getDistance(boost.getX(), boost.getY()) < 20:
                    self.liste_boosts_map.remove(boost)
                    if not self.groupe_rat.joueur.isReserveBoostFull():
                        self.groupe_rat.joueur.addBoost()
        
        # randint(0,50) == 0 permet de faire apparaitre un rat sur la map avec une probabilité de 1/50
        if random.randint(0,50) == 0 and len(self.liste_rat_map) < self.max_rats_inde:
            self.liste_rat_map.append(Rat(random.randint(AREA[0],AREA[1]), 2, is_player=False, size=3.0, independant=True, vitesse=3)) # Les rats apparaitront en haut de l'écran
        for i in range(len(self.liste_rat_map) - 1, -1, -1):  # Itération en sens inverse
            rat = self.liste_rat_map[i]
            rat.update(self.liste_rat_map)
            if rat.getY() == pyxel.height - 8:
                del self.liste_rat_map[i]
            elif rat.getDistance(self.groupe_rat.joueur.getX(), self.groupe_rat.joueur.getY()) < 20:
                self.groupe_rat.ajout_rat(rat)
                del self.liste_rat_map[i]
        
        if self.invincibilite == -1:
            for obstacle in self.obstacle.getPositions():
                if self.groupe_rat.joueur.getDistance(obstacle[0], obstacle[1]) < 20 and len(self.groupe_rat.liste_rats) != 0:
                    self.invincibilite = 0
                    del self.groupe_rat.liste_rats[random.randint(0, len(self.groupe_rat.liste_rats)-1)]
                    break
                else:
                    for rat in self.groupe_rat.liste_rats:
                        if rat.getDistance(obstacle[0], obstacle[1]) < 20 and len(self.groupe_rat.liste_rats) != 0:
                            self.invincibilite = 0
                            self.groupe_rat.liste_rats.remove(rat)
                            break
        else:
            self.invincibilite += 1
            if self.invincibilite > 30:
                self.invincibilite = -1
                    
        
        self.distance_parcouru += 1

        #Score update
        self.score = self.groupe_rat.getNbRats() * 1000

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(82, 350, 1, 24, 0, 24, 25, 0, 0, 8)
        pyxel.blt(170, 300, 1, 1, 0, 15, 25, 0, 0, 5)
        pyxel.blt(170, 380, 1, 1, 0, 15, -25, 0, 0, 5)
        pyxel.blt(266, 300, 1, 48, 25, 16, -25, 0, 0, 7.5)
        pyxel.blt(386, 320, 1, 48, 25, -16, 25, 0, 0, 7.5)
        pyxel.blt(518, 350, 1, 48, 0, 16, 25, 0, 0, 9)
        for i, group in enumerate(self.backgrounds):
            for bg in group:
                pyxel.blt(bg[0], (bg[1] + self.bg_positions[i]), bg[2], bg[3], bg[4], bg[5], bg[6], 0, 0, bg[7]+2)
        self.groupe_rat.draw()
        for boost in self.liste_boosts_map:
            boost.draw()
        for rat in self.liste_rat_map:
            rat.draw()
        self.obstacle.draw()
        pyxel.text(0,0, "Score: " + str(self.score), 7)
        # pyxel.text(0,20, f"Debug - distance parcouru : {self.distance_parcouru}",7)

        if self.groupe_rat.joueur.getReserveBoost() == 0:
            pyxel.blt(540, 10, 0, 161, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(560, 10, 0, 161, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(580, 10, 0, 161, 20, 10, 10, 5, 0, 2.0)

        elif self.groupe_rat.joueur.getReserveBoost() == 1:
            pyxel.blt(540, 10, 0, 141, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(560, 10, 0, 161, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(580, 10, 0, 161, 20, 10, 10, 5, 0, 2.0)

        elif self.groupe_rat.joueur.getReserveBoost() == 2:
            pyxel.blt(540, 10, 0, 141, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(560, 10, 0, 141, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(580, 10, 0, 161, 20, 10, 10, 5, 0, 2.0)

        else :
            pyxel.blt(540, 10, 0, 141, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(560, 10, 0, 141, 20, 10, 10, 5, 0, 2.0)
            pyxel.blt(580, 10, 0, 141, 20, 10, 10, 5, 0, 2.0)

# Lancement de l'application
App()