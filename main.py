from nonogram import Nonogram


def main():
    n = 10
    nonogram = Nonogram(n)

    rows = [
        [4],
        [1, 2],
        [1, 2, 2],
        [1, 3, 2],
        [8],
        [8],
        [8],
        [5, 3],
        [2, 4],
        [6],
    ]
    cols = [
        [1],
        [7],
        [1, 6],
        [1, 6, 1],
        [1, 6, 1],
        [1, 4, 2],
        [2, 3, 2],
        [9],
        [7],
        [1],
    ]

    nonogram.input(rows, cols)
    nonogram.solve()
    print(nonogram)

    nonogram.random()
    print(nonogram.rows)
    print(nonogram.cols)
    print(nonogram)


if __name__ == "__main__":
    main()
