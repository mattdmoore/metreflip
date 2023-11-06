import metreflip.Utilities
from metreflip import *
from scripts import pseudorandomiser
from os import listdir, chdir

if __name__ == '__main__':
    if '__main__.py' not in listdir():  # if called as project folder
        chdir('metreflip')

    participant_id = metreflip.Utilities.highest_file_num('data/memory') + 1
    window = Screen(size=(2000, 1125))
    drum_pad = DrumPad('SPD')
    blocks = pseudorandomiser.main(participant_id)
    experiment = Experiment(participant_id, window, drum_pad, blocks)
    experiment.run()
