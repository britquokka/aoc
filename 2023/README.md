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

[aoc-about]:   https://adventofcode.com/2023/about