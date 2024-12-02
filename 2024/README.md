[Advent of Code 2024][aoc-about]

### Day 1: Historian Hysteria
List comprehension and zip

zip: make an iterator than aggregate elements from each of the iterables.

The new iterator is a tuple

zip('ABCD', 'xy') --> Ax By
```  
list(zip('ABCD', 'xy'))
[('A', 'x'), ('B', 'y')]
```  

### Day 2: Red-Nosed Reports

zip and slicing practical work.

The fast (x4) implementation avoid to do a lot of useless iterations to find the bad level.
The drawback of the fast implementation is the amount of code.


[aoc-about]:   https://adventofcode.com/2024/about
