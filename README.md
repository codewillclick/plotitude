# plotitude
Simple organizing means between data generation/acquisition, table column expansion, and graphical rendering.

### Usage

`plotitude <script-name> [options...]`

Options
- **--loglevel**
  - following token can be one of... (case irrelevant)
    - info
    - debug
    - warning
    - error
    - critical

### Design details

There are three parallel blocks in a \*.tude script.
- source evaluation
- column expansion
- plot rendering

Take this example, for instance:
```
[source:randy.csv]
python randplot.py 0 100 34

[expand:randoo.csv: expandoo] <- randy.csv
dist x y
flat dist_x_y

[plot:gnuplot]
set term x11 1
set datafile separator ","
set key autotitle columnhead
plot "randy.csv"
pause -1

[plot:gnuplot]
set datafile separator ","
set key autotitle columnhead
set term x11 2
plot "randoo.csv" using 1:3
set term x11 3
plot "randoo.csv" using 2:3
pause -1
```

There can be one or more source blocks.  Each will run its trailing lines in order, outputting to the provided file name.  These run in parallel, waiting until completion of each before proceeding to Expansion.

There can be any number of expand blocks, as well, which run a series of python functions in listed order against every table row from their respective input files.  New columns are to be provided within these functions.  These also run in parallel until each's completion before Rendering.

There can be any number of plot blocks.  These are not named, and do not have output files.  They must work with what files have been generated or already happen to exist.  Each treats its trailing lines as a Here file, supplying that to the provided plotting command (_gnuplot_ in this case).  And finally, these too run in parallel.

All blocks with output files must carry unique output file names.

### Changelog

#### v0.1

New features
- plotitude module funcitonal
- runs initial example script to satisfaction

Bug fixes
- example file's gnuplot call now retains X11 windows until they are closed by hand... or Enter is hit in the terminal (not a feature)

Misc notes
- imperfect, e.g. having to hit enter in the terminal to properly close plotting threads
