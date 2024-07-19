from matplotlib.animation import FuncAnimation
from collections import deque
from interface.plotManager import PlotManager

class SimulationManager(PlotManager):
    def __init__(self, master):
        super().__init__(master)

    def setImageParameters(self, scale, periodLimit, timeStep):
        self.scale = scale
        self.maxTrajLength = int(periodLimit / timeStep)
        self.trajX = deque(maxlen=self.maxTrajLength)
        self.trajY = deque(maxlen=self.maxTrajLength)
        self.batchSize = 10
        if self.batchSize == 0:
            self.batchSize = 1

    def makePlot(self, solution):

        if hasattr(self, 'anim') and hasattr(self.anim, '_stop'):
            self.anim._stop()
            PlotManager.clearPlots()
        
        self.lineToDraw, = PlotManager.ax.plot([], [], 'b-')
        self.point, = PlotManager.ax.plot([], [], 'ko', markersize=8)

        self.solution = solution
        numFrames = len(solution)
        self.numBatches = numFrames // self.batchSize
        if numFrames % self.batchSize != 0:
            self.numBatches += 1
        
        self.batchIndex = 0
        self.anim = FuncAnimation(PlotManager.fig, self.updatePlot, frames=self.numBatches, interval=5, repeat=True)

    def updatePlot(self, batchIndex):
        startIndex = batchIndex * self.batchSize
        endIndex = min((batchIndex + 1) * self.batchSize, len(self.solution))
        
        x, y = zip(*self.solution[startIndex:endIndex])
        self.trajX.extend(x)
        self.trajY.extend(y)
        
        self.lineToDraw.set_data(self.trajX, self.trajY)
        
        self.point.set_data(x[-1], y[-1])
        
        PlotManager.ax.set_xlim(-self.scale, self.scale)
        PlotManager.ax.set_ylim(-self.scale, self.scale)
