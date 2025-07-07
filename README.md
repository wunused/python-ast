Primary Purpose: print out class hierarchy tree

**Usage**

Must always take in a file. This can be a relative (to the current working directory) or absolute path. With only the file as the positional argument, it prints out all the classes in it.

_Optional Arguments:_

-h | shows help message
-c | provides class inheritance tree for a specific class along with the filename each class is in
-f | type: flag. Must be used with -c. Adds each class' functions to the inheritance tree
-p | type: flag. Must be used with -c. Prints out full module path each class is in instead of filename
-a | type: flag. cannot be used with -c. Effectively runs -c on every class inside the file. Can be used with -f and -p
