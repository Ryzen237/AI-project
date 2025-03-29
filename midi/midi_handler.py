import mido
from pythonosc import udp_client


class MidiProcessor:
    def __init__(self, port_name='Virtual MIDI'):
        # Liste les ports MIDI disponibles
        available_ports = mido.get_input_names()
        print("Ports MIDI disponibles:", available_ports)  # Affiche les ports pour vérification

        # Si aucun port n'est disponible, lève une exception avec un message clair
        if not available_ports:
            raise RuntimeError("Aucun port MIDI détecté. Branche un périphérique ou utilise un port virtuel.")

        try:
            # Essaie d'ouvrir le premier port disponible
            self.port = mido.open_input(available_ports[0])
            print(f"Port MIDI ouvert: {available_ports[0]}")
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'ouverture du port MIDI: {str(e)}")

        # Initialisation du client OSC
        self.osc_client = udp_client.SimpleUDPClient('127.0.0.1', 7000)

    def real_time_stream(self):
        while True:
            # Traite les messages MIDI en attente
            for msg in self.port.iter_pending():
                yield msg
