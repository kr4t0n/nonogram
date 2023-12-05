import numpy as np
import os.path as osp
import numpy.typing as npt

from typing import List
from copy import deepcopy
from itertools import combinations


class BreakException(Exception):
    pass


class Nonogram:
    n: int
    nonogram: npt.NDArray

    rows: List[List[int]]
    cols: List[List[int]]

    def __init__(self, n: int) -> None:
        self.n = n
        self.nonogram = np.empty((n, n), dtype=np.int_)

        self._empty()

    def _empty(self) -> None:
        self.nonogram[:] = -1

    def _input_rows(self, rows: List[List[int]]) -> None:
        self.rows = rows
        assert len(self.rows) == self.n

    def _input_cols(self, cols: List[List[int]]) -> None:
        self.cols = cols
        assert len(self.cols) == self.n

    def input(self, rows: List[List[int]], cols: List[List[int]]) -> None:
        self._input_rows(rows)
        self._input_cols(cols)

    def input_from_file(self, row_file: str, col_file: str) -> None:
        if not osp.exists(row_file):
            raise ValueError(
                f"Rows file {row_file} does not exist, please check!"
            )
        if not osp.exists(col_file):
            raise ValueError(
                f"Cols file {col_file} does not exist, please check!"
            )

        rows: List[List[int]] = []
        cols: List[List[int]] = []

        with open(row_file, "r", encoding="utf-8") as fr:
            for line in fr.readlines():
                rows.append(list(map(int, line.strip().split(" "))))

        with open(col_file, "r", encoding="utf-8") as fc:
            for line in fc.readlines():
                cols.append(list(map(int, line.strip().split(" "))))

        self._input_rows(rows)
        self._input_cols(cols)

    def _solver_helper(
        self,
        residue: int,
        fills: List[int],
        constraint: npt.NDArray,
        result: List[int],
        possibilities: List[List[int]],
    ) -> List[List[int]]:
        c_index = np.where(constraint != -1)[0]

        if residue == 0 and len(fills) == 0:
            possibilities.append(result)

        if residue > 0:
            tmp_result = np.array(result + [0])
            c_index_needed = c_index[np.where(c_index < len(tmp_result))[0]]

            if np.logical_and.reduce(
                tmp_result[c_index_needed] == constraint[c_index_needed]
            ):
                self._solver_helper(
                    residue - 1,
                    fills,
                    constraint,
                    result + [0],
                    possibilities,
                )

        if len(fills) > 0:
            tmp_result = np.array(result + [1] * fills[0] + [0])
            c_index_needed = c_index[np.where(c_index < len(tmp_result))[0]]

            if np.logical_and.reduce(
                tmp_result[c_index_needed] == constraint[c_index_needed]
            ):
                self._solver_helper(
                    residue,
                    fills[1:],
                    constraint,
                    result + [1] * fills[0] + [0],
                    possibilities,
                )

        return possibilities

    def _solver(
        self,
        fills: List[int],
        constraint: npt.NDArray,
    ) -> npt.NDArray:
        residue = self.n - (np.sum(fills) + len(fills) - 1)

        possibilities = []
        self._solver_helper(
            residue,
            fills,
            constraint,
            result=[],
            possibilities=possibilities,
        )
        possibilities = np.array(possibilities)[:, :-1].astype(bool)

        constraint[np.logical_and.reduce(possibilities)] = 1
        constraint[np.logical_and.reduce(~possibilities)] = 0

        return constraint

    def solve(self) -> int:
        self._empty()

        while -1 in self.nonogram.reshape(-1):
            changed = False
            previous_filled = np.sum(self.nonogram)

            for idx, row in enumerate(self.rows):
                self.nonogram[idx, :] = self._solver(
                    row,
                    self.nonogram[idx, :],
                )

            for idx, col in enumerate(self.cols):
                self.nonogram[:, idx] = self._solver(
                    col,
                    self.nonogram[:, idx],
                )

            current_filled = np.sum(self.nonogram)

            if current_filled > previous_filled:
                changed = True

            if not changed:
                print("Solve failed...")
                return -1

        return 0

    def _gen_row_col(self) -> None:
        rows: List[List[int]] = []
        cols: List[List[int]] = []

        for idx in range(self.n):
            row = self.nonogram[idx, :]
            col = self.nonogram[:, idx]

            row_indices = np.where(row == 1)[0]
            row_buckets = np.split(
                row_indices,
                np.where(np.diff(row_indices) != 1)[0] + 1,
            )

            col_indices = np.where(col == 1)[0]
            col_buckets = np.split(
                col_indices,
                np.where(np.diff(col_indices) != 1)[0] + 1,
            )

            rows.append(list(map(len, row_buckets)))
            cols.append(list(map(len, col_buckets)))

        self.rows = rows
        self.cols = cols

    def random(self) -> None:
        self._empty()

        for idx in range(self.n):
            while True:
                self.nonogram[idx] = np.random.randint(0, 2, self.n)

                if np.sum(self.nonogram[idx]) > self.n / 2:
                    break

        self._gen_row_col()

        # ensure playable
        old_nonogram = deepcopy(self.nonogram)

        if self.solve() == -1:
            p_flip = np.where(
                np.logical_and(
                    self.nonogram == -1,
                    old_nonogram != 1,
                )
            )
            n_p_flip = len(p_flip[0])

            try:
                for i in range(n_p_flip):
                    combs = combinations(range(n_p_flip), i)

                    for comb in combs:
                        print(comb)
                        self.nonogram = deepcopy(old_nonogram)
                        for comb_idx in comb:
                            self.nonogram[
                                p_flip[0][comb_idx],
                                p_flip[1][comb_idx],
                            ] = 1
                            self._gen_row_col()

                        if self.solve() != -1:
                            flipped = i
                            raise BreakException
            except BreakException:
                pass

            print(f"Flipped {flipped} and succeed!")

    def __repr__(self) -> str:
        return_str = " "
        return_str += "-" * (int(self.n / 5) * 10 - 1)
        return_str += "\n"

        for i in range(self.n):
            row = self.nonogram[i]

            return_str += "|"
            return_str += "|".join(
                list(
                    map(
                        lambda x: " ".join(map(str, x)),
                        row.reshape(-1, 5),
                    )
                )
            )
            return_str += "|"
            return_str += "\n"

            if (i + 1) % 5 == 0:
                return_str += " "
                return_str += "-" * (int(self.n / 5) * 10 - 1)
                return_str += "\n"

        return_str = return_str.replace("1", "■")
        return_str = return_str.replace("0", " ")

        return return_str


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
    print(nonogram)


if __name__ == "__main__":
    main()
