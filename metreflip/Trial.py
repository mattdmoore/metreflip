from metreflip import RHYTHMS
from .Stimulus import *
from .TrialData import TestData, TrainData
from psychopy import clock
from random import random


class Trial:
    def __init__(self, experiment, rhythm_idx, parameters):
        self.experiment = experiment
        self.parameters = parameters
        self.rhythm = RHYTHMS[rhythm_idx].rotate(parameters['rotation'])
        self.rhythm_idx = rhythm_idx

    def __repr__(self):
        return str([self.rhythm, self.parameters])

    def train(self, trial_idx, block_idx, metre_loops=4, rhythm_loops=8):
        taps = []
        for i in range(2):
            ioi = self.experiment.base_ioi // (3 + i)
            cycle_duration = ioi * len(self.rhythm) / 1e3

            metre_stimulus = MetreStimulus(self.parameters['metre'], ioi=ioi)
            rhythm_stimulus = RhythmStimulus(self.rhythm, ioi=ioi)

            # Start context beat
            metre_stimulus.play(loops=metre_loops)
            self.experiment.drum_pad.listen()
            flip_interval = self.experiment.window.fixation_cross('Listen\n\n\nContext beat')
            clock.wait(cycle_duration - flip_interval)

            # Tap along
            flip_interval = self.experiment.window.fixation_cross('Tap along\n\n\nContext beat')
            clock.wait((metre_loops - 1) * cycle_duration - flip_interval)

            # Start rhythm
            rhythm_stimulus.play(loops=rhythm_loops)
            flip_interval = self.experiment.window.fixation_cross('Tap along\n\n\nRhythm {} ({})'
                                                                  .format(trial_idx + 1, ['slow', 'fast'][i]))
            clock.wait(rhythm_loops * cycle_duration - flip_interval)

            self.experiment.window.flip()
            clock.wait(self.experiment.iti + (random() - .5) * self.experiment.iti / 10)

            self.experiment.drum_pad.stop()
            taps.append([t.time for t in self.experiment.drum_pad.taps])

        result = TrainData(participant_id=self.experiment.participant_id,
                           block_idx=block_idx,
                           trial_idx=trial_idx,
                           rhythm_idx=self.rhythm_idx,
                           rotation=self.parameters['rotation'],
                           metre=self.parameters['metre'],
                           taps=taps)
        return result

    def test(self, trial_idx, block_idx, metre_loops=4, rhythm_loops=4):
        ioi = self.experiment.base_ioi // self.parameters['metre']

        null_metre_stimulus = MetreStimulus(self.parameters['metre'],
                                            ioi=ioi,
                                            null=True,
                                            invert=self.parameters['invert'])
        rhythm_stimulus = RhythmStimulus(self.rhythm, ioi=null_metre_stimulus.ioi)

        cycle_duration = null_metre_stimulus.ioi * len(self.rhythm) / 1e3

        if bool(block_idx):
            metre_stimulus = MetreStimulus(self.parameters['metre'],
                                           ioi=ioi,
                                           invert=self.parameters['invert'],
                                           fade_out=True)

            metre_stimulus.play()
            self.experiment.drum_pad.listen()
            flip_interval = self.experiment.window.fixation_cross('Listen\n\n\nDo not tap')
            clock.wait(cycle_duration - flip_interval)

            null_metre_stimulus.play(loops=metre_loops - 1)
            flip_interval = self.experiment.window.fixation_cross('Imagine the beat\n\n\nDo not tap')
            clock.wait((metre_loops - 1) * cycle_duration - flip_interval)
        else:
            metre_stimulus = MetreStimulus(self.parameters['metre'],
                                           ioi=ioi,
                                           invert=self.parameters['invert'])

            metre_stimulus.play(loops=metre_loops)
            self.experiment.drum_pad.listen()
            flip_interval = self.experiment.window.fixation_cross('Listen\n\n\nDo not tap')
            clock.wait(metre_loops * cycle_duration - flip_interval)

        rhythm_stimulus.play(loops=rhythm_loops)
        flip_interval = self.experiment.window.fixation_cross('Did you tap along with this rhythm before?\n\n\n')
        clock.wait(rhythm_loops * cycle_duration - flip_interval)

        t0 = clock.getTime()
        correct_response = self.experiment.window.test_prompt(self.parameters['foil'])
        reaction_time = clock.getTime() - t0
        self.experiment.drum_pad.stop()
        taps = [t.time for t in self.experiment.drum_pad.taps]

        result = TestData(participant_id=self.experiment.participant_id,
                          block_idx=block_idx,
                          trial_idx=trial_idx,
                          rhythm_idx=self.rhythm_idx,
                          rotation=self.parameters['rotation'],
                          metre=metre_stimulus.beat,
                          foil=self.parameters['foil'],
                          taps=taps,
                          invert=self.parameters['invert'],
                          correct_response=correct_response,
                          reaction_time=reaction_time)
        return result


class Practice(Trial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
