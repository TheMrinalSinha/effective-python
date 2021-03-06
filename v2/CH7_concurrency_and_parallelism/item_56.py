"""
Item 56: Know how to recognize when concurrency is necessary

Inevitably, as the scope of program grows, it also becomes more complicated.
Dealing with expanding requirements in a way that maintains clarity, testability,
& efficiency is one of the most difficult parts of programming. Perhaps the hardest
type of change to handle is moving from a single-threaded program to one that needs
multiple concurrent lines of execution.
"""

# Say that I want to implement conway's game of life, a class illustration of finite
# state automata. The rules of the game are simple: You have a two-dimensional grid
# of an attribute size. Each cell in the grid can either be alive or empty:

ALIVE = '*'
EMPTY = '-'

# I can represent the state of each cell with a simple container class. The class
# must have methods that allow me to get and set the value of any coordinate.
# Coordinates that are out of bounds should wraps around, making the grid act like
# an infinite looping space:

class Grid:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width  = width
        self.rows   = []

        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self) -> str:
        result = ""
        for row in self.rows:
            result += ''.join(row) + '\n'
        return result

# To see this class in action, I can create a Grid instance and set its initial state
# to a classic shape called a glider:

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)
print(grid)

# Now, I need a way to retrieve the status of neighboring cells. I can do this with a
# helper function that queries the grid and return the count of living neighbors. I use
# a simple function for the get parameter instead of passing in a whole Grid instance
# in order to reduce coupling

def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0) # North
    ne = get(y - 1, x + 1) # Northeast
    e_ = get(y + 0, x + 1) # East
    se = get(y + 1, x + 1) # Southeast
    s_ = get(y + 1, x + 0) # South
    sw = get(y + 1, x - 1) # Southwest
    w_ = get(y + 0, x - 1) # West
    nw = get(y - 1, x - 1) # Northwest

    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0

    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

# Now, i define the sample logic for conway's game of life, based on the game's three
# rules: die if a cell has fewer than two neighbors, die if a cell has more than three
# neighbors, or become alive if any empty cell has exactly three neighbors:

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY # Die: Too few
        elif neighbors > 3:
            return EMPTY # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE # Regenerate
    return state

# I can connect count_neighbors and game_logic together in another function that transitions
# the state of a cell. This function will be called each generation to figure out a cell's
# current state, inspect the neighboring cells around it, determine what its next state should
# be, and update the resulting grid accordingly. Again, I use a function interface for set
# instead of passing in the Grid instance to make this code more decoupled:

def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)

# finally, i can define a function that progresses the whole grid of cells forward by a
# single step and then returns a new grid containing the state fo the next generation.

def simulate(grid):
    next_grid = Grid(grid.height, grid.width)

    for y in range(grid.height):
        for x in range(grid.width):
            step_cell(y, x, grid.get, next_grid.set)
    return next_grid

# Now, I can progress the grid forward one generation at a time. You can see how the grid
# moves down and to the right on the grid based on the rules fromthe game_logic func
class ColumnPrinter:
    pass

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate(grid)

print(columns)


"""
Things to Remember

✦ A program often grows to require multiple concurrent lines of exe-
  cution as its scope and complexity increases.

✦ The most common types of concurrency coordination are fan-out
  (generating new units of concurrency) and fan-in (waiting for exist-
  ing units of concurrency to complete).

✦ Python has many different ways of achieving fan-out and fan-in.
"""
