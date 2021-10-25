
import unittest
import time
import rclpy

from simple_node import Node

from merlin2_arch_interfaces.msg import PlanAction
from merlin2_arch_interfaces.action import DispatchAction

from merlin2_basic_actions.merlin2_navigation_action import Merlin2NavigationAction


class FakeNavigationAction(Merlin2NavigationAction):
    def __init__(self):
        super().__init__()
        self.cancel = False

    def run_action(self, goal: PlanAction) -> bool:
        self.cancel = False
        counter = 0
        while not self.cancel and counter < 5:
            time.sleep(1)
            counter += 1

        if self.cancel:
            return False

        return True

    def cancel_action(self):
        self.cancel = True


class ClientNode(Node):
    def __init__(self):
        super().__init__("client_node", namespace="merlin2")

        self.action_client = self.create_action_client(
            DispatchAction, "navigation")

    def call_action(self):

        goal = DispatchAction.Goal()

        nav_action = PlanAction()
        nav_action.action_name = "navigation"
        nav_action.objects = ["wp1", "wp2"]

        goal.action = nav_action

        self.action_client.wait_for_server()
        self.action_client.send_goal(goal)

    def wait_action(self):
        self.action_client.wait_for_result()

    def cancel_action(self):
        while not self.action_client.is_working():
            time.sleep(1)

        return self.action_client.cancel_goal()

    def is_succeeded(self):
        return self.action_client.is_succeeded()

    def is_canceled(self):
        return self.action_client.is_canceled()


class TestMerlin2Action(unittest.TestCase):

    def setUp(self):
        rclpy.init()

        self.fake_action = FakeNavigationAction()
        self.client_node = ClientNode()

        super().setUp()

    def tearDown(self):
        super().tearDown()
        rclpy.shutdown()

    def test_action(self):

        self.client_node.call_action()
        self.client_node.wait_action()
        self.assertTrue(self.client_node.is_succeeded())

    def test_action_canceled(self):

        self.client_node.call_action()
        self.assertTrue(self.client_node.cancel_action())
        self.client_node.wait_action()
        self.assertTrue(self.client_node.is_canceled())
