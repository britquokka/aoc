# Advent of Code
Advent of Code solutions in python  

[Advent of Code][aoc-about]   is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as interview prep, company training, university coursework, practice problems, a speed contest, or to challenge each other

### Day 1: Calorie Counting 

### Day 4: Camp Cleanup

### Day 7: No Space Left On Device
today i learn to not confuse class attributes and instance attributes in Python
```
class Student:
    count = 0                       # class attribute ( static in java or C++)
    def __init__(self, name):
        Student.count += 1   
        self.name = name            # instance attribute
```
Class attributes are shared across all objects.

Instance attributes are specific to object and defined inside a constructor using the self parameter.

I used [composite design pattern][composite design pattern] to solve the puzzle

### Day 12: Hill Climbing Algorithm
My first [BFS (Breadth-first search)][graph]

A tuple is immutable, so it can be used as dictionary's key

### Day 16: Proboscidea Volcanium
My first DFS (Depth-first search) and another BFS to compute the shortest path between valves

I have learnt more on [travelling salesman problem][travelling salesman] than i need 

Next time, i will use [Floyd-Warshall Algorithm][graph algorithms] to compute the shortest path between all pair of nodes 

`frozenset`: Frozen set is just an immutable version of a Python set object. While elements of a set can be modified at any time, elements of the frozen set remain the same after creation.
Due to this, frozen sets can be used as keys in Dictionary or as elements of another set.

### Day 14: Regolith Reservoir

### Day 18: Boiling Boulders
Use a set instead of a list and the search of element in a list becomes incredibly faster

First use of Dataclasses and first overloading for add operator
```
@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)
```
The decorator @dataclass simplify the creation of data classes by auto-generating special 
methods such as `__init__()` and `__repr__()`. 

Use parameter `(frozen=True)` to make the dataclasses immutable and hashable so they can be used directly 
with a dict and a set

### Day 19: Not Enough Minerals
DFS with a LIFO instead of a recursive call

Use collections.deque() for LIFO or FIFO instead of queue module (A multi-producer, multi-consumer queue).

Collections.dequeue are 20% faster than queue. 

Queues (from queue module) are thread-safe and shall be reserved to multi-thread communication. 

I made two solutions for day 19 : one with dataclasses and add and sub methods overloading
and the other with direct integer manipulation

Dataclasses version is slower (part1: 47s , part2: 185s) than the other version (part1: 8s, part2: 29s)

### Day 23: Unstable Diffusion

### Day 21: Monkey Math
my first [dichotomy][dichotomy] in Python
```
  def dichotomy(f, a, b, e):
        delta = 1
        while delta > e:
            m = (a + b) / 2
            delta = abs(b - a)
            if f(m) == 0:
                return m
            elif f(a) * f(m) > 0:
                a = m
            else:
                b = m
        return a, b
```

### Day 6: Tuning Trouble

### Day 2: Rock Paper Scissors

### Day 3: Rucksack Reorganization
set and list slicing practical work

### Day 5: Supply Stacks
collections.deque() practical work

### Day 8: Treetop Tree House
list search by decrementing with range 

### Day 9: Rope Bridge
Initialize a list of tuple using the * operator
```
knots = [(0, 0)] * nb_knots
```



[aoc-about]:   https://adventofcode.com/2022/about
[composite design pattern]: https://refactoring.guru/design-patterns/composite/python/example#lang-features
[graph]: https://zestedesavoir.com/tutoriels/681/a-la-decouverte-des-algorithmes-de-graphe/727_bases-de-la-theorie-des-graphes/3352_graphes-et-representation-de-graphe/
[travelling salesman]: https://interstices.info/le-probleme-du-voyageur-de-commerce/
[graph algorithms]: https://iq.opengenus.org/list-of-graph-algorithms/
[dichotomy]: https://cpge.frama.io/fiches-cpge/Python/R%C3%A9solution%20f%28x%29%3D0/Dichotomie/