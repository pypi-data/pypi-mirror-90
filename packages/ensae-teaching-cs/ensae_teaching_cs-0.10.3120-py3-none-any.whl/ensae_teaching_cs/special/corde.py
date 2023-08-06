# -*- coding: utf-8 -*-
"""
@file
@brief Simulates a string which is falling but tied by its extremities. See :ref:`l-corde`.
"""
import os
import math
from pyquickhelper.loghelper import fLOG
from ..helpers.pygame_helper import wait_event, empty_main_loop


class Point:
    """
    définition d'un point : deux coordonnées et une masse
    """
    __slots__ = "x", "y", "m"

    def __init__(self, x, y, m):
        """
        définit un point de la corde, de coordonnées (x,y) et de masse m
        """
        self.x, self.y, self.m = float(x), float(y), float(m)

    def deplace_point(self, dep, dt):
        """
        déplace un point, le vecteur de déplacement est dp * dt
        où dep est aussi un point
        """
        self.x += float(dep.x) * dt
        self.y += float(dep.y) * dt

    def difference(self, p):
        """
        retourne le vecteur qui relie deux points, retourne un point
        """
        return Point(p.x - self.x, p.y - self.y, 0)

    def norme(self):
        """
        retourne la norme du vecteur (x,y)
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        """
        afficher le point
        """
        return "(x,y) = (%4.2f,%4.2f) masse %f" % (self.x, self.y, self.m)


class ObjetMasseReliees:
    """
    Définit un objet commun à une corde ou un pendule
    physiquement représenté comme un ensemble de masses
    reliées des élastiques.
    """

    def __init__(self, nb, p1, p2, m, k, g, f, lo):
        """
        @param          nb          nombre de points
        @param          p1          coordoonnées du premier point (fixe)
        @param          p2          coordoonnées du dernier point (fixe)
        @param          m           masse de la corde,
                                    répartie entre tous les points
        @param          k           raideur de l'élastique
        @param          g           intensité de l'apesanteur,
                                    valeur positive
        @param          f           vitesse de freinage
        @param          lo          longueur totale de la corde
        """
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        self.list = []
        self.vitesse = []
        for i in range(0, nb):
            x = x1 + float(i) * (x2 - x1) / float(nb - 1)
            y = y1 + float(i) * (y2 - y1) / float(nb - 1)
            self.list.append(Point(x, y, float(m) / nb))
            self.vitesse.append(Point(0, 0, 0))
        self.k = k * nb
        self.g = g
        self.lo = float(lo) / (nb - 1)
        self.f = f

    def force_point(self, i):
        """
        Calcule les forces qui s'exerce en un point,
        retourne un point *x, y*.
        """
        raise NotImplementedError()

    def iteration(self, dt):
        """
        Calcule les déplacements de chaque point et les met à jour,
        on ne déplace pas les points situés aux extrémités,
        retourne la somme des vitesses et des accélérations au carré.
        """
        raise NotImplementedError()


class Corde(ObjetMasseReliees):
    """
    Définition d'une corde, une liste de masses reliées
    par des élastiques et attachées au deux extrémités.
    """

    def force_point(self, i):
        """
        calcule les forces qui s'exerce en un point, retourne un point x,y
        """
        x, y = 0, 0
        # poids
        y -= self.g * self.list[i].m
        # voisin de gauche
        dxdy = self.list[i].difference(self.list[i - 1])
        d = dxdy.norme()
        if d > self.lo:
            dxdy.x = (d - self.lo) / d * dxdy.x
            dxdy.y = (d - self.lo) / d * dxdy.y
            x += self.k * dxdy.x
            y += self.k * dxdy.y
        # voisin de droite
        dxdy = self.list[i].difference(self.list[i + 1])
        d = dxdy.norme()
        if d > self.lo:
            dxdy.x = (d - self.lo) / d * dxdy.x
            dxdy.y = (d - self.lo) / d * dxdy.y
            x += self.k * dxdy.x
            y += self.k * dxdy.y
        # freinage
        x += - self.f * self.vitesse[i].x
        y += - self.f * self.vitesse[i].y

        return Point(x, y, 0)

    def iteration(self, dt):
        """
        Calcule les déplacements de chaque point et les met à jour,
        on ne déplace pas les points situés aux extrémités,
        retourne la somme des vitesses et des accélérations au carré.
        """
        force = [Point(0, 0, 0)]
        for i in range(1, len(self.list) - 1):
            xy = self.force_point(i)
            force.append(xy)
        force.append(Point(0, 0, 0))

        # déplacement
        for i in range(1, len(self.list) - 1):
            self.vitesse[i].deplace_point(force[i], dt)
            self.list[i].deplace_point(self.vitesse[i], dt)

        d = 0
        for f in force:
            d += self.vitesse[0].x ** 2 + f.x ** 2
            d += self.vitesse[1].y ** 2 + f.y ** 2

        return d


class Pendule(ObjetMasseReliees):
    """
    Définition d'un pendule, une liste de masses reliées
    par des élastiques et attachées à une extrémités.
    Contribution de *Pascal Grandeau*.
    """

    def force_point(self, i):
        """
        calcule les forces qui s'exerce en un point, retourne un point x,y
        """
        x, y = 0, 0
        # poids
        y -= self.g * self.list[i].m
        # voisin de gauche
        dxdy = self.list[i].difference(self.list[i - 1])
        d = dxdy.norme()
        if d > self.lo:
            dxdy.x = (d - self.lo) / d * dxdy.x
            dxdy.y = (d - self.lo) / d * dxdy.y
            x += self.k * dxdy.x
            y += self.k * dxdy.y
        # voisin de droite
        if i < len(self.list) - 1:
            dxdy = self.list[i].difference(self.list[i + 1])
            d = dxdy.norme()
            if d > self.lo:
                dxdy.x = (d - self.lo) / d * dxdy.x
                dxdy.y = (d - self.lo) / d * dxdy.y
                x += self.k * dxdy.x
                y += self.k * dxdy.y
        # freinage
        x += - self.f * self.vitesse[i].x
        y += - self.f * self.vitesse[i].y

        return Point(x, y, 0)

    def iteration(self, dt):
        """
        Calcule les déplacements de chaque point et les met à jour,
        on ne déplace pas les points situés aux extrémités,
        retourne la somme des vitesses et des accélérations au carré
        """
        force = [Point(0, 0, 0)]
        for i in range(1, len(self.list)):
            xy = self.force_point(i)
            force.append(xy)
        force.append(Point(0, 0, 0))

        # déplacement
        for i in range(1, len(self.list)):
            self.vitesse[i].deplace_point(force[i], dt)
            self.list[i].deplace_point(self.vitesse[i], dt)

        d = 0
        for _ in force:
            d += self.vitesse[0].x ** 2 + force[i].x ** 2
            d += self.vitesse[1].y ** 2 + force[i].y ** 2

        return d


def display_masses(corde, screen, pygame):
    """
    affichage de la corde à l'aide du module pyagame
    """
    y = screen.get_size()[1]
    color = (0, 0, 0)
    for p in corde.list:
        pygame.draw.circle(
            screen, color, (int(p.x), int(y - p.y)), int(p.m + 1))
    for i in range(0, len(corde.list) - 1):
        pygame.draw.line(screen, color,
                         (int(corde.list[i].x), int(y - corde.list[i].y)),
                         (int(corde.list[i + 1].x), int(y - corde.list[i + 1].y)))


def pygame_simulation(pygame, first_click=False, folder=None,
                      iter=1000, size=(800, 500), nb=10,
                      m=40, k=0.1, g=0.1, f=0.02, dt=0.1, step=10,
                      flags=0, model='corde', fLOG=fLOG):
    """
    Simulation graphique.
    Simule la chute d'une corde suspendue à ces deux extrémités.

    @param      pygame          module pygame (avoids importing in this file)
    @param      first_click     starts the simulation after a first click
    @param      folder          to save the simulation, an image per simulation
    @param      iter            number of iterations to run
    @param      fLOG            logging function

    @param      nb              nombre de points
    @param      m               masse de la corde,
                                répartie entre tous les points
    @param      k               raideur de l'élastique
    @param      g               intensité de l'apesanteur,
                                valeur positive
    @param      f               vitesse de freinage
    @param      dt              petit temps
    @param      step            marche
    @param      flags           see `pygame.display.set_mode
                                <https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode>`_
    @param      model           ``'corde'`` ou ``'pendule'``
    @param      fLOG            logging function

    La simulation ressemble à ceci dans le cas d'une corde :

    .. raw:: html

        <video autoplay="" controls="" loop="" height="400">
        <source src="http://www.xavierdupre.fr/enseignement/complements/corde.mp4" type="video/mp4" />
        </video>

    Ou cela dans le cas d'un pendule :

    .. raw:: html

        <video autoplay="" controls="" loop="" height="400">
        <source src="http://www.xavierdupre.fr/enseignement/complements/pendule.mp4" type="video/mp4" />
        </video>

    Pour lancer la simulation::

        from ensae_teaching_cs.special.corde import pygame_simulation
        import pygame
        pygame_simulation(pygame, model='corde')
    """
    # création de la corde
    nb = 10
    dx = size[0] // 8
    dy = size[1] // 8

    if model == 'corde':
        c = Corde(nb, (dx, size[1] - dy), (size[0] - dx, size[1] - dy),
                  m=m, k=k, g=g, f=f, lo=size[0])
    elif model == 'pendule':
        c = Pendule(nb, (size[0] // 2, size[1] - dy), (size[0] - dx, size[1] - dy),
                    m=m, k=k, g=g, f=f, lo=size[0] // 2)
    else:
        raise ValueError("Model '{}' is not recognized.".format(model))

    pygame.init()
    white = 255, 255, 255
    screen = pygame.display.set_mode(size, flags)

    # numéro d'itération
    it = 0

    images = []

    # continue tant que dep n'est pas proche de 0
    dep = len(c.list) * (size[0] * size[0] + size[1] * size[1])
    while dep > 1e-4 and it < iter:

        if it % step == 0:
            if it % (step * 10) == 0:
                fLOG("it={0}/{1} dep={2} #{3}".format(it, iter, dep, len(images)))
            empty_main_loop(pygame)
            screen.fill(white)
            display_masses(c, screen, pygame)
            pygame.display.flip()

        # on fait une pause dès la première itérations pour voir la corde
        # dans sa position initiale
        if it == 0 and first_click:
            wait_event(pygame)

        # "
        # unique instruction ajoutées par rapport à l'énoncé
        dep = c.iteration(dt)
        # "

        # on met à jour l'écran
        pygame.display.flip()

        if folder is not None and it % step == 0:
            images.append((it, screen.copy()))

        pygame.time.wait(2)

        # on incrémente le nombre d'itérations
        it += 1

    if folder is not None:
        fLOG("saving images")
        for it, screen in images:
            fLOG("saving image:", it)
            image = os.path.join(folder, "image_%04d.png" % it)
            pygame.image.save(screen, image)

    # le programme est terminé, on fait une pause pour voir le résultat final
    if first_click:
        wait_event(pygame)
