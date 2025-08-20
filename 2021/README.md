[Advent of Code 2021][aoc-about]

### Day 1: Sonar Sweep ! 
 List comprehension and slicing
 List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list

### Day 3: Binary diagnostic
join and zip

zip: make an iterator than aggregate elements from each of the iterables.

The new iterator is a tuple

zip('ABCD', 'xy') --> Ax By
```  
list(zip('ABCD', 'xy'))
[('A', 'x'), ('B', 'y')]
```  

join: return a string which is the concatenation of the string in iterables.
The join method is called on the wanted separator
```  
"-".join('ABCD')
'A-B-C-D'
```

### Day 6: Lanternfish 

### Day 7: The Treachery of Whales

### Day 9: Smoke Basin
firs use of a python generator to avoid to store big list in memory
```
  def all_points(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                p = Point(x, y)
                yield p
```
Python generators efficiently create iterators by generating values only when requested, avoiding the need to store the entire sequence in memory simultaneously.

When this function is called, it returns an iterator. Every call to next() method transfers the control back to the generator and fetches next point.

### Day 15: Chiton

My second [Dijkstra][Dijkstra].
Previous was applied on day23 of 2023

I use @classmethod to provide multiple constuctors for a class

```
class Cave:

    def __init__(self, risk_level_map, len_x: int, len_y: int):
        self.risk_level_map = risk_level_map
        self.len_x = len_x
        self.len_y = len_y
        self.destination = Point(self.len_x - 1, self.len_y - 1)

    @classmethod
    def build_cave(cls, risk_level_map):
        len_x = len(risk_level_map)
        len_y = len(risk_level_map[0])
        return cls(risk_level_map, len_x, len_y)

```
and invoke the __init__ of the parent class in a child class 

```
class BiggerCave(Cave):

    def __init__(self, risk_level_map, bigger_coefficient=5):
        self.orig_len_x = len(risk_level_map)
        self.orig_len_y = len(risk_level_map[0])
        Cave.__init__(self, risk_level_map,  self.orig_len_x*bigger_coefficient, self.orig_len_y * bigger_coefficient)
```

### Day 10: Syntax Scoring

collections.deque() practical work



[aoc-about]:   https://adventofcode.com/2021/about
[Dijkstra]: https://builtin.com/software-engineering-perspectives/dijkstras-algorithm