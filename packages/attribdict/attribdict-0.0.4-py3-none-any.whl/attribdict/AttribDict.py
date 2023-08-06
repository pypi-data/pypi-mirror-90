
"""
Author  Yiqun Chen
Time    2020-12-19
Docs    Allows access keys' value in attribute style and print it in readable style.
"""

import copy

class AttribDict:
    """
    An easy and readable dict.
    Example:
    >>> from attribdict import AttribDict as Dict
    >>> _d = {"attr"+str(i): i for i in range(4)}
    >>> d = Dict(_d)
    >>> print(d)
    attr0: 0
    attr1: 1
    attr2: 2
    attr3: 3
    >>> d.attr4.subattr1.subsubattr1 = {1, 2, 4}
    >>> d.attr5 = {"subattr"+str(i): i for i in range(3)}
    >>> print(d)
    attr0: 0
    attr1: 1
    attr2: 2
    attr3: 3
    attr4:
        - subattr1:
            - subsubattr1: {1, 2, 4}
    attr5:
        - subattr0: 0
        - subattr1: 1
        - subattr2: 2
    """
    def __init__(self, _dict=None, **kwargs):
        super(AttribDict, self).__init__()
        self.__dict__["_level"] = 0
        self.__dict__["_prefix"] = "_attr_"
        if _dict is not None:
            self._build_from_dict(_dict)
        if kwargs:
            self._build_from_dict(kwargs)

    def __setattr__(self, key, value):
        value = self.__class__(value) if isinstance(value, dict) else value
        self.__dict__[self._get_attr_name(key)] = value
        self._update()

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __getattr__(self, key):
        if not self._get_attr_name(key) in self.__dict__.keys():
            self.__dict__[self._get_attr_name(key)] = self.__class__()
            self._update()
        return self.__dict__[self._get_attr_name(key)]

    def hasattr(self, key):
        if self._get_attr_name(key) in self.__dict__.keys():
            return True
        else:
            return False

    def _update(self):
        _prefix = self.__dict__["_prefix"]
        _level = self.__dict__["_level"]
        for key, value in self.__dict__.items():
            if not _prefix in key:
                continue
            if isinstance(value, self.__class__):
                value.__dict__["_level"] = _level + 1
                value._update()

    def _build_from_dict(self, _dict: dict):
        for key, value in _dict.items():
            self.__setattr__(key, value)
        
    def _get_attr_name(self, name):
        return "{}{}".format(self._prefix, str(name))

    def __iter__(self):
        return iter(self.as_dict().items())

    def as_dict(self):
        """
        Return a python dict of self.
        """
        _dict = {}
        _prefix = self.__dict__["_prefix"]
        for key, value in self.__dict__.items():
            value = value.as_dict() if isinstance(value, self.__class__) else value
            if _prefix in key:
                _key = key.replace(_prefix, "")
                _dict[_key] = value
        return _dict

    def __copy__(self):
        _dict = self.__class__()
        _prefix = self.__dict__["_prefix"]
        for key, value in self.__dict__.items():
            if _prefix in key:
                key = key.replace(_prefix, "")
                _dict[key] = value
        return _dict

    def __deepcopy__(self, memo):
        other = self.__class__()
        _prefix = self.__dict__["_prefix"]
        for key, value in self.__dict__.items():
            if id(self) in memo:
                continue
            if _prefix in key:
                _key = key.replace(_prefix, "")
                other[copy.deepcopy(_key)] = copy.deepcopy(value, memo)
        memo[id(self)] = self
        return other

    def copy(self):
        """
        Return a shallow copy of self.
        """
        return self.__copy__()

    def deepcopy(self):
        """
        Return a deep copy of self.
        """
        return self.__deepcopy__({})

    def __str__(self):
        start = "-"
        string = []
        for key, value in self.__dict__.items():
            if not self._prefix in key:
                continue
            substring = "{}{} {}: {}{}".format(
                "\t"*self.__dict__["_level"], 
                start if self.__dict__["_level"] > 0 else "", 
                key.replace(self._prefix, ""), 
                "\n" if isinstance(value, self.__class__) else "", 
                str(value), 
            )
            string.append(substring)
        string = "\n".join(string)
        return string

