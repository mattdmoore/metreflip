from .Trial import *
from .SequenceMemory import *
from random import shuffle
from dataclass_csv import DataclassWriter
from psychopy import clock


class Experiment:
    def __init__(self, participant_id, window, drum_pad, blocks, base_ioi=600, iti=1):
        self.participant_id = participant_id
        self.window = window
        self.drum_pad = drum_pad
        self.blocks = blocks
        self.base_ioi = base_ioi
        self.iti = iti
        self.start_time = clock.getTime()

    def run(self, memory_trials=3):
        self.window.welcome_screen()
        for block in self.blocks.items():
            if block[0] < 2:
                train_data = self.train_block(block)
                self.write_data(train_data, TrialData)
            else:
                memory_data = self.memory_block(memory_trials)
                self.write_data(memory_data, MemoryData)
            test_data = self.test_block(block)
            self.write_data(test_data, TrialData, skip_header=block[0])

    def train_block(self, block):
        block_idx, trials = block
        trials = {key: val for key, val in trials.items() if not val['foil']}
        trials = self.shuffle_trials(trials)
        train_data = []

        self.window.training()
        for trial_idx, (rhythm_idx, parameters) in enumerate(trials.items()):
            trial = Trial(self, rhythm_idx, parameters)
            data = trial.train(trial_idx=trial_idx + block_idx * len(trials),
                               block_idx=block_idx)
            train_data.append(data)
        return train_data

    def test_block(self, block):
        block_idx, trials = block
        trials = self.shuffle_trials(trials)
        test_data = []

        self.window.testing(bool(block_idx))
        for trial_idx, (rhythm_idx, parameters) in enumerate(trials.items()):
            trial = Trial(self, rhythm_idx, parameters)
            data = trial.test(trial_idx=trial_idx + block_idx * len(trials),
                              block_idx=block_idx)
            test_data.append(data)
        return test_data

    def memory_block(self, n=3):
        memory_data = []
        for _ in range(n):
            task = SequenceMemory(self)
            memory_data.append(task.run())
        return memory_data

    def write_data(self, data, data_class, skip_header=False):
        data_path = "data/" if data_class == TrialData else "data/memory/"
        with open(data_path + "participant_{}.csv".format(self.participant_id), "a") as f:
            print(data)
            w = DataclassWriter(f, data, data_class)
            w.write(skip_header=skip_header)

    @staticmethod
    def shuffle_trials(trials):
        items = list(trials.items())
        shuffle(items)
        return dict(items)
