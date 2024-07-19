import tkinter as tk
from tkinter import Entry, Label, Button, Text, messagebox, filedialog
from source.celestialBody import CelestialBody
from interface.simulationManager import SimulationManager
from interface.trajManager import TrajManager
from interface.plotManager import PlotManager
from source.equation import Equation
import os
import shutil
from source.const import *

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Задача двух тел в гравитационном поле с запаздыванием по Герберу")
        self.root.configure(bg="#ffffff")

        self.frameParameters = tk.Frame(root, bg="#ffffff")
        self.frameButtons = tk.Frame(root, bg="#ffffff")
        self.frameCanvas = tk.Frame(root, bg="#ffffff")

        self.simulationManager = SimulationManager(self.frameCanvas)
        self.trajManager = TrajManager(self.frameCanvas)
        self.equation = Equation()

        self.solution = []
        self.time = []

        self.create_interface()

    def create_interface(self):
        self.frameParameters.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)
        self.frameButtons.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)
        self.frameCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_input_fields()
        self.create_buttons()
        self.create_log_display()

    def create_input_fields(self):
        labels = ["Star Mass (MS):", "Planet Mass (ME):", "Distance (au):", "Ecentricity:", "Time (years):", "Time Step (years):"]
        defaults = ["1.0", "1.0", "1.0", "0.0167", "10.0", "0.001"]
        self.entries = []

        for i, (label_text, default_value) in enumerate(zip(labels, defaults)):
            label = Label(self.frameParameters, text=label_text, bg="#ffffff")
            entry = Entry(self.frameParameters, bg="#ffffff")
            entry.insert(0, default_value)
            label.grid(row=i, column=0, pady=5, sticky="e")
            entry.grid(row=i, column=1, pady=5, padx=5, sticky="w")
            self.entries.append(entry)

    def create_buttons(self):
        button_data = [
            ("Run Simulation", self.runSimulation),
            ("Check", self.check),
            ("Draw Orbits", self.drawOrbits),
            ("Save Graph", self.saveGraph),
            ("Clear Graph", self.clearGraph)
        ]

        for text, command in button_data:
            button = Button(self.frameButtons, text=text, command=command, bg="#007acc", fg="white", bd=0, height=2, width=15)
            button.pack(side=tk.TOP, pady=5, padx=5)

    def create_log_display(self):
        self.logText = Text(self.frameParameters, height=10, width=40, bg="#ffffff", relief=tk.SUNKEN, bd=2)
        self.logText.grid(row=len(self.entries), column=0, columnspan=2, pady=10, padx=5, sticky="nsew")

    def update_log_display(self, log_content):
        self.logText.delete(1.0, tk.END)
        self.logText.insert(tk.END, log_content)

    def get_input_values(self):
        return [float(entry.get()) for entry in self.entries]

    def check(self):
        try:
            star_mass, planet_mass, initial_distance, ecentricity, _, _ = self.get_input_values()
            bodies = CelestialBody(star_mass, planet_mass)
            period = bodies.getPeriod(initial_distance, ecentricity)
            precession = bodies.getPrecession(initial_distance, ecentricity)
            beta = bodies.getBetaMax(initial_distance, ecentricity)

            log_content = (
                f"Kepler's Period:  {period:.5f}\n"
                f"Precession:       {precession:.1f}\n"
                f"Beta Max:         {beta:.5f}\n"
            )
            self.update_log_display(log_content)
        except Exception as e:
            messagebox.showerror("Parameter Check", f"Error checking parameters: {e}")

    def get_params(self, manager):
        try:
            star_mass, planet_mass, initial_distance, ecentricity, time, time_step = self.get_input_values()
            bodies = CelestialBody(star_mass, planet_mass)

            self.equation.setEquation(bodies)
            self.equation.setConditions(bodies.getState(initial_distance, ecentricity), time, time_step)
            results, times = self.equation.solution()

            self.process_results(manager, bodies, initial_distance, ecentricity, results, times, time_step)
        except Exception as e:
            messagebox.showerror("Parameter Check", f"Error solving equation: {e}")

    def process_results(self, manager, bodies, initial_distance, ecentricity, results, times, time_step):
        period = bodies.getPeriod(initial_distance, ecentricity)
        precession = bodies.getPrecession(initial_distance, ecentricity)
        beta = bodies.getBetaMax(initial_distance, ecentricity)
        manager.setImageParameters(initial_distance * 1.1, period, time_step)

        real_period, real_precession = self.equation.findPrecession(results, times, initial_distance, ecentricity)

        manager.makePlot(self.equation.convertToDecart(results))
        PlotManager.draw()

        log_content = (
            f"Kepler's Period:  {period:.5f}\n"
            f"Precession:       {precession:.5f}\n"
            f"Beta Max:         {beta:.5f}\n"
            f"Culc. Period:     {real_period:.5f}\n"
            f"Culc. Precession: {real_precession:.5f}\n"
        )
        self.update_log_display(log_content)

    def runSimulation(self):
        self.get_params(self.simulationManager)

    def drawOrbits(self):
        self.get_params(self.trajManager)

    def saveGraph(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if filename:
                PlotManager.getFigure().savefig(filename)
                messagebox.showinfo("Save Graph", f"Graph saved as {filename}")
        except Exception as e:
            messagebox.showerror("Save Graph", f"Error saving graph: {e}")

    def clearGraph(self):
        self.time = []
        self.solution = []
        PlotManager.clearPlots()
        PlotManager.draw()
