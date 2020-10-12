
from pddl_dao.pddl_dto.pddl_dto import PDDL_DTO


class PDDL_DTO_Type:

    def __init__(self, type_name: str):

        self.set_type_name(type_name)

        PDDL_DTO.__init__(self)

    def get_type_name(self) -> str:
        return self._type_name

    def set_type_name(self, type_name: str):
        self._type_name = type_name

    def __str__(self):
        return self._type_name
