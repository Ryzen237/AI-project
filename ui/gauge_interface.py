# ui/gauge_interface.py
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from core.gauge_theory import GaugeField, SU3Engine
from midi.midi_handler import MidiProcessor


class GaugeControlInterface(tk.Tk):
    def __init__(self, gauge_field, su3_engine):
        super().__init__()
        self.gauge = gauge_field
        self.su3 = su3_engine
        self.midi = MidiProcessor()
        self.is_running = False
        self.build_interface()
        self.setup_bindings()

    def build_interface(self):
        """Construit l'interface complète avec tous les contrôles"""
        self.title("Contrôleur de Jauge Musicale Quantique")

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panneau de contrôle XY
        control_frame = ttk.LabelFrame(main_frame, text="Champ de Jauge U(1)")
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(control_frame, width=400, height=400, bg='white')
        self.canvas.pack()
        self.indicator = self.canvas.create_oval(195, 195, 205, 205, fill='red')

        # Visualisation mathématique
        visu_frame = ttk.LabelFrame(main_frame, text="Espace de Phase")
        visu_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=visu_frame)
        self.canvas_plot.get_tk_widget().pack()

        # Contrôles SU(3)
        su3_frame = ttk.LabelFrame(main_frame, text="Transformations SU(3)")
        su3_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.su3_sliders = []
        for i in range(8):
            slider = ttk.Scale(su3_frame,
                               from_=-1.0,
                               to=1.0,
                               orient=tk.HORIZONTAL,
                               command=lambda v, idx=i: self.update_su3(idx, float(v)))
            slider.pack(fill=tk.X, padx=5, pady=2)
            self.su3_sliders.append(slider)

        # Contrôles MIDI
        midi_frame = ttk.LabelFrame(main_frame, text="Flux MIDI Temps Réel")
        midi_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.midi_listbox = tk.Listbox(midi_frame, height=8)
        self.midi_listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(midi_frame)
        button_frame.pack(fill=tk.X)

        self.start_btn = ttk.Button(button_frame,
                                    text="Démarrer le Flux",
                                    command=self.toggle_stream)
        self.start_btn.pack(side=tk.LEFT)

        self.quantize_btn = ttk.Button(button_frame,
                                       text="Quantizer",
                                       command=self.quantize_input)
        self.quantize_btn.pack(side=tk.RIGHT)

    def setup_bindings(self):
        """Configure les interactions utilisateur"""
        self.canvas.bind("<B1-Motion>", self.update_gauge)
        self.bind("<space>", lambda e: self.toggle_stream())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_gauge(self, event):
        """Met à jour le champ de jauge via le pad XY"""
        x = (event.x / 400 - 0.5) * 2
        y = (event.y / 400 - 0.5) * 2

        # Mise à jour des paramètres
        self.gauge.A_mu[0] = x * np.pi  # Modulation de phase
        self.gauge.A_mu[1] = y * 2.0  # Intensité rythmique

        # Animation du point rouge
        self.canvas.coords(self.indicator, event.x - 5, event.y - 5, event.x + 5, event.y + 5)

        # Mise à jour de la visualisation 3D
        self.update_3d_plot(x, y)

    def update_su3(self, generator_idx, intensity):
        """Applique une transformation SU(3) au rythme"""
        transformed = self.su3.transform(
            rhythm=np.array([1, 0, 0]),  # Pattern de base
            intensity=intensity,
            generator_idx=generator_idx
        )
        self.midi.send(transformed)

    def update_3d_plot(self, x, y):
        """Met à jour la visualisation mathématique"""
        self.ax.clear()

        # Génère un tore paramétrique pour représenter l'espace U(1)
        theta = np.linspace(0, 2. * np.pi, 100)
        phi = np.linspace(0, 2. * np.pi, 100)
        theta, phi = np.meshgrid(theta, phi)

        R = 1 + 0.3 * np.sin(self.gauge.A_mu[0] * theta)
        X = R * np.cos(theta)
        Y = R * np.sin(theta)
        Z = 0.5 * np.cos(phi + self.gauge.A_mu[1])

        self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        self.canvas_plot.draw()

    def toggle_stream(self):
        """Démarre/arrête le flux MIDI"""
        self.is_running = not self.is_running
        self.start_btn.config(text="Arrêter" if self.is_running else "Démarrer")
        if self.is_running:
            self.start_stream()

    def start_stream(self):
        """Gère le flux MIDI entrant"""
        try:
            for msg in self.midi.real_time_stream():
                if self.is_running:
                    self.process_midi(msg)
                    self.update_interface()
        except Exception as e:
            self.midi_listbox.insert(tk.END, f"Erreur: {str(e)}")

    def process_midi(self, msg):
        """Traite un message MIDI entrant"""
        # Conversion et transformation
        note_data = self.midi.midi_to_array(msg)
        transformed = self.gauge.apply_transformation(note_data)

        # Envoi vers la sortie
        self.midi.send_to_max(transformed)

        # Mise à jour de l'interface
        self.midi_listbox.insert(tk.END, f"Note: {note_data} → {transformed}")
        self.midi_listbox.see(tk.END)

    def quantize_input(self):
        """Quantize les notes MIDI sur la grille rythmique"""
        quantized = self.midi.quantize(
            self.midi.buffer,
            grid=1 / 16  # Grille de 1/16ème de note
        )
        self.midi.send(quantized)

    def update_interface(self):
        """Met à jour tous les éléments de l'interface"""
        self.update_idletasks()
        self.update()

    def on_close(self):
        """Nettoyage à la fermeture"""
        self.is_running = False
        self.midi.port.close()
        self.destroy()


if __name__ == "__main__":
    # Initialisation des composants
    gauge = GaugeField(dimension=4)
    su3 = SU3Engine()

    # Lancement de l'interface
    app = GaugeControlInterface(gauge, su3)
    app.mainloop()