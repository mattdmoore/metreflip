from dataclasses import dataclass


@dataclass(frozen=True)
class TrialData:
    participant_id: int
    block_idx: int
    trial_idx: int
    rhythm_idx: int
    rotation: int
    metre: int
    foil: bool
    taps: list
    invert: bool = None
    correct_response: bool = None


@dataclass(frozen=True)
class TrainData:
    participant_id: int
    block_idx: int
    trial_idx: int
    rhythm_idx: int
    rotation: int
    metre: int
    taps: list


@dataclass(frozen=True)
class TestData:
    participant_id: int
    block_idx: int
    trial_idx: int
    rhythm_idx: int
    rotation: int
    metre: int
    foil: bool
    taps: list
    invert: bool = None
    correct_response: bool = None
    reaction_time: float = None


@dataclass(frozen=True)
class MemoryData:
    participant_id: int
    sequence: list
    result: list
    start_time: float
    end_time: float
