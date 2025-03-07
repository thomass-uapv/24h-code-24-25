import pyxel
import math
import random

# Dimensions de la fenêtre et paramètres de simulation
WIDTH = 160
HEIGHT = 120
N_BOIDS = 30
MAX_SPEED = 2
MAX_FORCE = 0.03
PERCEPTION_RADIUS = 30

class Boid:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * MAX_SPEED
        self.vy = math.sin(angle) * MAX_SPEED

    def update(self, boids):
        # Calcul des forces résultantes basées sur les règles
        align = self.align(boids)
        cohere = self.cohere(boids)
        separate = self.separate(boids)

        # Application des forces
        self.vx += align[0] + cohere[0] + separate[0]
        self.vy += align[1] + cohere[1] + separate[1]

        # Limitation de la vitesse
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > MAX_SPEED:
            self.vx = (self.vx / speed) * MAX_SPEED
            self.vy = (self.vy / speed) * MAX_SPEED

        # Mise à jour de la position
        self.x += self.vx
        self.y += self.vy

        # Passage d'un bord à l'autre (effet wrap-around)
        if self.x < 0:
            self.x += WIDTH
        if self.x > WIDTH:
            self.x -= WIDTH
        if self.y < 0:
            self.y += HEIGHT
        if self.y > HEIGHT:
            self.y -= HEIGHT

    def align(self, boids):
        """Règle d'alignement : se diriger vers la moyenne des vitesses des voisins"""
        steering_x, steering_y, total = 0, 0, 0
        for other in boids:
            if other != self:
                dist = math.hypot(self.x - other.x, self.y - other.y)
                if dist < PERCEPTION_RADIUS:
                    steering_x += other.vx
                    steering_y += other.vy
                    total += 1
        if total > 0:
            steering_x /= total
            steering_y /= total
            # Normaliser et ajuster la vitesse désirée
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > 0:
                steering_x = (steering_x / mag) * MAX_SPEED
                steering_y = (steering_y / mag) * MAX_SPEED
            # Calcul du "steering" (différence avec la vitesse actuelle)
            steering_x -= self.vx
            steering_y -= self.vy
            # Limiter la force appliquée
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > MAX_FORCE:
                steering_x = (steering_x / mag) * MAX_FORCE
                steering_y = (steering_y / mag) * MAX_FORCE
        return (steering_x, steering_y)

    def cohere(self, boids):
        """Règle de cohésion : se rapprocher de la moyenne des positions des voisins"""
        center_x, center_y, total = 0, 0, 0
        for other in boids:
            if other != self:
                dist = math.hypot(self.x - other.x, self.y - other.y)
                if dist < PERCEPTION_RADIUS:
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
                desired_x = (desired_x / mag) * MAX_SPEED
                desired_y = (desired_y / mag) * MAX_SPEED
            steering_x = desired_x - self.vx
            steering_y = desired_y - self.vy
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > MAX_FORCE:
                steering_x = (steering_x / mag) * MAX_FORCE
                steering_y = (steering_y / mag) * MAX_FORCE
            return (steering_x, steering_y)
        return (0, 0)

    def separate(self, boids):
        """Règle de séparation : éviter les collisions avec les voisins proches"""
        steering_x, steering_y, total = 0, 0, 0
        for other in boids:
            if other != self:
                dist = math.hypot(self.x - other.x, self.y - other.y)
                # On utilise un rayon plus petit pour la séparation
                if dist < PERCEPTION_RADIUS / 2:
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
                steering_x = (steering_x / mag) * MAX_SPEED
                steering_y = (steering_y / mag) * MAX_SPEED
            steering_x -= self.vx
            steering_y -= self.vy
            mag = math.sqrt(steering_x ** 2 + steering_y ** 2)
            if mag > MAX_FORCE:
                steering_x = (steering_x / mag) * MAX_FORCE
                steering_y = (steering_y / mag) * MAX_FORCE
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

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Boids avec Pyxel")
        self.boids = [Boid() for _ in range(N_BOIDS)]
        pyxel.run(self.update, self.draw)

    def update(self):
        for boid in self.boids:
            boid.update(self.boids)

    def draw(self):
        pyxel.cls(0)
        for boid in self.boids:
            boid.draw()

# Lancement de l'application
App()
