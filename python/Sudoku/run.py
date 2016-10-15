#! /usr/bin/env python
import sys

from Sudoku import Sudoku
if len(sys.argv)>1:
    sudoku = Sudoku.from_text_file( sys.argv[1] )
else:
    sudoku = Sudoku.from_text_file( 'hoellisch2.txt' )

print 'Input:'
print sudoku

#converged = True#sudoku.solve()
converged = sudoku.solve()

if converged:
    print "Converged!"
    print sudoku
else:
    print "Not converged!"
    print sudoku
    print "Hypothesis:"
    print sudoku.hypothesis

