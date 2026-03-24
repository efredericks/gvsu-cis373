import time
import random

NUM_ROWS = 30
NUM_COLS = 80

grid = [ [' '] * NUM_COLS for _ in range(NUM_ROWS)]

player = {'r': 3, 'c': 3, 'vc': 1, 'vr': 0}

for r in range(NUM_ROWS):
    for c in range(NUM_COLS):
        if r == 0 or c == 0 or r == NUM_ROWS-1 or c == NUM_COLS-1:
            grid[r][c] = '#'
        else:
            if random.random() > 0.9:
                grid[r][c] = '#'

# ensure player's position is open
grid[player['r']][player['c']] = ' '

x = 20
while True:
    for r in range(NUM_ROWS):
        op_str = ""
        for c in range(NUM_COLS):
            if player['r'] == r and player['c'] == c:
                op_str += '\033[31;1;4m@\033[0m'#@'
            else:
                op_str += grid[r][c]

        print(f'\33[K{op_str}')
    time.sleep(0.5)
    print(f'\33[{NUM_ROWS}A', end='')

    # next position
    next_pos = {'r': player['r'] + player['vr'], 'c': player['c'] + player['vc']}
    if next_pos['r'] >= 0 and next_pos['r'] < NUM_ROWS and next_pos['c'] >= 0 and next_pos['c'] < NUM_COLS:
        if grid[next_pos['r']][next_pos['c']] != '#':
            player['r'] = next_pos['r']
            player['c'] = next_pos['c']
        else:
            if random.random() > 0.5:
                player['vc'] = random.choice([-1, 0, 1])
                player['vr'] = random.choice([-1,0,1])


#    print(f'\33[K{x}')
#
#    x -= 1
#    print(f'\33[K{x}')
#    x -= 1
#    time.sleep(0.5)

#    print('\33[2A', end='')
