from psychopy import visual, event, core
from os import listdir
from time import sleep


class Screen(visual.Window):
    def __init__(self, brightness=-.745, *args, **kwargs):
        self._queue = []
        super().__init__(
            color=(brightness,) * 3,
            allowGUI=False,
            waitBlanking=False,
            *args, **kwargs)
        self.mouse = event.Mouse(visible=False, win=self)
        self.frame_rate = self.getActualFrameRate(nIdentical=60, nMaxFrames=300)

        files = sorted(listdir('./instructions'))
        self.pages = [visual.ImageStim(self, './instructions/' + f) for f in files]

    def keyboard_response(self, close=False, any_key=False, num=False, auto_flip=False, poll_rate=100):
        key_options = {'left': -1,
                       'right': 1,
                       'return': 0,
                       'escape': 'close'}

        event.clearEvents()
        while not (key := event.getKeys()):
            self.flip() if auto_flip else core.wait(1 / poll_rate)

        if (key := key[0]) in key_options.keys():
            if key_options[key] == 'close':
                if close:
                    core.quit()
                return self.keyboard_response(close=True)
            else:
                return key_options[key]
        elif num:
            key = [int(s) for s in key if s.isdigit()]
            return key[0] if key else self.keyboard_response(num=True)
        elif any_key:
            return key
        else:
            return self.keyboard_response()

    def fixation_cross(self, text=None, size=10):
        t = self.getFutureFlipTime()
        fixation = [visual.Line(win=self, start=[-size, 0], end=[size, 0], units='pix'),
                    visual.Line(win=self, start=[0, -size], end=[0, size], units='pix')]

        if text:
            text = visual.TextStim(win=self,
                                   text=text,
                                   pos=[0, 0],
                                   font='Roboto')
            text.draw()
        [line.draw() for line in fixation]
        self.flip()
        return self.getFutureFlipTime() - t

    def welcome_screen(self, resume=False):
        self.pages[0].draw()
        self.flip()

        self.keyboard_response(any_key=True)
        return None if resume else self.instructions()

    def instructions(self):
        def clamp(x, lower, upper): return lower if x < lower else upper if x > upper else x

        first, last = 1, 7
        i = first
        while True:
            self.pages[i].draw()
            self.flip()

            if (key := self.keyboard_response()) == 0 and i == last:
                self.flip()
                return
            i = clamp(i + key, first, last)

    def training(self):
        self.pages[9].draw()
        self.flip()
        while self.keyboard_response() != 0:
            continue

    def testing(self, block):
        self.pages[10 + block].draw()
        self.flip()
        while self.keyboard_response() != 0:
            continue

    def test_prompt(self, foil):
        self.pages[13].draw()
        self.flip()
        while (key := self.keyboard_response()) not in (-1, 1):
            continue
        return (key > 0) == foil

    def inter_block_break(self):
        self.pages[8].draw()
        self.flip()
        while self.keyboard_response() != 0:
            continue

    def callAfterFlip(self, function, *args, **kwargs):
        self._queue.append({'function': function,
                            'args': args,
                            'kwargs': kwargs})

    def wait(self, duration):
        for _ in range(int(duration * self.frame_rate)):
            self.flip()

    def flip(self, *args, **kwargs):
        now = super().flip(*args, **kwargs)
        self._toCall = self._queue
        self._queue = []
        return now
