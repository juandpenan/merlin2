import unittest
import coverage
from pddl_dao.pddl_dto.pddl_dto_type import PddlDtoType
from pddl_dao.pddl_dto.pddl_dto_predicate import PddlDtoPredicate
from pddl_dao.pddl_dto.pddl_dto_action import PddlDtoAction
from pddl_dao.pddl_dto.pddl_dto_object import PddlDtoObject
from pddl_dao.pddl_dto.pddl_dto_condition_efect import PddlDtoConditionEffect


class Test_PDDL_DTO_Action(unittest.TestCase):

    def setUp(self):

        self._robot_type = PddlDtoType("robot")
        self._wp_type = PddlDtoType("wp")
        self._robot_at = PddlDtoPredicate(
            "robot_at", [self._robot_type, self._wp_type])

        r = PddlDtoObject(self._robot_type, "r")
        s = PddlDtoObject(self._wp_type, "s")
        d = PddlDtoObject(self._wp_type, "d")

        self._condition_1 = PddlDtoConditionEffect(PddlDtoConditionEffect.AT_START,
                                                   self._robot_at,
                                                   [r, s])

        self._effect_1 = PddlDtoConditionEffect(PddlDtoConditionEffect.AT_START,
                                                self._robot_at,
                                                [r, s],
                                                is_negative=True)

        self._effect_2 = PddlDtoConditionEffect(PddlDtoConditionEffect.AT_END,
                                                self._robot_at,
                                                [r, d])

        self.pddl_dto_action = PddlDtoAction(
            "navigation", [r, s, d], [self._condition_1], [self._effect_1, self._effect_2])

    def test_pddl_dto_action_str(self):
        self.maxDiff = None
        self.pddl_dto_action.set_durative(False)
        self.assertEqual("""\
(:action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:precondition (
\t\t(at start (robot_at r s))
\t)
\t:effect (and
\t\t(at start (not (robot_at r s)))
\t\t(at end (robot_at r d))
\t)
)""",
                         str(self.pddl_dto_action))

    def test_pddl_dto_action_str_durative(self):
        self.maxDiff = None
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (
\t\t(at start (robot_at r s))
\t)
\t:effect (and
\t\t(at start (not (robot_at r s)))
\t\t(at end (robot_at r d))
\t)
)""",
                         str(self.pddl_dto_action))

    def test_pddl_dto_action_str_durative_no_effects(self):
        self.maxDiff = None
        self.pddl_dto_action.set_effects_list([])
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (
\t\t(at start (robot_at r s))
\t)
\t:effect (
\t)
)""",
                         str(self.pddl_dto_action))

    def test_pddl_dto_action_str_durative_no_conditions(self):
        self.maxDiff = None
        self.pddl_dto_action.set_conditions_list([])
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (
\t)
\t:effect (and
\t\t(at start (not (robot_at r s)))
\t\t(at end (robot_at r d))
\t)
)""",
                         str(self.pddl_dto_action))

    def test_pddl_dto_action_str_durative_no_parameters(self):
        self.maxDiff = None
        self.pddl_dto_action.set_conditions_list([])
        self.pddl_dto_action.set_effects_list([])
        self.pddl_dto_action.set_parameters_list([])
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ()
\t:duration (= ?duration 10)
\t:condition (
\t)
\t:effect (
\t)
)""",
                         str(self.pddl_dto_action))

    def test_pddl_dto_action_get_action_name(self):
        self.assertEqual("navigation", self.pddl_dto_action.get_action_name())

    def test_pddl_dto_action_get_prameters_list(self):
        params_list = self.pddl_dto_action.get_parameters_list()
        self.assertEqual("r - robot", str(params_list[0]))
        self.assertEqual("s - wp", str(params_list[1]))
        self.assertEqual("d - wp", str(params_list[2]))

    def test_pddl_dto_action_get_conditions_list(self):
        conditions_list = self.pddl_dto_action.get_conditions_list()
        self.assertEqual("(at start (robot_at r s))", str(conditions_list[0]))

    def test_pddl_dto_action_get_effects_list(self):
        effects_list = self.pddl_dto_action.get_effects_list()
        self.assertEqual("(at start (not (robot_at r s)))",
                         str(effects_list[0]))
        self.assertEqual("(at end (robot_at r d))",
                         str(effects_list[1]))

    def test_pddl_dto_action_get_durative(self):
        self.assertTrue(self.pddl_dto_action.get_durative())

    def test_pddl_dto_action_get_duration(self):
        self.assertEqual(10, self.pddl_dto_action.get_duration())
