import mido
from psychopy.clock import Clock


class DrumPad:
    def __init__(self, device=''):
        # Device
        self.device = device
        self.port = mido.open_input(name=self._get_device(),
                                    callback=self._callback)

        # States
        self._default_msg = mido.Message('note_on', channel=9, note=60)
        self.listening = False
        self.msg = self._default_msg
        self.clock = Clock()
        self.taps = []

    def _get_device(self):
        inputs = mido.get_input_names()
        devices = [match for match in inputs if self.device in match]
        devices = list(dict.fromkeys(devices))

        if len(devices) == 0:
            raise ValueError('No device found matching name: {}'.format(self.device))

        if len(devices) == 1:
            return devices[0]

        prompt = ''.join(['{}: {}\n'.format(i, device) for i, device in enumerate(devices)])
        print(prompt, '\n')

        while idx := input('Select a device:') or len(devices) - 1:
            try:
                print(devices[int(idx)])
                return devices[int(idx)]
            except IndexError:
                print('Index out of range')
                continue
            except ValueError:
                print('Invalid input')
                continue

    def _callback(self, msg):
        msg.time = self.clock.getTime()
        if self._filter_message(msg):
            self.msg = msg
            # print(self.msg)
            self.taps.append(msg)

    def _filter_message(self, msg, cooldown=.1):
        if not self.listening:
            return
        if msg.type != 'note_on':
            return
        if msg.velocity == 0:
            return
        if (msg.time - self.msg.time) < cooldown:
            return
        return msg

    def listen(self, delay=0):
        self.reset(delay)
        self.listening = True

    def stop(self):
        self.listening = False

    def reset(self, delay=0):
        self.clock.reset(delay)
        self.listening = False
        self.msg = self._default_msg
        self.taps = []


class DummyPad:
    def __init__(self):
        self.taps = []
        pass

    def listen(self):
        pass

    def stop(self):
        pass

    def reset(self):
        pass
