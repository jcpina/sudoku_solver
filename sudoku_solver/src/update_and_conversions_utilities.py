from classes import SudokuLine
from classes import SudokuColumn
from classes import SudokuSquare

from classes import SUDOKU_UNIT, NUM_LINE_COL_PER_SQ

def linepos2square_idx(line, line_pos):
    """ returns the square index (0..8) common with the given line position """
    line_idx = line.line_idx
    square_idx = int(line_idx/NUM_LINE_COL_PER_SQ)*NUM_LINE_COL_PER_SQ + int(line_pos/NUM_LINE_COL_PER_SQ)
    return square_idx

def linepos2square_pos(line, line_pos):
    """ Converts the column position to the line position """
    line_idx = line.line_idx
    x = int(line_pos % NUM_LINE_COL_PER_SQ)
    y = int(line_idx % NUM_LINE_COL_PER_SQ)
    square_pos = (NUM_LINE_COL_PER_SQ*y + x)
    return(square_pos)

def colpos2square_idx(col, col_pos):
    """ returns the square index (0..8) common with the given column position """
    col_idx = col.column_idx
    square_idx = int(col_pos/NUM_LINE_COL_PER_SQ)*NUM_LINE_COL_PER_SQ + int(col_idx/NUM_LINE_COL_PER_SQ)
    return square_idx

def colpos2square_pos(col, col_pos):
    """ Converts the column position to the square position """
    
    # Already have the math for lines ... hence convert position of interest
    # from column to line
    line_idx = col_pos
    line_pos = col.column_idx
    x = int(line_pos % NUM_LINE_COL_PER_SQ)
    y = int(line_idx % NUM_LINE_COL_PER_SQ)
    square_pos = (NUM_LINE_COL_PER_SQ*y + x)
    return(square_pos)


def line_column_update_pos(line, line_pos, cols, item):
    """ Updates the line position and the common colon position """
    line_idx = line.line_idx
    if(line.line[line_pos] == 0):
        line.line[line_pos] = item
        
        col_idx = line_pos
        col_pos = line_idx
        cols[col_idx].column[col_pos] = item
    else:
        print(">>> Error! >>>\n Trying to change value at line[",line_idx,"], pos[",line_pos,"]")
        game_error.inc()
    
def line_square_update_pos(line, line_pos, squares):
    """ Updates the line position and the common square position """
    line_idx = line.line_idx
    value = line.line[line_pos]
    square_idx = linepos2square_idx(line, line_pos)
    square_pos = linepos2square_pos(line, line_pos)
    if(squares[square_idx].square[square_pos] == 0):
        squares[square_idx].square[square_pos] = value
    else:
        print(">>> Error! >>>\n Trying to change value at square[",square_idx,"], pos[",square_pos,"]")
        game_error.inc()

 
def column_line_update_pos(col, col_pos, lines, item):
    """ Updates the column position and the common line position """
    col_idx = col.column_idx
    if col.column[col_pos] == 0:
        col.column[col_pos] = item
        
        line_idx = col_pos
        line_pos = col_idx
        lines[line_idx].line[line_pos] = item
    else:
        print(">>> Error! >>>\n Trying to change value at column[",col_idx,"], pos[",pos,"]")
        game_error.inc()

    
def column_square_update_pos(col, col_pos, lines, squares):
    """ Updates the column position and the common square position """
    value = col.column[col_pos]
    col_idx = col.column_idx
    
    line_pos = col.column_idx
    line_idx = col_pos
    line_square_update_pos(lines[line_idx], line_pos, squares)
    
def square_line_column_update_pos(square, lines, cols, square_pos, item):
    """ Updates the column and line position common to the given square position """
    line_org = square.square_idx[0]
    col_org = square.square_idx[1]
    
    # Update line item
    line_idx = int(square_pos / NUM_LINE_COL_PER_SQ) + line_org
    line_pos = (square_pos % NUM_LINE_COL_PER_SQ) + col_org
    if(lines[line_idx].line[line_pos]) == 0:
        lines[line_idx].line[line_pos] = item
        
        # Update column item
        col_pos = line_idx
        col_idx = line_pos
        if(cols[col_idx].column[col_pos] == 0):
            cols[col_idx].column[col_pos] = item
        else:
            print(">>> Error! >>>\n Trying to change value at column[",col_idx,"], pos[",col_pos,"] old_val:", lines[line_idx].line[line_pos], "new val:", item)
            game_error.inc()
            

    else:
        print(">>> Error! >>>\n Trying to change value at line[",line_idx,"], pos[",line_pos,"]")
        game_error.inc()

    
def line_update_all(line, line_pos, cols, squares, item):
    """ Updates the line, column and square positions knowing the line position and item to update"""
    line_column_update_pos(line, line_pos, cols, item)
    line_square_update_pos(line, line_pos, squares)

def column_update_all(col, col_pos, lines, squares, item):
    """ Updates the line, column and square positions knowing the column position and item to update"""
    column_line_update_pos(col, col_pos, lines, item)
    column_square_update_pos(col, col_pos, lines, squares)
    
def square_update_all(square, sq_pos, lines, cols, item):
    """ Updates the line, column and square positions knowing the square position and item to update"""
    if square.square[sq_pos] == 0: 
        square.square[sq_pos] = item
        square_line_column_update_pos(square, lines, cols, sq_pos, item)
    else:
        print(">>> Error! >>>\n Trying to change value at square[",square.square_idx,"], pos[",sq_pos,"]")
        game_error.inc()
