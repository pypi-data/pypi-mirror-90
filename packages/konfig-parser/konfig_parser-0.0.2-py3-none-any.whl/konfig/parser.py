from yaml import load, Loader


class ParserDict(dict):
    def __init__(self, configuration):
        super(ParserDict, self).__init__(configuration)

        if isinstance(configuration, dict):
            for key, value in configuration.items():
                if not isinstance(value, dict):
                    self[key] = value
                else:
                    self.__setattr__(key, ParserDict(value))

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(ParserDict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(ParserDict, self).__delitem__(key)
        del self.__dict__[key]


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__(message)


class ConfParser(object):
    def __init__(self, path=None, conf_dict=None):
        self.config = None

        if not path and not conf_dict:
            raise ParserException("Either path or conf_dict must be present")
        elif path and conf_dict:
            raise ParserException("Only pass path or conf_dict")

        if path:
            self.load_from_path(path)
        elif conf_dict:
            if not isinstance(conf_dict, dict):
                raise ParserException("conf_dict must be of type 'dict'")

    def load_from_path(self, path):
        try:
            with open(path, "r") as fp:
                self.config = load(stream=fp, Loader=Loader)
        except IOError:
            raise ParserException(f"Error reading file: {path}")

    def to_obj(self):
        return ParserDict(configuration=self.config)
