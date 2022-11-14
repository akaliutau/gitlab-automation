from typing import List


class YAMLSection:
    """Represents logical section in YAML file
    """
    OFFSET = '  '

    def __init__(self, obj: dict):
        self.obj = obj

    def to_lines(self) -> List[str]:
        lst = list()
        self.add_lines('', self.obj, '', lst)
        return lst

    def add_lines(self, key_word: str, value: any, offset: str, builder: List[str]) -> None:
        if type(value) is str:
            builder.append(f'{offset}{key_word}:{value}')
        elif type(value) is list:
            builder.append(f'{offset}{key_word}:')
            for entry in value:
                builder.append(f'{offset}{self.OFFSET}- {entry}')
        elif type(value) is dict:
            builder.append(f'{offset}{key_word}:')
            for key in value.keys():
                builder.append(f'{offset}{key}:')
                self.add_lines(key_word=key, value=value.get(key), offset=offset + self.OFFSET, builder=builder)


class YAML:
    """Represents logical section in YAML file
    """

    def __init__(self):
        pass
