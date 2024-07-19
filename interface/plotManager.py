from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotManager:
    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("Body Trajectories")
    ax.set_xlabel('x, au')
    ax.set_ylabel('y, au')
    ax.grid(True)
    ax.tick_params(direction='in')
    canvas = None
    
    def __init__(self, master):
        self.master = master
        
        if PlotManager.canvas is None:
            PlotManager.canvas = FigureCanvasTkAgg(PlotManager.fig, master=self.master)
            PlotManager.canvas.get_tk_widget().pack()

    def setImageParameters(self, scale, periodLimit, timeStep):
        pass

    def makePlot(self, solution):
        pass

    @classmethod
    def getFigure(cls):
        return cls.fig

    @classmethod
    def draw(cls):
        cls.fig.tight_layout()
        cls.canvas.draw()

    @classmethod
    def clearPlots(cls):
        cls.ax.clear()
        cls.ax.set_title("Body Trajectories")
        cls.ax.set_xlabel('x, au')
        cls.ax.set_ylabel('y, au')
        cls.ax.grid(True)
        cls.ax.tick_params(direction='in')

