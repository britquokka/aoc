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

### Day 3: Mull It Over

RegEx practical work. 

I try for the first time a "match Statement".
A match statement takes an expression and compares its value to successive patterns given as one or more case blocks. This is superficially similar to a switch statement in C, Java or JavaScript (and many other languages),

```
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"
```

### Day 4: Ceres Search 

List comprehension practical work

### Day 6: Guard Gallivant 


[aoc-about]:   https://adventofcode.com/2024/about
