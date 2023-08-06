"""Main module."""

import itertools
import math
import os

from PIL import Image


LIGHTHOUSES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'lighthouses'
)

COLOURS = {
    'R': (255, 0, 0, 1),
    'G': (0, 255, 0, 1),
    'W': (255, 255, 255, 1),
    'Y': (255, 255, 0, 1),
    'Off': (0, 0, 0, 0)
}


def save_characteristic_as_image(
    description, size, write_buffer, base_img=None
):

    on_img, off_img = load_base_images(base_img)
    size = on_img.size if on_img is not None else size

    frames, durations = states_to_frames(
        size, collapse_states(characteristic_to_light_states(description)),
        on_img, off_img
    )
    frames = [frame.convert('RGB') for frame in frames]
    if len(frames) > 1:
        save_options = {
            "format": "GIF",
            "save_all": True,
            "append_images": frames[1:],
            "duration": durations,
            "loop": 0
        }
        if base_img is None:
            # If this is just a block light, these settings allow "Off"
            # to be fully transparent
            # Leaving them in place for images with lighthouses
            # can cause odd effects, due to combining palettes.
            save_options.update(
                {
                    "transparency": 0,
                    "optimize": False,
                    "disposal": 3
                }
            )

        frames[0].save(
            write_buffer, **save_options
        )
    else:
        frames[0].save(write_buffer, format="GIF")


def load_base_images(base_img):
    """
    Return the two base images needed to create a lighthouse animation.
    base_img is either

    - A full/relative path from the run context
    - The name of a directory under lighthouses here
    """
    if base_img is not None:
        if not os.path.exists(base_img):
            base_img = os.path.join(LIGHTHOUSES_DIR, base_img)
        return (
            Image.open(os.path.join(base_img, 'on.gif')).convert('RGBA'),
            Image.open(os.path.join(base_img, 'off.gif'))
        )
    return None, None


def characteristic_to_light_states(description):
    """
    Given a light characteristic, return a list of 2-tuples representing the
    state of light at any given time.

    A fixed light is the given colour, permanently

    >>> characteristic_to_light_states('F. R')
    [('R', 1)]
    """
    fragments = description.split()

    pattern_type, groups = parse_pattern(fragments.pop(0))
    colour, fragments = get_colour_code(fragments)
    try:
        period = parse_period(fragments)
    except IndexError:
        if must_have_period(pattern_type, groups):
            raise
        period = None
    if period is not None and cannot_have_period(pattern_type, groups):
        raise ValueError('Period is not allowed in this type of light')
    return TYPES[pattern_type](groups, colour, period)


def get_colour_code(fragments):

    if len(fragments) == 0 or fragments[0] not in COLOURS.keys():
        return 'W', fragments
    return fragments[0], fragments[1:]


def parse_period(fragments):
    """
    Given the split up characteristic, return the period in milliseconds

    The period is specified in seconds

    >>> parse_period(['2'])
    2000

    The letter 's' to mark the units may be present

    >>> parse_period(['3s'])
    3000

    It may be separated from the number by a space

    >>> parse_period(['4','s'])
    4000

    A Quick flash can only have a period if it has groups

    >>> parse_period(['3s'])
    3000
    """
    period_spec = fragments[-1]
    # The last term is the cycle period,
    # it may or may not have 's' for seconds
    # The 's' may or may not be attached to the number
    if period_spec == 's':
        period_spec = fragments[-2]
    if period_spec[-1] == 's':
        period_spec = period_spec[:-1]
    return int(float(period_spec) * 1000)


def cannot_have_period(pattern_type, groups):
    return pattern_type == 'f' or (pattern_type == 'q' and groups == [1])


def must_have_period(pattern_type, groups):
    return not(cannot_have_period(pattern_type, groups))


def parse_pattern(pattern):
    """
    Crack a pattern definition into its type and any grouping.

    A pattern consists of the pattern type (e.g. flashing, occulting)
    and optionally a group designation in parentheses.

    The pattern definition could just be the type

    >>> parse_pattern('Fl')
    ('fl', [1])

    It could have optional dots marking the abbreviation,
    these can be discarded

    >>> parse_pattern('L.Fl.')
    ('lfl', [1])

    It could have grouping information in parentheses

    >>> parse_pattern('Fl(2)')
    ('fl', [2])

    The group could be a composite group.

    >>> parse_pattern('Oc(2+1)')
    ('oc', [2, 1])
    """
    pattern_type, _, group_spec = pattern.partition('(')
    # Groups are separated by '+' in a composite pattern.
    groups = [
        int(group) for group in group_spec[:-1].split('+')
    ] if group_spec else [1]

    # Some light lists use dots, some don't, just throw them away
    return pattern_type.lower().replace('.', ''), groups


def collapse_states(states):
    """
    Given a list of light states, collapse any adjacent entries that have the
    same state.

    If there are no adjacent matching states, there is no change to the output

    >>> collapse_states([('R',1), ('Y', 1), ('R', 1)])
    [('R', 1), ('Y', 1), ('R', 1)]

    Adjacent states are collapsed, summing their durations

    >>> collapse_states([('R',1), ('R', 1), ('Y', 1)])
    [('R', 2), ('Y', 1)]

    >>> collapse_states([('R',1), ('R', 2), ('R', 3), ('Y', 1)])
    [('R', 6), ('Y', 1)]
    """
    new_states = states[:1]

    for state in states[1:]:
        last_state = new_states[-1]
        if state[0] == last_state[0]:
            new_states[-1] = (state[0], last_state[1] + state[1])
        else:
            new_states.append(state)
    return new_states


def states_to_frames(size, states, fg, off_img):

    def create_frame(colour):
        if colour == 'Off' and fg is not None:
            return off_img
        colour_img = Image.new('RGBA', size, color=COLOURS[colour])
        if fg is not None:
            colour_img.alpha_composite(fg)
        return colour_img
    return [
        create_frame(state[0])
        for state in states
    ], [state[1] for state in states]


def light_sequence(
    groups, colour1, colour2, total_period, colour1_period, colour2_period
):
    flash_period = colour1_period + colour2_period
    group_states = [
        single_flash(
            group, colour1, colour2, colour1_period, colour2_period
        ) for group in groups
    ]

    # When there are multiple groups,
    # the remainder is shared equally between each of them.
    # If the remainder is not perfectly divisible by the number of groups,
    # the final period swallows up the spare.
    # Being as this is calculated in milliseconds, this is imperceptible.
    remainder = total_period - (flash_period * sum(groups))
    remainder_share = math.floor(remainder/len(groups))
    final_remainder = remainder - (remainder_share * (len(groups)-1))

    for group_state in group_states[:-1]:
        group_state.append((colour2, remainder_share))
    group_states[-1].append((colour2, final_remainder))
    return list(itertools.chain.from_iterable(group_states))


def single_flash(flash_count, colour1, colour2, period1, period2):
    return [(colour1, period1), (colour2, period2)] * flash_count


def fixed(_groups, colour, _period):
    """
    The Fixed pattern is simply an always-on light in the given colour.
    groups and period are irrelevant.
    """
    return [(colour, 1)]


def flash(groups, colour, period):
    """
    A flash is a single colour displayed for a short period, followed by
    a longer period of darkness

    A single flash of a given colour is a 1 second flash

    >>> flash([1], 'R', 5000)
    [('R', 1000), ('Off', 4000)]

    Grouped flashes have a shorter duration

    >>> flash([3], 'R', 10000)
    [('R', 500), ('Off', 1000), ('R', 500), ('Off', 1000), ('R', 500),\
 ('Off', 1000), ('Off', 5500)]

    Composite groups are separated by an even period of darkness

    >>> flash([3, 1], 'R', 10000)
    [('R', 500), ('Off', 1000), ('R', 500), ('Off', 1000), ('R', 500),\
 ('Off', 1000), ('Off', 2000), ('R', 500), ('Off', 1000), ('Off', 2000)]

    The total duration of all states matches the requested period

    >>> sum((state[1] for state in flash([1], 'R', 5000))) == 5000
    True
    """

    if groups == [1]:
        if period <= 2000:
            raise ValueError(
                "The cycle period for a flash must be longer than 2 seconds"
            )

        return [
            (colour, 1000),
            ('Off', period-1000)
        ]

    return light_sequence(groups, colour, 'Off', period, 500, 1000)


def long_flash(groups, colour, period):
    """A Long flash is at least 2 seconds"""
    if groups == [1]:
        return [
            (colour, 2000),
            ('Off', period - 2000)
        ]
    return light_sequence(groups, colour, 'Off', period, 2000, 3000)


def isophase(_groups, colour, period):
    """
    isophase is a pattern with equal dark and light. There are no groups.
    """
    # Whole numbers are required, so odd numbers are dealt with by loading
    # the spare into the off period.
    # As this is in milliseconds, this will be imperceptible.
    # It is also unlikely, as the top-level input is in seconds
    # and has been multiplied up to milliseconds before reaching this
    # function
    return [
        (colour, math.floor(period/2)),
        ('Off', math.ceil(period/2))
    ]


def occulting(groups, colour, period):
    """
    An occulting pattern is the opposite of a flash - dark with longer light
    """
    if groups == [1]:
        return [
            ('Off', 1000),
            (colour, period - 1000)
        ]
    return light_sequence(groups, 'Off', colour, period, 500, 1000)


def quick(groups, colour, period):
    """
    A Quick flash is more than 50 per minute.
    """
    # The cycle period cannot be longer than 1.2s (60/50)
    # or shorter than 0.5s
    if groups == [1]:
        if period is not None:
            raise ValueError(
                "Quick Flash cycle periods must be longer than 0.5 seconds"
            )

        return [
            (colour, 250),
            ('Off', 750)
        ]

    return light_sequence(groups, 'Off', colour, period, 250, 500)


TYPES = {
    'f': fixed,
    'fl': flash,
    'q': quick,
    'lfl': long_flash,
    'iso': isophase,
    'oc': occulting
}
