
from typing import List

from pddl_dao.pddl_dao_interface.pddl_dao_predicate import PDDL_DAO_Predicate
from pddl_dao.mongoengine_pddl_dao.mongoengine_pddl_dao import Mongoengine_PDDL_DAO

from pddl_dao.mongoengine_pddl_dao.pddl_mongoengine_models import pddl_predicate as pddl_mongoengine_predicate_model

from pddl_dao.pddl_dto.pddl_dto_predicate import PDDL_DTO_Predicate
from pddl_dao.pddl_dto.pddl_dto_type import PDDL_DTO_Type

from pddl_dao.mongoengine_pddl_dao.mongoengine_pddl_dao_type import Mongoengine_PDDL_DAO_Type


class Mongoengine_PDDL_DAO_Predicate(PDDL_DAO_Predicate, Mongoengine_PDDL_DAO):

    def __init__(self, uri: str = None):

        PDDL_DAO_Predicate.__init__(self)
        Mongoengine_PDDL_DAO.__init__(self, uri)

        self._mongoengine_pddl_dao_type = Mongoengine_PDDL_DAO_Type(uri)

    def _mongoengine_to_dto(self, pddl_mongoengine_predicate: pddl_mongoengine_predicate_model) -> PDDL_DTO_Predicate:

        pddl_dto_type_list = []

        for pddl_type in pddl_mongoengine_predicate.pddl_types:
            pddl_dto_type = PDDL_DTO_Type(pddl_type.type_name)
            pddl_dto_type_list.append(pddl_dto_type)

        pddl_dto_predicate = PDDL_DTO_Predicate(
            pddl_mongoengine_predicate.predicate_name, pddl_dto_type_list)

        return pddl_dto_predicate

    def _dto_to_mongoengine(self, pddl_dto_predicate: PDDL_DTO_Predicate) -> pddl_mongoengine_predicate_model:

        pddl_mongoengine_predicate = pddl_mongoengine_predicate_model()

        pddl_mongoengine_predicate.predicate_name = pddl_dto_predicate.get_predicate_name()

        for pddl_dto_type in pddl_dto_predicate.get_pddl_types_list():

            pddl_mongoengine_type = self._mongoengine_pddl_dao_type._get_mongoengine(
                pddl_dto_type)

            # check if type exist
            if(not pddl_mongoengine_type):
                return None

            pddl_mongoengine_predicate.pddl_types.append(pddl_mongoengine_type)

        return pddl_mongoengine_predicate

    def _exist_in_mongo(self, pddl_dto_predicate: PDDL_DTO_Predicate) -> bool:

        if(self._get_mongoengine(pddl_dto_predicate)):
            return True
        return False

    def _get_mongoengine(self, pddl_dto_predicate: PDDL_DTO_Predicate) -> pddl_mongoengine_predicate_model:

        pddl_mongoengine_predicate = pddl_mongoengine_predicate_model.objects(
            predicate_name=pddl_dto_predicate.get_predicate_name())

        if(not pddl_mongoengine_predicate):
            return None

        return pddl_mongoengine_predicate[0]

    def get(self, predicate_name: str) -> PDDL_DTO_Predicate:

        pddl_mongoengine_predicate = pddl_mongoengine_predicate_model.objects(
            predicate_name=predicate_name)

        # check if predicate exist
        if(pddl_mongoengine_predicate):
            pddl_mongoengine_predicate = pddl_mongoengine_predicate[0]
            pddl_dto_predicate = self._mongoengine_to_dto(
                pddl_mongoengine_predicate)
            return pddl_dto_predicate

        else:
            return None

    def get_all(self) -> List[PDDL_DTO_Predicate]:

        pddl_mongoengine_predicate = pddl_mongoengine_predicate_model.objects
        pddl_dto_predicate_list = []

        for ele in pddl_mongoengine_predicate:
            pddl_dto_predicate = self._mongoengine_to_dto(ele)
            pddl_dto_predicate_list.append(pddl_dto_predicate)

        return pddl_dto_predicate_list

    def _save(self, pddl_dto_predicate: PDDL_DTO_Predicate) -> bool:

        if(self._exist_in_mongo(pddl_dto_predicate)):
            return False

        # propagating saving
        for pddl_dto_type in pddl_dto_predicate.get_pddl_types_list():
            result = self._mongoengine_pddl_dao_type.save(pddl_dto_type)
            if(not result):
                return False

        pddl_mongoengine_predicate = self._dto_to_mongoengine(
            pddl_dto_predicate)

        if(pddl_mongoengine_predicate):
            pddl_mongoengine_predicate.save()
            return True

        else:
            return False

    def _update(self, pddl_dto_predicate: PDDL_DTO_Predicate) -> bool:

        pddl_mongoengine_predicate = self._get_mongoengine(pddl_dto_predicate)

        # check if predicate exists
        if(pddl_mongoengine_predicate):
            new_pddl_predicate_mongoengine = self._dto_to_mongoengine(
                pddl_dto_predicate)

            if(new_pddl_predicate_mongoengine):
                pddl_mongoengine_predicate.predicate_name = new_pddl_predicate_mongoengine.predicate_name
                pddl_mongoengine_predicate.pddl_types = new_pddl_predicate_mongoengine.pddl_types
                pddl_mongoengine_predicate.save()
            else:
                return False

            return True

        else:
            return False

    def save(self, pddl_dto_predicate: PDDL_DTO_Predicate) -> bool:

        if(self._exist_in_mongo(pddl_dto_predicate)):
            return self._update(pddl_dto_predicate)

        else:
            return self._save(pddl_dto_predicate)

    def delete(self, pddl_dto_predicate: PDDL_DTO_Predicate) -> bool:

        pddl_mongoengine_predicate = self._get_mongoengine(pddl_dto_predicate)

        # check if predicate exists
        if(pddl_mongoengine_predicate):
            pddl_mongoengine_predicate.delete()
            return True

    def delete_all(self) -> bool:

        pddl_dto_predicate_list = self.get_all()

        for ele in pddl_dto_predicate_list:
            self.delete(ele)

        return True
