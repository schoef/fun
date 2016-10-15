''' Class that holds the Sudoku data struct
'''

import copy
import sys
from operator import mul

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield list(val)

class Sudoku:

    @staticmethod
    def cast_char_to_int ( char ):
        ''' Return int of possible, otherwise catch ValueError and return None
        '''
        try:
            res = int( char )
        except ValueError:
            res = None
        return res
    
    def __init__( self, data ):
        self.data         = data 
        self.initial_data = copy.deepcopy(data)
        # Initial hypothesis: For each in int i the square take [i], for None take range(1,10)
        self.hypothesis = map( lambda l: map( lambda i: [i] if isinstance(i, int) else range(1,10), l), data ) 

    def __str__( self ):

        res = ""
        for i_line, line in enumerate( self.data ):
            l_str = []
            for j_num, d in enumerate( line ):
                if self.initial_data[i_line][j_num] == line[j_num] and line[j_num] is not None:
                    l_str.append( bcolors.BOLD + ' ' + str(line[j_num]) + ' ' + bcolors.ENDC )
                elif line[j_num] is None:
                    l_str.append( "   " )
                else:
                    l_str.append( ' ' + str(line[j_num]) + ' ' )
            groups = list( group( l_str, 3 ) )
            l = u'\u2551'.encode('utf-8').join( map( lambda g: "|".join(g), groups ) )
            #l =  "|".join( l_str ) 
            res+=  l + '\n'
            if i_line in [2,5]:
                res+= u'\u256C'.encode('utf-8').join( [ u'\u2550'.encode('utf-8')*(3*4 - 1 ) for i in range(3) ] ) + '\n'


        return res
 
    @classmethod
    def from_text_file( cls, fname, delimiter = '/'):
        ''' Read file 'fname' line by line.
        txt file format: x1/x2/..../x9 ( 9 lines with 8 delimiters each)
        '''

        with open(fname) as f:
            content = f.readlines()

            _data = []

            for line in content:

                # Strip after '#'
                line = line.split("#")[0]

                # 9 numbers hould have 8 delimiters
                if line.count( delimiter ) != 8:
                    continue

                line_content = map( Sudoku.cast_char_to_int, line.split( delimiter ) )
                if len(line_content)==9:
                    _data.append( line_content )

            if len( _data ) == 9:
                return cls( _data )

    def is_done( self ):
        '''Check whether the board is solved by checking the length of hypothises is 1 on all positions
        '''
        return all( len(self.hypothesis[i][j])==1 for i in range(9) for j in range(9) )

    def has_no_duplicates( self, positions ):
        ''' Returns True if the values in self.data at 'positions' are unique (excluding None)
        '''
        vals = filter( lambda x: x is not None, [ self.data[p[0]][p[1]] for p in positions ] )
        return len(vals) == len(set(vals))

    def is_consistent( self ):
        ''' Check whether the current numbers in self.data satisy the rules
        '''

        # quadrants
        for i in range( 3 ):
            for j in range( 3 ):
                if not self.has_no_duplicates( [ [ 3*i + _i, 3*j + _j ] for _i in range(3) for _j in range(3) ] ):
                    return False
        # column
        for i in range( 9 ):
            if not self.has_no_duplicates( [ [ i,  _j ] for _j in range(9) ] ):
                return False
        # row 
        for j in range( 9 ):
            if not self.has_no_duplicates( [ [ _i,  j ] for _i in range(9) ] ):
                return False

        # check if there are zero hypothesis somewhere
        for i in range( 9 ):
            for j in range( 9 ):
                if len(self.hypothesis[i][j])==0:
                    return False

        return True 

    def update_data_from_hypothesis( self ):
        ''' Add the unambigous information (length of hypothesis is 1) from the hypothesis to data
        '''
        for i in range( 9 ):
            for j in range( 9 ):
                if len(self.hypothesis[i][j])==1 and self.data[i][j] is None:
                    #print "Found new entry at",i,j,"which is ",self.hypothesis[i][j][0]
                    self.data[i][j] = self.hypothesis[i][j][0]

    def eliminate_hypothesis( self, i, j ):
        ''' Remove all hypothesis that are inconsistent with the entry in position i,j
        '''

        changed = False

        # Accumulate all positions where we can't have the entry in i,j
        constraints = []

        # quadrant
        positions = []
        for _j in range(3):
            for _i in range(3):
                positions.append( [ 3*(i/3) + _i, 3*(j/3) + _j ] )
        constraints.append( positions )

        # column
        positions = []
        for _i in range(9):
            positions.append( [ _i, j ] ) 
        constraints.append( positions )

        # row
        positions = []
        for _j in range(9):
            positions.append( [ i, _j ] )
        constraints.append( positions )

        # remove from hypothesis from other fields if the number in this position is known:
        if len( self.hypothesis[i][j] ) == 1:
            num = self.hypothesis[i][j][0]

            for _i, _j in sum(constraints, []):
                if _i==i and _j==j: continue
                if num in self.hypothesis[_i][_j]:
                    changed = True
                    self.hypothesis[_i][_j].remove( num )
                    if len(self.hypothesis[_i][_j]) == 0:
                        print "Error! No hypothesis left for %i %i!"%(_i,_j)
                        print self
                        sys.exit( 0 )
        elif len( self.hypothesis[i][j] ) >= 1:
            # Try to find out whether there is a hypothesis at i,j that is unique in each column/row/quadrant
            for positions in constraints:
                for num in self.hypothesis[i][j]:
                    if sum( [ self.hypothesis[p[0]][p[1]].count( num ) for p in positions ] ) == 1:
                        # print "For %i,%i: Found unique constraint %i in %r"% ( i, j, num, positions )
                        # print [ self.hypothesis[p[0]][p[1]] for p in positions ]
                        self.hypothesis[i][j] = [ num ]
                        changed = True
                        break

                if changed: break
        else:
            print "Should not happen. Length of hypothesis is %i" % len( self.hypothesis[i][j] )

        self.update_data_from_hypothesis()
    
        return changed

    def eliminate_all_hypothesis( self ):
        ''' Loop over the board and eliminate hypothesis if there is smth to do.
        '''
        changed = False
        for i in range( 9 ):
            for j in range ( 9 ):
                if self.eliminate_hypothesis( i, j ):
                    changed = True

        return changed

    def solve( self ):

        if not self.is_consistent:  return False

        # Remove all hypothesis by looking at quadrants, vertical and horizontal lines until nothing changes
        while True:
            if not self.eliminate_all_hypothesis():
                # Nothing changes any more
                break

        if not self.is_consistent:  return False
        if self.is_done():          return True

        # Look at all hypothesis and make assumptions. Start with the shortest ones.
        non_trivial_hypothesis = [(self.hypothesis[i][j], i, j) for i in range(9) for j in range( 9 ) if len(self.hypothesis[i][j])>1]
        non_trivial_hypothesis.sort( key = lambda k:len( k[0]) )

        multiplicity = reduce(mul, [len(h[0]) for h in non_trivial_hypothesis], 1)

        # print self

        #print "NTH", non_trivial_hypothesis
        for possibilities, i, j in non_trivial_hypothesis:
            for assumption in possibilities:
                new_data        = copy.deepcopy( self.data )
                new_data[i][j]  = assumption
                # print "Set %i %i to assumption %i"%(i,j,assumption)
                new_sudoku = Sudoku( new_data )
                new_sudoku.initial_data = self.initial_data
                if new_sudoku.solve():
                    self.data = new_sudoku.data
                    self.hypothesis = new_sudoku.hypothesis
                    return True

        return False
