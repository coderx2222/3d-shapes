# 3d-shapes

This is a Python script for generating random shapes for 3d printing.
Just for fun and experimentation.

`USAGE:`<br>
`  -g <gen-stl-file> [ -n <num-shapes> ] [ -s <max-shape-size> ] [ -plot ]`<br>
`WHERE:`<br>
`  Output STL will be written to <gen-stl-file>`<br>
`  If -plot is specified it will plot the triangle points as a 3d scatter plot`<br>

For example:<br>
`$ python gen-stl.py -g output.stl -n 42 -s 10`<br>

The output.stl will be an ASCII format STL file.<br>
To 3d print the resulting shape you will then need to load the STL file in your
favorite Slicer program and convert the STL to gcode for your printer.<br>

Also, you can use Freecad or this Slic3r for viewing the STL files.<br>
https://slic3r.org/

