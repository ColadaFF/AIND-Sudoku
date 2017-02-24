assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [c[1] + str(c[0]) for c in list(enumerate(rows, start=1))]
diagonal_inv_units = [c[1] + str(c[0]) for c in list(enumerate(rows[::-1], start=1))]
unitlist_diag = row_units + column_units + square_units + [diagonal_units, diagonal_inv_units]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
units_diag = dict((s, [u for u in unitlist_diag if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)
peers_diag = dict((s, set(sum(units_diag[s], [])) - {s}) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    values_to_compare = [(key, value) for key, value in values.items() if len(value) == 2]
    for tuple in values_to_compare:
        square = tuple[0]
        value = tuple[1]
        for unit in units[square]:
            for peer in set(unit).intersection(set(peers[square])):
                if not set(values[peer]).difference(set(values[square])):
                    digit1 = value[0]
                    digit2 = value[1]
                    for item in set(unit).difference({square, peer}):
                        # If the item is not in the naked twins pair, remove the naked twins' values
                        # Eliminate the naked twins as possibilities for their peers
                        if digit1 in values[item]:
                            assign_value(values, item, values[item].replace(digit1, ""))
                        if digit2 in values[item]:
                            assign_value(values, item, values[item].replace(digit2, ""))
    return values


# concatenate every char in a with every chat in b
def cross(a, b):
    return [s + t for s in a for t in b]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()


def eliminate(values):
    """
       Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
       Input: A sudoku in dictionary form.
       Output: The resulting sudoku in dictionary form.
       """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers_diag[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
       Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
       Input: A sudoku in dictionary form.
       Output: The resulting sudoku in dictionary form.
       """
    for unit in unitlist_diag:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
       Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
       If the sudoku is solved, return the sudoku.
       If after an iteration of both functions, the sudoku remains the same, return the sudoku.
       Input: A sudoku in dictionary form.
       Output: The resulting sudoku in dictionary form.
       """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def fewest_val(values):
    solved_values = [[key, value] for key, value in values.items() if len(value) != 1]
    solved_values.sort(key=lambda tup: len(tup[1]))
    return solved_values[0]


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if (values is False):
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    fewest_values = fewest_val(values)
    for c in fewest_values[1]:
        new_sudoku = values.copy()
        new_sudoku[fewest_values[0]] = c
        result = search(new_sudoku)
        if (result):
            return result
            # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!


def solve(grid):
    values = grid_values(grid)
    return eliminate(search(values))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
