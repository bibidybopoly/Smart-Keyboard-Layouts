import sys
import populate as pop
import generate_fitness as gen
import mutate as mut
import file_manager as file
cleanup = False

try:
    while True:
        #Populate
        population = pop.populate()
        print("Populated...")
        print(f"Generation {file.get_index()}")
        cleanup = True

        #Generate Fitness
        population = gen.generate_fitness(population)
        print("Generated Fitness...")
        print(f"Best Fitness: {gen.get_max(population)}\nAverage Fitness: {gen.get_average(population)}")
        print("Top Keyboards:")
        top_keyb_pop = pop.pop_top_kb()
        for keyb in top_keyb_pop:
            print(keyb, top_keyb_pop[keyb][0])

        #Mutate
        population = mut.mutate(population)
        print("Mutated...")
        
        file.new_gen(population)
        file.trash()
        cleanup = False                                         

except KeyboardInterrupt:
    print("\nScript interrupted by user. Performing cleanup...")
    if cleanup:
        file.cleanup()
    sys.exit(0)