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


### Day 6: Wait For It
Find roots in a [quadratic polynomial][quadratic polynomial]]

[aoc-about]:   https://adventofcode.com/2023/about
[fonction du second degre]: https://campussaintjean.be/IMG/pdf/chapitre_3_la_fonction_du_second_degre_1_.pdf
[quadratic polynomial]: https://www.cuemath.com/algebra/roots-of-quadratic-equation/