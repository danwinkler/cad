boards = [10 * 12] * 3


def generate_needed_boards(n_vert, n_hori_long, n_hori_short):
    return (
        [n_vert] * 4
        + [n_hori_long] * 2
        + [n_hori_short] * 2
        + [n_hori_short] * 2  # For the cross supports
    )


needed_boards = generate_needed_boards(24, 8 * 12, 18)


def find_packing(boards, needed_boards):
    """
    Find the best packing of needed_boards into boards.
    Return a list of list of the packed boards, where the outer list index refers to the board index
    """

    # Sort the needed_boards in descending order to optimize packing
    needed_boards.sort(reverse=True)

    # Prepare the list of boards with their remaining lengths
    remaining_lengths = boards[:]

    # List of list to store how the boards are packed
    packed_boards = [[] for _ in boards]

    # Try to fit each needed board into one of the available boards
    for board_length in needed_boards:
        for i, available_length in enumerate(remaining_lengths):
            if board_length <= available_length:
                # If it fits, place the board in the current board
                packed_boards[i].append(board_length)
                remaining_lengths[i] -= board_length
                break
    return packed_boards


packed_boards = find_packing(boards, needed_boards)
print(packed_boards)
