# 3d-shapes

This is a Python script for generating random shapes for 3d printing.
Just for fun and experimentation.

USAGE:
  -g <gen-stl-file> [ -n <num-shapes> ] [ -s <max-shape-size> ] [ -plot ]
WHERE:
  Output STL will be written to <gen-stl-file>
  If -plot is specified it will plot the triangle points as a 3d scatter plot

For example:
$ python gen-stl.py -g output.stl -n 42 -s 10

The output.stl will be an ASCII format STL file.
To 3d print the resulting shape you will then need to load the STL file in your
favorite Slicer program and convert the STL to gcode for your printer.

If you like it, please leave a comment!

