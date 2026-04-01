# Smart Keyboard Layouts

A genetic algorithm that evolves keyboard layouts to minimize finger movement, written in Python. After running for hundreds of generations, the algorithm produced **Lak** — a custom keyboard layout optimized for the English language.

---

## What is Lak?

Lak is a keyboard layout designed entirely by this algorithm. Its name follows the same naming convention as Dvorak and Colemak — named after their creators. Lak combines the creator's last name, **Lang**, with the **"ak"** suffix shared by both Dvorak and Colemak.

The goal was simple: find a layout where your fingers travel as little as possible when typing real English text. The algorithm compared thousands of keyboard arrangements and gradually evolved them toward that goal, the same way nature evolves organisms over generations.

The finished Lak layout is included in the `reference_layouts/` folder as a `.klc` file, alongside QWERTY, Dvorak, Colemak, and an Alphabetical layout for comparison.

---

## How It Works

The algorithm follows the classic cycle of a genetic algorithm:

**1. Populate** — A generation of 25 keyboards is created. The first generation includes 21 randomly shuffled layouts plus QWERTY, Colemak, and Dvorak as a baseline. Later generations are built from the best survivors of the previous one.

**2. Score (Fitness)** — Each keyboard is scored by simulating typing a large sample of English text (`sample_text.txt`) and measuring the total distance each finger travels. A lower score is better.

**3. Mutate** — The top-performing keyboards are kept and randomly modified (keys swapped around) to produce the next generation. Weaker keyboards are discarded.

This cycle repeats indefinitely. Each generation's scores and top performers are saved to the `data/` folder, and every keyboard layout is saved as a `.klc` file in `generations/`.

---

## Project Structure

```
Smart_Keyboard_layouts/
│
├── src/                        # All Python source code
│   ├── main.py                 # Entry point — runs the algorithm
│   ├── initialize.py           # Creates the first generation
│   ├── populate.py             # Builds each new generation from survivors
│   ├── generate_fitness.py     # Scores each keyboard layout
│   ├── mutate.py               # Mutates keyboards to produce offspring
│   ├── file_manager.py         # Handles all file reading and writing
│   └── sample_text.txt         # Sample English text used for scoring
│
├── generations/                # Keyboard layouts generated during a run
├── reference_layouts/          # Reference layouts (QWERTY, Dvorak, Colemak, Lak)
├── top_keyboards/              # The best layouts found across all generations
└── data/                       # Data logs (scores per generation, high scores)
```

---

## Requirements

- Python 3.x
- No external libraries required — uses only the Python standard library

---

## How to Run

1. Clone this repository or download it as a ZIP
2. Open a terminal and navigate to the `src/` folder
3. Run:

```
python main.py
```

The algorithm will run continuously, printing each generation's best and average fitness score as it goes. Press **Ctrl+C** at any time to stop it cleanly — it will save its progress before exiting.

---

## Results

After hundreds of generations, the algorithm converged on the **Lak** keyboard layout. Lak consistently outscored QWERTY, Dvorak, and Colemak on the fitness test, meaning less total finger travel when typing the sample English text.

---

*Built as a personal project to explore genetic algorithms and keyboard ergonomics.*
