import math
from pathlib import Path
import file_manager as manager

# LIBRARY_PATH points to library.txt in the same folder as this script.
LIBRARY_PATH = Path(__file__).parent / "library.txt"

with open(LIBRARY_PATH, 'r') as file:
    data = file.read()
text = data.strip()


lp_pos = [0, 0]
lr_pos = [0, 0]
lm_pos = [0, 0]
li_pos = [0, 0]
ri_pos = [0, 0]
rm_pos = [0, 0]
rr_pos = [0, 0]
rp_pos = [0, 0]

fitness = 0

out_factor = 1.1
hand = ""
alternate_factor = 1

def adjust(x, pos):
    if x >= math.sqrt(pos[0]**2 + pos[1]**2):
        pos = [0, 0]
    else:
        pos[0] = math.copysign((abs(pos[0]) - x * math.cos(math.atan(pos[1] / pos[0]))), pos[0])
        pos[1] = math.copysign((abs(pos[1]) - x * math.sin(math.atan(pos[1] / pos[0]))), pos[1])

    return pos

def lshift():
    global fitness, lp_pos
    dx = math.sqrt((-1 - lp_pos[0])**2 + (-1 - lp_pos[1])**2)
    lp_pos = [-0.5, -1]
    fitness += dx*out_factor

def rshift():
    global fitness, rp_pos
    dx = math.sqrt((3 - rp_pos[0])**2 + (-1 - rp_pos[1])**2)
    rp_pos = [1.5, -1]
    fitness += dx*out_factor

def alternate(x):
    global hand, fitness
    if x == hand:
        fitness += alternate_factor
    elif x != hand:
        hand = x

def lp_hit(x, y):
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - lp_pos[0])**2 + (y - lp_pos[1])**2)
    lp_pos = [x, y]
    fitness += dx*out_factor

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)

def lr_hit(x, y):
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - lr_pos[0])**2 + (y - lr_pos[1])**2)
    lr_pos = [x, y]
    fitness += dx*out_factor

    lp_pos = adjust(dx, lp_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    rp_pos = adjust(dx, rp_pos)

def lm_hit(x, y):
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - lm_pos[0])**2 + (y - lm_pos[1])**2)
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
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - li_pos[0])**2 + (y - li_pos[1])**2)
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
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - ri_pos[0])**2 + (y - ri_pos[1])**2)
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
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - rm_pos[0])**2 + (y - rm_pos[1])**2)
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
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - rr_pos[0])**2 + (y - rr_pos[1])**2)
    rr_pos = [x, y]
    fitness += dx*out_factor

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    lp_pos = adjust(dx, lp_pos)
    rp_pos = adjust(dx, rp_pos)

def rp_hit(x, y):
    global fitness, lp_pos, lr_pos, lm_pos, li_pos, ri_pos, rm_pos, rr_pos, rp_pos
    dx = math.sqrt((x - lp_pos[0])**2 + (y - rp_pos[1])**2)
    rp_pos = [x, y]
    fitness += dx*out_factor

    lr_pos = adjust(dx, lr_pos)
    lm_pos = adjust(dx, lm_pos)
    li_pos = adjust(dx, li_pos)
    ri_pos = adjust(dx, ri_pos)
    rm_pos = adjust(dx, rm_pos)
    rr_pos = adjust(dx, rr_pos)
    lp_pos = adjust(dx, lp_pos)


def generate_fitness(keybs):
    global fitness, text
    keyboards = {}
    for keyb in keybs:
        board = keybs[keyb]
        fitness = 0
        lp1 = [board[1]["row_1"]["`"][0], board[1]["row_1"]["`"][1]]
        lp2 = [board[1]["row_1"]["1"][0], board[1]["row_1"]["1"][1]]
        lp3 = [board[1]["row_2"]["q"][0], board[1]["row_2"]["q"][1]]
        lp4 = [board[1]["row_3"]["a"][0], board[1]["row_3"]["a"][1]]
        lp5 = [board[1]["row_4"]["z"][0], board[1]["row_4"]["z"][1]]

        lr1 = [board[1]["row_1"]["2"][0], board[1]["row_1"]["2"][1]]
        lr2 = [board[1]["row_2"]["w"][0], board[1]["row_2"]["w"][1]]
        lr3 = [board[1]["row_3"]["s"][0], board[1]["row_3"]["s"][1]]
        lr4 = [board[1]["row_4"]["x"][0], board[1]["row_4"]["x"][1]]

        lm1 = [board[1]["row_1"]["3"][0], board[1]["row_1"]["3"][1]]
        lm2 = [board[1]["row_2"]["e"][0], board[1]["row_2"]["e"][1]]
        lm3 = [board[1]["row_3"]["d"][0], board[1]["row_3"]["d"][1]]
        lm4 = [board[1]["row_4"]["c"][0], board[1]["row_4"]["c"][1]]

        li1 = [board[1]["row_1"]["4"][0], board[1]["row_1"]["4"][1]]
        li2 = [board[1]["row_2"]["r"][0], board[1]["row_2"]["r"][1]]
        li3 = [board[1]["row_3"]["f"][0], board[1]["row_3"]["f"][1]]
        li4 = [board[1]["row_4"]["v"][0], board[1]["row_4"]["v"][1]]
        li5 = [board[1]["row_1"]["5"][0], board[1]["row_1"]["5"][1]]
        li6 = [board[1]["row_2"]["t"][0], board[1]["row_2"]["t"][1]]
        li7 = [board[1]["row_3"]["g"][0], board[1]["row_3"]["g"][1]]
        li8 = [board[1]["row_4"]["b"][0], board[1]["row_4"]["b"][1]]

        ri1 = [board[1]["row_1"]["6"][0], board[1]["row_1"]["6"][1]]
        ri2 = [board[1]["row_2"]["y"][0], board[1]["row_2"]["y"][1]]
        ri3 = [board[1]["row_3"]["h"][0], board[1]["row_3"]["h"][1]]
        ri4 = [board[1]["row_4"]["n"][0], board[1]["row_4"]["n"][1]]
        ri5 = [board[1]["row_1"]["7"][0], board[1]["row_1"]["7"][1]]
        ri6 = [board[1]["row_2"]["u"][0], board[1]["row_2"]["u"][1]]
        ri7 = [board[1]["row_3"]["j"][0], board[1]["row_3"]["j"][1]]
        ri8 = [board[1]["row_4"]["m"][0], board[1]["row_4"]["m"][1]]

        rm1 = [board[1]["row_1"]["8"][0], board[1]["row_1"]["8"][1]]
        rm2 = [board[1]["row_2"]["i"][0], board[1]["row_2"]["i"][1]]
        rm3 = [board[1]["row_3"]["k"][0], board[1]["row_3"]["k"][1]]
        rm4 = [board[1]["row_4"][","][0], board[1]["row_4"][","][1]]

        rr1 = [board[1]["row_1"]["9"][0], board[1]["row_1"]["9"][1]]
        rr2 = [board[1]["row_2"]["o"][0], board[1]["row_2"]["o"][1]]
        rr3 = [board[1]["row_3"]["l"][0], board[1]["row_3"]["l"][1]]
        rr4 = [board[1]["row_4"]["."][0], board[1]["row_4"]["."][1]]

        rp1 = [board[1]["row_1"]["0"][0], board[1]["row_1"]["0"][1]]
        rp2 = [board[1]["row_2"]["p"][0], board[1]["row_2"]["p"][1]]
        rp3 = [board[1]["row_3"][";"][0], board[1]["row_3"][";"][1]]
        rp4 = [board[1]["row_4"]["/"][0], board[1]["row_4"]["/"][1]]
        rp5 = [board[1]["row_1"]["-"][0], board[1]["row_1"]["-"][1]]
        rp6 = [board[1]["row_2"]["["][0], board[1]["row_2"]["["][1]]
        rp7 = [board[1]["row_3"]["'"][0], board[1]["row_3"]["'"][1]]
        rp8 = [board[1]["row_1"]["="][0], board[1]["row_1"]["="][1]]
        rp9 = [board[1]["row_2"]["]"][0], board[1]["row_2"]["]"][1]]
        rp10 = [board[1]["row_2"]["\\"][0], board[1]["row_2"]["\\"][1]]

        for char in text:
            if char == lp1[0]:
                alternate("l")
                lp_hit(-1.75, 2)
            elif char == lp1[1]:
                alternate("l")
                lp_hit(-1.75, 2)
                rshift()
            elif char == lp2[0]:
                alternate("l")
                lp_hit(-0.75, 2)
            elif char == lp2[1]:
                alternate("l")
                lp_hit(-0.75, 2)
                rshift()
            elif char == lp3[0]:
                alternate("l")
                lp_hit(-0.25, 1)
            elif char == lp3[1]:
                alternate("l")
                lp_hit(-0.25, 1)
                rshift()
            elif char == lp4[0]:
                alternate("l")
                lp_hit(0, 0)
            elif char == lp4[1]:
                alternate("l")
                lp_hit(0, 0)
                rshift()
            elif char == lp5[0]:
                alternate("l")
                lp_hit(0.5, -1)
            elif char == lp5[1]:
                alternate("l")
                lp_hit(0.5, -1)
                rshift()

            elif char == lr1[0]:
                alternate("l")
                lr_hit(-0.75, 2)
            elif char == lr1[1]:
                alternate("l")
                lr_hit(-0.75, 2)
                rshift()
            elif char == lr2[0]:
                alternate("l")
                lr_hit(-0.25, 1)
            elif char == lr2[1]:
                alternate("l")
                lr_hit(-0.25, 1)
                rshift()
            elif char == lr3[0]:
                alternate("l")
                lr_hit(0, 0)
            elif char == lr3[1]:
                alternate("l")
                lr_hit(0, 0)
                rshift()
            elif char == lr4[0]:
                alternate("l")
                lr_hit(0.5, -1)
            elif char == lr4[1]:
                alternate("l")
                lr_hit(0.5, -1)
                rshift()

            elif char == lm1[0]:
                alternate("l")
                lm_hit(-0.75, 2)
            elif char == lm1[1]:
                alternate("l")
                lm_hit(-0.75, 2)
                rshift()
            elif char == lm2[0]:
                alternate("l")
                lm_hit(-0.25, 1)
            elif char == lm2[1]:
                alternate("l")
                lm_hit(-0.25, 1)
                rshift()
            elif char == lm3[0]:
                alternate("l")
                lm_hit(0, 0)
            elif char == lm3[1]:
                alternate("l")
                lm_hit(0, 0)
                rshift()
            elif char == lm4[0]:
                alternate("l")
                lm_hit(0.5, -1)
            elif char == lm4[1]:
                alternate("l")
                lm_hit(0.5, -1)
                rshift()

            elif char == li1[0]:
                alternate("l")
                li_hit(-0.75, 2)
            elif char == li1[1]:
                alternate("l")
                li_hit(-0.75, 2)
                rshift()
            elif char == li2[0]:
                alternate("l")
                li_hit(-0.25, 1)
            elif char == li2[1]:
                alternate("l")
                li_hit(-0.25, 1)
                rshift()
            elif char == li3[0]:
                alternate("l")
                li_hit(0, 0)
            elif char == li3[1]:
                alternate("l")
                li_hit(0, 0)
                rshift()
            elif char == li4[0]:
                alternate("l")
                li_hit(0.5, -1)
            elif char == li4[1]:
                alternate("l")
                li_hit(0.5, -1)
                rshift()
            elif char == li5[0]:
                alternate("l")
                li_hit(0.25, 2)
            elif char == li5[1]:
                alternate("l")
                li_hit(0.25, 2)
                rshift()
            elif char == li6[0]:
                alternate("l")
                li_hit(0.75, 1)
            elif char == li6[1]:
                alternate("l")
                li_hit(0.75, 1)
                rshift()
            elif char == li7[0]:
                alternate("l")
                li_hit(1, 0)
            elif char == li7[1]:
                alternate("l")
                li_hit(1, 0)
                rshift()
            elif char == li8[0]:
                alternate("l")
                li_hit(1.5, -1)
            elif char == li8[1]:
                alternate("l")
                li_hit(1.5, -1)
                rshift()

            elif char == ri1[0]:
                alternate("r")
                ri_hit(-1.75, 2)
            elif char == ri1[1]:
                alternate("r")
                ri_hit(-1.75, 2)
                lshift()
            elif char == ri2[0]:
                alternate("r")
                ri_hit(-1.25, 1)
            elif char == ri2[1]:
                alternate("r")
                ri_hit(-1.25, 1)
                lshift()
            elif char == ri3[0]:
                alternate("r")
                ri_hit(-1, 0)
            elif char == ri3[1]:
                alternate("r")
                ri_hit(-1, 0)
                lshift()
            elif char == ri4[0]:
                alternate("r")
                ri_hit(-0.5, -1)
            elif char == ri4[1]:
                alternate("r")
                ri_hit(-0.5, -1)
                lshift()
            elif char == ri5[0]:
                alternate("r")
                ri_hit(-0.75, 2)
            elif char == ri5[1]:
                alternate("r")
                ri_hit(-0.75, 2)
                lshift()
            elif char == ri6[0]:
                alternate("r")
                ri_hit(-0.25, 1)
            elif char == ri6[1]:
                alternate("r")
                ri_hit(-0.25, 1)
                lshift()
            elif char == ri7[0]:
                alternate("r")
                ri_hit(0, 0)
            elif char == ri7[1]:
                alternate("r")
                ri_hit(0, 0)
                lshift()
            elif char == ri8[0]:
                alternate("r")
                ri_hit(0.5, -1)
            elif char == ri8[1]:
                alternate("r")
                ri_hit(0.5, -1)
                lshift()

            elif char == rm1[0]:
                alternate("r")
                rm_hit(-0.75, 2)
            elif char == rm1[1]:
                alternate("r")
                rm_hit(-0.75, 2)
                lshift()
            elif char == rm2[0]:
                alternate("r")
                rm_hit(-0.25, 1)
            elif char == rm2[1]:
                alternate("r")
                rm_hit(-0.25, 1)
                lshift()
            elif char == rm3[0]:
                alternate("r")
                rm_hit(0, 0)
            elif char == rm3[1]:
                alternate("r")
                rm_hit(0, 0)
                lshift()
            elif char == rm4[0]:
                alternate("r")
                rm_hit(0.5, -1)
            elif char == rm4[1]:
                alternate("r")
                rm_hit(0.5, -1)
                lshift()

            elif char == rr1[0]:
                alternate("r")
                rr_hit(-0.75, 2)
            elif char == rr1[1]:
                alternate("r")
                rr_hit(-0.75, 2)
                lshift()
            elif char == rr2[0]:
                alternate("r")
                rr_hit(-0.25, 1)
            elif char == rr2[1]:
                alternate("r")
                rr_hit(-0.25, 1)
                lshift()
            elif char == rr3[0]:
                alternate("r")
                rr_hit(0, 0)
            elif char == rr3[1]:
                alternate("r")
                rr_hit(0, 0)
                lshift()
            elif char == rr4[0]:
                alternate("r")
                rr_hit(0.5, -1)
            elif char == rr4[1]:
                alternate("r")
                rr_hit(0.5, -1)
                lshift()

            elif char == rp1[0]:
                alternate("r")
                rp_hit(-0.75, 2)
            elif char == rp1[1]:
                alternate("r")
                rp_hit(-0.75, 2)
                lshift()
            elif char == rp2[0]:
                alternate("r")
                rp_hit(-0.25, 1)
            elif char == rp2[1]:
                alternate("r")
                rp_hit(-0.25, 1)
                lshift()
            elif char == rp3[0]:
                alternate("r")
                rp_hit(0, 0)
            elif char == rp3[1]:
                alternate("r")
                rp_hit(0, 0)
                lshift()
            elif char == rp4[0]:
                alternate("r")
                rp_hit(0.5, -1)
            elif char == rp4[1]:
                alternate("r")
                rp_hit(0.5, -1)
                lshift()
            elif char == rp5[0]:
                alternate("r")
                rp_hit(0.25, 2)
            elif char == rp5[1]:
                alternate("r")
                rp_hit(0.25, 2)
                lshift()
            elif char == rp6[0]:
                alternate("r")
                rp_hit(0.75, 1)
            elif char == rp6[1]:
                alternate("r")
                rp_hit(0.75, 1)
                lshift()
            elif char == rp7[0]:
                alternate("r")
                rp_hit(1, 0)
            elif char == rp7[1]:
                alternate("r")
                rp_hit(1, 0)
                lshift()
            elif char == rp8[0]:
                alternate("r")
                rp_hit(1.25, 2)
            elif char == rp8[1]:
                alternate("r")
                rp_hit(1.25, 2)
                lshift()
            elif char == rp9[0]:
                alternate("r")
                rp_hit(1.75, 1)
            elif char == rp9[1]:
                alternate("r")
                rp_hit(1.75, 1)
                lshift()
            elif char == rp10[0]:
                alternate("r")
                rp_hit(2.75, 1)
            elif char == rp10[1]:
                alternate("r")
                rp_hit(2.75, 1)
                lshift()
        
        fitness = round(fitness)
        board[0] = fitness
        print(fitness)
        keyboards.update({keyb:board})
        manager.appendscores(keyb, fitness)

    return keyboards

def get_max(gen):
    list = []
    for keyb in gen:
        list.append(gen[keyb][0])
    list.sort()
    manager.appendmax(list[0])
    manager.update_high(gen, list[0])
    manager.update_top_keybs(gen, list)
    return list[0]
    

def get_average(gen):
    total = 0
    for keyb in gen:
        total += gen[keyb][0]
    
    average = round(total / 25)
    manager.appendaverage(average)
    return average