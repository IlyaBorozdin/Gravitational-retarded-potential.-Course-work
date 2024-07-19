from source.const import *
from math import *

class CelestialBody:
    def __init__(self, starMass, planetMass):
        self.starMass = starMass * SUN_MASS
        self.planetMass = planetMass
        self.reducedMass = self.starMass * self.planetMass / (self.starMass + self.planetMass)
        self.systemMass = self.starMass + self.planetMass

    def __call__(self, state, t):

        r, dr, phi, dphi = state
        ddr, ddphi = self.getAccelerations(r, dr, phi, dphi)

        return [dr, ddr, dphi, ddphi]

    def getAccelerations(self, r, dr, phi, dphi):

        ddr = (r * dphi * dphi - G * self.systemMass * (1 - 3 * dr * dr / C2) / (r * r)) / (1 + 6 * G * self.systemMass / (r * C2))

        ddphi = -2 * dr * dphi / r

        return ddr, ddphi
    
    def getDecart(self, r, phi):

        x1 = r * cos(phi)
        y1 = r * sin(phi)

        return x1, y1
    
    def getState(self, distance, ecentricity):

        dphi = sqrt(G * self.systemMass * (1 - ecentricity) / distance) / distance

        return [distance, 0.0, 0.0, dphi]
    
    def getPeriod(self, distance, ecentricity):

        return 2 * pi * sqrt((distance / (1 + ecentricity)) ** 3 / (G * self.systemMass))
    
    def getBetaMax(self, distance, ecentricity):

        return (1 + ecentricity) * sqrt(G * self.systemMass / distance / (1 - ecentricity)) / C
    
    def getDistanceMin(self, distance, ecentricity):

        return (1 - ecentricity) / (1 + ecentricity) * distance / self.getSchwarzschild()
    
    def getSchwarzschild(self):

        return 2 * G * self.starMass / C2
    
    def getPrecession(self, distance, ecentricity):

        return 6 * pi * G * self.starMass / (C2 * (1 - ecentricity * ecentricity) * self.getPeriod(distance, ecentricity) * distance / (1 + ecentricity)) * SEC_PER_CEN
    