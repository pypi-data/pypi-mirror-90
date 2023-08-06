from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Final, List, Optional

from ycontract import contract

from exclock.sound_player import Player
from exclock.util import get_real_sound_filename, get_time_delta_from_str, notify_all

DEFAULT_TITLE: Final[str] = 'ExClock'


def inner_str(s: str, d: dict) -> str:
    start_secs: List[int] = []
    end_secs: List[int] = []
    for i, c in enumerate(s):
        if len(start_secs) == len(end_secs) and c == '{':
            start_secs.append(i)
        if len(start_secs) == len(end_secs) + 1 and c == '}':
            end_secs.append(i)

    calcs = dict()
    for start, end in zip(start_secs, end_secs):
        target = s[start + 1:end]
        calcs[target] = eval(target, {}, d)

    for key, val in calcs.items():
        s = s.replace('{' + key + '}', str(val))
    return s


@dataclass
class Sound:
    message: str
    sound_filename: str

    def __post_init__(self) -> None:
        self.sound_filename = get_real_sound_filename(self.sound_filename)

    @contract(lambda self: Path(self.sound_filename).exists())
    def play(self):
        p = Player(self.sound_filename)
        p.play()

    @classmethod
    @contract(
        lambda json: 'message' in json,
        lambda json: isinstance(json.get('sound_filename', 'dummy'), str),
    )
    def from_dict(cls, json: dict) -> Sound:
        return Sound(
            message=json['message'],
            sound_filename=get_real_sound_filename(json.get('sound_filename')),
        )

    @contract(lambda other: type(other) == Sound)
    def __eq__(self, other) -> bool:
        return self.message == other.message and self.sound_filename == other.sound_filename


@dataclass
class ClockTimer:
    sounds: Dict[int, Sound]  # Dict from sec to sound
    loop: Optional[int]
    title: str

    @property
    def sorted_sounds(self) -> Dict[int, Sound]:
        return {sec: self.sounds[sec] for sec in sorted(self.sounds)}

    @contract(lambda count: count >= 0)
    def run_once(self, count: int, show_message: bool) -> None:
        sounds = self.sorted_sounds

        ps = []

        secs = list(sounds.keys())
        for i, (sec, sound) in enumerate(sounds.items()):
            spend_sec = secs[i] - (0 if i == 0 else secs[i - 1])
            message = inner_str(sound.message, {'count': count})
            notify_all(
                title=self.title,
                message=message,
                spend_sec=spend_sec,
                is_first=sec == 0 and count == 1,
                show_message=show_message,
            )

            ps.append(sound.play())

    def run(self, *, show_message: bool) -> None:
        count = 1
        if isinstance(self.loop, int):
            for _ in range(self.loop):
                self.run_once(count=count, show_message=show_message)
                count += 1
        else:
            while True:
                self.run_once(count=count, show_message=show_message)
                count += 1

    @classmethod
    @contract(
        lambda json: isinstance(json, dict),
        lambda json: 'sounds' in json,
    )
    def from_dict(cls, json: dict) -> ClockTimer:
        sounds = {}
        for sec, sound in json['sounds'].items():
            sec = get_time_delta_from_str(sec)
            sounds[sec] = Sound.from_dict(sound)

        return ClockTimer(sounds=sounds, loop=json.get('loop', 1), title=json['title'])
