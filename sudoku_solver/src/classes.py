LINE_SQUARE_INDEXES = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
COLUMN_SQUARE_INDEXES = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]

SQUARE_LINES_INDEX_POS = ((0, 1, 2), (0, 1, 2), (0, 1, 2),
                          (3, 4, 5), (3, 4, 5), (3, 4, 5),
                          (6, 7, 8), (6, 7, 8), (6, 7, 8)
                          )
                          
SQUARE_COLUMNS_INDEX_POS = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 1, 2), (3, 4, 5), (6, 7, 8)
                          )
                        
SUDOKU_UNIT = 9             # Basic unit of sudoku 9 lines, 9 columns, 9 squares, 9 positions per ...
NUM_LINE_COL_PER_SQ = 3     # Number lines and/or columns that are common with any given square


class SudokuLine:
    """ 1 Line Sudoku """
    
    def __init__(self, line, idx):
        self.num_elmnt_per_line = SUDOKU_UNIT
        self.line = line
        self.line_idx = idx
        self.line_scratch = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.scratch = []
  
        #self.line = [0,0,0,0,0,0,0,0,0]
        # for i in range (0, self.num_elmnt_per_line):
        #     while True:
        #         print("Enter line value index ", i, ":\t")
        #         n = input()
        #         try:
        #             n = int(n)
        #         except ValueError:
        #             print("Sorry,", n, 'is not a number')
        #         else:
        #             if (n >= 0) and (n <= 9) and (self.is_duplicated(n) == False) :
        #                 self.line[i] = n
        #                 break;
        #             else:
        #                 print("Value entered not in range or duplicated")

    def is_duplicated(self, n):
        iter = 0
        if n == 0:
            return False
        else:
            for i in range (0, SUDOKU_UNIT):
                if (self.line[i] == n) :
                    iter += 1;
                    if (iter > 1):
                        return True
    
            return False
        
    def has_item(self, item):
        '''
        Returns True if the line contains already the item
        '''
        
        for i in range(0, self.num_elmnt_per_line):
            if (self.line[i] == item) :
                return True
        return False
    
    def item_possible_locations(self, squares, columns, item):
        '''
        For a given line returns all positions which can accept a given number
        by looking at each common square and column
        '''
        # print("Line index: ", self.line_idx, "Intercepts Squares: ", LINE_SQUARE_INDEXES[int(self.line_idx/3)])
        
        for i in range (0, self.num_elmnt_per_line):
            if (self.line[i] == 0):
                self.line_scratch[i] = ' '
            else:
                self.line_scratch[i] = 'x'
            
        for i in LINE_SQUARE_INDEXES[int(self.line_idx/NUM_LINE_COL_PER_SQ)]:
            if(squares[i].has_item(item)):
                pos = i%NUM_LINE_COL_PER_SQ
                self.line_scratch[(pos*NUM_LINE_COL_PER_SQ) + 0] = 'x'
                self.line_scratch[(pos*NUM_LINE_COL_PER_SQ) + 1] = 'x'
                self.line_scratch[(pos*NUM_LINE_COL_PER_SQ) + 2] = 'x'
        
        i = 0
        for column in columns:
            if(column.has_item(item)):
                self.line_scratch[i] = 'x'
            i += 1
                
        return(self.line_scratch)
    
    def item_unique_possibility(self, scratch):
        '''
        Returns the position if its unique
        '''
        
        hits = 0;
        for i in range(0, self.num_elmnt_per_line):
            if (scratch[i] == ' ') :
                hits+=1
                pos = i
        if hits == 1:
            return pos
        else:
            return -1
        
    def build_all_items(self, squares, columns, item):
        self.scratch.clear()
        
        #Check if the line has already the item
        if self.has_item(item):
            return(self.scratch)
        
        for line_pos in range(0,9):
            # Check If position in line has is empty
            if self.line[line_pos] == 0:
                #Check if square where line position is located has already the item
                sq_idx = (int(self.line_idx / 3) * 3) + (int(line_pos/3))
                if not (squares[sq_idx].has_item(item)):
                    col_idx = line_pos
                    # Check if column intercepting the line position has already the item
                    if not (columns[col_idx].has_item(item)):
                        self.scratch.append((line_pos, item))
                
        return(self.scratch)
    
    def show_elements(self):
        print('[',self.line_idx,']',self.line)
            
        
class SudokuColumn:
    def __init__(self, lines, index):
        self.num_elmnt_per_column = SUDOKU_UNIT
        self.column_idx = index
        self.column = []
        self.column_scratch = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.scratch = []


        for i in range (0, self.num_elmnt_per_column):
            self.column.append(lines[i].line[index])

    def is_duplicated(self, n):
        iter = 0
        if n == 0:
            return False
        else:
            for i in range (0, SUDOKU_UNIT):
                if (self.column[i] == n) :
                    iter += 1;
                    if (iter > 1):
                        return True
    
            return False

    def has_item(self, item):
        for i in range(0, self.num_elmnt_per_column):
            if (self.column[i] == item) :
                return True
        return False

    def item_possible_locations(self, squares, columns, item):
        # print("Column index: ", self.column_idx, "Intercepts Squares: ", COLUMN_SQUARE_INDEXES[int(self.column_idx/NUM_LINE_COL_PER_SQ)])
        
        for i in range (0, self.num_elmnt_per_column):
            if (self.column[i] == 0):
                self.column_scratch[i] = ' '
            else:
                self.column_scratch[i] = 'x'
            
        for i in COLUMN_SQUARE_INDEXES[int(self.column_idx/NUM_LINE_COL_PER_SQ)]:
            if(squares[i].has_item(item)):
                pos = int(i/NUM_LINE_COL_PER_SQ)
                self.column_scratch[(pos*NUM_LINE_COL_PER_SQ) + 0] = 'x'
                self.column_scratch[(pos*NUM_LINE_COL_PER_SQ) + 1] = 'x'
                self.column_scratch[(pos*NUM_LINE_COL_PER_SQ) + 2] = 'x'
        
        i = 0
        for column in columns:
            if(column.has_item(item)):
                self.column_scratch[i] = 'x'
            i += 1
                
        return(self.column_scratch)

    def item_unique_possibility(self, scratch):
        hits = 0;
        for i in range(0, self.num_elmnt_per_column):
            if (scratch[i] == ' ') :
                hits+=1
                pos = i
        if hits == 1:
            return pos
        else:
            return -1
        
    def build_all_items(self, squares, lines, item):
        self.scratch.clear()
        
        #Check if the column has already the item
        if self.has_item(item):
            return(self.scratch)
        
        for col_pos in range(0,9):
            # Check If position in column is empty
            if self.column[col_pos] == 0:
                #Check if square where line position is located has already the item
                sq_idx = (int(col_pos / 3) * 3) + (int(self.column_idx/3))
                if not (squares[sq_idx].has_item(item)):
                    line_idx = col_pos
                    # Check if line intercepting the column position has already the item
                    if not (lines[line_idx].has_item(item)):
                        self.scratch.append((col_pos, item))
                
        return(self.scratch)

    def show_elements(self):
        print(self.column)
            

class SudokuSquare:
    def __init__(self, lines, idx):
        self.num_elmnt_per_square = SUDOKU_UNIT
        self.square = []
        self.square_idx = idx
        self.square_scratch = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.scratch = []
        # self.test = ((0, 1, 2), (0, 1, 2), (0, 1, 2),
        #           (3, 4, 5), (3, 4, 5), (3, 4, 5),
        #           (6, 7, 8), (6, 7, 8), (6, 7, 8)
        #           )

        
        for i in range (0, NUM_LINE_COL_PER_SQ):
            self.square.append(lines[idx[0]].line[idx[1]+i])
        for i in range (0, NUM_LINE_COL_PER_SQ):
            self.square.append(lines[idx[0]+1].line[idx[1]+i])
        for i in range (0, NUM_LINE_COL_PER_SQ):
            self.square.append(lines[idx[0]+2].line[idx[1]+i])
            
    def has_item(self, item):
        for i in range(0, self.num_elmnt_per_square):
            if (self.square[i] == item) :
                return True
        return False
    
    def item_possible_locations(self, lines, columns, item):
        idx = self.square_idx
        for i in range (0, self.num_elmnt_per_square):
            if (self.square[i] == 0):
                self.square_scratch[i] = ' '
            else:
                self.square_scratch[i] = 'x'
            
        for i in range (0, NUM_LINE_COL_PER_SQ):
            if (lines[idx[0]+i].has_item(item)) :
                self.square_scratch[(i*NUM_LINE_COL_PER_SQ)+0] = self.square_scratch[(i*NUM_LINE_COL_PER_SQ)+1] = self.square_scratch[(i*NUM_LINE_COL_PER_SQ)+2] = 'x'
            if (columns[idx[1]+i].has_item(item)) :
                self.square_scratch[i+0] = self.square_scratch[i+3] = self.square_scratch[i+6] = 'x'
                
        return(self.square_scratch)
    
    def item_unique_possibility(self, scratch):
        hits = 0;
        for i in range(0, self.num_elmnt_per_square):
            if (scratch[i] == ' ') :
                hits+=1
                pos = i
        if hits == 1:
            return pos
        else:
            return -1
        

    def build_all_items(self, lines, columns, item, sq_idx):
        self.scratch.clear()
        sq_pos = 0;
        line_indices = SQUARE_LINES_INDEX_POS[sq_idx]
        col_indices = SQUARE_COLUMNS_INDEX_POS[sq_idx]
        for l in line_indices:
            for c in col_indices:
                line_idx = l
                col_idx = c
                if (self.square[sq_pos] == 0):
                    if not (lines[line_idx].has_item(item)):
                        if not (columns[col_idx].has_item(item)):
                            self.scratch.append((sq_pos,item))
                sq_pos += 1
        return(self.scratch)
    
    def show_elements(self):
        print(self.square)
        
class SudokuError:
    """ Error Handler """
    
    def __init__(self):
        self.error = 0
        
    def inc(self):
        self.error += 1
        
    def get(self):
        return(self.error)
        
  


