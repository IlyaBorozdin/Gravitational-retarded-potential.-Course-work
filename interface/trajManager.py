from interface.plotManager import PlotManager

class TrajManager(PlotManager):
    def __init__(self, master):
        super().__init__(master)

    def makePlot(self, solution):
        PlotManager.ax.plot(solution[:, 0], solution[:, 1])
