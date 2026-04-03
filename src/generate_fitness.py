# generate_fitness.py
# Scores each keyboard layout by simulating typing a sample of English text on it.
#
# The fitness score represents the total distance all fingers travel while typing the
# sample text. A lower score means less movement - and therefore a better layout.
#
# The keyboard is modelled as a 2D coordinate grid. Each key has an (x, y) position,
# and each finger has a current position that updates as it moves between keys.
# When a finger moves to a key, the Euclidean distance travelled is added to the score.
#
# Outer fingers are penalised more than inner fingers: pinky_factor > ring_factor > 1.0.
# This steers the algorithm toward layouts that keep common keys on stronger fingers.
# Hand alternation is also tracked: staying on the same hand too long adds a small penalty.

import math
from pathlib import Path
import file_manager as manager

# SAMPLE_TEXT_PATH points to sample_text.txt in the same folder as this script.
SAMPLE_TEXT_PATH = Path(__file__).parent / "sample_text.txt"

# Load the sample text once at startup so it does not need to be re-read every generation.
with open(SAMPLE_TEXT_PATH, 'r') as file:
    data = file.read()
text = data.strip()

# Current [x, y] position of each finger on the keyboard grid.
# Named: l = left, r = right; p = pinky, r = ring, m = middle, i = index.
lp_pos = [0, 0]
lr_pos = [0, 0]
lm_pos = [0, 0]
li_pos = [0, 0]
ri_pos = [0, 0]
rm_pos = [0, 0]
rr_pos = [0, 0]
rp_pos = [0, 0]

fitness         = 0    # Accumulated travel distance for the current keyboard being scored.
pinky_factor    = 1.3  # Penalty multiplier for pinky fingers - highest, to discourage outer key use.
ring_factor     = 1.1  # Penalty multiplier for ring fingers - moderate outer-finger penalty.
hand            = ""   # Tracks which hand typed the last character ("l" or "r").
alternate_factor = 1   # Penalty added when the same hand is used consecutively.


def adjust(x, pos):
    """
    Simulates the natural tendency of fingers to drift back toward rest position.

    When one finger moves by distance x, all other fingers on the same hand shift
    slightly back toward [0, 0] by the same amount (or all the way if x is large enough).
    This models how real fingers pull each other when one extends far from the home row.

    The distance each finger actually travels during the adjustment is added to the
    fitness score, because returning to rest position is real finger movement.
    """
    global fitness
    dist_to_origin = math.hypot(pos[0], pos[1])
    if dist_to_origin == 0 or x >= dist_to_origin:
        fitness += dist_to_origin   # Finger travels all the way back to rest.
        pos = [0, 0]
    else:
        fitness += x                # Finger travels x units toward rest.
        scale = 1.0 - x / dist_to_origin
        pos = [pos[0] * scale, pos[1] * scale]
    return pos


def lshift():
    """Simulates pressing Left Shift with the left pinky. Uses pinky_factor."""
    global fitness, lp_pos
    dx = math.hypot(-1 - lp_pos[0], -1 - lp_pos[1])
    lp_pos = [-0.5, -1]
    fitness += dx * pinky_factor


def rshift():
    """Simulates pressing Right Shift with the right pinky. Uses pinky_factor."""
    global fitness, rp_pos
    dx = math.hypot(3 - rp_pos[0], -1 - rp_pos[1])
    rp_pos = [1.5, -1]
    fitness += dx * pinky_factor


def alternate(x):
    """
    Tracks which hand was last used. If the same hand types two characters in a row,
    a small penalty is added to the fitness score to discourage single-hand sequences.
    """
    global hand, fitness
    if x == hand:
        fitness += alternate_factor
    else:
        hand = x


def lp_hit(x, y):
    """
    Moves the left pinky to key at position (x, y) and adds the travel distance
    to the fitness score. Also adjusts all other fingers slightly toward rest.
    The pinky penalty (pinky_factor) is applied - higher than the ring factor -
    to further discourage use of the outermost finger.
    """
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - lp_pos[0], y - lp_pos[1])
    lp_pos = [x, y]
    fitness += dx * pinky_factor

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)


def lr_hit(x, y):
    """Moves the left ring finger to (x, y). Applies ring finger penalty (ring_factor)."""
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - lr_pos[0], y - lr_pos[1])
    lr_pos = [x, y]
    fitness += dx * ring_factor

    lp_pos = adjust(dx, lp_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)


def lm_hit(x, y):
    """Moves the left middle finger to (x, y). No outer finger penalty."""
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - lm_pos[0], y - lm_pos[1])
    lm_pos = [x, y]
    fitness += dx

    lr_pos = adjust(dx, lr_pos)
    lp_pos = adjust(dx, lp_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)


def li_hit(x, y):
    """Moves the left index finger to (x, y). No outer finger penalty."""
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - li_pos[0], y - li_pos[1])
    li_pos = [x, y]
    fitness += dx

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    lp_pos = adjust(dx, lp_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)


def ri_hit(x, y):
    """Moves the right index finger to (x, y). No outer finger penalty."""
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - ri_pos[0], y - ri_pos[1])
    ri_pos = [x, y]
    fitness += dx

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    lp_pos = adjust(dx, lp_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)


def rm_hit(x, y):
    """Moves the right middle finger to (x, y). No outer finger penalty."""
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - rm_pos[0], y - rm_pos[1])
    rm_pos = [x, y]
    fitness += dx

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    lp_pos = adjust(dx, lp_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)


def rr_hit(x, y):
    """Moves the right ring finger to (x, y). Applies ring finger penalty (ring_factor)."""
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - rr_pos[0], y - rr_pos[1])
    rr_pos = [x, y]
    fitness += dx * ring_factor

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    lp_pos = adjust(dx, lp_pos)
    rp_pos = adjust(dx, rp_pos)


def rp_hit(x, y):
    """Moves the right pinky to (x, y). Applies pinky finger penalty (pinky_factor)."""
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.hypot(x - rp_pos[0], y - rp_pos[1])
    rp_pos = [x, y]
    fitness += dx * pinky_factor

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    lp_pos = adjust(dx, lp_pos)


# Static table mapping each physical key position (row, key) to the finger function that
# presses it, its coordinate on the grid, and which hand it belongs to.
# This is board-independent - it reflects the physical keyboard geometry, not the layout.
# Built once at module load so generate_fitness() can use it without rebuilding each time.
KEY_LAYOUT = (
    # row         key    hit_fn   x       y    hand
    ("row_1",  "`",   lp_hit, -1.75,   2,   "l"),
    ("row_1",  "1",   lp_hit, -0.75,   2,   "l"),
    ("row_2",  "q",   lp_hit, -0.25,   1,   "l"),
    ("row_3",  "a",   lp_hit,  0,      0,   "l"),
    ("row_4",  "z",   lp_hit,  0.5,   -1,   "l"),

    ("row_1",  "2",   lr_hit, -0.75,   2,   "l"),
    ("row_2",  "w",   lr_hit, -0.25,   1,   "l"),
    ("row_3",  "s",   lr_hit,  0,      0,   "l"),
    ("row_4",  "x",   lr_hit,  0.5,   -1,   "l"),

    ("row_1",  "3",   lm_hit, -0.75,   2,   "l"),
    ("row_2",  "e",   lm_hit, -0.25,   1,   "l"),
    ("row_3",  "d",   lm_hit,  0,      0,   "l"),
    ("row_4",  "c",   lm_hit,  0.5,   -1,   "l"),

    ("row_1",  "4",   li_hit, -0.75,   2,   "l"),
    ("row_2",  "r",   li_hit, -0.25,   1,   "l"),
    ("row_3",  "f",   li_hit,  0,      0,   "l"),
    ("row_4",  "v",   li_hit,  0.5,   -1,   "l"),
    ("row_1",  "5",   li_hit,  0.25,   2,   "l"),
    ("row_2",  "t",   li_hit,  0.75,   1,   "l"),
    ("row_3",  "g",   li_hit,  1,      0,   "l"),
    ("row_4",  "b",   li_hit,  1.5,   -1,   "l"),

    ("row_1",  "6",   ri_hit, -1.75,   2,   "r"),
    ("row_2",  "y",   ri_hit, -1.25,   1,   "r"),
    ("row_3",  "h",   ri_hit, -1,      0,   "r"),
    ("row_4",  "n",   ri_hit, -0.5,   -1,   "r"),
    ("row_1",  "7",   ri_hit, -0.75,   2,   "r"),
    ("row_2",  "u",   ri_hit, -0.25,   1,   "r"),
    ("row_3",  "j",   ri_hit,  0,      0,   "r"),
    ("row_4",  "m",   ri_hit,  0.5,   -1,   "r"),

    ("row_1",  "8",   rm_hit, -0.75,   2,   "r"),
    ("row_2",  "i",   rm_hit, -0.25,   1,   "r"),
    ("row_3",  "k",   rm_hit,  0,      0,   "r"),
    ("row_4",  ",",   rm_hit,  0.5,   -1,   "r"),

    ("row_1",  "9",   rr_hit, -0.75,   2,   "r"),
    ("row_2",  "o",   rr_hit, -0.25,   1,   "r"),
    ("row_3",  "l",   rr_hit,  0,      0,   "r"),
    ("row_4",  ".",   rr_hit,  0.5,   -1,   "r"),

    ("row_1",  "0",   rp_hit, -0.75,   2,   "r"),
    ("row_2",  "p",   rp_hit, -0.25,   1,   "r"),
    ("row_3",  ";",   rp_hit,  0,      0,   "r"),
    ("row_4",  "/",   rp_hit,  0.5,   -1,   "r"),
    ("row_1",  "-",   rp_hit,  0.25,   2,   "r"),
    ("row_2",  "[",   rp_hit,  0.75,   1,   "r"),
    ("row_3",  "'",   rp_hit,  1,      0,   "r"),
    ("row_1",  "=",   rp_hit,  1.25,   2,   "r"),
    ("row_2",  "]",   rp_hit,  1.75,   1,   "r"),
    ("row_2",  "\\",  rp_hit,  2.75,   1,   "r"),
)


def generate_fitness(keybs):
    """
    Scores every keyboard in the given dictionary by simulating typing the sample text.

    For each keyboard:
      1. All finger positions and state are reset so each keyboard is scored fairly.
      2. A character-to-action lookup dict is built from the layout and KEY_LAYOUT table.
      3. Every character in the sample text is looked up in the dict in O(1) time.
      4. The total finger travel distance is accumulated as the fitness score.
      5. The final score is stored back into the keyboard entry and logged to disk.

    A lower score is better - it means less finger movement to type the same text.
    Returns the keyboard dictionary with updated fitness scores.
    """
    global fitness, hand, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    keyboards = {}

    for keyb in keybs:
        board = keybs[keyb]

        # Reset all finger positions and state for each new keyboard.
        fitness = 0
        hand    = ""
        lp_pos  = [0, 0]
        lr_pos  = [0, 0]
        lm_pos  = [0, 0]
        li_pos  = [0, 0]
        ri_pos  = [0, 0]
        rm_pos  = [0, 0]
        rr_pos  = [0, 0]
        rp_pos  = [0, 0]

        # Build a character -> (hit_fn, x, y, hand_side, shift_fn) lookup for this layout.
        # shift_fn is None for lowercase characters and the opposing hand's shift for uppercase.
        key_map = {}
        r = board[1]
        for row, key, hit_fn, x, y, hand_side in KEY_LAYOUT:
            shift_fn = rshift if hand_side == "l" else lshift
            key_map[r[row][key][0]] = (hit_fn, x, y, hand_side, None)
            key_map[r[row][key][1]] = (hit_fn, x, y, hand_side, shift_fn)

        # Simulate typing the sample text using the lookup dict.
        for char in text:
            if char in key_map:
                hit_fn, x, y, hand_side, shift_fn = key_map[char]
                alternate(hand_side)
                hit_fn(x, y)
                if shift_fn is not None:
                    shift_fn()

        # Round the score, store it back in the board entry, and log it.
        fitness = round(fitness)
        board[0] = fitness
        print(fitness)
        keyboards[keyb] = board
        manager.appendscores(keyb, fitness)

    return keyboards


def get_max(gen):
    """
    Finds the best (lowest) fitness score in the current generation.

    Sorts all scores, then logs the best one, checks for an all-time high score,
    and updates the saved top keyboards list. Returns the best score.
    """
    scores = [gen[keyb][0] for keyb in gen]
    scores.sort()
    manager.appendmax(scores[0])
    manager.update_high(gen, scores[0])
    manager.update_top_keybs(gen, scores)
    return scores[0]


def get_average(gen):
    """
    Calculates the average fitness score across all 25 keyboards in the generation.

    Logs the result to disk and returns it. Used to track whether the population
    is improving over time.
    """
    total = sum(gen[keyb][0] for keyb in gen)
    average = round(total / 25)
    manager.appendaverage(average)
    return average
