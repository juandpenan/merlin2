from pddl_dao.pddl_dto.pddl_dto_proposition import PDDL_DTO_Proposition


class PDDL_DTO_ConditionEffect(PDDL_DTO_Proposition):

    AT_START = "at start"
    AT_END = "at end"
    OVER_ALL = "over all"

    def __init__(self, time, pddl_predicate, pddl_objects_list=None, is_negative=False):
        self.set_time(time)
        self.set_is_negative(is_negative)
        super(PDDL_DTO_ConditionEffect, self).__init__(
            pddl_predicate, pddl_objects_list)

    def get_time(self):
        return self._time

    def set_time(self, time):
        self._time = time

    def get_is_negative(self):
        return self._is_negative

    def set_is_negative(self, is_negative):
        self._is_negative = is_negative

    def __str__(self):
        super_string = super(PDDL_DTO_ConditionEffect, self).__str__()
        string = "(" + self._time + " "
        if(self._is_negative):
            string += "(not "

        string += super_string

        string += ")"
        if(self._is_negative):
            string += ")"

        return string
