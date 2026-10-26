import pygame
import math
from conf import *  # WIDTH, HEIGHT, G, MU
from random import random, randint


class Pinguin(pygame.sprite.Sprite):
    def __init__(self, banquise):
        super().__init__()
        self.image = pygame.image.load("pinguin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (271 // 4, 399 // 4))
        self.rect = self.image.get_rect()
        self.banquise = banquise

        self.largeur_glace = self.banquise.rect.width

        self.distance_centre = 0.0
        self.vitesse = 0.0
        self.vy_chute = 0.0
        self.a_bouge = False

        # On appelle directement reapparaitre() pour initialiser l'état et l'impulsion du premier tour
        self.reapparaitre()

    def physique(self):
        angle_rad = math.radians(-self.banquise.rotation)
        acceleration = G * math.sin(angle_rad)
        force_normale = G * math.cos(angle_rad)
        frottement = MU * force_normale

        if self.vitesse > 0.1:
            acceleration -= frottement
        elif self.vitesse < -0.1:
            acceleration += frottement
        else:
            if abs(acceleration) < frottement:
                acceleration = 0
                self.vitesse = 0

        self.vitesse += acceleration
        self.distance_centre += self.vitesse

        # On enregistre le fait que le pingouin a pris de la vitesse
        if abs(self.vitesse) > 0.2:
            self.a_bouge = True

        # S'il a bougé et qu'il est de nouveau complètement arrêté, il est stabilisé !
        if self.a_bouge and self.vitesse == 0:
            self.reapparaitre()

        # Vérification de la sortie de l'iceberg
        if abs(self.distance_centre) > self.largeur_glace / 2:
            self.etat = "TOMBANT"
            self.vy_chute = 0

    def maj_coordonnees(self):
        angle_rad = math.radians(-self.banquise.rotation)
        centre_x = self.banquise.rect.centerx
        centre_y = self.banquise.rect.centery

        # On utilise la hauteur de l'image d'origine pour ne pas que le pingouin s'enfonce
        epaisseur_glace = self.rect.h

        offset_x = epaisseur_glace * math.sin(angle_rad)
        offset_y = -epaisseur_glace * math.cos(angle_rad)

        x_pente = self.distance_centre * math.cos(angle_rad)
        y_pente = self.distance_centre * math.sin(angle_rad)

        self.rect.midbottom = (centre_x + x_pente + offset_x, centre_y + y_pente + offset_y)

    def reapparaitre(self):
        self.distance_centre = 0.0
        self.etat = "ATTENTE"
        self.temps_reapparition = pygame.time.get_ticks()
        self.a_bouge = False
        self.maj_coordonnees()

        # Génération de la vitesse initiale (latérale aléatoire)
        self.vitesse = (5 + random() * 2) * (-1) ** randint(0, 1)

    def update(self):
        if self.etat == "SUR_GLACE":
            self.physique()
            self.maj_coordonnees()
        elif self.etat == "TOMBANT":
            # Chute libre indépendante de l'iceberg
            self.vy_chute += G
            self.rect.y += self.vy_chute
            # Réapparition quand il sort de l'écran par le bas
            if self.rect.top > HEIGHT:
                self.reapparaitre()
        elif self.etat == "ATTENTE":
            # Reste accroché au centre pendant l'attente
            self.maj_coordonnees()
            if pygame.time.get_ticks() - self.temps_reapparition > 3000:
                self.etat = "SUR_GLACE"

    def draw(self, ecran):
        ecran.blit(self.image, self.rect)

        # Dessin de la flèche d'accélération pendant l'attente
        if self.etat == "ATTENTE":
            self.banquise.rotation = 0
            self.banquise.tourne()

            # Amplificateur visuel ajusté pour la vitesse
            longueur = self.vitesse * 10

            # Couleur : Vert si l'impulsion est faible, Rouge si elle est forte
            if abs(self.vitesse) < 15:
                couleur = (0, 255, 0)  # Vert
            else:
                couleur = (255, 0, 0)  # Rouge

            deb_x = self.rect.centerx
            deb_y = self.rect.centery

            # Coordonnées du vecteur de la flèche le long de l'horizontale
            fin_x = deb_x + longueur
            fin_y = deb_y

            # Dessin de la ligne principale
            pygame.draw.line(ecran, couleur, (deb_x, deb_y), (fin_x, fin_y), 6)

            # Dessin de la pointe (vraie flèche géométrique)
            if abs(longueur) > 5:
                taille_pointe = 15
                # L'angle dépend de la direction (vers la droite ou vers la gauche)
                angle_vecteur = 0 if self.vitesse > 0 else math.pi
                angle_pointe = math.pi * 0.85  # Environ 150 degrés en arrière

                pt1_x = fin_x + taille_pointe * math.cos(angle_vecteur + angle_pointe)
                pt1_y = fin_y + taille_pointe * math.sin(angle_vecteur + angle_pointe)

                pt2_x = fin_x + taille_pointe * math.cos(angle_vecteur - angle_pointe)
                pt2_y = fin_y + taille_pointe * math.sin(angle_vecteur - angle_pointe)

                pygame.draw.polygon(ecran, couleur, [(fin_x, fin_y), (pt1_x, pt1_y), (pt2_x, pt2_y)])