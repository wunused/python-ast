This test is to check if a "from . import x" statement is correctly handled

The analyzer should recognize that . refers to the same directory it is and grab the module x to be analyzed. We know it has passed the test if something in x is inherited and in the output, that thing is in a branch with x.py as the filename next to it