import numpy as np
from scipy.integrate import odeint
import math
from source.const import *

class Equation:
    def __init__(self):
        self.equation = None
        self.state = None
        self.time = None
        self.timeStep = None

    def setEquation(self, equation):
        self.equation = equation

    def setConditions(self, state, time, timeStep):
        self.state = state
        self.time = time
        self.timeStep = timeStep

    def solution(self):

        times = np.arange(0.0, self.time, self.timeStep)
        results = odeint(self.equation, self.state, times)

        return results, times
    
    def convertToDecart(self, results):

        decartResults = []
        for relative_coords in results:
            r, _, phi, _ = relative_coords
            x1, y1 = self.equation.getDecart(r, phi)
            decartResults.append([x1, y1])
        
        return np.array(decartResults)
    
    def findPrecession(self, results, times, dist, e):

        count = 0
        psi = 0.0
        n = 0
        for i in range(2, len(results)):
            r1, dr1, phi1, dphi1 = results[i - 1]
            r2, dr2, phi2, dphi2 = results[i]

            if dr1 > 0.0 and dr2 < 0.0:
                count += 1
                psi = phi2 - 2 * math.pi * count + (dr2 / dphi2) * (dist / r2 / r2) * (1 - e) / e
                n = i 

        period = (times[n] - times[0]) / count
        precession = psi / (times[n] - times[0]) * SEC_PER_CEN

        return period, precession



