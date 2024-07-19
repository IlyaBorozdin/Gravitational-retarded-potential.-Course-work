from interface.plotManager import PlotManager

class GraphManager(PlotManager):
    def __init__(self, master):
        super().__init__(master)

    def setImageParameters(self, scale, periodLimit, timeStep):
        self.slice = int(periodLimit / timeStep)

    def makePlot(self, solution):
        self.solution = solution
        xFirst = solution[:self.slice, 0]
        yFirst = solution[:self.slice, 1]
        xLast = solution[-self.slice:, 0]
        yLast = solution[-self.slice:, 1]

        PlotManager.ax.plot(xFirst, yFirst, label='First {} points'.format(self.slice))
        PlotManager.ax.plot(xLast, yLast, label='Last {} points'.format(self.slice))
        PlotManager.ax.legend()
