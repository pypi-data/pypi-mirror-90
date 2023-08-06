import optparse
from pathlib import Path
from sys import exit, stderr
from typing import Final, List

import json5 as json
from cerberus import Validator

from exclock.entities import ClockTimer
from exclock.util import (
    get_real_json_filename,
    get_real_sound_filename,
    is_time_delta_cerberus_validate,
)


def get_title_from_json_filename(json_filename: str) -> str:
    basename = Path(json_filename).name
    return basename.split('.')[0].capitalize()


CLOCK_JSON_SCHEMA: Final[dict] = {
    'sounds':
        {
            'type': 'dict',
            'required': True,
            'keysrules': {
                'type': 'string',
                'check_with': is_time_delta_cerberus_validate,
            },
            'valuesrules':
                {
                    'type': 'dict',
                    'schema':
                        {
                            'message': {
                                'type': 'string',
                                'required': True,
                            },
                            'sound_filename': {
                                'type': 'string',
                            },
                        },
                }
        },
    'loop': {
        'type': 'integer',
        'nullable': True,
    },
    'show_message': {
        'type': 'boolean',
    },
    'title': {
        'type': 'string',
    }
}


def check_raw_clock(d) -> None:
    if type(d) != dict:
        raise ValueError("clock file err: doesn't mean dict.")

    # cerberus
    validator = Validator(CLOCK_JSON_SCHEMA, allow_unknown=True)
    validator.validate(d)

    if validator.errors:
        raise ValueError(
            '\n'.join([f'{key}: {values}' for key, values in validator.errors.items()]))

    # check to exist sound_filename
    for time_s, sound in d['sounds'].items():
        sound_filename = sound.get('sound_filename')
        sound_filename = get_real_sound_filename(sound_filename)

        if not Path(sound_filename).exists():
            raise FileNotFoundError(f"clock file err: {sound['sound_filename']} is not found.")


def main(opt: optparse.Values, args: List[str]) -> None:
    if len(args) != 1:
        print('Length of argument should be 1.', file=stderr)
        exit(1)

    json_filename = get_real_json_filename(args[0])
    try:
        with open(json_filename) as f:
            jdata = json.load(f)
    except ValueError as err:
        print(f'{json_filename} is Incorrect format for json5:\n' + f'{err.args[0]}', file=stderr)
        exit(1)
    except FileNotFoundError:
        print(f'{args[0]} is not found.', file=stderr)
        exit(1)

    try:
        check_raw_clock(jdata)
    except Exception as err:
        print(err.args[0], file=stderr)
        exit(1)

    show_message = jdata.get('show_message', False)
    jdata['title'] = jdata.get('title', get_title_from_json_filename(json_filename))
    clock_timer = ClockTimer.from_dict(jdata)
    try:
        clock_timer.run(show_message=show_message)
    except KeyboardInterrupt:
        ...
    finally:
        print('bye')
