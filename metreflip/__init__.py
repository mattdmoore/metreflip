__all__ = [
    # Classes
    'DrumPad',
    'DummyPad',
    'Rhythms',
    'Stimulus',
    'Experiment',
    'Screen',
    'Grid',

    # Variables
    'devices',
    'device_info',

    # Functions
    'last_cached',

    # Constants
    'DEFAULT_SAMPLE_RATE',
    'TIME',
    'RHYTHMS',
    'RHYTHM_PARAMETERS',
]

from psychopy.preferences import prefs
from psychopy.tools import systemtools
from rhythm_parameters import *
from .DrumPad import *
from .Rhythms import *
from .Screen import *
from .Utilities import *
from .Grid import *
from .SequenceMemory import *

RHYTHMS = Rhythms(12)

TIME = {
    'ms': 1e3,
    'milliseconds': 1e3,
    's': 1,
    'seconds': 1
}

prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 3

devices = systemtools.getAudioDevices()
preferred_device = ['Scarlett', 'FireFace']

if len([device := key for key in devices.keys()  # If exactly one match for preferred device
        for p in preferred_device if p in key]) == 1:
    prefs.hardware['audioDevice'] = device
else:
    prompt = '\n'.join('{}: {}'.format(i, key) for i, key in enumerate(devices.keys()))
    print(prompt, '\n')
    while idx := input('Select audio device: ') or len(devices) - 1:
        try:
            idx = int(idx)
            device = list(devices.keys())[idx]
            prefs.hardware['audioDevice'] = device
            break
        except IndexError:
            print('Index out of range')
            continue
        except ValueError:
            print('Invalid input')
            continue

device_info = devices[device]
# DEFAULT_SAMPLE_RATE = devices[device]['defaultSampleRate']
DEFAULT_SAMPLE_RATE = 96e3

print('Audio settings:')
print('\n'.join('\t{}: {}'.format(key, value) for key, value in prefs.hardware.items()))
print('Device info: ')
print('\n'.join('\t{}: {}'.format(key, value) for key, value in devices[device].items()))

from .Experiment import *
from .Stimulus import *

if __name__ == "__main__":
    pass
