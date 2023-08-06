
# AttribDict

## Introduction

AttribDict is an easy to use and easy to read dict, it is more flexible and human readable.

## Examples

```python
>>> from attribdict import AttribDict as Dict
>>> _d = {"attr"+str(i): i for i in range(4)}
>>> d = Dict(_d) # create a AttribDict instance from a dict
>>> print(d)
attr0: 0
attr1: 1
attr2: 2
attr3: 3
```

You can also recursively create an attribute from other data type including ```dict```: 

```python
# continue to previous code
>>> d.attr4.subattr1.subsubattr1 = {1, 2, 4} # recursively create attribute
>>> d.attr5.subattr1 = {"subsubattr"+str(i): i for i in range(3)} # recursively create from a dict
>>> print(d)
attr0: 0
attr1: 1
attr2: 2
attr3: 3
attr4:
    - subattr1:
        - subsubattr1: {1, 2, 4}
attr5:
    - subattr1:
        - subsubattr0: 0
        - subsubattr1: 1
        - subsubattr2: 2
```

Additionally, ```AttribDict``` also support create attributes from a recursively ```dict```: 

```python
# continue to previous code
>>> _d = {"_attr1": {"_subattr1": {"_subsubattr1": "hello attribdict"}}} # create attributes from a recursively dict
>>> d._attr = _d
>>> print(d)
attr0: 0
attr1: 1
attr2: 2
attr3: 3
attr4:
    - subattr1:
        - subsubattr1: {1, 2, 4}
attr5:
    - subattr1:
        - subsubattr0: 0
        - subsubattr1: 1
        - subsubattr2: 2
_attr:
    - _attr1:
        - _subattr1:
            - _subsubattr1: hello attribdict
```

If you want to convert an AttribDict instance into a python ```dict```, just use ```.as_dict``` method: 

```python
# continue to previous code
>>> _dict = d.as_dict()
>>> print(_dict)
{'attr0': 0, 'attr1': 1, 'attr2': 2, 'attr3': 3, 'attr4': {'subattr1': {'subsubattr1': {1, 2, 4}}}, 'attr5': {'subattr1': {'subsubattr0': 0, 'subsubattr1': 1, 'subsubattr2': 2}}, '_attr': {'_attr1': {'_subattr1': {'_subsubattr1': 'hello attribdict'}}}}
```

You can also access value in traditional ```dict``` way, for example: 

```python
>>> print(d["_attr"].as_dict())
{'_attr1': {'_subattr1': {'_subsubattr1': 'hello attribdict'}}}
```

Please feel free if you want to access value in following style:

```python
>>> print(d._attr["_attr1"]._subattr1["_subsubattr1"])
hello attribdict
```

AttribDict instance is iterable, thus you can use ```for``` statement and so on to iteratively visit the attributes and corresponding values. Note that it will return (attribute, value) pair, sub-AttribDict will be converted to a python ```dict``` for more convenient use: 

```python
# continue to previous code
>>> for key, value in d:
...     print("key: ", key)
...     print("value: ", value)
...
key:  attr0
value:  0
key:  attr1
value:  1
key:  attr2
value:  2
key:  attr3
value:  3
key:  attr4
value:  {'subattr1': {'subsubattr1': {1, 2, 4}}}
key:  attr5
value:  {'subattr1': {'subsubattr0': 0, 'subsubattr1': 1, 'subsubattr2': 2}}
key:  _attr
value:  {'_attr1': {'_subattr1': {'_subsubattr1': 'hello attribdict'}}}
```

Here is another example about iterable, the rest code is omitted: 

```python
>>> it = iter(d)
>>> next(it)
('attr0', 0)
>>> next(it)
('attr1', 1)
>>> next(it)
('attr2', 2) 
```

AttribDict offers two ways to copy and deepcopy an instance:

```python
>>> import copy
>>> d_copy = d.copy()
>>> print(d._attr is d_copy._attr)
True
>>> copy_d = copy.copy(d)
>>> print(d._attr is copy_d._attr)
>>> True
>>> d_deepcopy = d.deepcopy()
>>> print(d._attr is d_deepcopy._attr)
False
>>> print(d.attr4.subattr1.subsubattr1 is d_deepcopy.attr4.subattr1.subsubattr1)
False
>>> deepcopy_d = copy.deepcopy(d)
>>> print(d._attr is deepcopy_d._attr)
>>> False
>>> print(d.attr4.subattr1.subsubattr1 is deepcopy_d.attr4.subattr1.subsubattr1)
False
```

If you want to check whether an object contains attribute `attrX`, please use `obj.hasattr("attrX")` but `hasattr(obj, "attrX")` as the latter one will create a new AttributeDict instance named `attrX`. 

```python
>>> d.hasattr("attrX")
False
>>> hasattr(d, "attrX")
True
```

## Installation

You can install AttribDict by pip.

```
pip install attribdict
```