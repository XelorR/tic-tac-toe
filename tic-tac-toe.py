#!/usr/bin/env python3

"""Tic-Tac-Toe game."""

import re
import random


def init_game():
    """Take user input do define game parameters before start."""
    ai = (
        False
        if input(
            "Do You want to play with AI(a) or Human?(h). Default --- Human."
            + "\nYour choice: "
        ).upper()
        in ["H", ""]
        else True
    )
    player_one_plays_crosses = (
        (
            True
            if input("Please select X or O. Default --- X" + "\nYour choise: ").upper()
            in ["X", ""]
            else False
        )
        if ai
        else True
    )
    return ai, player_one_plays_crosses


board = [["." for _ in range(3)] for _ in range(3)]


def print_board():
    """Print current board state."""
    print("| \\ | 0 | 1 | 2 |")
    print("|---+---+---+---|")
    for i, row in enumerate(board):
        print(f"| {i} |", end="")
        for col in row:
            print(f" {col} |", end="")
        print()
        print("|---+---+---+---|")


def get_user_input(crosses):
    """Get coordinates from keyboard."""
    x_or_o = "X" if crosses else "O"
    return list(
        map(
            int,
            list(
                re.sub(
                    "[^0-9]",
                    "",
                    input(
                        f"\n{x_or_o} turn.\n"
                        + "Provide row and column coords "
                        + "(two numbers like '2 1' or '21', other symbols ignored)"
                        + "\nYour choice: "
                    ),
                )
            ),
        )
    )


def get_ai_input(crosses):
    """Get coordinates from algorithm."""
    x_or_o = "X" if crosses else "O"
    opponent = "O" if crosses else "X"
    print(f"\n{x_or_o} turn (AI).")

    # Check for winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] == ".":
                board[i][j] = x_or_o
                if check_winning_combination(crosses):
                    board[i][j] = "."
                    return [i, j]
                board[i][j] = "."

    # Check for blocking move
    for i in range(3):
        for j in range(3):
            if board[i][j] == ".":
                board[i][j] = opponent
                if check_winning_combination(not crosses):
                    board[i][j] = "."
                    return [i, j]
                board[i][j] = "."

    # Make a random move
    while True:
        x, y = random.randint(0, 2), random.randint(0, 2)
        if board[x][y] == ".":
            return [x, y]


def check_winning_combination(crosses, verbose=False):
    """Check winning combination."""
    x_or_o = "X" if crosses else "O"
    # check rows
    for row in board:
        if row.count(x_or_o) == 3:
            if verbose:
                print(f"{x_or_o} wins!")
            return True
    # check columns
    for col in range(3):
        if [row[col] for row in board].count(x_or_o) == 3:
            if verbose:
                print(f"{x_or_o} wins!")
            return True
    # check diagonals
    if [board[i][i] for i in range(3)].count(x_or_o) == 3:
        if verbose:
            print(f"{x_or_o} wins!")
        return True
    if [board[i][2 - i] for i in range(3)].count(x_or_o) == 3:
        if verbose:
            print(f"{x_or_o} wins!")
        return True
    # check if whole board occupied
    if sum(["." not in row for row in board]) == 3:
        if verbose:
            print("Draw!")
        return True
    return False


def reinput(func):
    """Decorate to add wrong input notification."""

    def wrapper(*args, **kwargs):
        print("\n!!! Wrong input, try again !!!")
        result = func(*args, **kwargs)
        return result

    return wrapper


def play(ai, crosses):
    """Play loop."""
    print("\nBlank field:")
    print_board()
    while True:
        x_or_o = "X" if crosses else "O"

        if crosses or not ai:
            input_func = get_user_input
        else:
            input_func = get_ai_input
        get_again = reinput(input_func)

        xy = input_func(crosses)
        if board[xy[0]][xy[1]] != ".":
            xy = get_again(crosses)
        board[xy[0]][xy[1]] = x_or_o

        print_board()
        if check_winning_combination(crosses, verbose=True):
            exit()
        crosses = not crosses


if __name__ == "__main__":
    ai, player_one_plays_crosses = init_game()
    play(ai, player_one_plays_crosses)
