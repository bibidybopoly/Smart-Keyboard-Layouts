# initialize.py
# Responsible for creating the very first generation of keyboards.
# All subsequent generations are produced by mutate.py instead.
#
# A keyboard layout is stored as a dictionary with this structure:
#   { key_position: [lowercase_char, uppercase_char], ... }
# grouped into four rows (row_1 through row_4), mirroring a physical keyboard.

import file_manager as manager
import mutate as mut

def gen1():
    """
    Creates and saves Generation 1 — the starting population for the algorithm.

    The first generation contains 25 keyboards total:
      - 21 randomly shuffled layouts (to explore a wide range of possibilities)
      - QWERTY, Colemak, Dvorak, and Alphabetical (as known baselines for comparison)
    """
    gen = {}

    # Generate 21 random keyboard layouts to seed the population with diversity.
    for i in range(21):
        keyb = mut.gen_rand()
        keyb = mut.correct(keyb)
        gen.update(keyb)

    # QWERTY — the standard layout used by most people.
    gen.update(mut.correct(["-", {
        "row_1":{"`":["`","~"],"1":["1","!"],"2":["2",'@'],"3":["3","#"],"4":["4","$"],"5":["5","%"],"6":["6","^"],"7":["7","&"],"8":["8","*"],"9":["9","("],"0":["0",")"],"-":["-","_"],"=":["=","+"]},
        "row_2":{"q":["q","Q"],"w":["w","W"],"e":["e","E"],"r":["r","R"],"t":["t","T"],"y":["y","Y"],"u":["u","U"],"i":["i","I"],"o":["o","O"],"p":["p","P"],"[":["[","{"],"]":["]","}"],"\\":["\\","|"]},
        "row_3":{"a":["a","A"],"s":["s","S"],"d":["d","D"],"f":["f","F"],"g":["g","G"],"h":["h","H"],"j":["j","J"],"k":["k","K"],"l":["l","L"],";":[";",":"],"'":["'","\""]},
        "row_4":{"z":["z","Z"],"x":["x","X"],"c":["c","C"],"v":["v","V"],"b":["b","B"],"n":["n","N"],"m":["m","M"],",":[",","<"],".":[".",">"],"/":["/","?"]}
        }]))

    # Colemak — an ergonomic layout designed to reduce finger movement from QWERTY.
    gen.update(mut.correct(["-", {
        "row_1":{"`":["`","~"],"1":["1","!"],"2":["2",'@'],"3":["3","#"],"4":["4","$"],"5":["5","%"],"6":["6","^"],"7":["7","&"],"8":["8","*"],"9":["9","("],"0":["0",")"],"-":["-","_"],"=":["=","+"]},
        "row_2":{"q":["q","Q"],"w":["w","W"],"e":["f","F"],"r":["p","P"],"t":["g","G"],"y":["j","J"],"u":["l","L"],"i":["u","U"],"o":["y","Y"],"p":[";",":"],"[":["[","{"],"]":["]","}"],"\\":["\\","|"]},
        "row_3":{"a":["a","A"],"s":["r","R"],"d":["s","S"],"f":["t","T"],"g":["d","D"],"h":["h","H"],"j":["n","N"],"k":["e","E"],"l":["i","I"],";":["o","O"],"'":["'","\""]},
        "row_4":{"z":["z","Z"],"x":["x","X"],"c":["c","C"],"v":["v","V"],"b":["b","B"],"n":["k","K"],"m":["m","M"],",":[",","<"],".":[".",">"],"/":["/","?"]}
        }]))

    # Dvorak — one of the oldest alternative layouts, designed in the 1930s.
    gen.update(mut.correct(["-", {
        "row_1":{"`":["`","~"],"1":["1","!"],"2":["2",'@'],"3":["3","#"],"4":["4","$"],"5":["5","%"],"6":["6","^"],"7":["7","&"],"8":["8","*"],"9":["9","("],"0":["0",")"],"-":["[","{"],"=":["]","}"]},
        "row_2":{"q":["'","\""],"w":[",","<"],"e":[".",">"],"r":["p","P"],"t":["y","Y"],"y":["f","F"],"u":["g","G"],"i":["c","C"],"o":["r","R"],"p":["l","L"],"[":["/","?"],"]":["=","+"],"\\":["\\","|"]},
        "row_3":{"a":["a","A"],"s":["o","O"],"d":["e","E"],"f":["u","U"],"g":["i","I"],"h":["d","D"],"j":["h","H"],"k":["t","T"],"l":["n","N"],";":["s","S"],"'":["-","_"]},
        "row_4":{"z":[";",":"],"x":["q","Q"],"c":["j","J"],"v":["k","K"],"b":["x","X"],"n":["b","B"],"m":["m","M"],",":["w","W"],".":["v","V"],"/":["z","Z"]}
        }]))

    # Alphabetical — letters in A-Z order. Included as a naive baseline.
    gen.update(mut.correct(["-", {
        "row_1":{"`":["`","~"],"1":["1","!"],"2":["2",'@'],"3":["3","#"],"4":["4","$"],"5":["5","%"],"6":["6","^"],"7":["7","&"],"8":["8","*"],"9":["9","("],"0":["0",")"],"-":["-","_"],"=":["=","+"]},
        "row_2":{"q":["a","A"],"w":["b","B"],"e":["c","C"],"r":["d","D"],"t":["e","E"],"y":["f","F"],"u":["g","G"],"i":["h","H"],"o":["i","I"],"p":["j","J"],"[":["[","{"],"]":["]","}"],"\\":["\\","|"]},
        "row_3":{"a":["k","K"],"s":["l","L"],"d":["m","M"],"f":["n","N"],"g":["o","O"],"h":["p","P"],"j":["q","Q"],"k":["r","R"],"l":["s","S"],";":[";",":"],"'":["'","\""]},
        "row_4":{"z":["t","T"],"x":["u","U"],"c":["v","V"],"v":["w","W"],"b":["x","X"],"n":["y","Y"],"m":["z","Z"],",":[",","<"],".":[".",">"],"/":["/","?"]}
        }]))

    # Save the completed generation to disk.
    manager.new_gen(gen)
