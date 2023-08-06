from random import choice
import re
from . import Arr


def __case(variable: str = '', operator: str = '') -> str:
    if ' ' in variable:
        variables = variable.split(' ')
        variable = ''.join(v.capitalize() for v in variables)

    return re.sub(r'(?<!^)(?=[A-Z])', operator, variable).lower()


def kebabcase(variable: str = '') -> str:
    return __case(variable, '-')


def camelcase(variable: str = '') -> str:
    word = pascalcase(variable)
    return word[0].lower() + word[1:]


def pascalcase(variable: str = '') -> str:
    regex = re.compile("[^A-Za-z]+")
    variable = regex.split(variable)
    wordsTitle = list(map(lambda x: x.title(), variable))
    return ''.join(wordsTitle)


def snakecase(variable: str = '') -> str:
    return __case(variable, '_')


def isStr(variable=None) -> bool:
    return isinstance(variable, str)


def isEmpty(variable: str = None) -> bool:
    if type(variable) == int:
        return False

    return False if variable is not None and len(variable) > 0 else True


def isAscii(variable=None) -> bool:
    try:
        variable.decode('ascii')
    except:
        return False
    else:
        return True


def limit(variable: str = '', length: int = None, placeholder='') -> str:
    length = length if length is not None else len(variable)
    return (variable[:length] + placeholder) if len(variable) > length else variable


def words(variable: str = '', length: int = None, placeholder='') -> str:
    word = variable.split(' ')
    length = length if length is not None else len(word)
    newWord = ' '.join(word[0:length])
    return newWord + placeholder


def random(length: int = 16) -> str:
    numberLetters = '0123456789'
    stringLetters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ln = 3 if length >= 3 else 1

    random_string = ''.join(list(map(lambda x: choice(stringLetters), range(ln))))
    random_string += ''.join(list(map(lambda x: choice(stringLetters + numberLetters), range(length - ln))))

    return random_string


def start(variable: str = '', check: str = None) -> str:
    if len(variable) > 0:
        variable = check + variable if variable[0] != check else variable

    return variable


class of:

    def __init__(self, variable: str = ''):
        self.__variable = variable

    def append(self, variable: str = ''):
        self.__variable += variable
        return self

    def prepend(self, variable: str = ''):
        self.__variable = variable + self.__variable
        return self

    def replace(self, v1: str = None, v2: str = None):
        self.__variable = self.__variable.replace(v1, v2)
        return self

    def replaceFirst(self, v1: str = None, v2: str = None):
        self.__variable = self.__variable.replace(v1, v2, 1)
        return self

    def __reversed(self):
        self.__variable = self.__variable[len(self.__variable)::-1]

    def replaceLast(self, v1: str = None, v2: str = None):
        self.__reversed()
        self.replaceFirst(v1, v2)
        self.__reversed()
        return self

    def replaceList(self, param: str = None, replaces: list = []):
        for x in replaces:
            self.replaceFirst(param, x)
        return self

    def replaceMatches(self, match: str = None, variable: str = None):
        regex = re.compile(match)
        variables = regex.split(self.__variable)
        variables = Arr.array_filter(variables)
        self.__variable = variable.join(variables)
        return self

    def after(self, param: str = None):
        if isEmpty(param):
            return self

        first = self.__variable.find(param)
        self.__variable = self.__variable[first+len(param):] if first != -1 else self.__variable
        return self

    def afterLast(self, param: str = None):
        if isEmpty(param):
            return self

        first = self.__variable.rfind(param)
        self.__variable = self.__variable[first+len(param):] if first != -1 else self.__variable
        return self

    def before(self, param: str = None):
        if isEmpty(param):
            return self

        first = self.__variable.find(param)
        self.__variable = self.__variable[:first] if first != -1 else self.__variable
        return self

    def beforeLast(self, param: str = None):
        if isEmpty(param):
            return self

        first = self.__variable.rfind(param)
        self.__variable = self.__variable[:first] if first != -1 else self.__variable
        return self

    def getValue(self) -> str:
        return self.__variable
