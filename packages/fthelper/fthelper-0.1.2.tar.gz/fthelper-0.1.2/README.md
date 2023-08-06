FTHelper V0.1
---

FTHelper is a package developed for dictionary and list operations.

```python
from fthelper import *
# or
from fthelper import Arr, Str
```

# Dictionary and list methods (Arr)

---

### <span style="color:#006dad">Array Column</span>

Returns the values from a single column of the dictionary, identified by the column name

```python
myList = [
    {
        'name': 'fatih',
        'surname': 'irday'
    },
    {
        'name': 'tugba',
        'surname': 'irday'
    },
    {
        'name': 'tunahan',
        'surname': 'irday'
    }
]

result = Arr.column(arr=myList, key='name')
# ['fatih', 'tugba', 'tunahan']


developers = [
    {'developer': {'id': 1, 'name': 'Rasmus', 'surname': 'LERDORF'}},
    {'developer': {'id': 2, 'name': 'Guido van', 'surname': 'ROSSUM'}},
    {'developer': {'id': 3, 'name': 'Fatih', 'surname': 'IRDAY'}},
]
result = Arr.column(arr=developers, key='developer.surname')

# ['LERDORF', 'ROSSUM', 'IRDAY']
```

### <span style="color:#006dad">Selectors</span>

Shifts the selected value of the list off and returns it.

#### first

```python
myList = [2, 4, 6, 8, 10]
result = Arr.first(arr=myList)
# 2
```

#### last

```python
result = Arr.last(arr=myList)
# 10
```

#### Single get

```python
single = {'local': 100, 'poc': 200, 'product': 300}
result = Arr.get(single, 'poc')
# 200

tree = {'products': {'desk': {'price': 100}, 'ask': {'price': 120}}}
result = Arr.get(tree, 'products.desk.price')
# 100

developers = [
    {'developer': {'id': 1, 'name': 'Rasmus', 'surname': 'LERDORF'}},
    {'developer': {'id': 2, 'name': 'Guido van', 'surname': 'ROSSUM'}},
    {'developer': {'id': 3, 'name': 'Fatih', 'surname': 'IRDAY'}},
]
result = Arr.get(arr=developers, key_path='developer.name')
# ['Rasmus', 'Guido van', 'Fatih']
```

### <span style="color:#006dad">Combine</span>

Creates a dictionary by using the values from the keys list as keys, and the values from the values listed as the
corresponding values.

```python
keys = ['a', 'b', 'c']
vals = (1, 2, 3)

result = Arr.combine(keys, vals)
# {'a': 1, 'b': 2, 'c': 3}
```

### <span style="color:#006dad">Divide</span>

Divides dictionary into keys and values

```python
keyList, ValueList = Arr.divide({
    'name': 'tunahan',
    'surname': 'irday'
})
# ['name', 'surname']
# ['tunahan', 'irday']
```

### <span style="color:#006dad">Have an item (Has)</span>

Have an item in the dictionary

```python
single = {'local': 100, 'poc': 200, 'product': 300}
result = Arr.has(single, 'poc')
# True

result = Arr.has(single, 'demo')
# False

tree = {'products': {'desk': {'price': 100}, 'ask': {'price': 120}}}
result = Arr.has(tree, 'products.desk.price')
# True

result = Arr.has(tree, 'products.desk.prices')
# False

developers = [
    {'developer': {'id': 1, 'name': 'Rasmus', 'surname': 'LERDORF'}},
    {'developer': {'id': 2, 'name': 'Guido van', 'surname': 'ROSSUM'}},
    {'developer': {'id': 3, 'name': 'Fatih', 'surname': 'IRDAY'}},
]
result = Arr.has(arr=developers, key_path='developer.name')
# True

result = Arr.has(arr=developers, key_path='developer.language')
# False
```

### <span style="color:#006dad">Only</span>

Getting dictionary list from dictionaries

```python
single = {'name': 'Desk', 'price': 100, 'orders': 10}
result = Arr.only(single, ['name', 'price'])
# {'name': 'Desk', 'price': 100}
```

### <span style="color:#006dad">Pluck</span>

The `pluck` method retrieves all of the values for a given key:

```python
myList = [
    {
        'name': 'fatih',
        'surname': 'irday'
    },
    {
        'name': 'tugba',
        'surname': 'irday'
    },
    {
        'name': 'tunahan',
        'surname': 'irday'
    }
]

r = Arr.pluck(myList, keys='name')
# ['fatih', 'tugba', 'tunahan']

r = Arr.pluck(myList, keys='name', vals='surname')
# {'fatih': 'irday', 'tugba': 'irday', 'tunahan': 'irday'}


multiple = [
    {'developer': {'id': 1, 'name': 'Rasmus', 'surname': 'LERDORF'}},
    {'developer': {'id': 2, 'name': 'Guido van', 'surname': 'ROSSUM'}},
    {'developer': {'id': 3, 'name': 'Fatih', 'surname': 'IRDAY'}},
]

r = Arr.pluck(multiple, keys='developer.id', vals='developer.name')
# {1: 'Rasmus', 2: 'Guido van', 3: 'Fatih'}

r = Arr.pluck(multiple, keys='developer.id')
# {1: None, 2: None, 3: None}

r = Arr.pluck(multiple, vals='developer.name')
# ['Rasmus', 'Guido van', 'Fatih']
```

### <span style="color:#006dad">Prepend</span>

Add items to the top of the list

```python
r = Arr.prepend(['a', 'b', 'c'], 'd')
['d', 'a', 'b', 'c']
```

### <span style="color:#006dad">Exists</span>

Used to search dictionaries or list

```python
r = Arr.exists(['a', 'b', 'c'], search='c')
# True

myDict = {'id': 3, 'name': 'Fatih', 'surname': 'IRDAY'}
r = Arr.exists(myDict, search='Fatih')
# True


developers = [
    {'developer': {'id': 1, 'name': 'Rasmus', 'surname': 'LERDORF'}},
    {'developer': {'id': 2, 'name': 'Guido van', 'surname': 'ROSSUM'}},
    {'developer': {'id': 3, 'name': 'Fatih', 'surname': 'IRDAY'}},
]
r = Arr.exists(developers, search='Guido van', key='developer.name')
# True


myDict = {'developer': {'id': 3, 'name': 'Fatih', 'surname': 'IRDAY'}}
r = Arr.keyExists(myDict, 'developer')
# True

r = Arr.keyExists(myDict, 'developer.id')
# True
```

### <span style="color:#006dad">Random</span>

Fetches a random item from the list

```python
r = Arr.random(['a', 'b', 'c'])
# b
```

### <span style="color:#006dad">Wrap</span>

The `wrap` method wraps the given value in an list or dictionary.

```python
r = Arr.wrap(None)
# []

r = Arr.wrap()
# []

r = Arr.wrap('demo')
# ['demo']

r = Arr.wrap('developer.name.first', 'fatih')
# {'developer': {'name': {'first': 'fatih'}}}
```

### <span style="color:#006dad">Array Filter</span>

filters empty and none values in the list.

```python
ff = ['', None, 14, 'qwe']
r = Arr.array_filter(ff)
# [14, 'qwe']
```

<br />


# String methods (Str)

---

### <span style="color:#006dad">Random</span>

Creates a string of the specified length. Runs as 16 characters if length is not specified

```python
result = Str.random()
# lQCcgS8V3fRfpjS4

result = Str.random(20)
# KLzXIkwNstlEs97oZuLd
```



### <span style="color:#006dad">Limit</span>

The `limit` method truncates the given string to the specified length. An additional string may be passed to this method via its third argument to specify which string should be appended to the end of the truncated string

```python
result = Str.limit('Perfectly balanced, as all things should be.', 9)
# Perfectly

result = Str.limit('Perfectly balanced, as all things should be.', 9, '!..')
# Perfectly!..
```



### <span style="color:#006dad">Words</span>

The `words` method limits the number of words in a string. An additional string may be passed to this method via its third argument to specify which string should be appended to the end of the truncated string

```python
result = Str.limit('Perfectly balanced, as all things should be.', 9)
# Perfectly

result = Str.limit('Perfectly balanced, as all things should be.', 9, '!..')
# Perfectly!..
```



### <span style="color:#006dad">String Cases</span>

StringCase methods convert the given string to the desired StringCase

* kebab case
* camel case
* pascal case
* snake case

```python
result = Str.kebabcase('fatih irday')
# fatih-irday

result = Str.camelcase('fatih irday')
# fatihIrday

result = Str.pascalcase('fatih irday')
# FatihIrday

result = Str.snakecase('fatih irday')
# fatih_irday
```



### <span style="color:#006dad">isStr</span>

The `isStr` method determines if a given string matches a given pattern

```python
result = Str.isStr('13')
# True

result = Str.isStr(13)
# False
```



### <span style="color:#006dad">isAscii</span>

The `isAscii` method determines if a given ASCII matches a given pattern

```python
result = Str.isAscii('ascii code'.encode())
# True

result = Str.isAscii('ascii code')
# False
```



### <span style="color:#006dad">isEmpty</span>

The `isEmpty` method determines if the given string is empty

```python
result = Str.isEmpty('string')
# False

result = Str.isEmpty(13)
# False

result = Str.isEmpty(None)
# True

result = Str.isEmpty('')
# True
```



### <span style="color:#006dad">Start</span>

The `start` method adds a single instance of the given value to a string if it does not already start with that value

```python
result = Str.start('this/string', '/')
# /this/string

result = Str.start('/this/string', '/')
# /this/string
```


<br />

## Fluent strings (Str.of)

Fluent strings provide a more fluent, object-oriented interface for working with string values, allowing you to chain multiple string operations together using a more readable syntax compared to traditional string operations.


### <span style="color:#006dad">Append</span>

The `append` method appends the given values to the string

```python
of = Str.of('Fatih').append(' Irday')
of.getValue()
# Fatih Irday
```

### <span style="color:#006dad">Prepend</span>

The `prepend` method prepends the given values onto the string

```python
of = Str.of('Fatih Irday').prepend('Person : ')
of.getValue()
# Person : Fatih Irday
```

### <span style="color:#006dad">Replace</span>

The `replace` method replaces a given string within the string

```python
of = Str.of('Python 2.x, Python version 2').replace('2', '3')
of.getValue()
# Person : Python 3.x, Python version 3
```

### <span style="color:#006dad">Replace First</span>

The `replaceFirst` method replaces the first occurrence of a given value in a string

```python
of = Str.of('Python 2.x, Python version 2').replaceFirst('2', '3')
of.getValue()
# Person : Python 3.x, Python version 2
```

### <span style="color:#006dad">Replace Last</span>

The `replaceLast` method replaces the last occurrence of a given value in a string

```python
of = Str.of('Python 2.x, Python version 2').replaceLast('2', '3')
of.getValue()
# Person : Python 2.x, Python version 3
```

### <span style="color:#006dad">Replace List</span>

The `replaceList` method replaces a given value in the string sequentially using a list

```python
of = Str.of('Python ?.x and ?.x').replaceList('?', ['3.6', '3.9'])
of.getValue()
# Python 3.6.x and 3.9.x
```

### <span style="color:#006dad">Replace Matches</span>

The `replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string

```python
of = Str.of('(+1) 501-555-1000').replaceMatches("[^A-Za-z0-9]", '')
of.getValue()
# 15015551000
```

### <span style="color:#006dad">After</span>

The `after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string

```python
of = Str.of('This is my name').after('is')
of.getValue()
# ' is my name'
```

### <span style="color:#006dad">After Last</span>

The `afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string

```python
of = Str.of('This is my name').afterLast('is')
of.getValue()
# ' my name'
```

### <span style="color:#006dad">Before</span>

The `before` method returns everything before the given value in a string

```python
of = Str.of('This is my name').before('is')
of.getValue()
# ' Th'
```

### <span style="color:#006dad">Before Last</span>

The `beforeLast` method returns everything before the last occurrence of the given value in a string

```python
of = Str.of('This is my name').beforeLast('is')
of.getValue()
# ' This'
```