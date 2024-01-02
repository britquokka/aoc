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
At each iteration, 
col contains [ rows[0][ j ], rows[1][ j ],... ]


### Day 13: Point of Incidence

Python all() is used to find reflection point in a list of string

all() Return True if all elements of the iterable are true (or if the iterable is empty)

```
up_range = range(proposal + 1, len(lines))
down_range = range(proposal, -1, -1)
found = all([lines[i] == lines[j] for i, j in zip(up_range, down_range)])
```

### Day 15: Lens Library

[aoc-about]:   https://adventofcode.com/2023/about
[fonction du second degre]: https://campussaintjean.be/IMG/pdf/chapitre_3_la_fonction_du_second_degre_1_.pdf
[quadratic polynomial]: https://www.cuemath.com/algebra/roots-of-quadratic-equation/
[bisect]: https://docs.python.org/3/library/bisect.html
[bisect_right]: https://www.educative.io/answers/what-is-bisectbisectright-in-python
[mebeim day12]: https://github.com/mebeim/aoc/tree/master/2023#day-12---hot-springs
