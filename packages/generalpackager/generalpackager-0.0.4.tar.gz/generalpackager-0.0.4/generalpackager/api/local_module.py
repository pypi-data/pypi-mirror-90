
from generallibrary import ObjInfo


class LocalModule:
    """ Tools to interface a Local Python Module. """
    def __init__(self, module):
        self.module = module

        self.objInfo = ObjInfo(self.module)
        self.objInfo.filters = [self._filter]

        assert self.objInfo.is_module()
        self._generate_attributes()

    def _filter(self, objInfo):
        """ :param ObjInfo objInfo: """
        is_part_of_module = getattr(objInfo.module(), "__name__", "").startswith(self.module.__name__)
        return objInfo.public() and (objInfo.is_class() or objInfo.is_method()) and is_part_of_module

    def _generate_attributes(self):
        self.objInfo.get_attrs(depth=-1)



























