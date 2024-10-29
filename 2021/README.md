[Advent of Code 2021][aoc-about]

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

[aoc-about]:   https://adventofcode.com/2021/about

