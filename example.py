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

    c = cube.Cube(base_str)
    c.sequence(" ".join(solver.moves))
    print(c)
    c.inverse_sequence(" ".join(solver_t.moves))

    print("Solved:")
    print(c, end="\n\n")


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


if __name__ == "__main__":
    solve_for_target()
