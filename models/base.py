from typing import get_type_hints


class BaseModel:
    # Базовая модель

    def create(self, src: dict):
        #  Сериализатор модели
        if hasattr(self, 'src'):
            src = self.src
        self_typing = get_type_hints(self)
        for k, v in src.items():
            if k in self_typing:
                if isinstance(v, dict):
                    attr = self_typing[k].__new__(self_typing[k])
                    attr.create(v)
                    self.__setattr__(k, attr)
                elif type(v) == self_typing[k]:
                    attr = v
                    self.__setattr__(k, attr)

        self_typing = get_type_hints(self)
        for k, v in self_typing.items():
            if not hasattr(self, k):
                setattr(self, k, None)
