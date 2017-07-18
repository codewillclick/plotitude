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

#### Script file
There are three parallel blocks in a \*.tude script.
- source evaluation
- column expansion
- plot rendering

Take this example, for instance:
```ini
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

There can be any number of expand blocks, as well, which run a series of python functions in listed order against every table row from their respective input files.  New columns are to be provided within these functions.  Multiple modules in the block's third token are comma-delimited.  These also run in parallel until each's completion before Rendering.

There can be any number of plot blocks.  These are not named, and do not have output files.  They must work with what files have been generated or already happen to exist.  Each treats its trailing lines as a Here file, supplying that to the provided plotting command (_gnuplot_ in this case).  And finally, these too run in parallel.

All blocks with output files must carry unique output file names.

#### Expansion functions

All listed and imported expansion python modules provide a flat list of functions for use in the Expansion step.  Take this, for instance.

```python
#!/usr/bin/env python

import math
import logging as L

def dist(t,r,enum,args):
        kx,ky = args[0:2]
        a = int(r[enum[kx]])
        b = int(r[enum[ky]])
        key = '_'.join(['dist',kx,ky])
        t[key] = math.sqrt(a*a + b*b)
        return ((key,t[key]),)

def flat(t,r,enum,args):
        kv = args[0]
        key = 'flat_' + kv
        t[key] = int(float(r[enum[kv]]))
        return ((key,t[key]),)


if __name__ == '__main__':
        import sys

        print "Shouldn't be running this as __main__, yo!"
```

Here are listed two functions, _dist_ and _flat_, which take the format...

- `func(t,r,enum,args)`
  - Arguments:
    - t: OrderedDict passed through to gather new columns and values
    - r: list representing a tokenized/split row string
      - this may be addressed in the future, given how slow that makes things in the face of tables thousands of columns wide
      - new columns are added as the function chain progresses
    - enum: OrderedDict storing key-value pairs of \<column-name\>:\<row-index\>.
      - also grows as the function chain progresses
    - args: arguments provided the function from the expand block
      - these ought be assumed column names
  - Returns:
    - a list of (\<column-name\>:\<value\>) pairs
    - return values are directly used to expand both _r_ and _enum_, so this is a must.

(Note this is the first draft of this specification/methodology and may be subject to change.)

### Changelog

#### v0.1

New features
- plotitude module functional
- runs initial example script to satisfaction

Bug fixes
- example file's gnuplot call now retains X11 windows until they are closed by hand... or Enter is hit in the terminal (not a feature)

Misc notes
- imperfect, e.g. having to hit enter in the terminal to properly close plotting threads
