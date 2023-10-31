from psychopy import visual


class Grid:
    def __init__(self, window, size=150, margin=50, dims=(3, 3)):
        self.window = window
        self.squares = {row + (col * dims[0]):
                        Square(window,
                               pos=(row * (size + margin) - (dims[0] - 1) * (size + margin) / 2,
                                    col * (size + margin) - (dims[1] - 1) * (size + margin) / 2),
                               size=size)
                        for col in range(dims[1])
                        for row in range(dims[0])}

    def __getitem__(self, item):
        return self.squares[item]

    def copy_sequence(self, sequence, attempt=0, max_attempts=2, interval=.5, start_after=1):
        self.window.wait(start_after)
        for s in sequence:
            self[s - 1].activate()
            self.window.wait(interval)

        response = []
        while not sequence.finished(response):
            key = self.window.keyboard_response(num=True, auto_flip=True)
            response.append(key)
            self[key-1].activate(correct=sequence.correct(response))

        if not sequence.correct(response):
            if attempt == max_attempts - 1:
                self.window.wait(1)
                return response
            return self.copy_sequence(sequence, attempt=attempt+1)

        return None


class Square(visual.Rect):
    def __init__(self, window, brightness=-.2, *args, **kwargs):
        self.window = window
        self.brightness = (brightness,) * 3
        super().__init__(win=window,
                         autoDraw=True,
                         units='pix',
                         *args, **kwargs)
        self.fillColor = brightness

    def activate(self, delay=.15, correct=None):
        if correct is not None:
            self.fillColor = (0, 1, 0) if correct else (1, 0, 0)
        else:
            self.fillColor = (1, 1, 1)
        self._fade(delay=delay)

    def _fade(self,
              delay=None, delay_frames=None,
              duration=.15, duration_frames=None,
              increment=None, frame=0):
        if delay or delay_frames:
            if not delay_frames:
                delay_frames = int(self.window.frame_rate * delay)
            if frame < delay_frames:
                self.window.callAfterFlip(self._fade,
                                          delay_frames=delay_frames,
                                          duration=duration,
                                          frame=frame+1)
            else:
                self.window.callAfterFlip(self._fade, duration=duration)

        else:
            if not duration_frames:
                duration_frames = int(self.window.frame_rate * duration)
                increment = [(a - b) / duration_frames for a, b in zip(self.brightness, self.fillColor)]
            if frame < duration_frames:
                self.fillColor = [a + b for a, b in zip(self.fillColor, increment)]
                self.window.callAfterFlip(self._fade,
                                          duration_frames=duration_frames,
                                          increment=increment,
                                          frame=frame+1)
