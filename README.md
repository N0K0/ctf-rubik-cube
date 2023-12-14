![PyPI](https://img.shields.io/pypi/v/ctf-rubik-cube)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ctf-rubik-cube)

**Forked from https://github.com/pglass/cube, this would not be possible without his work. <3**

# Overview

This is a Python 3 implementation of a (3x3) Rubik's Cube solver.

It contains:

- A simple implementation of the cube
- A solver that follows a fixed algorithm
- An unintelligent solution sequence optimizer
- A decent set of test cases

On top of that, this CTF fork contains:
- An extension of the cube that allows each piece to contain a piece of data (like a character)
- No new tests!
- A move inverter, to move us into an arbitrary state

## Installation

The package is hosted on PyPI.
```
pip install ctf-rubik-cube
```


# Example Usage

```python
from rubik.cube import Cube
c = Cube("OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR")
print(c)
```

```
    OOO
    OOO
    OOO
YYY WWW GGG BBB
YYY WWW GGG BBB
YYY WWW GGG BBB
    RRR
    RRR
    RRR
```

```python

from rubik import cube
from rubik.solve import Solver


def solve_with_data():

    """
    cube_str looks like:
        UUU                       0  1  2
        UUU                       3  4  5
        UUU                       6  7  8
    LLL FFF RRR BBB      9 10 11 12 13 14 15 16 17 18 19 20
    LLL FFF RRR BBB     21 22 23 24 25 26 27 28 29 30 31 32
    LLL FFF RRR BBB     33 34 35 36 37 38 39 40 41 42 43 44
        DDD                      45 46 47
        DDD                      48 49 50
        DDD                      51 52 53
    """

    # Note that the middle piece can be arbitrary, not locked to ULFRBD
    # Using colors here for readability, but you can use any string
    start_str = "BBWOGYWGRYGGRYGYROGWRGRRWWOYORBYRBOYOWRWGOBBYGOBBBWOYW"
    data_str = "{LOLS_SLWCS_A?REBLE}RAOPGNKKØGFEP__URSAAUIUO_PLLDOEXB_"

    c_root = cube.Cube(start_str, data_str)
    print("Initial colors:")
    print(c_root, end="\n\n")
    print("Initial data:")
    print(c_root.str_data(), end="\n\n")

    solver = Solver(c_root)
    solver.solve()

    print("Solved colors:")
    print(c_root, end="\n\n")

    print("Solved data:")
    print(c_root.str_data(), end="\n\n")

    print("As you can try to read out: 'PAPA{FLAGS_ARE_FUN}'")


if __name__ == '__main__':
    solve_with_data()
```

```
Initial colors:
    BBW
    OGY
    WGR
YGG RYG YRO GWR
GRR WWO YOR BYR
BOY OWR WGO BBY
    GOB
    BBW
    OYW

Initial data:
    {LO
    LS_
    SLW
CS_ A?R EBL E}R
AOP GNK KØG FEP
__U RSA AUI UO_
    PLL
    DOE
    XB_

Solved colors:
    RRR
    RRR
    RRR
BBB WWW GGG YYY
BBB WWW GGG YYY
BBB WWW GGG YYY
    OOO
    OOO
    OOO

Solved data:
    RBW
    GOP
    APA
{FL AGS _AR E_C
OOL }NE USL ?EB
_DU _SO ESP UK_
    ILL
    _ØL
    XKR

As you can try to read out: 'PAPA{FLAGS_ARE_FUN}'
```

# Solve for target pattern:

```python
from rubik import cube
from rubik.solve import Solver
from solve_random_cubes import random_cube

def solve_for_target():
    base_str = random_cube().flat_str()
    target_str = random_cube().flat_str()

    print(f"Base: {base_str}")
    print(f"Target: {target_str}")

    c_root = cube.Cube(base_str)
    c_target = cube.Cube(target_str)

    print("Initial:")
    print(c_root, end="\n\n")

    solver = Solver(c_root)
    solver.solve()

    solver_t = Solver(c_target)
    solver_t.solve()

    # Generate new cube
    c = cube.Cube(base_str)
    # Solve to base state
    c.sequence(" ".join(solver.moves))
    print(c)
    
    # Solve to target state, but inversing a solve to base state from the target
    c.inverse_sequence(" ".join(solver_t.moves))

    print("Solved:")
    print(c, end="\n\n")

if __name__ == '__main__':
    solve_for_target()

```


## Implementation

### Piece

The cornerstone of this implementation is the Piece class. A Piece stores three
pieces of information:

1. An integer `position` vector `(x, y, z)` where each component is in {-1, 0,
1}:
    - `(0, 0, 0)` is the center of the cube
    - the positive x-axis points to the right face
    - the positive y-axis points to the up face
    - the positive z-axis points to the front face

2. A `colors` vector `(cx, cy, cz)`, giving the color of the sticker along each
axis. Null values are place whenever that Piece has less than three sides. For
example, a Piece with `colors=('Orange', None, 'Red')` is an edge piece with an
`'Orange'` sticker facing the x-direction and a `'Red'` sticker facing the
z-direction. The Piece doesn't know or care which direction along the x-axis
the `'Orange'` sticker is facing, just that it is facing in the x-direction and
not the y- or z- directions.

3. A `data` vector `(dx, dy, dz)`, giving the data of the sticker along each axis

Using the combination of `position` and `color` vectors makes it easy to
identify any Piece by its absolute position or by its unique combination of
colors.

A Piece provides a method `Piece.rotate(matrix)`, which accepts a (90 degree)
rotation matrix. A matrix-vector multiplication is done to update the Piece's
`position` vector. Then we update the `colors` vector, by swapping exactly two
entries in the `colors` vector:

- For example, a corner Piece has three stickers of different colors. After a
  90 degree rotation of the Piece, one sticker remains facing down the same
  axis, while the other two stickers swap axes. This corresponds to swapping the
  positions of two entries in the Piece’s `colors` vector.
- For an edge or face piece, the argument is the same as above, although we may
  swap around one or more null entries.

### Cube

The Cube class is built on top of the Piece class. The Cube stores a list of
Pieces and provides nice methods for flipping slices of the cube, as well as
methods for querying the current state. (I followed standard [Rubik's Cube
notation](http://ruwix.com/the-rubiks-cube/notation/))

Because the Piece class encapsulates all of the rotation logic, implementing
rotations in the Cube class is dead simple - just apply the appropriate
rotation matrix to all Pieces involved in the rotation. An example: To
implement `Cube.L()` - a clockwise rotation of the left face - do the
following:

1. Construct the appropriate [rotation matrix](
http://en.wikipedia.org/wiki/Rotation_matrix) for a 90 degree rotation in the
`x = -1` plane.
2. Select all Pieces satisfying `position.x == -1`.
3. Apply the rotation matrix to each of these Pieces.

To implement `Cube.X()` - a clockwise rotation of the entire cube around the
positive x-axis - just apply a rotation matrix to all Pieces stored in the
Cube.

### Solver

The solver implements the algorithm described
[here](http://www.chessandpoker.com/rubiks-cube-solution.html). It is a
layer-by-layer solution. First the front-face (the `z = 1` plane) is solved,
then the middle layer (`z = 0`), and finally the back layer (`z = -1`). When
the solver is done, `Solver.moves` is a list representing the solution
sequence.

My first correct-looking implementation of the solver average 252.5 moves per
solution sequence on 135000 randomly-generated cubes (with no failures).
Implementing a dumb optimizer reduced the average number of moves to 192.7 on
67000 randomly-generated cubes. The optimizer does the following:

1. Eliminate full-cube rotations by "unrotating" the moves (Z U L D Zi becomes
L D R)
2. Eliminate moves followed by their inverse (R R Ri Ri is gone)
3. Replace moves repeated three times with a single turn in the opposite
direction (R R R becomes Ri)

The solver is not particularly fast. On my machine (a 4.0 Ghz i7), it takes
about 0.06 seconds per solve on CPython, which is roughly 16.7 solves/second.
On PyPy, this is reduced to about 0.013 seconds per solve, or about 76
solves/second.
