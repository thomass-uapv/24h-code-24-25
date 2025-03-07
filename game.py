import pyxel
import math
import random

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
        self.vx = math.cos(angle) * self.vitesse # quantité de pixel à déplacer sur l'axe x
        self.vy = math.sin(angle) * self.vitesse # quantité de pixel à déplacer sur l'axe y

    def update(self, liste_rats):
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
        elif self.independant:
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
        else:
            # Calcul des forces résultantes basées sur les règles
            align = self.align(liste_rats)
            cohere = self.cohere(liste_rats)
            separate = self.separate(liste_rats)

            # Application des forces
            self.vx += align[0] + cohere[0] + separate[0]
            self.vy += align[1] + cohere[1] + separate[1]

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

    def align(self, liste_rats):
        """Règle d'alignement : se diriger vers la moyenne des vitesses des voisins"""
        steering_x, steering_y, total = 0, 0, 0
        for other in liste_rats:
            if other != self:
                dist = math.hypot(self.x - other.x, self.y - other.y)
                if dist < self.rayon_perception:
                    steering_x += other.vx
                    steering_y += other.vy
                    total += 1
        if total > 0:
            steering_x /= total
            steering_y /= total
            # Normaliser et ajuster la vitesse désirée
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > 0:
                steering_x = (steering_x / mag) * self.vitesse
                steering_y = (steering_y / mag) * self.vitesse
            # Calcul du "steering" (différence avec la vitesse actuelle)
            steering_x -= self.vx
            steering_y -= self.vy
            # Limiter la force appliquée
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > self.max_force:
                steering_x = (steering_x / mag) * self.max_force
                steering_y = (steering_y / mag) * self.max_force
        return (steering_x, steering_y)

    def cohere(self, liste_rats):
        """Règle de cohésion : se rapprocher de la moyenne des positions des voisins"""
        center_x, center_y, total = 0, 0, 0
        for other in liste_rats:
            if other != self:
                dist = math.hypot(self.x - other.x, self.y - other.y)
                if dist < self.rayon_perception:
                    center_x += other.x
                    center_y += other.y
                    total += 1
        if total > 0:
            center_x /= total
            center_y /= total
            desired_x = center_x - self.x
            desired_y = center_y - self.y
            mag = math.sqrt(desired_x ** 2 + desired_y ** 2)
            if mag > 0:
                desired_x = (desired_x / mag) * self.vitesse
                desired_y = (desired_y / mag) * self.vitesse
            steering_x = desired_x - self.vx
            steering_y = desired_y - self.vy
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > self.max_force:
                steering_x = (steering_x / mag) * self.max_force
                steering_y = (steering_y / mag) * self.max_force
            return (steering_x, steering_y)
        return (0, 0)

    def separate(self, liste_rats):
        """Règle de séparation : éviter les collisions avec les voisins proches"""
        steering_x, steering_y, total = 0, 0, 0
        for other in liste_rats:
            if other != self:
                dist = math.hypot(self.x - other.x, self.y - other.y)
                # On utilise un rayon plus petit pour la séparation
                if dist < self.rayon_perception / 2:
                    diff_x = self.x - other.x
                    diff_y = self.y - other.y
                    if dist > 0:
                        diff_x /= dist
                        diff_y /= dist
                    steering_x += diff_x
                    steering_y += diff_y
                    total += 1
        if total > 0:
            steering_x /= total
            steering_y /= total
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > 0:
                steering_x = (steering_x / mag) * self.vitesse
                steering_y = (steering_y / mag) * self.vitesse
            steering_x -= self.vx
            steering_y -= self.vy
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > self.max_force:
                steering_x = (steering_x / mag) * self.max_force
                steering_y = (steering_y / mag) * self.max_force
        return (steering_x, steering_y)

    def draw(self):
        """Dessine le boid sous forme de petit triangle orienté selon sa vitesse"""
        angle = math.atan2(self.vy, self.vx)
        size = 4
        # Calcul des points du triangle
        x1 = self.x + math.cos(angle) * size
        y1 = self.y + math.sin(angle) * size
        x2 = self.x + math.cos(angle + 2.5) * size
        y2 = self.y + math.sin(angle + 2.5) * size
        x3 = self.x + math.cos(angle - 2.5) * size
        y3 = self.y + math.sin(angle - 2.5) * size
        pyxel.tri(x1, y1, x2, y2, x3, y3, 7)

class GroupeRat:
    def __init__(self, coordonne, max_rats = 20):
        self.joueur = Rat(coordonne[0], coordonne[1], 3.0, True)
        self.max_rats = max_rats
        self.liste_rats = []
    
    def draw(self):
        self.joueur.draw()
        for rat in self.liste_rats:
            rat.draw()

    def update(self):
        self.joueur.update(self.liste_rats)
        for rat in self.liste_rats:
            rat.update(self.liste_rats)

    def ajout_rat(self, rat):
        self.liste_rats.append(rat)

class App:
    def __init__(self):
        self.max_rats_inde = 4
        self.liste_rat_map = []

        self.groupe_rat = GroupeRat((100, 100))

        pyxel.init(160, 120, title="Boids avec Pyxel")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.groupe_rat.update()
        for rat in self.liste_rat_map:
            rat.update(self.liste_rat_map)

    def draw(self):
        pyxel.cls(0)
        self.groupe_rat.draw()
        for rat in self.liste_rat_map:
            rat.draw()

# Lancement de l'application
App()
