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

### Installation

#### Requirements
. written in Python 2.7 (may include 3.\* in the future)

#### Install steps

Just git clone, and you're set.  Maybe symlink _plotitude_ into `/usr/local/bin`?

#### Extra considerations

If using *gnuplot*, the default *yum* install package on Amazon Linux may not include the *X11* terminal.  If building gnuplot, oneself, take the argument _--with-x_ into account.  As such: `./configure --with-x`... along with whatever other options you please.

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

[set]
?term=$OS|x11|wxt
sep=,

[plot:gnuplot] <- randy.csv,(@+1)
set term @<term> 1
set datafile separator "@<sep>"
set key autotitle columnhead
plot "randy.csv" using @x:@y
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
```ini
[source:randy.csv]
python randplot.py 0 100 34
```

There can be any number of expand blocks, as well, which run a series of python functions in listed order against every table row from their respective input files.  New columns are to be provided within these functions.  Multiple modules in the block's third token are comma-delimited.  These also run in parallel until each's completion before Rendering.
```ini
[expand:randoo.csv: expandoo] <- randy.csv
dist x y
flat dist_x_y
```

There can be any number of plot blocks.  These are not named, and do not have output files.  They must work with what files have been generated or already happen to exist.  Each treats its trailing lines as a Here file, supplying that to the provided plotting command (_gnuplot_ in this case).  And finally, these too run in parallel.
```ini
[plot:gnuplot]
set datafile separator ","
set key autotitle columnhead
set term x11 2
plot "randoo.csv" using 1:3
set term x11 3
plot "randoo.csv" using 2:3
pause -1
```

All blocks with output files must carry unique output file names.

#### Dynamic elements

Not mentioned in **Script file** above are the script's more dynamic properties.  Note that, at the moment, it's somewhat adhoc.

- set block
  - setting variables
    - setting regular variables for string replacement in plot blocks
    - system environment string replacement
    - case selection dependent on said system environment variables
- plot block string replacement
  - variable insertion into plot script
  - column name -> column index replacement

When setting variables, syntax is as follows.  Case conditions begin with a "?", and the cases are separated by "|".  The integer value of the first string in the split array is what determines which element is picked, with 0 belonging to the second string.  In this case, I use the value of the _OS_ system environment variable to decide whether to plot with a terminal Linux supports, or Windows.  The second variable, _sep_, is simply assigned the string ",".
```ini
[set]
?term=$OS|x11|wxt
sep=,
```

There are two string replacement behaviors in the plot block.  Column index replacement builds an index table with the column names of source files passed in (`<- randy.csv`).  The second element in the source file list is a modifier on the index value to return.  `(@+1)` will add 1 to the index table's returned value, `(@-2)` will subtract 2, and so forth.  This is useful for cases when columns are indexed beginning with 1, like with **gnuplot**.  Syntax for use is `@colname`, with an "@" immediately followed by the column name which's index to retrieve.
```ini
[plot:gnuplot] <- randy.csv,(@+1)
set term @<term> 1
set datafile separator "@<sep>"
set key autotitle columnhead
plot "randy.csv" using @x:@y
pause -1
```

The more straightforward string replacement is variable insertion, denoted thus: `@<term>`, with an "@" followed by the variable name surrounded by "<>".  That simply inserts the value of the specified variable in that location.

#### System environment variables

At present, this is denoted by `$OS`, a "$" followed by the env variable's name.  This does not refer to shell variables, but instead a set of system properties determined at the start of **plotitude** execution.  Presently, these variables are available.

- OS
  - either **0** for Linux, or **1** for Windows, depending on the operating system

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
