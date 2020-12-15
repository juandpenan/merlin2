
""" DAO Example Node """

import rclpy

from pddl_dao.pddl_dao_factory import (
    PddlDaoFactoryFactory,
    PddlDaoFamilies
)

from pddl_dto import (
    PddlTypeDto,
    PddlObjectDto,
    PddlPredicateDto,
    PddlPropositionDto,
    PddlConditionEffectDto,
    PddlActionDto
)

from threaded_node.node import Node


class DaoExampleNode(Node):
    """ DAO Example Node Class """

    def __init__(self):

        super().__init__("dao_example_node")

        pddl_dao_factory_factory = PddlDaoFactoryFactory()

        uri = "mongodb://localhost:27017/merlin2"
        pddl_dao_family = PddlDaoFamilies.MONGOENGINE

        pddl_dao_factory = pddl_dao_factory_factory.create_pddl_dao_factory(pddl_dao_family,
                                                                            uri=uri,
                                                                            node=self)

        # creating DAOs
        pddl_type_dao = pddl_dao_factory.create_pddl_type_dao()
        pddl_object_dao = pddl_dao_factory.create_pddl_object_dao()
        pddl_predicate_dao = pddl_dao_factory.create_pddl_predicate_dao()
        pddl_proposition_dao = pddl_dao_factory.create_pddl_proposition_dao()
        pddl_action_dao = pddl_dao_factory.create_pddl_action_dao()

        # types
        robot_type = PddlTypeDto("robot")
        wp_type = PddlTypeDto("wp")

        # predicates
        robot_at = PddlPredicateDto(
            "robot_at", [robot_type, wp_type])

        # objects
        rb1 = PddlObjectDto(robot_type, "rb1")
        wp1 = PddlObjectDto(wp_type, "wp1")
        wp2 = PddlObjectDto(wp_type, "wp2")

        # propositions
        pddl_proposition_dto = PddlPropositionDto(robot_at, [rb1, wp1])
        pddl_goal_dto = PddlPropositionDto(robot_at, [rb1, wp2], is_goal=True)

        # actions
        r = PddlObjectDto(robot_type, "r")
        s = PddlObjectDto(wp_type, "s")
        d = PddlObjectDto(wp_type, "d")

        condition_1 = PddlConditionEffectDto(robot_at,
                                             [r, s],
                                             time=PddlConditionEffectDto.AT_START)

        effect_1 = PddlConditionEffectDto(robot_at,
                                          [r, s],
                                          time=PddlConditionEffectDto.AT_START,
                                          is_negative=True)

        effect_2 = PddlConditionEffectDto(robot_at,
                                          [r, d],
                                          time=PddlConditionEffectDto.AT_END)

        pddl_action_dto = PddlActionDto(
            "navigation", [r, s, d], [condition_1], [effect_1, effect_2])

        # saving all
        pddl_object_dao.save(rb1)
        pddl_object_dao.save(wp1)
        pddl_object_dao.save(wp2)

        pddl_proposition_dao.save(pddl_proposition_dto)
        pddl_proposition_dao.save(pddl_goal_dto)

        pddl_action_dao.save(pddl_action_dto)


def main(args=None):
    rclpy.init(args=args)

    node = DaoExampleNode()

    # node.join_spin()

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
