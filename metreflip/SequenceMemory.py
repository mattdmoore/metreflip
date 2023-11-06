from random import randint
from .Grid import Grid
from .TrialData import MemoryData
from psychopy import clock


class SequenceMemory:
    def __init__(self, experiment):
        self.experiment = experiment
        self.grid = Grid(experiment.window)
        self.sequence = Sequence()

    def run(self, max_length=20):
        start_time = clock.getTime()
        while not (result := self.grid.copy_sequence(self.sequence)):
            if len(self.sequence) == max_length:
                return self.finish(result, start_time, clock.getTime())
            self.sequence.grow()
        return self.finish(result, start_time, clock.getTime())

    def finish(self, result, start_time, end_time):
        self.grid.window.wait(1)
        for square in self.grid.squares.values():
            square.setAutoDraw(False)
        return MemoryData(participant_id=self.experiment.participant_id,
                          sequence=[s for s in self.sequence],
                          result=result,
                          start_time=start_time-self.experiment.start_time,
                          end_time=end_time-self.experiment.start_time)


class Sequence(list):
    def __init__(self):
        super().__init__([randint(1, 9)])

    def grow(self):
        while (val := randint(1, 9)) in self[-2:]:
            continue
        self.append(val)

    def correct(self, other):
        return all([a == b for a, b in zip(self, other)]) if self.finished(other) else None

    def finished(self, other):
        return len(self) == len(other)
