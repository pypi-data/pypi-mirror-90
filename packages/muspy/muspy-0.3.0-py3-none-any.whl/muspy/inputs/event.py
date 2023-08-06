"""Event-based representation input interface."""
from collections import defaultdict
from operator import attrgetter

import numpy as np
from numpy import ndarray

from ..classes import Note, Track
from ..music import DEFAULT_RESOLUTION, Music


def from_event_representation(
    array: ndarray,
    resolution: int = DEFAULT_RESOLUTION,
    program: int = 0,
    is_drum: bool = False,
    use_single_note_off_event: bool = False,
    use_end_of_sequence_event: bool = False,
    max_time_shift: int = 100,
    velocity_bins: int = 32,
    default_velocity: int = 64,
    duplicate_note_mode: str = "fifo",
) -> Music:
    """Decode event-based representation into a Music object.

    Parameters
    ----------
    array : ndarray
        Array in event-based representation to decode. Cast to integer
        if not of integer type.
    resolution : int
        Time steps per quarter note. Defaults to
        `muspy.DEFAULT_RESOLUTION`.
    program : int, optional
        Program number according to General MIDI specification [1].
        Acceptable values are 0 to 127. Defaults to 0 (Acoustic Grand
        Piano).
    is_drum : bool, optional
        A boolean indicating if it is a percussion track. Defaults to
        False.
    use_single_note_off_event : bool
        Whether to use a single note-off event for all the pitches. If
        True, a note-off event will close all active notes, which can
        lead to lossy conversion for polyphonic music. Defaults to
        False.
    use_end_of_sequence_event : bool
        Whether to append an end-of-sequence event to the encoded
        sequence. Defaults to False.
    max_time_shift : int
        Maximum time shift (in ticks) to be encoded as an separate
        event. Time shifts larger than `max_time_shift` will be
        decomposed into two or more time-shift events. Defaults to 100.
    velocity_bins : int
        Number of velocity bins to use. Defaults to 32.
    default_velocity : int
        Default velocity value to use when decoding. Defaults to 64.
    duplicate_note_mode : {'fifo', 'lifo', 'close_all'}
        Policy for dealing with duplicate notes. When a note off event
        is presetned while there are multiple correspoding note on
        events that have not yet been closed, we need a policy to decide
        which note on messages to close. This is only effective when
        `use_single_note_off_event` is False. Defaults to 'fifo'.

        - 'fifo' (first in first out): close the earliest note on
        - 'lifo' (first in first out): close the latest note on
        - 'close_all': close all note on messages

    Returns
    -------
    :class:`muspy.Music`
        Decoded Music object.

    References
    ----------
    [1] https://www.midi.org/specifications/item/gm-level-1-sound-set

    """
    # Cast the array to integer
    if not np.issubdtype(array.dtype, np.integer):
        array = array.astype(np.int)

    # Compute offsets
    offset_note_on = 0
    offset_note_off = 128
    offset_time_shift = 129 if use_single_note_off_event else 256
    offset_velocity = offset_time_shift + max_time_shift
    if use_end_of_sequence_event:
        offset_eos = offset_velocity + velocity_bins

    # Compute vocabulary size
    if use_single_note_off_event:
        vocab_size = 129 + max_time_shift + velocity_bins
    else:
        vocab_size = 256 + max_time_shift + velocity_bins
    if use_end_of_sequence_event:
        vocab_size += 1

    # Decode events
    time = 0
    velocity = default_velocity
    velocity_factor = 128 / velocity_bins
    notes = []

    # Keep track of active note on messages
    active_notes = defaultdict(list)

    # Iterate over the events
    for event in array.flatten().tolist():
        # Skip unknown events
        if event < offset_note_on or event >= vocab_size:
            continue

        # End-of-sequence events
        if use_end_of_sequence_event and event == offset_eos:
            break

        # Note on events
        if event < offset_note_off:
            pitch = event - offset_note_on
            active_notes[pitch].append(
                Note(time=time, pitch=pitch, duration=-1, velocity=velocity)
            )

        # Note off events
        elif event < offset_time_shift:
            # Close all notes
            if use_single_note_off_event:
                if active_notes:
                    for pitch, note_list in active_notes.items():
                        for note in note_list:
                            note.duration = time - note.time
                            notes.append(note)
                    active_notes = defaultdict(list)
                continue

            pitch = event - offset_note_off

            # Skip it if there is no active notes
            if not active_notes[pitch]:
                continue

            # NOTE: There is no way to disambiguate duplicate notes of
            # the same pitch. Thus, we need a policy for handling
            # duplicate notes.

            # 'FIFO': (first in first out) close the earliest note
            elif duplicate_note_mode.lower() == "fifo":
                note = active_notes[pitch][0]
                note.duration = time - note.time
                notes.append(note)
                del active_notes[pitch][0]

            # 'LIFO': (last in first out) close the latest note on
            elif duplicate_note_mode.lower() == "lifo":
                note = active_notes[pitch][-1]
                note.duration = time - note.time
                notes.append(note)
                del active_notes[pitch][-1]

            # 'close_all' - close all note on events
            elif duplicate_note_mode.lower() == "close_all":
                for note in active_notes[pitch]:
                    note.duration = time - note.time
                    notes.append(note)
                del active_notes[pitch]

        # Time-shift events
        elif event < offset_velocity:
            time += event - offset_time_shift + 1

        # Velocity events
        elif event < vocab_size:
            velocity = int((event - offset_velocity) * velocity_factor)

    # Sort the notes
    notes.sort(key=attrgetter("time", "pitch", "duration", "velocity"))

    # Create the Track and Music objects
    track = Track(program=program, is_drum=is_drum, notes=notes)
    music = Music(resolution=resolution, tracks=[track])

    return music
