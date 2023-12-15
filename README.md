# Nonogram

## Introduction

Nonograms are logic puzzles that involve filling in grids based on the numbers given at the side of the grid. The numbers indicate how many unbroken lines of filled-in squares there are in any given row or column. For example, a clue of "4 8 3" would mean there are sets of four, eight, and three filled squares, in that order, with at least one blank square between successive groups.

The objective is to fill the grid to reveal a hidden picture. Solving nonograms requires logical thinking and sometimes a bit of trial and error. These puzzles come in various sizes and complexities, from simple 5x5 grids to much larger and more challenging ones.

## Solve Nonogram

Support you have a 10x10 nonogram puzzle, with rows and columns conditions as,

```text
rows: [[4], [1, 2], [1, 2, 2], [1, 3, 2], [8], [8], [8], [5, 3], [2, 4], [6]]
cols: [[1], [7], [1, 6], [1, 6, 1], [1, 6, 1], [1, 4, 2], [2, 3, 2], [9], [7], [1]]
```

You can solve this puzzle with,

```python
from nonogram import Nonogram

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
```

You will have the output as,

```text
 -------------------
|      ■ ■|■ ■      |
|    ■    |  ■ ■    |
|  ■   ■ ■|    ■ ■  |
|  ■   ■ ■|■   ■ ■  |
|  ■ ■ ■ ■|■ ■ ■ ■  |
 -------------------
|  ■ ■ ■ ■|■ ■ ■ ■  |
|  ■ ■ ■ ■|■ ■ ■ ■  |
|■ ■ ■ ■ ■|    ■ ■ ■|
|  ■ ■    |■ ■ ■ ■  |
|    ■ ■ ■|■ ■ ■    |
 -------------------
```

## Play Nonogram

You can also randomly generate a nonogram to play, just simply use,

```python
nonogram.random()
print(nonogram.rows)
print(nonogram.cols)
```

You will have the rows and cows and columns conditions as,

```text
rows: [[1, 5], [2, 5], [4, 4], [1, 2, 3], [3, 1, 2, 1], [3, 4], [6, 1], [4, 3], [2, 2, 3], [3, 2, 1, 1]]
cols: [[2, 1, 1, 1], [9], [1, 6], [2, 3], [3, 4], [2, 1, 2], [6], [6, 3], [4, 4], [3, 2, 3]]
```

You can also have a peek of the output image using,

```python
print(nonogram)
```

```text
 -------------------
|■        |■ ■ ■ ■ ■|
|■ ■      |■ ■ ■ ■ ■|
|  ■ ■ ■ ■|  ■ ■ ■ ■|
|  ■   ■ ■|  ■ ■ ■  |
|■ ■ ■   ■|  ■ ■   ■|
 -------------------
|  ■ ■ ■  |  ■ ■ ■ ■|
|■ ■ ■ ■ ■|■     ■  |
|  ■ ■ ■ ■|    ■ ■ ■|
|  ■ ■   ■|■   ■ ■ ■|
|■ ■ ■   ■|■   ■   ■|
 -------------------
```