[Advent of Code 2023][aoc-about]

### Day 1: Trebuchet?! 
There are several ways to find a digit in a string.


You can use List comprehension. It offers a shorter syntax when you want to create a new list based on the values of an existing list
```
text="3cf4kbkclqfourseven4"           
digits = [c for c in text if c.isdigit()]
```
or use the filter function to filter out numeric elements from the list
```  
text="3cf4kbkclqfourseven4" 
digits = list(filter(lambda c: c.isdigit(), text))
```  

### Day 2: Cube Conundrum

###  Day 4: Scratchcards
Set intersection with intersection method
```
set1 = {2, 3, 5}
set2 = {1, 3, 5}
new_set = set1.intersection(set2)
```
or with & operator
```
new_set = set1 & set2
```

### Day 5: If You Give A Seed A Fertilizer
[Array bisection algorithm][bisect] to find insertion point in a list or interval.

Use it to optimize map lookup
```
a_list = [1,3,5,7,10,25,49,55]
new_item = 25
idx = bisect.bisect_right(nums, new_item)
```
Result is idx=6


### Day 6: Wait For It
Find roots in a [quadratic polynomial][quadratic polynomial]]

### Day 7: Camel Cards
List count() method returns the count of how many times a given object occurs in a list . 
```
hand = 'J2JJ3'
Counters = [hand.count(c) for c in set(hand)]
```
Result is Counters = [3,1,1]

### Day 10: Pipe Maze (part 1 only)

### Day 12: Hot Springs (part 2 KO)

a DFS is used  
* Part 1 example execution time is 0.0 s
* Part 1 full input execution time is 0.90 s
* Part 2 example execution time is 2.95 s
* Part 2 full input (1000 rows)  is KO when too many ? on the row.

Part 2 can have more than 80 millions arrangements per row. DFS can take almost 20 mn per row with this implementation !

I take the solution adapted to DFS provided by  [mebeim][mebeim day12]

DFS LIFO implementation is converted to recursive DFS and use a cache 
to avoid to do the same search a lot of times.

Part 2 full input execution time is now 1.6 s

### Day 14: Parabolic Reflector Dish

### Day 11: Cosmic Expansion
Python unzip (zip with * operator) is used to transpose rows and columns in input data
``` 
def transpose(rows: list):
    return ["".join(col) for col in zip(*rows)]
```
the zip() function takes multiple iterable objects as arguments and returns an iterator of tuples containing
elements from each of the iterables.
```
>>> numbers = [1, 2, 3]
>>> letters = ['a', 'b', 'c']
>>> zipped = zip(numbers, letters)
>>> list(zipped)
[(1, 'a'), (2, 'b'), (3, 'c')]
```

### Day 13: Point of Incidence

Python all() is used to find reflection point in a list of string

all() Return True if all elements of the iterable are true (or if the iterable is empty)

```
up_range = range(proposal + 1, len(lines))
down_range = range(proposal, -1, -1)
found = all([lines[i] == lines[j] for i, j in zip(up_range, down_range)])
```

### Day 15: Lens Library


### Day 16: The Floor Will Be Lava

Another DFS with LIFO implementation

### Profiler in PyCharm

```
$ pip install snakeviz
$ pip install cprofilev
```
Create new run/debug cfg named "day16 cProfile"
and add to Interpreter Options 
```
-B -m cProfile -o output.prof
```
or
```
-B -m cProfilev
```
and visualize cProfile result in GUI
```
$ snakeviz program.prof
```
### Day 23: A Long Walk
Depth-First Search (DFS) practical work.

For part 2, a weighted graph is used. Only node with intersection ( = with more than 2 edges ) from the initial grid are kept in the graph. 

Each edge has a weight equal to the distance between 2 nodes connected by the edge

The weighted graph is represented by an adjacency list.

### Day 21: Step Counter
For part 1 , a DFS with state store is used. 
It avoids to redo the same exploration several times

### Day 8: Haunted Wasteland

For part 2, all way from nodes 'xxA' to 'yyA' don't intersect, 
so you need to find the number of steps for each network path and compute the [LCM][LCM] of the steps found.

###  Day 9: Mirage Maintenance
Slicing and recursive function practical works

The built-in function any(iterable) is used to test if an element of the list is > 0

### Day 17: Clumsy Crucible

My first [Dijkstra][Dijkstra]

It uses a priority queue
```
import heapq
customers = []
heapq.heappush(customers, (2, "Harry"))
heapq.heappush(customers, (3, "Charles"))
heapq.heappush(customers, (1, "Riya"))
heapq.heappush(customers, (4, "Stacy"))
while customers:
     print(heapq.heappop(q))
#Will print names in the order: Riya, Harry, Charles, Stacy.
```
### Day 18: Lavaduct Lagoon

The [shoelace formula][shoelace] is used to determine the area of a 
simple polygon whose vertices are described by their Cartesian 
coordinates in the plane.  

Python itertools.pairwise is used to iterate on two consecutive elements in a list
```
pairwise('ABCDEFG') --> AB BC CD DE EF FG
```
```
def shoelace_formula(vertices: list):
    res = 0
    # vertex is a tuple who contains coordinate (y, x)
    for vertex, next_vertex in itertools.pairwise(vertices):
        res += vertex[1] * next_vertex[0] - vertex[0] * next_vertex[1]
    return abs(res) / 2
```

### Day 19: Aplenty

[composite design pattern][composite design pattern] is used to solve the puzzle


[aoc-about]:   https://adventofcode.com/2023/about
[fonction du second degre]: https://campussaintjean.be/IMG/pdf/chapitre_3_la_fonction_du_second_degre_1_.pdf
[quadratic polynomial]: https://www.cuemath.com/algebra/roots-of-quadratic-equation/
[bisect]: https://docs.python.org/3/library/bisect.html
[bisect_right]: https://www.educative.io/answers/what-is-bisectbisectright-in-python
[mebeim day12]: https://github.com/mebeim/aoc/tree/master/2023#day-12---hot-springs
[LCM]: https://en.wikipedia.org/wiki/Least_common_multiple
[Dijkstra]: https://builtin.com/software-engineering-perspectives/dijkstras-algorithm
[shoelace]: http://villemin.gerard.free.fr/GeomLAV/Polygone/Lacet.htm
[composite design pattern]: https://refactoring.guru/design-patterns/composite/python/example#lang-features
