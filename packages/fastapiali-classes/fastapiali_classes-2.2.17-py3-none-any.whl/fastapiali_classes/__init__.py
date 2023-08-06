class WrapperException(Exception):

    def __init__(self, msg: str, orginal_exception: Exception):
        super().__init__(msg)
        self._msg = msg
        self.original_exception = orginal_exception

    def __str__(self):
        return '{}\nOrigine: {}'.format(super().__str__(), str(self.original_exception))

    @property
    def msg(self):
        return self._msg

    def get_ancestor_exception(self):
        try:
            return self.original_exception.get_ancestor_exception()
        except AttributeError:
            return self.original_exception


class RecordException(Exception):

    def __init__(self, msg: str, record):
        super().__init__(msg)
        self._msg = msg
        self.record = record

    def __str__(self):
        return '{parent_ex}\nRecord: {rcd}, {rcd_class}:{rcd_dict}'.format(
            parent_ex=super().__str__(), rcd=str(self.record), rcd_class=getattr(self.record, "__class__", None),
            rcd_dict=getattr(self.record, "__dict__", None))

    @property
    def msg(self):
        return self._msg
