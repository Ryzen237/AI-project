from core.gauge_theory import GaugeField, SU3Engine
from ui.gauge_interface import GaugeControlInterface
from midi.midi_handler import MidiProcessor


def main():
    gauge = GaugeField()
    su3 = SU3Engine()
    midi = MidiProcessor()
    ui = GaugeControlInterface(gauge, su3)


    try:
        ui.mainloop()
    except KeyboardInterrupt:
        midi.port.close()


if __name__ == "__main__":
    main()