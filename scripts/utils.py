from typing import List


class YAMLSection:
    """Represents logical section in YAML file
    """
    OFFSET = '  '

    def __init__(self, obj: dict):
        self.obj = obj

    def to_lines(self) -> List[str]:
        lst = list()
        self._add_lines('', self.obj, '', lst)
        return lst

    def _add_lines(self, key_word: str, value: any, offset: str, builder: List[str]) -> None:
        if type(value) is str:
            builder.append(f'{offset}{key_word}: {value}')
        elif type(value) is list:
            builder.append(f'{offset}{key_word}:')
            for entry in value:
                builder.append(f'{offset}{self.OFFSET}- {entry}')
        elif type(value) is dict and key_word:
            builder.append(f'{offset}{key_word}:')
            for key in value.keys():
                self._add_lines(key_word=key, value=value.get(key), offset=offset + self.OFFSET, builder=builder)
        elif type(value) is dict:
            for key in value.keys():
                self._add_lines(key_word=key, value=value.get(key), offset=offset, builder=builder)


class YAML:
    """Represents logical section in YAML file
    """

    def __init__(self):
        self.sections_li = list()
        self.sections_map = dict()

    def to_string(self) -> str:
        ret = list()
        for stage in self.sections_li:
            ret.extend(YAMLSection(self.sections_map.get(stage)).to_lines())
            ret.append('')
        return '\n'.join(ret)

    def add(self, section_name: str, section: dict):
        self.sections_li.append(section_name)
        self.sections_map[section_name] = section

    def get(self, section_name: str) -> dict:
        return self.sections_map.get(section_name)
