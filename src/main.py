# main.py
# Entry point for the keyboard layout genetic algorithm.
# Run this file to start the evolution process. Press Ctrl+C to stop it cleanly.

import sys
import populate as pop
import generate_fitness as gen
import mutate as mut
import file_manager as file

# cleanup tracks whether we're mid-generation when interrupted.
# If True at the time of a KeyboardInterrupt, the partial generation is removed.
cleanup = False

try:
    # The algorithm runs indefinitely until the user presses Ctrl+C.
    while True:

        # Step 1: Build a new population of keyboard layouts for this generation.
        population = pop.populate()
        print("Populated...")
        print(f"Generation {file.get_index()}")
        cleanup = True  # A generation is now in progress.

        # Step 2: Score every keyboard by simulating typing on it.
        # Lower scores are better (less total finger travel distance).
        population = gen.generate_fitness(population)
        print("Generated Fitness...")
        print(f"Best Fitness: {gen.get_max(population)}\nAverage Fitness: {gen.get_average(population)}")

        # Print the current all-time top keyboards for reference.
        print("Top Keyboards:")
        top_keyb_pop = pop.pop_top_kb()
        for keyb in top_keyb_pop:
            print(keyb, top_keyb_pop[keyb][0])

        # Step 3: Mutate the best keyboards to create the next generation.
        population = mut.mutate(population)
        print("Mutated...")

        # Save the new generation to disk and remove the previous one.
        file.new_gen(population)
        file.trash()
        cleanup = False  # Generation completed successfully.

except KeyboardInterrupt:
    # User pressed Ctrl+C. Clean up any incomplete generation before exiting.
    print("\nScript interrupted by user. Performing cleanup...")
    if cleanup:
        file.cleanup()
    sys.exit(0)
