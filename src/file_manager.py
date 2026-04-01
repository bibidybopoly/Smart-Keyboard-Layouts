# file_manager.py
# Handles all reading from and writing to disk.
#
# This is the backbone of the algorithm's persistence layer. Every time a generation
# is scored, mutated, or saved, this module is responsible for updating the .klc files
# and the CSV data logs. It also manages loading generations back from disk on startup.
#
# .klc files are Windows Keyboard Layout Creator files. The algorithm uses them as its
# native storage format for keyboard layouts because they contain all key mappings in a
# structured, human-readable format and can be installed directly on Windows to try a
# layout for real.

from pathlib import Path
import populate as pop
import os
import shutil
import initialize as initial

# BASE_DIR points to the root Smart_Keyboard_layouts folder,
# no matter where this project is saved on any computer.
BASE_DIR = Path(__file__).parent.parent

CSV_ALL_KEYBOARDS = BASE_DIR / "data" / "Keyboard_All_Keyboards_CSV.txt"
CSV_ALL_GENS      = BASE_DIR / "data" / "Keyboard_All_Gens_CSV.txt"
CSV_HIGH_SCORES   = BASE_DIR / "data" / "Keyboard_High_Scores_CSV.txt"
GENERATIONS_DIR   = BASE_DIR / "generations"
TOP_KEYBOARDS_DIR = BASE_DIR / "top_keyboards"

# Maps each typeable character to its Unicode name and hex code.
# Used when writing .klc files, which require Unicode names rather than raw characters.
keyname_key = {
    "`":["GRAVE ACCENT", "0060"], "~":["TILDE", "007e"], "1":["DIGIT ONE", "1"], "!":["EXCLAMATION MARK", "0021"], "2":["DIGIT TWO", "2"], "@":["COMMERCIAL AT", "0040"], "3":["DIGIT THREE", "3"], "#":["NUMBER SIGN", "0023"], "4":["DIGIT FOUR", "4"], "$":["DOLLAR SIGN", "0024"], "5":["DIGIT FIVE", "5"], "%":["PERCENT SIGN", "0025"], "6":["DIGIT SIX", "6"], "^":["CIRCUMFLEX ACCENT", "005e"], "7":["DIGIT SEVEN", "7"], "&":["AMPERSAND", "0026"], "8":["DIGIT EIGHT", "8"], "*":["ASTERISK", "002a"], "9":["DIGIT NINE", "9"], "(":["LEFT PARENTHESIS", "0028"], "0":["DIGIT ZERO", "0"], ")":["RIGHT PARENTHESIS", "0029"], "-":["HYPHEN-MINUS", "002d"], "_":["LOW LINE", "005f"], "=":["EQUALS SIGN", "003d"], "+":["PLUS SIGN", "002b"],
    "q":["LATIN SMALL LETTER Q", "q"], "Q":["LATIN CAPITAL LETTER Q", "Q"], "w":["LATIN SMALL LETTER W", "w"], "W":["LATIN CAPITAL LETTER W", "W"], "e":["LATIN SMALL LETTER E", "e"], "E":["LATIN CAPITAL LETTER E", "E"], "r":["LATIN SMALL LETTER R", "r"], "R":["LATIN CAPITAL LETTER R", "R"], "t":["LATIN SMALL LETTER T", "t"], "T":["LATIN CAPITAL LETTER T", "T"], "y":["LATIN SMALL LETTER Y", "y"], "Y":["LATIN CAPITAL LETTER Y", "Y"], "u":["LATIN SMALL LETTER U", "u"], "U":["LATIN CAPITAL LETTER U", "U"], "i":["LATIN SMALL LETTER I", "i"], "I":["LATIN CAPITAL LETTER I", "I"], "o":["LATIN SMALL LETTER O", "o"], "O":["LATIN CAPITAL LETTER O", "O"], "p":["LATIN SMALL LETTER P", "p"], "P":["LATIN CAPITAL LETTER P", "P"], "[":["LEFT SQUARE BRACKET", "005b"], "{":["LEFT CURLY BRACKET", "007b"], "]":["RIGHT SQUARE BRACKET", "005d"], "}":["RIGHT CURLY BRACKET", "007d"], "\\":["REVERSE SOLIDUS", "005c"], "|":["VERTICAL LINE", "007c"],
    "a":["LATIN SMALL LETTER A", "a"], "A":["LATIN CAPITAL LETTER A", "A"], "s":["LATIN SMALL LETTER S", "s"], "S":["LATIN CAPITAL LETTER S", "S"], "d":["LATIN SMALL LETTER D", "d"], "D":["LATIN CAPITAL LETTER D", "D"], "f":["LATIN SMALL LETTER F", "f"], "F":["LATIN CAPITAL LETTER F", "F"], "g":["LATIN SMALL LETTER G", "g"], "G":["LATIN CAPITAL LETTER G", "G"], "h":["LATIN SMALL LETTER H", "h"], "H":["LATIN CAPITAL LETTER H", "H"], "j":["LATIN SMALL LETTER J", "j"], "J":["LATIN CAPITAL LETTER J", "J"], "k":["LATIN SMALL LETTER K", "k"], "K":["LATIN CAPITAL LETTER K", "K"], "l":["LATIN SMALL LETTER L", "l"], "L":["LATIN CAPITAL LETTER L", "L"], ";":["SEMICOLON", "003b"], ":":["COLON", "003a"], "'":["APOSTROPHE", "0027"], "\"":["QUOTATION MARK", "0022"],
    "z":["LATIN SMALL LETTER Z", "z"], "Z":["LATIN CAPITAL LETTER Z", "Z"], "x":["LATIN SMALL LETTER X", "x"], "X":["LATIN CAPITAL LETTER X", "X"], "c":["LATIN SMALL LETTER C", "c"], "C":["LATIN CAPITAL LETTER C", "C"], "v":["LATIN SMALL LETTER V", "v"], "V":["LATIN CAPITAL LETTER V", "V"], "b":["LATIN SMALL LETTER B", "b"], "B":["LATIN CAPITAL LETTER B", "B"], "n":["LATIN SMALL LETTER N", "n"], "N":["LATIN CAPITAL LETTER N", "N"], "m":["LATIN SMALL LETTER M", "m"], "M":["LATIN CAPITAL LETTER M", "M"], ",":["COMMA", "002c"], "<":["LESS-THAN SIGN", "003c"], ".":["FULL STOP", "002e"], ">":["GREATER-THAN SIGN", "003e"], "/":["SOLIDUS", "002f"], "?":["QUESTION MARK", "003f"],
    }

def gen_name(keyb):
    """
    Generates a unique name for a keyboard layout based on its top-row keys,
    following the same convention as QWERTY (named after its Q-W-E-R-T-Y row).

    Forbidden characters (symbols that are invalid in filenames) are skipped.
    If the generated name already exists, a numeric suffix (_1, _2, etc.) is added.
    The name is also registered in the all-keyboards CSV log.

    Returns the keyboard's name as a string.
    """
    with open(CSV_ALL_KEYBOARDS, 'r') as file:
        data = file.read()
    lines = []
    line = ""
    for char in data:
        if char == "\n":
            lines.append(line)
            line = ""
        else:
            line += chara

    names = []
    for line in lines:
        name = ""
        index = 0
        for char in line:
            if index == 1 and char != "," and char != " ":
                name += char
            elif char == ",":
                index += 1
        names.append(name)
    forbidden = ["&", "%", "*", "#", "$", "!", "'", "\"", "@", "+", "`", "=", "<", ">", "{", "}", ":", "/", "\\", "|", "?", ","]

    Q = keyb[1]["row_2"]["q"][0]
    if Q in forbidden:
        Q = ""

    W = keyb[1]["row_2"]["w"][0]
    if W in forbidden:
        W = ""

    E = keyb[1]["row_2"]["e"][0]
    if E in forbidden:
        E = ""

    R = keyb[1]["row_2"]["r"][0]
    if R in forbidden:
        R = ""

    T = keyb[1]["row_2"]["t"][0]
    if T in forbidden:
        T = ""

    Y = keyb[1]["row_2"]["y"][0]
    if Y in forbidden:
        Y = ""

    keybname = Q.capitalize() + W.capitalize() + E.capitalize() + R.capitalize() + T.capitalize() + Y.capitalize()

    num = 1
    while keybname in names:
        if f"_{num-1}" in keybname:
            keybname = keybname[:-len(f"_{num-1}")]
        keybname += f"_{num}"
        num += 1

    with open(CSV_ALL_KEYBOARDS, 'a') as file:
        file.write(f"Gen{int(get_index()) + 1}, {keybname}, -\n")
        
    return keybname

def get_index():
    """
    Returns the current generation number by reading the last entry in the
    all-generations CSV. Returns 0 if no generations have been run yet.
    """
    with open(CSV_ALL_GENS, 'r') as file:
        data = file.read()
    lines = []
    line = ""
    for char in data:
        if char == "\n":
            lines.append(line)
            line = ""
        else:
            line += char

    gen = ""
    if len(lines) == 0:
        return 0

    for char in lines[-1]:
        if char != ",":
            gen += char
        else:
            break

    return gen[3::]

def appendmax(max):
    """
    Writes the best (lowest) fitness score of the current generation into the
    all-generations CSV. Called after all keyboards in a generation are scored.
    """
    with open(CSV_ALL_GENS, 'r') as file:
        data = file.read()
    lines = []
    line = ""
    for char in data:
        if char == "\n":
            lines.append(line)
            line = ""
        else:
            line += char

    lines[-1] = lines[-1][:-1]
    lines[-1] += f"{max}"

    with open(CSV_ALL_GENS, 'w') as file:
        for line in lines:
            file.write(line + "\n")

def appendaverage(average):
    """
    Writes the average fitness score of the current generation into the
    all-generations CSV alongside the best score already recorded there.
    """
    with open(CSV_ALL_GENS, 'r') as file:
        data = file.read()
    lines = []
    line = ""
    for char in data:
        if char == "\n":
            lines.append(line)
            line = ""
        else:
            line += char

    gen = ""
    max = ""
    index = 0
    for char in lines[-1]:
        if index == 0 and char != ",":
            gen += char
        elif index == 2 and char != ",":
            max += char
        elif char == ",":
            index += 1
    
    lines[-1] = gen + ", " + f"{average}," + max

    with open(CSV_ALL_GENS, 'w') as file:
        for line in lines:
            file.write(line + "\n")

def appendscores(keyb, fitness):
    """
    Records a keyboard's fitness score in two places:
      1. The all-keyboards CSV (updates the placeholder '-' with the real score).
      2. The keyboard's own .klc file (stored in the COMPANY field for easy reading).
    """
    with open(CSV_ALL_KEYBOARDS, 'r') as file:
        data = file.read()
    lines = []
    line = ""
    for char in data:
        if char == "\n":
            lines.append(line)
            line = ""
        else:
            line += char

    for i, line in enumerate(lines):
        if f" {keyb}," in line:
            lines[i] = f"Gen{get_index()}, {keyb}, {fitness}"

    with open(CSV_ALL_KEYBOARDS, 'w') as file:
        for line in lines:
            file.write(line + "\n")

    keybs = []
    genpath = GENERATIONS_DIR / f"Gen{get_index()}"
    for kb in Path(genpath).iterdir():
        keybs.append(kb)

    for path in keybs:
        if keyb == str(path)[len(genpath)+1:-4]:
            with open(path, 'r') as keybfile:
                keybdata = keybfile.read()
            lines = []
            line = ""
            for char in keybdata:
                if char == "\n":
                    lines.append(line)
                    line = ""
                else:
                    line += char

            lines[2] = f"COMPANY	\"{fitness}\""

            with open(genpath / f"{keyb}.klc", 'w') as file:
                for line in lines:
                    file.write(line + "\n")
        


def update_high(gen, high):
    """
    Checks if the best score from the current generation is an all-time record.
    If so, appends the new record to the high-scores CSV along with the generation
    number and the name of the keyboard that achieved it.
    """
    with open(CSV_HIGH_SCORES, 'r') as file:
        data = file.read()
    lines = []
    line = ""
    for char in data:
        if char == "\n":
            lines.append(line)
            line = ""
        else:
            line += char
    record = ""

    if len(lines) == 0:
        record  = 9999999999999999

    else:
        index = 0
        for char in lines[-1]:
            if index == 2 and char != " " and char != ",":
                record += char
            elif char == ",":
                index += 1

    gennum = get_index()

    keybname = ""

    for keyb in gen:
        if gen[keyb][0] == high:
            keybname = keyb

    if high < int(record):
        lines += [f"Gen{gennum}, {keybname}, {high}"]
        with open(CSV_HIGH_SCORES, 'w') as file:
            for line in lines:
                file.write(line + "\n")

def update_top_keybs(gen, list):
    """
    Maintains the all-time top 5 best keyboard layouts in the top_keyboards/ folder.

    Combines the scores from the current generation with the existing top keyboards,
    keeps only the 5 lowest scores, removes any .klc files that no longer qualify,
    and writes new .klc files for any keyboards that have earned a spot.
    """
    topfitnesses = []
    topgen = pop.pop_top_kb()
    for topkeyb in topgen:
        topfitnesses.append(int(topgen[topkeyb][0]))

    fitnesses = topfitnesses + list
    fitnesses.sort()
    fitnesses = fitnesses[0:5]

    files = []
    for file in Path(TOP_KEYBOARDS_DIR).iterdir():
        files.append(file)

    for file in files:
        with open(file, 'r') as rfile:
            data = rfile.read()
        lines = []
        line = ""
        for char in data:
            if char == "\n":
                lines.append(line)
                line = ""
            else:
                line += char
        
        num = ""
        cond = False
        for char in lines[2]:
            if cond and char != "\"":
                num += char
            elif char == "\"":
                cond = not cond
        if not int(num) in fitnesses:
            os.remove(file)

    for keyb in gen:
        if gen[keyb][0] in fitnesses:
            score = gen[keyb][0]
            accent = gen[keyb][1]["row_1"]["`"][0]
            tilde = gen[keyb][1]["row_1"]["`"][1]
            one = gen[keyb][1]["row_1"]["1"][0]
            exclamation = gen[keyb][1]["row_1"]["1"][1] 
            two = gen[keyb][1]["row_1"]["2"][0] 
            at = gen[keyb][1]["row_1"]["2"][1] 
            three = gen[keyb][1]["row_1"]["3"][0] 
            pound = gen[keyb][1]["row_1"]["3"][1]
            four = gen[keyb][1]["row_1"]["4"][0]
            dollar = gen[keyb][1]["row_1"]["4"][1]
            five = gen[keyb][1]["row_1"]["5"][0]
            percent = gen[keyb][1]["row_1"]["5"][1]
            six = gen[keyb][1]["row_1"]["6"][0]
            carat = gen[keyb][1]["row_1"]["6"][1]
            seven = gen[keyb][1]["row_1"]["7"][0]
            ampersand = gen[keyb][1]["row_1"]["7"][1]
            eight = gen[keyb][1]["row_1"]["8"][0]
            asterisk = gen[keyb][1]["row_1"]["8"][1]
            nine = gen[keyb][1]["row_1"]["9"][0]
            lparanthesis = gen[keyb][1]["row_1"]["9"][1]
            zero = gen[keyb][1]["row_1"]["0"][0]
            rparanthesis = gen[keyb][1]["row_1"]["0"][1]
            minus = gen[keyb][1]["row_1"]["-"][0]
            underscore = gen[keyb][1]["row_1"]["-"][1]
            equals = gen[keyb][1]["row_1"]["="][0]
            plus = gen[keyb][1]["row_1"]["="][1]

            q = gen[keyb][1]["row_2"]["q"][0]
            Q = gen[keyb][1]["row_2"]["q"][1]
            w = gen[keyb][1]["row_2"]["w"][0]
            W = gen[keyb][1]["row_2"]["w"][1]
            e = gen[keyb][1]["row_2"]["e"][0]
            E = gen[keyb][1]["row_2"]["e"][1]
            r = gen[keyb][1]["row_2"]["r"][0]
            R = gen[keyb][1]["row_2"]["r"][1]
            t = gen[keyb][1]["row_2"]["t"][0]
            T = gen[keyb][1]["row_2"]["t"][1]
            y = gen[keyb][1]["row_2"]["y"][0]
            Y = gen[keyb][1]["row_2"]["y"][1]
            u = gen[keyb][1]["row_2"]["u"][0]
            U = gen[keyb][1]["row_2"]["u"][1]
            i = gen[keyb][1]["row_2"]["i"][0]
            I = gen[keyb][1]["row_2"]["i"][1]
            o = gen[keyb][1]["row_2"]["o"][0]
            O = gen[keyb][1]["row_2"]["o"][1]
            p = gen[keyb][1]["row_2"]["p"][0]
            P = gen[keyb][1]["row_2"]["p"][1]
            lsquare = gen[keyb][1]["row_2"]["["][0]
            lcurly = gen[keyb][1]["row_2"]["["][1]
            rsquare = gen[keyb][1]["row_2"]["]"][0]
            rcurly = gen[keyb][1]["row_2"]["]"][1]
            fslash = gen[keyb][1]["row_2"]["\\"][0]
            vline = gen[keyb][1]["row_2"]["\\"][1]

            a = gen[keyb][1]["row_3"]["a"][0]
            A = gen[keyb][1]["row_3"]["a"][1]
            s = gen[keyb][1]["row_3"]["s"][0]
            S = gen[keyb][1]["row_3"]["s"][1]
            d = gen[keyb][1]["row_3"]["d"][0]
            D = gen[keyb][1]["row_3"]["d"][1]
            f = gen[keyb][1]["row_3"]["f"][0]
            F = gen[keyb][1]["row_3"]["f"][1]
            g = gen[keyb][1]["row_3"]["g"][0]
            G = gen[keyb][1]["row_3"]["g"][1]
            h = gen[keyb][1]["row_3"]["h"][0]
            H = gen[keyb][1]["row_3"]["h"][1]
            j = gen[keyb][1]["row_3"]["j"][0]
            J = gen[keyb][1]["row_3"]["j"][1]
            k = gen[keyb][1]["row_3"]["k"][0]
            K = gen[keyb][1]["row_3"]["k"][1]
            l = gen[keyb][1]["row_3"]["l"][0]
            L = gen[keyb][1]["row_3"]["l"][1]
            semicolon = gen[keyb][1]["row_3"][";"][0]
            colon = gen[keyb][1]["row_3"][";"][1]
            apostrophe = gen[keyb][1]["row_3"]["'"][0]
            quote = gen[keyb][1]["row_3"]["'"][1]
            
            z = gen[keyb][1]["row_4"]["z"][0]
            Z = gen[keyb][1]["row_4"]["z"][1]
            x = gen[keyb][1]["row_4"]["x"][0]
            X = gen[keyb][1]["row_4"]["x"][1]
            c = gen[keyb][1]["row_4"]["c"][0]
            C = gen[keyb][1]["row_4"]["c"][1]
            v = gen[keyb][1]["row_4"]["v"][0]
            V = gen[keyb][1]["row_4"]["v"][1]
            b = gen[keyb][1]["row_4"]["b"][0]
            B = gen[keyb][1]["row_4"]["b"][1]
            n = gen[keyb][1]["row_4"]["n"][0]
            N = gen[keyb][1]["row_4"]["n"][1]
            m = gen[keyb][1]["row_4"]["m"][0]
            M = gen[keyb][1]["row_4"]["m"][1]
            comma = gen[keyb][1]["row_4"][","][0]
            less = gen[keyb][1]["row_4"][","][1]
            period = gen[keyb][1]["row_4"]["."][0]
            great = gen[keyb][1]["row_4"]["."][1]
            bslash = gen[keyb][1]["row_4"]["/"][0]
            question = gen[keyb][1]["row_4"]["/"][1]

            file_contents = f"""KBD	{keyb}	\"{keyb}\"

COMPANY	\"{score}\"

LOCALENAME	\"en-US\"

LOCALEID	\"00000409\"

VERSION	1.0

SHIFTSTATE

0	//Column 4
1	//Column 5 : Shft
2	//Column 6 :       Ctrl

LAYOUT		;an extra '@' at the end is a dead key

//SC	VK_		Cap	0	1	2
//--	----		----	----	----	----

02	1		0	{keyname_key[one][1]}	{keyname_key[exclamation][1]}	-1		// {keyname_key[one][0]}, {keyname_key[exclamation][0]}, <none>
03	2		0	{keyname_key[two][1]}	{keyname_key[at][1]}	-1		// {keyname_key[two][0]}, {keyname_key[at][0]}, <none>
04	3		0	{keyname_key[three][1]}	{keyname_key[pound][1]}	-1		// {keyname_key[three][0]}, {keyname_key[pound][0]}, <none>
05	4		0	{keyname_key[four][1]}	{keyname_key[dollar][1]}	-1		// {keyname_key[four][0]}, {keyname_key[dollar][0]}, <none>
06	5		0	{keyname_key[five][1]}	{keyname_key[percent][1]}	-1		// {keyname_key[five][0]}, {keyname_key[percent][0]}, <none>
07	6		0	{keyname_key[six][1]}	{keyname_key[carat][1]}	-1		// {keyname_key[six][0]}, {keyname_key[carat][0]}, <none>
08	7		0	{keyname_key[seven][1]}	{keyname_key[ampersand][1]}	-1		// {keyname_key[seven][0]}, {keyname_key[ampersand][0]}, <none>
09	8		0	{keyname_key[eight][1]}	{keyname_key[asterisk][1]}	-1		// {keyname_key[eight][0]}, {keyname_key[asterisk][0]}, <none>
0a	9		0	{keyname_key[nine][1]}	{keyname_key[lparanthesis][1]}	-1		// {keyname_key[nine][0]}, {keyname_key[lparanthesis][0]}, <none>
0b	0		0	{keyname_key[zero][1]}	{keyname_key[rparanthesis][1]}	-1		// {keyname_key[zero][0]}, {keyname_key[rparanthesis][0]}, <none>
0c	OEM_MINUS	0	{keyname_key[minus][1]}	{keyname_key[underscore][1]}	-1		// {keyname_key[minus][0]}, {keyname_key[underscore][0]}, <none>
0d	OEM_PLUS	0	{keyname_key[equals][1]}	{keyname_key[plus][1]}	-1		// {keyname_key[equals][0]}, {keyname_key[plus][0]}, <none>
10	Q		1	{keyname_key[q][1]}	{keyname_key[Q][1]}	-1		// {keyname_key[q][0]}, {keyname_key[Q][0]}, <none>
11	W		1	{keyname_key[w][1]}	{keyname_key[W][1]}	-1		// {keyname_key[w][0]}, {keyname_key[W][0]}, <none>
12	E		1	{keyname_key[e][1]}	{keyname_key[E][1]}	-1		// {keyname_key[e][0]}, {keyname_key[E][0]}, <none>
13	R		1	{keyname_key[r][1]}	{keyname_key[R][1]}	-1		// {keyname_key[r][0]}, {keyname_key[R][0]}, <none>
14	T		1	{keyname_key[t][1]}	{keyname_key[T][1]}	-1		// {keyname_key[t][0]}, {keyname_key[T][0]}, <none>
15	Y		1	{keyname_key[y][1]}	{keyname_key[Y][1]}	-1		// {keyname_key[y][0]}, {keyname_key[Y][0]}, <none>
16	U		1	{keyname_key[u][1]}	{keyname_key[U][1]}	-1		// {keyname_key[u][0]}, {keyname_key[U][0]}, <none>
17	I		1	{keyname_key[i][1]}	{keyname_key[I][1]}	-1		// {keyname_key[i][0]}, {keyname_key[I][0]}, <none>
18	O		1	{keyname_key[o][1]}	{keyname_key[O][1]}	-1		// {keyname_key[o][0]}, {keyname_key[O][0]}, <none>
19	P		1	{keyname_key[p][1]}	{keyname_key[P][1]}	-1		// {keyname_key[p][0]}, {keyname_key[P][0]}, <none>
1a	OEM_4		0	{keyname_key[lsquare][1]}	{keyname_key[lcurly][1]}	-1		// {keyname_key[lsquare][0]}, {keyname_key[lcurly][0]}, <none>
1b	OEM_6		0	{keyname_key[rsquare][1]}	{keyname_key[rcurly][1]}	-1		// {keyname_key[rsquare][0]}, {keyname_key[rcurly][0]}, <none>
1e	A		1	{keyname_key[a][1]}	{keyname_key[A][1]}	-1		// {keyname_key[a][0]}, {keyname_key[A][0]}, <none>
1f	S		1	{keyname_key[s][1]}	{keyname_key[S][1]}	-1		// {keyname_key[s][0]}, {keyname_key[S][0]}, <none>
20	D		1	{keyname_key[d][1]}	{keyname_key[D][1]}	-1		// {keyname_key[d][0]}, {keyname_key[D][0]}, <none>
21	F		1	{keyname_key[f][1]}	{keyname_key[F][1]}	-1		// {keyname_key[f][0]}, {keyname_key[F][0]}, <none>
22	G		1	{keyname_key[g][1]}	{keyname_key[G][1]}	-1		// {keyname_key[g][0]}, {keyname_key[G][0]}, <none>
23	H		1	{keyname_key[h][1]}	{keyname_key[H][1]}	-1		// {keyname_key[h][0]}, {keyname_key[H][0]}, <none>
24	J		1	{keyname_key[j][1]}	{keyname_key[J][1]}	-1		// {keyname_key[j][0]}, {keyname_key[J][0]}, <none>
25	K		1	{keyname_key[k][1]}	{keyname_key[K][1]}	-1		// {keyname_key[k][0]}, {keyname_key[K][0]}, <none>
26	L		1	{keyname_key[l][1]}	{keyname_key[L][1]}	-1		// {keyname_key[l][0]}, {keyname_key[L][0]}, <none>
27	OEM_1		0	{keyname_key[semicolon][1]}	{keyname_key[colon][1]}	-1		// {keyname_key[semicolon][0]}, {keyname_key[colon][0]}, <none>
28	OEM_7		0	{keyname_key[apostrophe][1]}	{keyname_key[quote][1]}	-1		// {keyname_key[apostrophe][0]}, {keyname_key[quote][0]}, <none>
29	OEM_3		0	{keyname_key[accent][1]}	{keyname_key[tilde][1]}	-1		// {keyname_key[accent][0]}, {keyname_key[tilde][0]}, <none>
2b	OEM_5		0	{keyname_key[fslash][1]}	{keyname_key[vline][1]}	-1		// {keyname_key[fslash][0]}, {keyname_key[vline][0]}, <none>
2c	Z		1	{keyname_key[z][1]}	{keyname_key[Z][1]}	-1		// {keyname_key[z][0]}, {keyname_key[Z][0]}, <none>
2d	X		1	{keyname_key[x][1]}	{keyname_key[X][1]}	-1		// {keyname_key[x][0]}, {keyname_key[X][0]}, <none>
2e	C		1	{keyname_key[c][1]}	{keyname_key[C][1]}	-1		// {keyname_key[c][0]}, {keyname_key[C][0]}, <none>
2f	V		1	{keyname_key[v][1]}	{keyname_key[V][1]}	-1		// {keyname_key[v][0]}, {keyname_key[V][0]}, <none>
30	B		1	{keyname_key[b][1]}	{keyname_key[B][1]}	-1		// {keyname_key[b][0]}, {keyname_key[B][0]}, <none>
31	N		1	{keyname_key[n][1]}	{keyname_key[N][1]}	-1		// {keyname_key[n][0]}, {keyname_key[N][0]}, <none>
32	M		1	{keyname_key[m][1]}	{keyname_key[M][1]}	-1		// {keyname_key[m][0]}, {keyname_key[M][0]}, <none>
33	OEM_COMMA	0	{keyname_key[comma][1]}	{keyname_key[less][1]}	-1		// {keyname_key[comma][0]}, {keyname_key[less][0]}, <none>
34	OEM_PERIOD	0	{keyname_key[period][1]}	{keyname_key[great][1]}	-1		// {keyname_key[period][0]}, {keyname_key[great][0]}, <none>
35	OEM_2		0	{keyname_key[bslash][1]}	{keyname_key[question][1]}	-1		// {keyname_key[bslash][0]}, {keyname_key[question][0]}, <none>
39	SPACE		0	0020	0020	0020		// SPACE, SPACE, SPACE
56	OEM_102	0	005c	007c	001c		// REVERSE SOLIDUS, VERTICAL LINE, INFORMATION SEPARATOR FOUR
53	DECIMAL	0	002e	002e	-1		// FULL STOP, FULL STOP, 

KEYNAME

01	Esc
0e	Backspace
0f	Tab
1c	Enter
1d	Ctrl
2a	Shift
36	\"Right Shift\"
37	\"Num *\"
38	Alt
39	Space
3a	\"Caps Lock\"
3b	F1
3c	F2
3d	F3
3e	F4
3f	F5
40	F6
41	F7
42	F8
43	F9
44	F10
45	Pause
46	\"Scroll Lock\"
47	\"Num 7\"
48	\"Num 8\"
49	\"Num 9\"
4a	\"Num -\"
4b	\"Num 4\"
4c	\"Num 5\"
4d	\"Num 6\"
4e	\"Num +\"
4f	\"Num 1\"
50	\"Num 2\"
51	\"Num 3\"
52	\"Num 0\"
53	\"Num Del\"
54	\"Sys Req\"
57	F11
58	F12
7c	F13
7d	F14
7e	F15
7f	F16
80	F17
81	F18
82	F19
83	F20
84	F21
85	F22
86	F23
87	F24

KEYNAME_EXT

1c	\"Num Enter\"
1d	\"Right Ctrl\"
35	\"Num /\"
37	\"Prnt Scrn\"
38	\"Right Alt\"
45	\"Num Lock\"
46	Break
47	Home
48	Up
49	\"Page Up\"
4b	Left
4d	Right
4f	End
50	Down
51	\"Page Down\"
52	Insert
53	Delete
54	<00>
56	Help
5b	\"Left Windows\"
5c	\"Right Windows\"
5d	Application

DESCRIPTIONS

0409	{keyb}
LANGUAGENAMES

0409	English (United States)
ENDKBD
"""
            with open(TOP_KEYBOARDS_DIR / f"{keyb}.klc", 'x') as keybfile:
                pass
            with open(TOP_KEYBOARDS_DIR / f"{keyb}.klc", 'w') as keybfile:
                keybfile.write(file_contents)

    

    newfiles = []
    for newfile in Path(TOP_KEYBOARDS_DIR).iterdir():
        newfiles.append(newfile)

    if len(newfiles) > 5:
        removenum = len(newfiles) - 5
    else:
        removenum = 0
    
    i = 1
    for fitness in fitnesses[::-1]:
        files = []
        for file in Path(TOP_KEYBOARDS_DIR).iterdir():
            files.append(file)

        for file in files:
            if removenum == 0:
                return 0
            with open(file, 'r') as rfile:
                data = rfile.read()
            lines = []
            line = ""
            for char in data:
                if char == "\n":
                    lines.append(line)
                    line = ""
                else:
                    line += char
            
            num = ""
            cond = False
            for char in lines[2]:
                if cond and char != "\"":
                    num += char
                elif char == "\"":
                    cond = not cond
            
            if int(num) == fitness:
                os.remove(file)
                removenum -= 1 
        
def get_gen():
    """
    Loads the most recent generation of keyboards from the generations/ folder.

    Finds the highest-numbered generation subfolder, reads every .klc file inside it,
    and returns the raw lines of each file as a list of lists.

    If no generations exist yet (fresh start), automatically calls initialize.gen1()
    to create the first generation, then loads it.
    """
    gen = []
    files = []
    for genfile in GENERATIONS_DIR.iterdir():
        files.append(genfile)

    if len(files) == 0:
        initial.gen1()
        return get_gen()

    else:
        indexes = []
        for file in files:
            file = str(file)
            indexes.append(int(file[41:]))
        indexes.sort()

        for path in files:
            if int(str(path)[41:]) == indexes[-1]:
                keybfiles = []
                for keybfile in Path(path).iterdir():
                    keybfiles.append(keybfile)

        for path in keybfiles:
            keyb = []
            with open(path, 'r') as datafile:
                data = datafile.read()

            line = ""
            for char in data:
                if char == "\n":
                    keyb.append(line)
                    line = ""
                else:
                    line += char

            gen.append(keyb)

        return gen

def get_top_keybs():
    """
    Loads all keyboard .klc files from the top_keyboards/ folder and returns
    their raw lines as a list of lists — same format as get_gen().
    """
    gen = []
    files = []
    for file in Path(TOP_KEYBOARDS_DIR).iterdir():
        files.append(file)

    for path in files:
        with open(path, 'r') as file:
            data = file.read()
        keyb = []
        line = ""
        for char in data:
            if char == "\n":
                keyb.append(line)
                line = ""
            else:
                line += char
        gen.append(keyb)

    return gen

def new_gen(gen):
    """
    Saves a new generation to disk.

    Creates a new subfolder inside generations/ (e.g. Gen42/), writes every keyboard
    in the generation as a .klc file inside it, and appends a placeholder entry to
    the all-generations CSV which will be filled in with scores once evaluated.

    The .klc file format is the standard Windows Keyboard Layout Creator format,
    which means any layout saved here can be installed and used on Windows directly.
    """
    gen_name = f"Gen{int(get_index()) + 1}"
    path = GENERATIONS_DIR / gen_name
    os.mkdir(path)

    with open(CSV_ALL_GENS, 'a') as file:
        file.write(f"{gen_name}, -, -\n")
    
    for keyb in gen:
        score = gen[keyb][0]
        accent = gen[keyb][1]["row_1"]["`"][0]
        tilde = gen[keyb][1]["row_1"]["`"][1]
        one = gen[keyb][1]["row_1"]["1"][0]
        exclamation = gen[keyb][1]["row_1"]["1"][1] 
        two = gen[keyb][1]["row_1"]["2"][0] 
        at = gen[keyb][1]["row_1"]["2"][1] 
        three = gen[keyb][1]["row_1"]["3"][0] 
        pound = gen[keyb][1]["row_1"]["3"][1]
        four = gen[keyb][1]["row_1"]["4"][0]
        dollar = gen[keyb][1]["row_1"]["4"][1]
        five = gen[keyb][1]["row_1"]["5"][0]
        percent = gen[keyb][1]["row_1"]["5"][1]
        six = gen[keyb][1]["row_1"]["6"][0]
        carat = gen[keyb][1]["row_1"]["6"][1]
        seven = gen[keyb][1]["row_1"]["7"][0]
        ampersand = gen[keyb][1]["row_1"]["7"][1]
        eight = gen[keyb][1]["row_1"]["8"][0]
        asterisk = gen[keyb][1]["row_1"]["8"][1]
        nine = gen[keyb][1]["row_1"]["9"][0]
        lparanthesis = gen[keyb][1]["row_1"]["9"][1]
        zero = gen[keyb][1]["row_1"]["0"][0]
        rparanthesis = gen[keyb][1]["row_1"]["0"][1]
        minus = gen[keyb][1]["row_1"]["-"][0]
        underscore = gen[keyb][1]["row_1"]["-"][1]
        equals = gen[keyb][1]["row_1"]["="][0]
        plus = gen[keyb][1]["row_1"]["="][1]

        q = gen[keyb][1]["row_2"]["q"][0]
        Q = gen[keyb][1]["row_2"]["q"][1]
        w = gen[keyb][1]["row_2"]["w"][0]
        W = gen[keyb][1]["row_2"]["w"][1]
        e = gen[keyb][1]["row_2"]["e"][0]
        E = gen[keyb][1]["row_2"]["e"][1]
        r = gen[keyb][1]["row_2"]["r"][0]
        R = gen[keyb][1]["row_2"]["r"][1]
        t = gen[keyb][1]["row_2"]["t"][0]
        T = gen[keyb][1]["row_2"]["t"][1]
        y = gen[keyb][1]["row_2"]["y"][0]
        Y = gen[keyb][1]["row_2"]["y"][1]
        u = gen[keyb][1]["row_2"]["u"][0]
        U = gen[keyb][1]["row_2"]["u"][1]
        i = gen[keyb][1]["row_2"]["i"][0]
        I = gen[keyb][1]["row_2"]["i"][1]
        o = gen[keyb][1]["row_2"]["o"][0]
        O = gen[keyb][1]["row_2"]["o"][1]
        p = gen[keyb][1]["row_2"]["p"][0]
        P = gen[keyb][1]["row_2"]["p"][1]
        lsquare = gen[keyb][1]["row_2"]["["][0]
        lcurly = gen[keyb][1]["row_2"]["["][1]
        rsquare = gen[keyb][1]["row_2"]["]"][0]
        rcurly = gen[keyb][1]["row_2"]["]"][1]
        fslash = gen[keyb][1]["row_2"]["\\"][0]
        vline = gen[keyb][1]["row_2"]["\\"][1]

        a = gen[keyb][1]["row_3"]["a"][0]
        A = gen[keyb][1]["row_3"]["a"][1]
        s = gen[keyb][1]["row_3"]["s"][0]
        S = gen[keyb][1]["row_3"]["s"][1]
        d = gen[keyb][1]["row_3"]["d"][0]
        D = gen[keyb][1]["row_3"]["d"][1]
        f = gen[keyb][1]["row_3"]["f"][0]
        F = gen[keyb][1]["row_3"]["f"][1]
        g = gen[keyb][1]["row_3"]["g"][0]
        G = gen[keyb][1]["row_3"]["g"][1]
        h = gen[keyb][1]["row_3"]["h"][0]
        H = gen[keyb][1]["row_3"]["h"][1]
        j = gen[keyb][1]["row_3"]["j"][0]
        J = gen[keyb][1]["row_3"]["j"][1]
        k = gen[keyb][1]["row_3"]["k"][0]
        K = gen[keyb][1]["row_3"]["k"][1]
        l = gen[keyb][1]["row_3"]["l"][0]
        L = gen[keyb][1]["row_3"]["l"][1]
        semicolon = gen[keyb][1]["row_3"][";"][0]
        colon = gen[keyb][1]["row_3"][";"][1]
        apostrophe = gen[keyb][1]["row_3"]["'"][0]
        quote = gen[keyb][1]["row_3"]["'"][1]
        
        z = gen[keyb][1]["row_4"]["z"][0]
        Z = gen[keyb][1]["row_4"]["z"][1]
        x = gen[keyb][1]["row_4"]["x"][0]
        X = gen[keyb][1]["row_4"]["x"][1]
        c = gen[keyb][1]["row_4"]["c"][0]
        C = gen[keyb][1]["row_4"]["c"][1]
        v = gen[keyb][1]["row_4"]["v"][0]
        V = gen[keyb][1]["row_4"]["v"][1]
        b = gen[keyb][1]["row_4"]["b"][0]
        B = gen[keyb][1]["row_4"]["b"][1]
        n = gen[keyb][1]["row_4"]["n"][0]
        N = gen[keyb][1]["row_4"]["n"][1]
        m = gen[keyb][1]["row_4"]["m"][0]
        M = gen[keyb][1]["row_4"]["m"][1]
        comma = gen[keyb][1]["row_4"][","][0]
        less = gen[keyb][1]["row_4"][","][1]
        period = gen[keyb][1]["row_4"]["."][0]
        great = gen[keyb][1]["row_4"]["."][1]
        bslash = gen[keyb][1]["row_4"]["/"][0]
        question = gen[keyb][1]["row_4"]["/"][1]

        file_contents = f"""KBD	{keyb}	\"{keyb}\"

COMPANY	\"{score}\"

LOCALENAME	\"en-US\"

LOCALEID	\"00000409\"

VERSION	1.0

SHIFTSTATE

0	//Column 4
1	//Column 5 : Shft
2	//Column 6 :       Ctrl

LAYOUT		;an extra '@' at the end is a dead key

//SC	VK_		Cap	0	1	2
//--	----		----	----	----	----

02	1		0	{keyname_key[one][1]}	{keyname_key[exclamation][1]}	-1		// {keyname_key[one][0]}, {keyname_key[exclamation][0]}, <none>
03	2		0	{keyname_key[two][1]}	{keyname_key[at][1]}	-1		// {keyname_key[two][0]}, {keyname_key[at][0]}, <none>
04	3		0	{keyname_key[three][1]}	{keyname_key[pound][1]}	-1		// {keyname_key[three][0]}, {keyname_key[pound][0]}, <none>
05	4		0	{keyname_key[four][1]}	{keyname_key[dollar][1]}	-1		// {keyname_key[four][0]}, {keyname_key[dollar][0]}, <none>
06	5		0	{keyname_key[five][1]}	{keyname_key[percent][1]}	-1		// {keyname_key[five][0]}, {keyname_key[percent][0]}, <none>
07	6		0	{keyname_key[six][1]}	{keyname_key[carat][1]}	-1		// {keyname_key[six][0]}, {keyname_key[carat][0]}, <none>
08	7		0	{keyname_key[seven][1]}	{keyname_key[ampersand][1]}	-1		// {keyname_key[seven][0]}, {keyname_key[ampersand][0]}, <none>
09	8		0	{keyname_key[eight][1]}	{keyname_key[asterisk][1]}	-1		// {keyname_key[eight][0]}, {keyname_key[asterisk][0]}, <none>
0a	9		0	{keyname_key[nine][1]}	{keyname_key[lparanthesis][1]}	-1		// {keyname_key[nine][0]}, {keyname_key[lparanthesis][0]}, <none>
0b	0		0	{keyname_key[zero][1]}	{keyname_key[rparanthesis][1]}	-1		// {keyname_key[zero][0]}, {keyname_key[rparanthesis][0]}, <none>
0c	OEM_MINUS	0	{keyname_key[minus][1]}	{keyname_key[underscore][1]}	-1		// {keyname_key[minus][0]}, {keyname_key[underscore][0]}, <none>
0d	OEM_PLUS	0	{keyname_key[equals][1]}	{keyname_key[plus][1]}	-1		// {keyname_key[equals][0]}, {keyname_key[plus][0]}, <none>
10	Q		1	{keyname_key[q][1]}	{keyname_key[Q][1]}	-1		// {keyname_key[q][0]}, {keyname_key[Q][0]}, <none>
11	W		1	{keyname_key[w][1]}	{keyname_key[W][1]}	-1		// {keyname_key[w][0]}, {keyname_key[W][0]}, <none>
12	E		1	{keyname_key[e][1]}	{keyname_key[E][1]}	-1		// {keyname_key[e][0]}, {keyname_key[E][0]}, <none>
13	R		1	{keyname_key[r][1]}	{keyname_key[R][1]}	-1		// {keyname_key[r][0]}, {keyname_key[R][0]}, <none>
14	T		1	{keyname_key[t][1]}	{keyname_key[T][1]}	-1		// {keyname_key[t][0]}, {keyname_key[T][0]}, <none>
15	Y		1	{keyname_key[y][1]}	{keyname_key[Y][1]}	-1		// {keyname_key[y][0]}, {keyname_key[Y][0]}, <none>
16	U		1	{keyname_key[u][1]}	{keyname_key[U][1]}	-1		// {keyname_key[u][0]}, {keyname_key[U][0]}, <none>
17	I		1	{keyname_key[i][1]}	{keyname_key[I][1]}	-1		// {keyname_key[i][0]}, {keyname_key[I][0]}, <none>
18	O		1	{keyname_key[o][1]}	{keyname_key[O][1]}	-1		// {keyname_key[o][0]}, {keyname_key[O][0]}, <none>
19	P		1	{keyname_key[p][1]}	{keyname_key[P][1]}	-1		// {keyname_key[p][0]}, {keyname_key[P][0]}, <none>
1a	OEM_4		0	{keyname_key[lsquare][1]}	{keyname_key[lcurly][1]}	-1		// {keyname_key[lsquare][0]}, {keyname_key[lcurly][0]}, <none>
1b	OEM_6		0	{keyname_key[rsquare][1]}	{keyname_key[rcurly][1]}	-1		// {keyname_key[rsquare][0]}, {keyname_key[rcurly][0]}, <none>
1e	A		1	{keyname_key[a][1]}	{keyname_key[A][1]}	-1		// {keyname_key[a][0]}, {keyname_key[A][0]}, <none>
1f	S		1	{keyname_key[s][1]}	{keyname_key[S][1]}	-1		// {keyname_key[s][0]}, {keyname_key[S][0]}, <none>
20	D		1	{keyname_key[d][1]}	{keyname_key[D][1]}	-1		// {keyname_key[d][0]}, {keyname_key[D][0]}, <none>
21	F		1	{keyname_key[f][1]}	{keyname_key[F][1]}	-1		// {keyname_key[f][0]}, {keyname_key[F][0]}, <none>
22	G		1	{keyname_key[g][1]}	{keyname_key[G][1]}	-1		// {keyname_key[g][0]}, {keyname_key[G][0]}, <none>
23	H		1	{keyname_key[h][1]}	{keyname_key[H][1]}	-1		// {keyname_key[h][0]}, {keyname_key[H][0]}, <none>
24	J		1	{keyname_key[j][1]}	{keyname_key[J][1]}	-1		// {keyname_key[j][0]}, {keyname_key[J][0]}, <none>
25	K		1	{keyname_key[k][1]}	{keyname_key[K][1]}	-1		// {keyname_key[k][0]}, {keyname_key[K][0]}, <none>
26	L		1	{keyname_key[l][1]}	{keyname_key[L][1]}	-1		// {keyname_key[l][0]}, {keyname_key[L][0]}, <none>
27	OEM_1		0	{keyname_key[semicolon][1]}	{keyname_key[colon][1]}	-1		// {keyname_key[semicolon][0]}, {keyname_key[colon][0]}, <none>
28	OEM_7		0	{keyname_key[apostrophe][1]}	{keyname_key[quote][1]}	-1		// {keyname_key[apostrophe][0]}, {keyname_key[quote][0]}, <none>
29	OEM_3		0	{keyname_key[accent][1]}	{keyname_key[tilde][1]}	-1		// {keyname_key[accent][0]}, {keyname_key[tilde][0]}, <none>
2b	OEM_5		0	{keyname_key[fslash][1]}	{keyname_key[vline][1]}	-1		// {keyname_key[fslash][0]}, {keyname_key[vline][0]}, <none>
2c	Z		1	{keyname_key[z][1]}	{keyname_key[Z][1]}	-1		// {keyname_key[z][0]}, {keyname_key[Z][0]}, <none>
2d	X		1	{keyname_key[x][1]}	{keyname_key[X][1]}	-1		// {keyname_key[x][0]}, {keyname_key[X][0]}, <none>
2e	C		1	{keyname_key[c][1]}	{keyname_key[C][1]}	-1		// {keyname_key[c][0]}, {keyname_key[C][0]}, <none>
2f	V		1	{keyname_key[v][1]}	{keyname_key[V][1]}	-1		// {keyname_key[v][0]}, {keyname_key[V][0]}, <none>
30	B		1	{keyname_key[b][1]}	{keyname_key[B][1]}	-1		// {keyname_key[b][0]}, {keyname_key[B][0]}, <none>
31	N		1	{keyname_key[n][1]}	{keyname_key[N][1]}	-1		// {keyname_key[n][0]}, {keyname_key[N][0]}, <none>
32	M		1	{keyname_key[m][1]}	{keyname_key[M][1]}	-1		// {keyname_key[m][0]}, {keyname_key[M][0]}, <none>
33	OEM_COMMA	0	{keyname_key[comma][1]}	{keyname_key[less][1]}	-1		// {keyname_key[comma][0]}, {keyname_key[less][0]}, <none>
34	OEM_PERIOD	0	{keyname_key[period][1]}	{keyname_key[great][1]}	-1		// {keyname_key[period][0]}, {keyname_key[great][0]}, <none>
35	OEM_2		0	{keyname_key[bslash][1]}	{keyname_key[question][1]}	-1		// {keyname_key[bslash][0]}, {keyname_key[question][0]}, <none>
39	SPACE		0	0020	0020	0020		// SPACE, SPACE, SPACE
56	OEM_102	0	005c	007c	001c		// REVERSE SOLIDUS, VERTICAL LINE, INFORMATION SEPARATOR FOUR
53	DECIMAL	0	002e	002e	-1		// FULL STOP, FULL STOP, 

KEYNAME

01	Esc
0e	Backspace
0f	Tab
1c	Enter
1d	Ctrl
2a	Shift
36	\"Right Shift\"
37	\"Num *\"
38	Alt
39	Space
3a	\"Caps Lock\"
3b	F1
3c	F2
3d	F3
3e	F4
3f	F5
40	F6
41	F7
42	F8
43	F9
44	F10
45	Pause
46	\"Scroll Lock\"
47	\"Num 7\"
48	\"Num 8\"
49	\"Num 9\"
4a	\"Num -\"
4b	\"Num 4\"
4c	\"Num 5\"
4d	\"Num 6\"
4e	\"Num +\"
4f	\"Num 1\"
50	\"Num 2\"
51	\"Num 3\"
52	\"Num 0\"
53	\"Num Del\"
54	\"Sys Req\"
57	F11
58	F12
7c	F13
7d	F14
7e	F15
7f	F16
80	F17
81	F18
82	F19
83	F20
84	F21
85	F22
86	F23
87	F24

KEYNAME_EXT

1c	\"Num Enter\"
1d	\"Right Ctrl\"
35	\"Num /\"
37	\"Prnt Scrn\"
38	\"Right Alt\"
45	\"Num Lock\"
46	Break
47	Home
48	Up
49	\"Page Up\"
4b	Left
4d	Right
4f	End
50	Down
51	\"Page Down\"
52	Insert
53	Delete
54	<00>
56	Help
5b	\"Left Windows\"
5c	\"Right Windows\"
5d	Application

DESCRIPTIONS

0409	{keyb}
LANGUAGENAMES

0409	English (United States)
ENDKBD
"""
        with open(GENERATIONS_DIR / gen_name / f"{keyb}.klc", 'x') as file:
            pass
        with open(GENERATIONS_DIR / gen_name / f"{keyb}.klc", 'w') as file:
            file.write(file_contents)

def cleanup():
    """
    Called when the user interrupts the algorithm (Ctrl+C) mid-generation.

    Resets the last CSV entry so the incomplete generation is not counted,
    keeping the data log consistent for the next run.
    """
    with open(CSV_ALL_GENS, 'r') as file:
        data = file.read()
    lines = []
    line = ""
    for char in data:
        if char == "\n":
            lines.append(line)
            line = ""
        else:
            line += char

    lines[-1] = f"Gen{get_index()}, -, -"

    with open(CSV_ALL_GENS, 'w') as file:
        for line in lines:
            file.write(line + "\n")

def trash():
    """
    Deletes old generation folders to prevent the generations/ folder from growing
    indefinitely over hundreds of runs.

    Keeps Gen1 (the original baseline) and the current generation. Everything
    in between is deleted. This is safe because the algorithm only ever needs
    the most recent generation to continue evolving.
    """
    files = []
    for file in GENERATIONS_DIR.iterdir():
        files.append(file)

    index = get_index()
    if len(str(index)) == 1:
        return 0

    index = str(index)[:-1]
    for generation in files:
        generation = f"{generation}"
        
        if generation[-1] != "1" and generation[41:-1] != index:
            shutil.rmtree(generation)