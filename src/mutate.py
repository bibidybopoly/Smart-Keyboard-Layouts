# mutate.py
# Responsible for producing each new generation of keyboards from the previous one.
#
# There are four mutation strategies, each representing a different way to modify
# a keyboard layout. The algorithm randomly picks one per keyboard each generation.

import populate as pop
import random as rand
import file_manager as manager


def top5(gen):
    """
    Returns the 5 best-scoring keyboards from the given generation.
    Lower scores are better (less finger travel distance).
    """
    top5 = {}
    list= []
    for keyb in gen:
        list.append(gen[keyb][0])
    list.sort()
    list = list[0:5]

    for index, i in enumerate(list):
        for keyb in gen:
            if i == gen[keyb][0] and index == 0:
                top5.update({keyb:gen[keyb]})
            elif i == gen[keyb][0] and index == 1:
                top5.update({keyb:gen[keyb]})
            elif i == gen[keyb][0] and index == 3:
                top5.update({keyb:gen[keyb]})
            elif i == gen[keyb][0] and index == 3:
                top5.update({keyb:gen[keyb]})
            elif i == gen[keyb][0] and index == 4:
                top5.update({keyb:gen[keyb]})

    return top5


def correct(keyb):
    """
    Enforces layout rules on a keyboard after it has been randomized or mutated.

    The rules ensure the layout stays valid and sensible:
      - Bracket pairs (e.g. [ and ]) must stay on adjacent keys.
      - Letters must occupy the lowercase slot of their key.
      - Special characters like ' and ; are shuffled but kept together as pairs.

    This prevents the algorithm from evolving layouts that would be physically
    confusing or impossible to use correctly.
    """
    rows = ["row_1", "row_2", "row_3", "row_4"]
    row1 = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="]
    row2 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"]
    row3 = ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"]
    row4 = ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
    rowkeys = [row1, row2, row3, row4]

    # Keys that opening brackets are not allowed to be placed on.
    leftlockkeys = [
        ["row_1", "`", 0], ["row_1", "1", 0], ["row_1", "2", 0], ["row_1", "3", 0], ["row_1", "4", 0], ["row_1", "5", 0], ["row_1", "6", 0], ["row_1", "7", 0], ["row_1", "8", 0], ["row_1", "9", 0], ["row_1", "0", 0], ["row_1", "=", 0], ["row_1", "=", 1],
        ["row_2", "\\", 0], ["row_2", "\\", 1],
        ["row_3", "'", 0], ["row_3", "'", 1],
        ["row_4", "/", 0], ["row_4", "/", 1],
        ]

    # Keys that number symbols are not allowed to be placed on.
    toplockkeys = [
        ["row_1", "1", 1], ["row_1", "2", 1], ["row_1", "3", 1], ["row_1", "4", 1], ["row_1", "5", 1], ["row_1", "6", 1], ["row_1", "7", 1], ["row_1", "8", 1], ["row_1", "9", 1], ["row_1", "0", 1],
        ["row_1", "1", 0], ["row_1", "2", 0], ["row_1", "3", 0], ["row_1", "4", 0], ["row_1", "5", 0], ["row_1", "6", 0], ["row_1", "7", 0], ["row_1", "8", 0], ["row_1", "9", 0], ["row_1", "0", 0]
    ]

    # Keys that letters are not allowed to be placed on.
    letterlockkeys = [
        ["row_1", "1", 0], ["row_1", "2", 0], ["row_1", "3", 0], ["row_1", "4", 0], ["row_1", "5", 0], ["row_1", "6", 0], ["row_1", "7", 0], ["row_1", "8", 0], ["row_1", "9", 0], ["row_1", "0", 0]
    ]

    leftchars = ("[", "{", "<", "(")
    rights = ("]", "}", ">", ")")
    rightspos = {}
    leftspos = {}
    new_leftspos = {}

    # Ensure each opening bracket is placed to the left of its closing bracket.
    for right, leftchar in enumerate(leftchars):
        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                for i in range(0,2):
                    if leftchar == keyb[1][row][char][i]:
                        leftspos.update({leftchar:[row, char, i]})

        new_leftspos[leftchar] = leftspos[leftchar]
        while new_leftspos[leftchar] in leftlockkeys:
            randrow = rand.randint(0, 3)
            randchar = rand.randint(0, (len(rowkeys[randrow])-1))
            randcase = rand.randint(0, 1)
            new_leftspos[leftchar] = [rows[randrow], rowkeys[randrow][randchar], randcase]

        replace = keyb[1][new_leftspos[leftchar][0]][new_leftspos[leftchar][1]][new_leftspos[leftchar][2]]
        keyb[1][new_leftspos[leftchar][0]][new_leftspos[leftchar][1]][new_leftspos[leftchar][2]] = leftchar
        keyb[1][leftspos[leftchar][0]][leftspos[leftchar][1]][leftspos[leftchar][2]] = replace

        rightrownum = 0
        cond = False
        while not cond:
            for charnum, char in enumerate(rowkeys[rightrownum]):
                for i in range(0,2):
                    if rights[right] == keyb[1][rows[rightrownum]][char][i]:
                        rightspos.update({rights[right]:[rows[rightrownum], char, i]})
                        cond = True
            rightrownum += 1

        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                for i in range(0,2):
                    if leftchar == keyb[1][row][char][i]:
                        replace = keyb[1][row][rowkeys[rownum][charnum+1]][i]
                        keyb[1][row][rowkeys[rownum][charnum+1]][i] = rights[right]
                        keyb[1][rightspos[rights[right]][0]][rightspos[rights[right]][1]][rightspos[rights[right]][2]] = replace
                        leftlockkeys.append([row, rowkeys[rownum][charnum - 1], 1])
                        leftlockkeys.append([row, char, i])
                        leftlockkeys.append([row, rowkeys[rownum][charnum + 1], i])
                        toplockkeys.append([row, char, 0])
                        toplockkeys.append([row, rowkeys[rownum][charnum + 1], 0])
                        toplockkeys.append([row, char, 1])
                        toplockkeys.append([row, rowkeys[rownum][charnum + 1], 1])
                        letterlockkeys.append([row, char, 0])
                        letterlockkeys.append([row, rowkeys[rownum][charnum + 1], 0])

    # All 26 letters mapped to their lowercase/uppercase pair.
    letters = {
        "q":["q", "Q"], "w":["w", "W"], "e":["e", "E"], "r":["r", "R"], "t":["t", "T"], "y":["y", "Y"], "u":["u", "U"], "i":["i", "I"], "o":["o", "O"], "p":["p", "P"],
        "a":["a", "A"], "s":["s", "S"], "d":["d", "D"], "f":["f", "F"], "g":["g", "G"], "h":["h", "H"], "j":["j", "J"], "k":["k", "K"], "l":["l", "L"],
        "z":["z", "Z"], "x":["x", "X"], "c":["c", "C"], "v":["v", "V"], "b":["b", "B"], "n":["n", "N"], "m":["m", "M"]
        }

    # Place each letter in the lowercase slot of a valid key position.
    for letter in letters:

        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                for i in range(0,2):
                    if letter == keyb[1][row][char][i]:
                        initialpos = [row, char, i]

        new_initialpos = [initialpos[0], initialpos[1], 0]
        while new_initialpos in letterlockkeys:
            randrow = rand.randint(0, 3)
            randchar = rand.randint(0, (len(rowkeys[randrow])-1))
            new_initialpos = [rows[randrow], rowkeys[randrow][randchar], 0]

        replace = keyb[1][new_initialpos[0]][new_initialpos[1]][0]
        keyb[1][new_initialpos[0]][new_initialpos[1]][0] = letter
        keyb[1][initialpos[0]][initialpos[1]][initialpos[2]] = replace

        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                for i in range(0,2):
                    if letters[letter][1] == keyb[1][row][char][i]:
                        replacepos = [row, char, i]

        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                if letter == keyb[1][row][char][0]:
                    replace = keyb[1][row][char][1]
                    keyb[1][row][char][1] = letters[letter][1]
                    keyb[1][replacepos[0]][replacepos[1]][replacepos[2]] = replace
                    toplockkeys.append([row, char, 0])
                    toplockkeys.append([row, char, 1])
                    letterlockkeys.append([row, char, 0])

    # Special character pairs (' ") and (; :) are shuffled but kept together.
    specchars = {"'":["'", "\""], ";":[";", ":"]}

    for speccharset in specchars:
        rand.shuffle(specchars[speccharset])

        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                for i in range(0,2):
                    if specchars[speccharset][0] == keyb[1][row][char][i]:
                        initialpos = [row, char, i]

        new_initialpos = initialpos
        while new_initialpos in toplockkeys:
            randrow = rand.randint(0, 3)
            randchar = rand.randint(0, (len(rowkeys[randrow])-1))
            randcase = rand.randint(0, 1)
            new_initialpos = [rows[randrow], rowkeys[randrow][randchar], randcase]

        replace = keyb[1][new_initialpos[0]][new_initialpos[1]][new_initialpos[2]]
        keyb[1][new_initialpos[0]][new_initialpos[1]][new_initialpos[2]] = specchars[speccharset][0]
        keyb[1][initialpos[0]][initialpos[1]][initialpos[2]] = replace

        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                for i in range(0,2):
                    if specchars[speccharset][1] == keyb[1][row][char][i]:
                        replacepos = [row, char, i]

        for rownum, row in enumerate(rows):
            for charnum, char in enumerate(rowkeys[rownum]):
                for i in range(0,2):
                    if specchars[speccharset][0] == keyb[1][row][char][i]:
                        replace = keyb[1][row][char][abs(i-1)]
                        keyb[1][row][char][abs(i-1)] = specchars[speccharset][1]
                        keyb[1][replacepos[0]][replacepos[1]][replacepos[2]] = replace
                        toplockkeys.append([row, char, i])
                        toplockkeys.append([row, char, abs(i-1)])

    # Assign the keyboard a name based on its top-row characters and return it.
    keyb = {manager.gen_name(keyb): keyb}
    return keyb


def gen_rand():
    """
    Generates a completely random keyboard layout by shuffling all characters
    and assigning them to key positions.

    Returns the keyboard as an uncorrected [name, layout] list.
    Call correct() on the result before using it in the algorithm.
    """
    char_list = [
        "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
        "q", "Q", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y", "u", "U", "i", "I", "o", "O", "p", "P", "[", "{", "]", "}", "\\", "|",
        "a", "A", "s", "S", "d", "D", "f", "F", "g", "G", "h", "H", "j", "J", "k", "K", "l", "L", ";", ":", "'", "\"",
        "z", "Z", "x", "X", "c", "C", "v", "V", "b", "B", "n", "N", "m", "M", ",", "<", ".", ">", "/", "?"
        ]
    rand.shuffle(char_list)

    accent = char_list[0]
    tilde = char_list[1]
    exclamation = char_list[2]
    at = char_list[3]
    pound = char_list[4]
    dollar = char_list[5]
    percent = char_list[6]
    carat = char_list[7]
    ampersand = char_list[8]
    asterisk = char_list[9]
    lparanthesis = char_list[10]
    rparanthesis = char_list[11]
    minus = char_list[12]
    underscore = char_list[13]
    equal = char_list[14]
    plus = char_list[15]

    q_low = char_list[16]
    q_up = char_list[17]
    w_low = char_list[18]
    w_up = char_list[19]
    e_low = char_list[20]
    e_up = char_list[21]
    r_low = char_list[22]
    r_up = char_list[23]
    t_low = char_list[24]
    t_up = char_list[25]
    y_low = char_list[26]
    y_up = char_list[27]
    u_low = char_list[28]
    u_up = char_list[29]
    i_low = char_list[30]
    i_up = char_list[31]
    o_low = char_list[32]
    o_up = char_list[33]
    p_low = char_list[34]
    p_up = char_list[35]
    lsquare = char_list[36]
    lcurly = char_list[37]
    rsquare = char_list[38]
    rcurly = char_list[39]
    fslash = char_list[40]
    vline = char_list[41]

    a_low = char_list[42]
    a_up = char_list[43]
    s_low = char_list[44]
    s_up = char_list[45]
    d_low = char_list[46]
    d_up = char_list[47]
    f_low = char_list[48]
    f_up = char_list[49]
    g_low = char_list[50]
    g_up = char_list[51]
    h_low = char_list[52]
    h_up = char_list[53]
    j_low = char_list[54]
    j_up = char_list[55]
    k_low = char_list[56]
    k_up = char_list[57]
    l_low = char_list[58]
    l_up = char_list[59]
    semicolon = char_list[60]
    colon = char_list[61]
    apostrophe = char_list[62]
    quote = char_list[63]

    z_low = char_list[64]
    z_up = char_list[65]
    x_low = char_list[66]
    x_up = char_list[67]
    c_low = char_list[68]
    c_up = char_list[69]
    v_low = char_list[70]
    v_up = char_list[71]
    b_low = char_list[72]
    b_up = char_list[73]
    n_low = char_list[74]
    n_up = char_list[75]
    m_low = char_list[76]
    m_up = char_list[77]
    comma = char_list[78]
    less = char_list[79]
    period = char_list[80]
    greater = char_list[81]
    bslash = char_list[82]
    question = char_list[83]

    keyb = ["-", {
        "row_1":{"`":[accent,tilde],"1":["1",exclamation],"2":["2",at],"3":["3",pound],"4":["4",dollar],"5":["5",percent],"6":["6",carat],"7":["7",ampersand],"8":["8",asterisk],"9":["9",lparanthesis],"0":["0",rparanthesis],"-":[minus,underscore],"=":[equal,plus]},
        "row_2":{"q":[q_low,q_up],"w":[w_low,w_up],"e":[e_low,e_up],"r":[r_low,r_up],"t":[t_low,t_up],"y":[y_low,y_up],"u":[u_low,u_up],"i":[i_low,i_up],"o":[o_low,o_up],"p":[p_low,p_up],"[":[lsquare,lcurly],"]":[rsquare,rcurly],"\\":[fslash,vline]},
        "row_3":{"a":[a_low,a_up],"s":[s_low,s_up],"d":[d_low,d_up],"f":[f_low,f_up],"g":[g_low,g_up],"h":[h_low,h_up],"j":[j_low,j_up],"k":[k_low,k_up],"l":[l_low,l_up],";":[semicolon,colon],"'":[apostrophe,quote]},
        "row_4":{"z":[z_low,z_up],"x":[x_low,x_up],"c":[c_low,c_up],"v":[v_low,v_up],"b":[b_low,b_up],"n":[n_low,n_up],"m":[m_low,m_up],",":[comma,less],".":[period,greater],"/":[bslash,question]}
    }]

    return keyb


def mutation1(keyb1, keyb2):
    """
    Crossover mutation: replaces the left half of keyb1 with the left half of keyb2.

    This simulates biological crossover, where two parents produce an offspring
    that inherits traits from both. Any duplicate characters introduced by the
    crossover are resolved by substituting in the missing characters.
    """
    rows = ("row_1","row_2","row_3","row_4")
    lrow1 = ["`", "1", "2", "3", "4", "5"]
    lrow2 = ["q", "w", "e", "r", "t"]
    lrow3 = ["a", "s", "d", "f", "g"]
    lrow4 = ["z", "x", "c", "v", "b"]
    lrowkeys = (lrow1, lrow2, lrow3, lrow4)

    copykeys = [
        "`","~","1","!","2","@","3","#","4","$","5","%","6","^","7","&","8","*","9","(","0",")","-","_","=","+",
        "q","Q","w","W","e","E","r","R","t","T","y","Y","u","U","i","I","o","O","p","P","[","{","]","}","\\","|",
        "a","A","s","S","d","D","f","F","g","G","h","H","j","J","k","K","l","L",";",":","'","\"",
        "z","Z","x","X","c","C","v","V","b","B","n","N","m","M",",","<",".",">","/","?"
        ]

    # Copy the left-hand keys from keyb2 into keyb1.
    for i, row in enumerate(rows):
        for char in lrowkeys[i]:
            keyb1[1][row][char][0] = keyb2[1][row][char][0]
            keyb1[1][row][char][1] = keyb2[1][row][char][1]

    # Find any characters that now appear twice due to the crossover.
    keybkeys = []
    for row in keyb1[1]:
        for char in keyb1[1][row]:
            keybkeys.append(keyb1[1][row][char][0])
            keybkeys.append(keyb1[1][row][char][1])

    dupechars = []
    for char in keybkeys:
        if keybkeys.count(char) >= 2:
            if not char in dupechars:
                dupechars.append(char)

    # Find any characters that are now missing from the layout.
    missingkeys = []
    for key in copykeys:
        if not key in keybkeys:
            missingkeys.append(key)

    # Replace each duplicate on the right side with a missing character.
    rrow1 = ("6", "7", "8", "9", "0", "-", "=")
    rrow2 = ("y", "u", "i", "o", "p", "[", "]", "\\")
    rrow3 = ("h", "j", "k", "l", ";", "'")
    rrow4 = ("n", "m", ",", ".", "/")
    rrowkeys = [rrow1, rrow2, rrow3, rrow4]

    for i, row in enumerate(rows):
        for char in rrowkeys[i]:
            for i in range(2):
                if keyb1[1][row][char][i] in dupechars:
                    keyb1[1][row][char][i] = missingkeys[dupechars.index(keyb1[1][row][char][i])]

    keyb1[0] = "mutation1"

    return keyb1


def mutation2(keyb):
    """
    Swap mutation: randomly swaps two individual characters anywhere on the keyboard.

    This is the smallest possible change — a single character exchange.
    It allows the algorithm to make fine-grained adjustments to a layout.
    """
    rows = ["row_1", "row_2", "row_3", "row_4"]
    row1 = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="]
    row2 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"]
    row3 = ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"]
    row4 = ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
    rowkeys = [row1, row2, row3, row4]

    rowi1 = rand.randint(0,3)
    rowi2 = rand.randint(0,3)

    randrow1 = rows[rowi1]
    randrow2 = rows[rowi2]

    case1 = rand.randint(0,1)
    case2 = rand.randint(0,1)

    nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    randkey1 = rowkeys[rowi1][rand.randint(0, (len(rowkeys[rowi1])-1))]
    randkey2 = rowkeys[rowi2][rand.randint(0, (len(rowkeys[rowi2])-1))]

    # Avoid swapping number keys in the lowercase position.
    while randkey1 in nums and case1 == 0:
        randkey1 = rowkeys[rowi1][rand.randint(0, (len(rowkeys[rowi1])-1))]

    while randkey2 in nums and case2 == 0:
        randkey2 = rowkeys[rowi2][rand.randint(0, (len(rowkeys[rowi2])-1))]

    # Perform the swap.
    let1 = keyb[1][randrow2][randkey2][case2]
    let2 = keyb[1][randrow1][randkey1][case1]
    keyb[1][randrow1][randkey1][case1] = let1
    keyb[1][randrow2][randkey2][case2] = let2

    keyb[0] = "mutation2"

    return keyb


def mutation3(keyb):
    """
    Row swap mutation: swaps all the characters between two randomly chosen rows
    (rows 2, 3, and 4 only — the letter rows).

    This is a large-scale change that can radically reorganize a layout.
    """
    rows = ["row_2", "row_3", "row_4"]
    row2 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
    row3 = ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"]
    row4 = ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
    rowkeys = [row2, row3, row4]
    rand1 = rand.randint(0,2)
    rand2 = rand.randint(0,2)

    for i in range(10):
        let1_low = keyb[1][rows[rand2]][rowkeys[rand2][i]][0]
        let1_up = keyb[1][rows[rand2]][rowkeys[rand2][i]][1]

        let2_low = keyb[1][rows[rand1]][rowkeys[rand1][i]][0]
        let2_up = keyb[1][rows[rand1]][rowkeys[rand1][i]][1]

        keyb[1][rows[rand1]][rowkeys[rand1][i]][0] = let1_low
        keyb[1][rows[rand1]][rowkeys[rand1][i]][1] = let1_up
        keyb[1][rows[rand2]][rowkeys[rand2][i]][0] = let2_low
        keyb[1][rows[rand2]][rowkeys[rand2][i]][1] = let2_up

    keyb[0] = "mutation3"

    return keyb


def mutation4(keyb):
    """
    Column swap mutation: swaps all the characters between two randomly chosen
    vertical columns across rows 2, 3, and 4.

    Columns are the vertical groupings of keys (e.g. Q/A/Z, W/S/X, etc.).
    This keeps finger-column assignments intact while shuffling which column
    gets which set of characters.
    """
    rows = ["row_2", "row_3", "row_4"]
    c1 = {"row_2":"q", "row_3":"a", "row_4":"z"}
    c2 = {"row_2":"w", "row_3":"s", "row_4":"x"}
    c3 = {"row_2":"e", "row_3":"d", "row_4":"c"}
    c4 = {"row_2":"r", "row_3":"f", "row_4":"v"}
    c5 = {"row_2":"t", "row_3":"g", "row_4":"b"}
    c6 = {"row_2":"y", "row_3":"h", "row_4":"n"}
    c7 = {"row_2":"u", "row_3":"j", "row_4":"m"}
    c8 = {"row_2":"i", "row_3":"k", "row_4":","}
    c9 = {"row_2":"o", "row_3":"l", "row_4":"."}
    c10 = {"row_2":"p", "row_3":";", "row_4":"/"}
    columns = (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)
    rand1 = rand.randint(0,9)
    rand2 = rand.randint(0,9)

    for row in rows:
        let1_low = keyb[1][row][columns[rand2][row]][0]
        let1_up = keyb[1][row][columns[rand2][row]][1]

        let2_low = keyb[1][row][columns[rand1][row]][0]
        let2_up = keyb[1][row][columns[rand1][row]][1]

        keyb[1][row][columns[rand1][row]][0] = let1_low
        keyb[1][row][columns[rand1][row]][1] = let1_up
        keyb[1][row][columns[rand2][row]][0] = let2_low
        keyb[1][row][columns[rand2][row]][1] = let2_up

    keyb[0] = "mutation4"

    return keyb


def mutate(gen):
    """
    Produces the next generation of keyboards from the current one.

    Combines the top 5 keyboards from the current generation with the all-time
    top keyboards, then applies a random mutation to each. If the resulting pool
    has fewer than 25 keyboards, random layouts are added to fill it out.
    All keyboards are then run through correct() to ensure layout validity.
    """
    # Gather the best keyboards from the all-time records and the current generation.
    pop_top = pop.pop_top_kb()
    pop_current = top5(gen)
    pop_top.update(pop_current)
    keybs = pop_top

    new_gen = {}
    keyb_list = []
    for keyb in keybs:
        keyb_list.append(keyb)

    # Apply a random mutation to each keyboard, twice over, to fill the new generation.
    for i in range(2):
        for keyb in keybs:
            mut_num = rand.randint(1,4)
            if mut_num == 1:
                new_gen.update({len(new_gen):mutation1(keybs[keyb], keybs[keyb_list[rand.randint(0, len(keyb_list)-1)]])})
            elif mut_num == 2:
                new_gen.update({len(new_gen):mutation2(keybs[keyb])})
            elif mut_num == 3:
                new_gen.update({len(new_gen):mutation3(keybs[keyb])})
            elif mut_num == 4:
                new_gen.update({len(new_gen):mutation4(keybs[keyb])})

    # Pad with random layouts if we don't yet have 25 keyboards.
    while len(new_gen) < 25:
        new_gen.update({len(new_gen):gen_rand()})

    # Run every keyboard through correct() to enforce layout rules, then reset scores.
    final_gen = {}
    for keyb in new_gen:
        final_gen.update(correct(new_gen[keyb]))

    for keyb in final_gen:
        final_gen[keyb][0] = "-"

    return final_gen
