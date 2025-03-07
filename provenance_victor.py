import random
import pyxel

class App:
    def __init__(self):
        self.max_rat = 30  # Nombre max de rats
        self.joueur = Rat(50, 50, True, 3.0)  # Le joueur
        self.ordre_rat = OrdreRat(self.joueur)  # Créer l'ordre des rats

        pyxel.init(200, 200, title="Rats", fps=60, display_scale=2)
        pyxel.load("test.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.joueur.update()
        
        # Ajouter un rat avec une chance de 1/50 s'il y a de la place
        if random.randint(0, 50) == 0 and len(self.ordre_rat.liste_rats) < self.max_rat:
            self.ordre_rat.ajout_rat(Rat(random.randint(0, pyxel.width), 2, False, 1.0))

        self.ordre_rat.update()  # Mise à jour des rats suiveurs

    def draw(self):
        pyxel.cls(0)
        self.joueur.draw()
        self.ordre_rat.draw()  # Dessiner tous les rats

class Rat:
    def __init__(self, x=50, y=50, is_player=False, size=1.0):
        self.x = x
        self.y = y
        self.is_player = is_player
        self.size = size
        self.vx = 0
        self.vy = 0
        self.vitesse_max = 2  # Vitesse max pour les rats suiveurs
        self.sprite = (8,0,8,8)
        self.img = 0

    def mouvement(self):
        if self.is_player:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x = min(192, self.x + 3)
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x = max(0, self.x - 3)
            if pyxel.btn(pyxel.KEY_DOWN):
                self.y = min(192, self.y + 3)
            if pyxel.btn(pyxel.KEY_UP):
                self.y = max(0, self.y - 3)

    def update(self):
        if self.is_player:
            self.mouvement()
        else:
            self.x += self.vx
            self.y += self.vy

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3])

class OrdreRat:
    def __init__(self, joueur):
        self.joueur = joueur
        self.liste_rats = []

    def ajout_rat(self, rat):
        self.liste_rats.append(rat)

    def boid_behavior(self):
        if not self.liste_rats:
            return

        facteur_cohesion = 0.02
        facteur_alignement = 0.05
        facteur_separation = 0.1
        distance_separation = 10

        cible_x = self.joueur.x 
        cible_y = self.joueur.y - 20 * (1 if pyxel.btn(pyxel.KEY_LEFT) else -1)

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
            if vitesse > rat.vitesse_max:
                rat.vx = (rat.vx / vitesse) * rat.vitesse_max
                rat.vy = (rat.vy / vitesse) * rat.vitesse_max

            rat.vx += (cible_x - rat.x) * 0.02
            rat.vy += (cible_y - rat.y) * 0.02

    def update(self):
        self.boid_behavior()
        for rat in self.liste_rats:
            rat.update()

    def draw(self):
        for rat in self.liste_rats:
            rat.draw()

App()
