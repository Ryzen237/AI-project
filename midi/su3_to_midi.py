import mido
from mido import Message, MidiFile, MidiTrack


class SU3MidiConverter:
    def __init__(self, bpm=120):
        self.ticks_per_beat = 480
        self.tempo = mido.bpm2tempo(bpm)

    def polyrhythm_to_midi(self, rhythm, output_file='poly.mid'):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        track.append(MetaMessage('set_tempo', tempo=self.tempo))

        for value in rhythm:
            note_on = Message('note_on', note=60, velocity=int(127 * abs(value)), time=0)
            note_off = Message('note_off', note=60, time=int(self.ticks_per_beat * abs(value)))
            track.extend([note_on, note_off])

        mid.save(output_file)