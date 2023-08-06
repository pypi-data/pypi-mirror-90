# Advent of Code Optical Character Recognition (adventocr)

Some Advent of Code puzzles provide visual outputs which must be 
converted into text. This package is a helper to automate this task.

## Installation

```
pip install adventocr
```

## Usage

An example puzzle output may look something like

```python
word = [
    '#', '#', '#', '#', ' ', '#', '#', '#', '#', ' ',
    '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ',
    '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', ' ',
    '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ',
    '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ',
    '#', '#', '#', '#', ' ', '#', ' ', ' ', ' ', ' '
]
```

When tidied and printed, this appears to be 
```
#### #### 
#    #    
###  ###  
#    #    
#    #    
#### #
```

This process can be automated through:

```python
import adventocr
parsed = adventocr.word(word)
parsed
```

```python
'EF' 
```
