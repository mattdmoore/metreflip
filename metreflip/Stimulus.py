from __future__ import annotations

from metreflip import DEFAULT_SAMPLE_RATE, TIME
from psychopy import sound
import numpy as np


class _Tone:
    def __init__(self,
                 duration=50,
                 amplitude=1,
                 sample_rate=DEFAULT_SAMPLE_RATE,
                 unit='ms'):

        self.unit = TIME[unit]
        self.sample_rate = sample_rate

        self.duration = duration / self.unit
        self.amplitude = amplitude

        self.n_samples = int(sample_rate * self.duration)
        self.t = np.arange(self.n_samples, dtype=np.float32)
        self.samples = np.zeros(self.t.shape)

        self.curves = {'linear': self._linear,
                       'quadratic': self._quadratic,
                       'exponential': self._exponential}

    def append_silence(self, duration):
        self.samples = np.pad(self.samples, (0, int(self.sample_rate * duration / self.unit)), constant_values=0)

    def __add__(self, other: _Tone) -> _Tone:
        self.samples = np.append(self.samples, other.samples)
        return self

    def __iadd__(self, other: _Tone) -> _Tone:
        return self + other

    def __mul__(self, other: int) -> _Tone:
        self.samples = np.tile(self.samples, other)
        return self

    @staticmethod
    def _envelope(func):
        def wrapper(self, duration, reverse=False, *args, **kwargs):
            idx = int(self.sample_rate * duration / self.unit)
            if reverse:
                self.samples[:len(self.samples) - (1 + idx):-1] *= func(0, 1, idx, *args, **kwargs) * self.amplitude
            else:
                self.samples[:idx] *= func(0, 1, idx, *args, **kwargs) * self.amplitude

        return wrapper

    @_envelope
    def _linear(*args, **kwargs):
        return np.linspace(*args, **kwargs)

    @_envelope
    def _quadratic(*args, **kwargs):
        return np.linspace(*args, **kwargs) ** 2

    @_envelope
    def _exponential(*args, **kwargs):
        args = list(args)
        args[0] += 1e-3
        args[2] -= 1
        return np.append(0, np.geomspace(*args, **kwargs))


class Sine(_Tone):
    def __init__(self,
                 silence,
                 duration=50,
                 frequency=(220, 440),
                 attack=2,
                 decay=48,
                 attack_curve='linear',
                 decay_curve='quadratic',
                 *args, **kwargs):
        super().__init__(duration, *args, **kwargs)
        if isinstance(frequency, int):
            frequency = (frequency,)
        self.samples = sum(
            [np.sin(2 * np.pi * self.t * f / self.sample_rate) * self.amplitude for f in frequency]) / len(frequency)
        self.curves[attack_curve](attack)
        self.curves[decay_curve](decay, reverse=True)
        self.append_silence(silence - duration)


class RhythmStimulus(sound.Sound):
    def __init__(self, rhythm, ioi, *args, **kwargs):
        self.waveform = Sine(silence=ioi, *args, **kwargs)
        for onset in rhythm[1:]:
            if onset:
                self.waveform += Sine(silence=ioi, *args, **kwargs)
            else:
                self.waveform.append_silence(ioi)
        super().__init__(self.waveform.samples, sampleRate=self.waveform.sample_rate)


class MetreStimulus(sound.Sound):
    def __init__(self, beat, ioi, cycle=12, null=False, invert=False, fade_out=False, *args, **kwargs):

        self.beat = cycle // beat if invert else beat
        self.ioi = ioi // (self.beat / beat) if invert else ioi

        if null:
            self.beat = cycle + 1

        for i in range(cycle):
            if i % cycle == 0:
                if i == 0:
                    self.waveform = Sine(silence=self.ioi,
                                         frequency=(219, 220, 221, 440, 880),
                                         *args, **kwargs)
                else:
                    self.waveform += Sine(silence=self.ioi,
                                          frequency=(219, 220, 221, 440, 880),
                                          *args, **kwargs)
            elif i % self.beat == 0:
                self.waveform += Sine(silence=self.ioi,
                                      frequency=(218, 219, 220, 221, 222),
                                      amplitude=(cycle * 1.5 - i) / (cycle * 1.5) if fade_out else 1,
                                      *args, **kwargs)

            else:
                self.waveform += Sine(silence=self.ioi,
                                      frequency=(218, 219, 220, 221, 222),
                                      amplitude=.25,
                                      *args, **kwargs)
        super().__init__(self.waveform.samples, sampleRate=self.waveform.sample_rate)
