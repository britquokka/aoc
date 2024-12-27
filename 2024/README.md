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

Part2 in day06_fast.py implementation is x4 faster. 
It uses at each test a part of the previous computed path to avoid to redo the same thing several time 

### Day 10: Hoof It

Depth-first search (DFS) practical work

### Day 14: Restroom Redoubt

part 1 only is solved.
In part 2, we need to find a Christmas tree which is drawn by robots positions in area at a specific time
but I don't know how to solve that. Try to find the map with the more adjacent robots  ?  


### Day 18: RAM Run

BFS (Breadth First Search) practical works

### Day 12: Garden Groups

BFS too



[aoc-about]:   https://adventofcode.com/2024/about
