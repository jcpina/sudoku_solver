from classes import SUDOKU_UNIT, NUM_LINE_COL_PER_SQ

# States for the guess algorithm
GUESS_STATE_1  = 0
GUESS_STATE_2  = GUESS_STATE_1 + 1 
GUESS_STATE_3  = GUESS_STATE_2 + 1 
GUESS_STATE_4  = GUESS_STATE_3 + 1
GUESS_STATE_END = -1

class SudokuGuess:
    def __init__(self):
        self.guess_state = GUESS_STATE_1
        self.guess_candidates = []
        self.hit_counter = 0
        self.guess_count = 0
        self.hit_1st_per_position = [0,0,0,0,0,0,0,0,0]
        self.hit_last_per_position =  [0,0,0,0,0,0,0,0,0]
        self.guessed_idx = 0
        self.guessed_value = 0
        self.guessed_position = 0
        
        
    def state_1(self, lines, columns, squares):
        print("Looking at Lines for duets ...")
        for line_idx in range(0,9):
            hit_count_per_position = [0,0,0,0,0,0,0,0,0]
            '''
            If there is only 2 hits in the position counter, then this
            the line is a candidate for the guess game
            '''
    
            for item in range(1,10):
                '''
                The scratch buffer is a list of (line_position, candidate_value)
                for all positions in a given given line
                '''
                scratch = lines[line_idx].build_all_items(squares, columns, item)
                for l in scratch:
                    hit_count_per_position[l[0]] +=1
                    self.hit_last_per_position[l[0]] = l[1]
                    if(hit_count_per_position[l[0]] == 1): # and l[1] != 0:
                        self.hit_1st_per_position[l[0]] = l[1] 
    
            for pos in range(0,9):
                if hit_count_per_position[pos] == 2:
                    print("line Candidate [", line_idx, "] at pos: ", pos, " for item(s): ", self.hit_1st_per_position[pos], self.hit_last_per_position[pos])
                    self.hit_counter += 1
                    self.guess_candidates.append([line_idx, pos, self.hit_1st_per_position[pos], self.hit_last_per_position[pos]])
                    
                    self.guess_state = GUESS_STATE_2
                        
        ''' We found our guesses '''
        print("We found", self.hit_counter,"candidates")
        for candidate in self.guess_candidates:
            print("line Candidate [", candidate[0], "] at pos: ", candidate[1],
                   " for item(s): ", candidate[2], candidate[3])
        return self.guess_state    
        
            
    def state_2_3(self):
        if (self.guess_count < self.hit_counter):
            ''' We still have guess resources '''
            
            ''' Get the original sudoku puzzle '''
            # lines.clear()
            # lines = original_sudoku_lines()

            ''' get the next guess resource '''
            candidate = self.guess_candidates[self.guess_count]
            line_idx = candidate[0]
            line_pos = candidate[1]
            
            if(self.guess_state == GUESS_STATE_2):
                line_value = candidate[2]   # First option
            else:
                line_value = candidate[3]   # Second option   
        
            print("\n\t\t\tGuess count:", (self.guess_count + 1))
            if (self.guess_state == GUESS_STATE_2):
                print("\t\t=== Guessing 1st attempt line idx:", line_idx, "line pos:", line_pos, "value:", line_value)
                self.guess_state = GUESS_STATE_3     # Informs the guess option for the next loop if required
            else:
                print("\t\t=== Guessing 2nd attempt line idx:", line_idx, "line pos:", line_pos, "value:", line_value)
                self.guess_state = GUESS_STATE_2      # Informs the guess option for the next loop if required
                self.guess_count += 1    # Increments the number of used guess's resources
                
            self.guessed_idx = line_idx
            self.guessed_value = line_value
            self.guessed_position = line_pos
            
            return(True)    # Value to Update

        else:
            # This happens if you ran out of options
            self.guess_state = GUESS_STATE_END
            return(False)   # No more values to update
            
    def get_state(self):
        return self.guess_state
    
