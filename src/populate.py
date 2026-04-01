# populate.py
# Responsible for loading keyboard layouts from disk and translating them into
# the dictionary format used by the rest of the algorithm.
#
# Keyboards are stored on disk as .klc files (Windows keyboard layout files).
# This module reads those files and converts them into a usable Python structure.

import file_manager as file

# Maps Unicode character names (as they appear in .klc files) to their actual characters.
# Used when parsing .klc files to reconstruct keyboard layouts.
keyname_key = {
    "GRAVEACCENT" :"`", "TILDE" :"~", "DIGITONE" :"1", "EXCLAMATIONMARK" :"!", "DIGITTWO" :"2", "COMMERCIALAT" :"@", "DIGITTHREE" :"3", "NUMBERSIGN" :"#", "DIGITFOUR" :"4", "DOLLARSIGN" :"$", "DIGITFIVE" :"5", "PERCENTSIGN" :"%", "DIGITSIX" :"6", "CIRCUMFLEXACCENT" :"^", "DIGITSEVEN" :"7", "AMPERSAND" :"&", "DIGITEIGHT" :"8", "ASTERISK" :"*", "DIGITNINE" :"9", "LEFTPARENTHESIS" :"(", "DIGITZERO" :"0", "RIGHTPARENTHESIS" :")", "HYPHEN-MINUS" :"-", "LOWLINE" :"_", "EQUALSSIGN" :"=", "PLUSSIGN" :"+",
    "LATINSMALLLETTERQ" :"q", "LATINCAPITALLETTERQ" :"Q", "LATINSMALLLETTERW" :"w", "LATINCAPITALLETTERW" :"W", "LATINSMALLLETTERE" :"e", "LATINCAPITALLETTERE" :"E", "LATINSMALLLETTERR" :"r", "LATINCAPITALLETTERR" :"R", "LATINSMALLLETTERT" :"t", "LATINCAPITALLETTERT" :"T", "LATINSMALLLETTERY" :"y", "LATINCAPITALLETTERY" :"Y", "LATINSMALLLETTERU" :"u", "LATINCAPITALLETTERU" :"U", "LATINSMALLLETTERI" :"i", "LATINCAPITALLETTERI" :"I", "LATINSMALLLETTERO" :"o", "LATINCAPITALLETTERO" :"O", "LATINSMALLLETTERP" :"p", "LATINCAPITALLETTERP" :"P", "LEFTSQUAREBRACKET" :"[", "LEFTCURLYBRACKET" :"{", "RIGHTSQUAREBRACKET" :"]", "RIGHTCURLYBRACKET" :"}", "REVERSESOLIDUS" :"\\", "VERTICALLINE" :"|",
    "LATINSMALLLETTERA" :"a", "LATINCAPITALLETTERA" :"A", "LATINSMALLLETTERS" :"s", "LATINCAPITALLETTERS" :"S", "LATINSMALLLETTERD" :"d", "LATINCAPITALLETTERD" :"D", "LATINSMALLLETTERF" :"f", "LATINCAPITALLETTERF" :"F", "LATINSMALLLETTERG" :"g", "LATINCAPITALLETTERG" :"G", "LATINSMALLLETTERH" :"h", "LATINCAPITALLETTERH" :"H", "LATINSMALLLETTERJ" :"j", "LATINCAPITALLETTERJ" :"J", "LATINSMALLLETTERK" :"k", "LATINCAPITALLETTERK" :"K", "LATINSMALLLETTERL" :"l", "LATINCAPITALLETTERL" :"L", "SEMICOLON" :";", "COLON" :":", "APOSTROPHE" :"'", "QUOTATIONMARK" :"\"",
    "LATINSMALLLETTERZ" :"z", "LATINCAPITALLETTERZ" :"Z", "LATINSMALLLETTERX" :"x", "LATINCAPITALLETTERX" :"X", "LATINSMALLLETTERC" :"c", "LATINCAPITALLETTERC" :"C", "LATINSMALLLETTERV" :"v", "LATINCAPITALLETTERV" :"V", "LATINSMALLLETTERB" :"b", "LATINCAPITALLETTERB" :"B", "LATINSMALLLETTERN" :"n", "LATINCAPITALLETTERN" :"N", "LATINSMALLLETTERM" :"m", "LATINCAPITALLETTERM" :"M", "COMMA" :",", "LESS-THANSIGN" :"<", "FULLSTOP" :".", "GREATER-THANSIGN" :">", "SOLIDUS" :"/", "QUESTIONMARK" :"?",
    }


def keyname(line):
    """
    Parses a single line from a .klc file and extracts the lowercase and uppercase
    character assigned to that key.

    Returns a tuple: (lowercase_char, uppercase_char)
    """
    a = ""
    b = ""
    cond = 0
    for char in line:
        if cond == 2 and char != " " and char != ",":
            a += char
        elif cond == 3 and char != " " and char != ",":
            b += char
        elif char == "/" or char == ",":
            cond += 1
    return (a, b)


def translate(gen):
    """
    Converts a list of raw .klc file lines into the keyboard dictionary format
    used throughout the algorithm.

    Each keyboard in 'gen' is a list of lines from its .klc file. This function
    reads the relevant lines, maps the Unicode key names to actual characters,
    and assembles the standard { row: { position: [low, up] } } structure.

    Returns a dictionary of { keyboard_name: [score, layout] }.
    """
    kbs = {}
    for index, keyb in enumerate(gen):
        # Extract the keyboard's name from its .klc header.
        name = ""
        cond = False
        for char in gen[index][0]:
            if cond and char != "\"":
                name += char
            elif char == "\"":
                cond = not cond

        # Extract the keyboard's fitness score stored in the .klc file.
        score = ""
        cond = False
        for char in gen[index][2]:
            if cond and char != "\"":
                score += char
            elif char == "\"":
                cond = not cond

        # Read each key definition line and map it to the corresponding character.
        for index, line in enumerate(gen[index][21:68]):
            index += 21

            if index == 21:
                one= keyname_key[keyname(line)[0]]
                exclamation= keyname_key[keyname(line)[1]]
            elif index == 22:
                two= keyname_key[keyname(line)[0]]
                at= keyname_key[keyname(line)[1]]
            elif index == 23:
                three= keyname_key[keyname(line)[0]]
                pound= keyname_key[keyname(line)[1]]
            elif index == 24:
                four= keyname_key[keyname(line)[0]]
                dollar= keyname_key[keyname(line)[1]]
            elif index == 25:
                five= keyname_key[keyname(line)[0]]
                percent= keyname_key[keyname(line)[1]]
            elif index == 26:
                six= keyname_key[keyname(line)[0]]
                carat= keyname_key[keyname(line)[1]]
            elif index == 27:
                seven= keyname_key[keyname(line)[0]]
                ampersand= keyname_key[keyname(line)[1]]
            elif index == 28:
                eight= keyname_key[keyname(line)[0]]
                asterisk= keyname_key[keyname(line)[1]]
            elif index == 29:
                nine= keyname_key[keyname(line)[0]]
                lparanthesis= keyname_key[keyname(line)[1]]
            elif index == 30:
                zero= keyname_key[keyname(line)[0]]
                rparanthesis= keyname_key[keyname(line)[1]]
            elif index == 31:
                minus= keyname_key[keyname(line)[0]]
                underscore= keyname_key[keyname(line)[1]]
            elif index == 32:
                equal= keyname_key[keyname(line)[0]]
                plus= keyname_key[keyname(line)[1]]
            elif index == 33:
                q_low= keyname_key[keyname(line)[0]]
                q_up= keyname_key[keyname(line)[1]]
            elif index == 34:
                w_low= keyname_key[keyname(line)[0]]
                w_up= keyname_key[keyname(line)[1]]
            elif index == 35:
                e_low= keyname_key[keyname(line)[0]]
                e_up= keyname_key[keyname(line)[1]]
            elif index == 36:
                r_low= keyname_key[keyname(line)[0]]
                r_up= keyname_key[keyname(line)[1]]
            elif index == 37:
                t_low= keyname_key[keyname(line)[0]]
                t_up= keyname_key[keyname(line)[1]]
            elif index == 38:
                y_low= keyname_key[keyname(line)[0]]
                y_up= keyname_key[keyname(line)[1]]
            elif index == 39:
                u_low= keyname_key[keyname(line)[0]]
                u_up= keyname_key[keyname(line)[1]]
            elif index == 40:
                i_low= keyname_key[keyname(line)[0]]
                i_up= keyname_key[keyname(line)[1]]
            elif index == 41:
                o_low= keyname_key[keyname(line)[0]]
                o_up= keyname_key[keyname(line)[1]]
            elif index == 42:
                p_low= keyname_key[keyname(line)[0]]
                p_up= keyname_key[keyname(line)[1]]
            elif index == 43:
                lsquare= keyname_key[keyname(line)[0]]
                lcurly= keyname_key[keyname(line)[1]]
            elif index == 44:
                rsquare= keyname_key[keyname(line)[0]]
                rcurly= keyname_key[keyname(line)[1]]
            elif index == 45:
                a_low= keyname_key[keyname(line)[0]]
                a_up= keyname_key[keyname(line)[1]]
            elif index == 46:
                s_low= keyname_key[keyname(line)[0]]
                s_up= keyname_key[keyname(line)[1]]
            elif index == 47:
                d_low= keyname_key[keyname(line)[0]]
                d_up= keyname_key[keyname(line)[1]]
            elif index == 48:
                f_low= keyname_key[keyname(line)[0]]
                f_up= keyname_key[keyname(line)[1]]
            elif index == 49:
                g_low= keyname_key[keyname(line)[0]]
                g_up= keyname_key[keyname(line)[1]]
            elif index == 50:
                h_low= keyname_key[keyname(line)[0]]
                h_up= keyname_key[keyname(line)[1]]
            elif index == 51:
                j_low= keyname_key[keyname(line)[0]]
                j_up= keyname_key[keyname(line)[1]]
            elif index == 52:
                k_low= keyname_key[keyname(line)[0]]
                k_up= keyname_key[keyname(line)[1]]
            elif index == 53:
                l_low= keyname_key[keyname(line)[0]]
                l_up= keyname_key[keyname(line)[1]]
            elif index == 54:
                semicolon= keyname_key[keyname(line)[0]]
                colon= keyname_key[keyname(line)[1]]
            elif index == 55:
                apostrophe= keyname_key[keyname(line)[0]]
                quote= keyname_key[keyname(line)[1]]
            elif index == 56:
                accent= keyname_key[keyname(line)[0]]
                tilde= keyname_key[keyname(line)[1]]
            elif index == 57:
                fslash= keyname_key[keyname(line)[0]]
                vline= keyname_key[keyname(line)[1]]
            elif index == 58:
                z_low= keyname_key[keyname(line)[0]]
                z_up= keyname_key[keyname(line)[1]]
            elif index == 59:
                x_low= keyname_key[keyname(line)[0]]
                x_up= keyname_key[keyname(line)[1]]
            elif index == 60:
                c_low= keyname_key[keyname(line)[0]]
                c_up= keyname_key[keyname(line)[1]]
            elif index == 61:
                v_low= keyname_key[keyname(line)[0]]
                v_up= keyname_key[keyname(line)[1]]
            elif index == 62:
                b_low= keyname_key[keyname(line)[0]]
                b_up= keyname_key[keyname(line)[1]]
            elif index == 63:
                n_low= keyname_key[keyname(line)[0]]
                n_up= keyname_key[keyname(line)[1]]
            elif index == 64:
                m_low= keyname_key[keyname(line)[0]]
                m_up= keyname_key[keyname(line)[1]]
            elif index == 65:
                comma= keyname_key[keyname(line)[0]]
                less= keyname_key[keyname(line)[1]]
            elif index == 66:
                period= keyname_key[keyname(line)[0]]
                greater= keyname_key[keyname(line)[1]]
            elif index == 67:
                bslash= keyname_key[keyname(line)[0]]
                question= keyname_key[keyname(line)[1]]

        # Assemble the final keyboard dictionary and add it to the results.
        kbs.update({name:[score, {
            "row_1":{"`":[accent,tilde],"1":[one,exclamation],"2":[two,at],"3":[three,pound],"4":[four,dollar],"5":[five,percent],"6":[six,carat],"7":[seven,ampersand],"8":[eight,asterisk],"9":[nine,lparanthesis],"0":[zero,rparanthesis],"-":[minus,underscore],"=":[equal,plus]},
            "row_2":{"q":[q_low,q_up],"w":[w_low,w_up],"e":[e_low,e_up],"r":[r_low,r_up],"t":[t_low,t_up],"y":[y_low,y_up],"u":[u_low,u_up],"i":[i_low,i_up],"o":[o_low,o_up],"p":[p_low,p_up],"[":[lsquare,lcurly],"]":[rsquare,rcurly],"\\":[fslash,vline]},
            "row_3":{"a":[a_low,a_up],"s":[s_low,s_up],"d":[d_low,d_up],"f":[f_low,f_up],"g":[g_low,g_up],"h":[h_low,h_up],"j":[j_low,j_up],"k":[k_low,k_up],"l":[l_low,l_up],";":[semicolon,colon],"'":[apostrophe,quote]},
            "row_4":{"z":[z_low,z_up],"x":[x_low,x_up],"c":[c_low,c_up],"v":[v_low,v_up],"b":[b_low,b_up],"n":[n_low,n_up],"m":[m_low,m_up],",":[comma,less],".":[period,greater],"/":[bslash,question]}
            }]})

    return kbs


def populate():
    """
    Loads the current generation of keyboards from disk and returns them
    as a translated dictionary ready for scoring.
    """
    gen = file.get_gen()
    return translate(gen)


def pop_top_kb():
    """
    Loads the all-time top-performing keyboards from disk and returns them
    as a translated dictionary.
    """
    gen = file.get_top_keybs()
    return translate(gen)
