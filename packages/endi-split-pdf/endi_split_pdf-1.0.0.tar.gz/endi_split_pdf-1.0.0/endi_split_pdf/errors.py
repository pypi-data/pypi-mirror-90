class AutosplitError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        if not hasattr(self, 'message'):
            self.message = "Default message"


class Incoherence(AutosplitError):
    pass


class ParseError(AutosplitError):
    pass
