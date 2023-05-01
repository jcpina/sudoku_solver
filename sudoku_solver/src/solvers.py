from classes import SudokuLine
from classes import SudokuColumn
from classes import SudokuSquare
from update_and_conversions_utilities import *

from classes import SUDOKU_UNIT, NUM_LINE_COL_PER_SQ

def solve_square(lines, columns, squares):
    hit = False
    for num in range(1,10):
        for i in squares:
            if not (i.has_item(num)) :
                # item is missing, let's see if we can find it ..
                sq_scratch = i.item_possible_locations(lines, columns, num)
                pos = i.item_unique_possibility(sq_scratch)
                if pos >= 0:
                    print(">>>>>>> Hit for square:", i.square_idx, " at pos: ", pos, " for item: ", num)
                    square_update_all(i, pos, lines, columns, num)
                    hit = True
    return(hit)

def solve_line(lines, columns, squares):
    hit = False
    for num in range(1,10):
        for i in lines:
            if not (i.has_item(num)) :
                line_scratch = i.item_possible_locations(squares, columns, num)
                line_pos = i.item_unique_possibility(line_scratch)
                if line_pos >= 0:
                    print(">>>>>>> Hit line[", i.line_idx, "]:", i.line, " at pos: ", line_pos, " for item: ", num)
                    line_update_all(i, line_pos, columns, squares, num)
                    hit = True
    return(hit)

def solve_column(lines, columns, squares):
    hit = False
    for num in range(1,10):
        for i in columns:
            if not (i.has_item(num)) :
                line_scratch = i.item_possible_locations(squares, lines, num)
                col_pos = i.item_unique_possibility(line_scratch)
                if col_pos >= 0:
                    print(">>>>>>> Hit column[", i.column_idx, "]:", i.column, " at pos: ", col_pos, " for item: ", num)
                    column_update_all(i, col_pos, lines, squares, num)
                    hit = True
    return(hit)

def solve_square_lev_2(lines, columns, squares):
    hit = False
    for sq_idx in range(0,9):
        hit_count_per_position = [0,0,0,0,0,0,0,0,0]
        '''
        If there is only 1 hit in the position counter, then this
        array will have the value that is correct at this position
        '''
        hit_last_per_position =  [0,0,0,0,0,0,0,0,0]

        for item in range(1,10):
            '''
            The scratch buffer is a list of (square_position, candidate_value)
            for all positions in a given given square
            '''
            scratch = squares[sq_idx].build_all_items(lines, columns, item, sq_idx)
            for l in scratch:
                hit_count_per_position[l[0]] +=1
                hit_last_per_position[l[0]] = l[1]

        for pos in range(0,9):
            if hit_count_per_position[pos] == 1:
                print(">>>>>>> Hit square[", sq_idx, "] at pos: ", pos, " for item: ", hit_last_per_position[pos])
                square_update_all(squares[sq_idx], pos, lines, columns, hit_last_per_position[pos])
                hit = True
    return(hit)

def solve_line_lev_2(lines, columns, squares):
    hit = False
    for line_idx in range(0,9):
        hit_count_per_position = [0,0,0,0,0,0,0,0,0]
        '''
        If there is only 1 hit in the position counter, then this
        array will have the value that is correct at this position
        '''
        hit_last_per_position =  [0,0,0,0,0,0,0,0,0]

        for item in range(1,10):
            '''
            The scratch buffer is a list of (line_position, candidate_value)
            for all positions in a given given line
            '''
            scratch = lines[line_idx].build_all_items(squares, columns, item)
            for l in scratch:
                hit_count_per_position[l[0]] +=1
                hit_last_per_position[l[0]] = l[1]

        for pos in range(0,9):
            if hit_count_per_position[pos] == 1:
                print(">>>>>>> Hit line[", line_idx, "] at pos: ", pos, " for item: ", hit_last_per_position[pos])
                line_update_all(lines[line_idx], pos, columns, squares, hit_last_per_position[pos])
                hit = True
    return(hit)

def solve_column_lev_2(lines, columns, squares):
    hit = False
    for col_idx in range(0,9):
        hit_count_per_position = [0,0,0,0,0,0,0,0,0]
        '''
        If there is only 1 hit in the position counter, then this
        array will have the value that is correct at this position
        '''
        hit_last_per_position =  [0,0,0,0,0,0,0,0,0]

        for item in range(1,10):
            '''
            The scratch buffer is a list of (line_position, candidate_value)
            for all positions in a given given line
            '''
            scratch = columns[col_idx].build_all_items(squares, lines, item)
            for l in scratch:
                hit_count_per_position[l[0]] +=1
                hit_last_per_position[l[0]] = l[1]

        for pos in range(0,9):
            if hit_count_per_position[pos] == 1:
                print(">>>>>>> Hit column[", col_idx, "] at pos: ", pos, " for item: ", hit_last_per_position[pos])
                column_update_all(columns[col_idx], pos, lines, squares, hit_last_per_position[pos])
                hit = True
    return(hit)
