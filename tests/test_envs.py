'''Unit tests for all of the envs'''

import numpy as np
import unittest

from social_dilemmas.envs.harvest import HarvestEnv
from social_dilemmas.envs.agent import HarvestAgent
from social_dilemmas.envs.cleanup import CleanupEnv
from social_dilemmas.envs.agent import CleanupAgent

MINI_HARVEST_MAP = [
    '@@@@@@',
    '@ P  @',
    '@  AA@',
    '@  AA@',
    '@  AP@',
    '@@@@@@',
]

MINI_CLEANUP_MAP = [
    '@@@@@@',
    '@ P  @',
    '@H BB@',
    '@R BB@',
    '@S BP@',
    '@@@@@@',
]

# maps used to test different spawn positions and apple positions

# basic empty map with walls
BASE_MAP_1 = [
    '@@@@@@@',
    '@     @',
    '@     @',
    '@     @',
    '@     @',
    '@     @',
    '@@@@@@@'
]
TEST_MAP_1 = np.array(
    [['@'] * 7,
     ['@'] + [' '] * 5 + ['@'],
     ['@'] + [' '] * 5 + ['@'],
     ['@'] + [' '] * 5 + ['@'],
     ['@'] + [' '] * 5 + ['@'],
     ['@'] + [' '] * 5 + ['@'],
     ['@'] * 7]
)

# basic empty map with 1 starting apple
BASE_MAP_2 = [
    '@@@@@@',
    '@    @',
    '@    @',
    '@    @',
    '@  A @',
    '@@@@@@'
]
TEST_MAP_2 = np.array(
    [['@'] * 6,
     ['@'] + [' '] * 4 + ['@'],
     ['@'] + [' '] * 4 + ['@'],
     ['@'] + [' '] * 4 + ['@'],
     ['@'] + [' '] * 2 + ['A'] + [' '] + ['@'],
     ['@'] * 6]
)


class TestHarvestEnv(unittest.TestCase):

    def tearDown(self):
        """Remove the env"""
        self.env = None

    def test_step(self):
        """Just check that the step method works at all for all possible actions"""
        self.env = HarvestEnv(ascii_map=MINI_HARVEST_MAP, num_agents=1)
        self.env.reset()
        # FIXME(ev) magic number
        for i in range(8):
            self.env.step({'agent-0': i})

    def test_reset(self):
        self.env = HarvestEnv(ascii_map=MINI_HARVEST_MAP, num_agents=0)
        self.env.reset()
        # check that the map is full of apples
        test_map = np.array([['@', '@', '@', '@', '@', '@'],
                             ['@', ' ', ' ', ' ', ' ', '@'],
                             ['@', ' ', ' ', 'A', 'A', '@'],
                             ['@', ' ', ' ', 'A', 'A', '@'],
                             ['@', ' ', ' ', 'A', ' ', '@'],
                             ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(self.env.map, test_map)

    def test_walls(self):
        """Check that the spawned map and base map have walls in the right place"""
        self.env = HarvestEnv(BASE_MAP_1, num_agents=0)
        self.env.reset()
        np.testing.assert_array_equal(self.env.base_map[0, :], np.array(['@'] * 7))
        np.testing.assert_array_equal(self.env.base_map[-1, :], np.array(['@'] * 7))
        np.testing.assert_array_equal(self.env.base_map[:, 0], np.array(['@'] * 7))
        np.testing.assert_array_equal(self.env.base_map[:, -1], np.array(['@'] * 7))

        np.testing.assert_array_equal(self.env.map[0, :], np.array(['@'] * 7))
        np.testing.assert_array_equal(self.env.map[-1, :], np.array(['@'] * 7))
        np.testing.assert_array_equal(self.env.map[:, 0], np.array(['@'] * 7))
        np.testing.assert_array_equal(self.env.map[:, -1], np.array(['@'] * 7))

    def test_view(self):
        """Confirm that an agent placed at the right point returns the right view"""
        agent_id = 'agent-0'
        self.construct_map(TEST_MAP_1, agent_id, [3, 3], 'UP')

        # check if the view is correct if there are no walls
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[' '] * 5,
             [' '] * 5,
             [' '] * 2 + ['P'] + [' '] * 2,
             [' '] * 5,
             [' '] * 5]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if the view is correct if the top wall is just in view
        self.move_agent(agent_id, [2, 3])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [['@'] * 5,
             [' '] * 5,
             [' '] * 2 + ['P'] + [' '] * 2,
             [' '] * 5,
             [' '] * 5]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if if the view is correct if the view exceeds the top view
        self.move_agent(agent_id, [1, 3])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[''] * 5,
             ['@'] * 5,
             [' '] * 2 + ['P'] + [' '] * 2,
             [' '] * 5,
             [' '] * 5]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if the view is correct if the left wall is just in view
        self.move_agent(agent_id, [3, 2])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [['@'] + [' '] * 4,
             ['@'] + [' '] * 4,
             ['@'] + [' '] + ['P'] + [' '] * 2,
             ['@'] + [' '] * 4,
             ['@'] + [' '] * 4]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if if the view is correct if the view exceeds the left view
        self.move_agent(agent_id, [3, 1])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[''] + ['@'] + [' '] * 3,
             [''] + ['@'] + [' '] * 3,
             [''] + ['@'] + ['P'] + [' '] * 2,
             [''] + ['@'] + [' '] * 3,
             [''] + ['@'] + [' '] * 3]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if the view is correct if the bot wall is just in view
        self.move_agent(agent_id, [4, 3])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[' '] * 5,
             [' '] * 5,
             [' '] * 2 + ['P'] + [' '] * 2,
             [' '] * 5,
             ['@'] * 5]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if if the view is correct if the view exceeds the bot view
        self.move_agent(agent_id, [5, 3])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[' '] * 5,
             [' '] * 5,
             [' '] * 2 + ['P'] + [' '] * 2,
             ['@'] * 5,
             [''] * 5]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if the view is correct if the right wall is just in view
        self.move_agent(agent_id, [3, 4])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[' '] * 4 + ['@'],
             [' '] * 4 + ['@'],
             [' '] * 2 + ['P'] + [' '] + ['@'],
             [' '] * 4 + ['@'],
             [' '] * 4 + ['@']]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if if the view is correct if the view exceeds the right view
        self.move_agent(agent_id, [3, 5])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[' '] * 3 + ['@'] + [''],
             [' '] * 3 + ['@'] + [''],
             [' '] * 2 + ['P'] + ['@'] + [''],
             [' '] * 3 + ['@'] + [''],
             [' '] * 3 + ['@'] + ['']]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        # check if if the view is correct if the agent is in the bottom right corner
        self.move_agent(agent_id, [5, 5])
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [[' '] * 3 + ['@'] + [''],
             [' '] * 3 + ['@'] + [''],
             [' '] * 2 + ['P'] + ['@'] + [''],
             ['@'] * 4 + [''],
             [''] * 5]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

    def test_apple_spawn(self):
        # render apples a bunch of times and check that the probabilities are within
        # a bound of what you expect. This test fill fail w/ <INSERT> probability
        self.env = HarvestEnv(MINI_HARVEST_MAP, num_agents=0)
        self.env.reset()
        self.env.map = TEST_MAP_2.copy()

        # First test, if we step 300 times, are there five apples there?
        # This should fail maybe one in 1000000 times
        for i in range(300):
            self.env.step({})
        num_apples = self.env.count_apples(self.env.map)
        self.assertEqual(num_apples, 5)

        # Now, if a point is temporarily obscured by a beam but an apple should spawn there
        # check that the apple still spawns there
        self.env = HarvestEnv(ascii_map=MINI_HARVEST_MAP, num_agents=2)
        self.env.reset()

        # test that agents can't walk into other agents
        self.move_agent('agent-0', [3, 1])
        self.move_agent('agent-1', [3, 3])
        self.env.agents['agent-0'].update_map_agent_rot('UP')
        self.env.agents['agent-1'].update_map_agent_rot('UP')
        # test that an apple can spawn where a beam currently is
        self.env.update_custom_moves({'agent-1': 'FIRE'})
        self.env.execute_reservations()
        self.env.update_map_apples([[3, 2]])
        self.env.clean_map()
        expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                 ['@', ' ', ' ', ' ', ' ', '@'],
                                 ['@', ' ', ' ', 'A', 'A', '@'],
                                 ['@', 'P', 'A', 'P', 'A', '@'],
                                 ['@', ' ', ' ', 'A', ' ', '@'],
                                 ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(expected_map, self.env.map)

        # If an agent is temporarily obscured by a beam, and an apple attempts to spawn there
        # no apple should spawn
        self.env.update_custom_moves({'agent-1': 'FIRE'})
        self.env.execute_reservations()
        self.env.update_map_apples([[3, 1]])
        self.env.clean_map()

        expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                 ['@', ' ', ' ', ' ', ' ', '@'],
                                 ['@', ' ', ' ', 'A', 'A', '@'],
                                 ['@', 'P', 'A', 'P', 'A', '@'],
                                 ['@', ' ', ' ', 'A', ' ', '@'],
                                 ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(expected_map, self.env.map)

    def test_agent_actions(self):
        # set up the map
        agent_id = 'agent-0'
        self.construct_map(TEST_MAP_1.copy(), agent_id, [2, 2], 'LEFT')

        # Test that all the moves and rotations work correctly
        # test when facing left
        self.env.update_moves({agent_id: 'MOVE_LEFT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 3])
        self.env.update_moves({agent_id: 'MOVE_RIGHT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        self.env.update_moves({agent_id: 'MOVE_UP'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [1, 2])
        self.env.update_moves({agent_id: 'MOVE_DOWN'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        # test when facing up
        self.rotate_agent(agent_id, 'UP')
        self.env.update_moves({agent_id: 'MOVE_LEFT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [1, 2])
        self.env.update_moves({agent_id: 'MOVE_RIGHT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        self.env.update_moves({agent_id: 'MOVE_UP'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 1])
        self.env.update_moves({agent_id: 'MOVE_DOWN'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        # test when facing down
        self.rotate_agent(agent_id, 'DOWN')
        self.env.update_moves({agent_id: 'MOVE_LEFT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [3, 2])
        self.env.update_moves({agent_id: 'MOVE_RIGHT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        self.env.update_moves({agent_id: 'MOVE_UP'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 3])
        self.env.update_moves({agent_id: 'MOVE_DOWN'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        # test when facing right
        self.rotate_agent(agent_id, 'RIGHT')
        self.env.update_moves({agent_id: 'MOVE_LEFT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 1])
        self.env.update_moves({agent_id: 'MOVE_RIGHT'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        self.env.update_moves({agent_id: 'MOVE_UP'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [3, 2])
        self.env.update_moves({agent_id: 'MOVE_DOWN'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])

        # check that stay works properly
        self.env.update_moves({agent_id: 'STAY'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])
        self.assertEqual(self.env.map[2, 2], 'P')

        # quick test of stay
        self.env.update_moves({agent_id: 'STAY'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 2])

        # if an agent tries to move through a wall they should stay in the same place
        self.rotate_agent(agent_id, 'UP')
        self.move_agent(agent_id, [2, 1])
        self.env.update_moves({agent_id: 'MOVE_UP'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents[agent_id].get_pos(), [2, 1])

        # rotations correctly update the agent state
        self.rotate_agent(agent_id, 'UP')
        # clockwise
        self.env.update_moves({agent_id: 'TURN_CLOCKWISE'})
        self.assertEqual('RIGHT', self.env.agents[agent_id].get_orientation())
        self.env.update_moves({agent_id: 'TURN_CLOCKWISE'})
        self.assertEqual('DOWN', self.env.agents[agent_id].get_orientation())
        self.env.update_moves({agent_id: 'TURN_CLOCKWISE'})
        self.assertEqual('LEFT', self.env.agents[agent_id].get_orientation())
        self.env.update_moves({agent_id: 'TURN_CLOCKWISE'})
        self.assertEqual('UP', self.env.agents[agent_id].get_orientation())

        # counterclockwise
        self.env.update_moves({agent_id: 'TURN_COUNTERCLOCKWISE'})
        self.assertEqual('LEFT', self.env.agents[agent_id].get_orientation())
        self.env.update_moves({agent_id: 'TURN_COUNTERCLOCKWISE'})
        self.assertEqual('DOWN', self.env.agents[agent_id].get_orientation())
        self.env.update_moves({agent_id: 'TURN_COUNTERCLOCKWISE'})
        self.assertEqual('RIGHT', self.env.agents[agent_id].get_orientation())
        self.env.update_moves({agent_id: 'TURN_COUNTERCLOCKWISE'})
        self.assertEqual('UP', self.env.agents[agent_id].get_orientation())

        # test firing
        self.rotate_agent(agent_id, 'UP')
        self.move_agent(agent_id, [3, 2])
        self.env.update_custom_moves({agent_id: 'FIRE'})
        self.env.execute_reservations()
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [['@'] + [' '] * 4,
             ['@'] + ['F'] * 2 + [' '] * 2,
             ['@'] + ['F'] + ['P'] + [' '] * 2,
             ['@'] + ['F'] * 2 + [' '] * 2,
             ['@'] + [' '] * 4]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        self.env.clean_map()

        self.rotate_agent(agent_id, 'DOWN')
        self.move_agent(agent_id, [3, 2])
        self.env.update_custom_moves({agent_id: 'FIRE'})
        self.env.execute_reservations()
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [['@'] + [' '] * 4,
             ['@'] + [' '] + ['F'] * 3,
             ['@'] + [' '] + ['P'] + ['F'] * 2,
             ['@'] + [' '] + ['F'] * 3,
             ['@'] + [' '] * 4]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

        self.construct_map(MINI_HARVEST_MAP.copy(), agent_id, [3, 2], 'RIGHT')
        self.env.update_map_apples(self.env.apple_points)
        self.env.execute_reservations()
        self.env.update_moves({agent_id: 'MOVE_RIGHT'})
        self.env.execute_reservations()
        self.env.update_moves({agent_id: 'MOVE_LEFT'})
        self.env.execute_reservations()
        agent_view = self.env.agents[agent_id].get_state()
        expected_view = np.array(
            [['@', ' ', ' ', ' ', ' '],
             ['@', ' ', ' ', 'A', 'A'],
             ['@', ' ', 'P', ' ', 'A'],
             ['@', ' ', ' ', 'A', ' '],
             ['@', '@', '@', '@', '@']]
        )
        np.testing.assert_array_equal(expected_view, agent_view)

    def test_agent_rewards(self):
        self.env = HarvestEnv(ascii_map=MINI_HARVEST_MAP, num_agents=2)
        self.env.reset()
        self.move_agent('agent-0', [2, 2])
        self.move_agent('agent-1', [3, 2])
        self.env.agents['agent-0'].update_map_agent_rot('UP')
        self.env.agents['agent-1'].update_map_agent_rot('UP')
        # walk over an apple
        self.env.update_moves({'agent-0': 'MOVE_DOWN',
                               'agent-1': 'MOVE_DOWN'})
        self.env.execute_reservations()
        reward_0 = self.env.agents['agent-0'].compute_reward()
        reward_1 = self.env.agents['agent-1'].compute_reward()
        self.assertTrue(reward_0 == 1)
        self.assertTrue(reward_1 == 1)
        # fire a beam from agent 1 to 2
        self.env.agents['agent-1'].update_map_agent_rot('LEFT')
        self.env.update_custom_moves({'agent-1': 'FIRE'})
        self.env.execute_reservations()
        reward_0 = self.env.agents['agent-0'].compute_reward()
        reward_1 = self.env.agents['agent-1'].compute_reward()
        self.assertTrue(reward_0 == -50)
        self.assertTrue(reward_1 == -1)

    def test_agent_conflict(self):
        '''Test that agent conflicts are correctly resolved'''

        # test that if there are two agents and two spawning points, they hit both of them
        self.env = HarvestEnv(ascii_map=MINI_HARVEST_MAP, num_agents=2)
        self.env.reset()
        np.testing.assert_array_equal(self.env.base_map, self.env.map)

        # test that agents can't walk into other agents
        self.env.reserved_slots.append([3, 3, 'P', 'agent-0'])
        self.env.reserved_slots.append([3, 4, 'P', 'agent-1'])
        self.env.agents['agent-0'].update_map_agent_rot('UP')
        self.env.agents['agent-1'].update_map_agent_rot('UP')
        self.env.execute_reservations()
        self.env.update_moves({'agent-0': 'MOVE_DOWN'})
        self.env.execute_reservations()
        self.env.update_moves({'agent-1': 'MOVE_UP'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents['agent-0'].get_pos(), [3, 3])
        np.testing.assert_array_equal(self.env.agents['agent-1'].get_pos(), [3, 4])

        # test that agents can't walk through each other
        self.env.update_moves({'agent-0': 'MOVE_DOWN', 'agent-1': 'MOVE_UP'})
        self.env.execute_reservations()
        np.testing.assert_array_equal(self.env.agents['agent-0'].get_pos(), [3, 3])
        np.testing.assert_array_equal(self.env.agents['agent-1'].get_pos(), [3, 4])

        # test that if an agents firing beam hits another agent it gets covered
        self.env.update_moves({'agent-0': 'MOVE_UP'})
        self.env.execute_reservations()
        self.env.clean_map()
        self.env.update_custom_moves({'agent-1': 'FIRE'})
        self.env.execute_reservations()
        expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                 ['@', ' ', ' ', ' ', ' ', '@'],
                                 ['@', 'F', 'F', 'F', 'F', '@'],
                                 ['@', 'F', 'F', 'F', 'P', '@'],
                                 ['@', 'F', 'F', 'F', 'F', '@'],
                                 ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(expected_map, self.env.map)
        # but by the next step, the agent is visible again
        self.env.clean_map()
        self.env.execute_reservations()
        expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                 ['@', ' ', ' ', ' ', ' ', '@'],
                                 ['@', ' ', ' ', 'A', 'A', '@'],
                                 ['@', ' ', 'P', ' ', 'P', '@'],
                                 ['@', ' ', ' ', 'A', ' ', '@'],
                                 ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(expected_map, self.env.map)

        # test that if two agents fire on each other than they're still there after
        self.env.agents['agent-0'].update_map_agent_rot('DOWN')
        self.env.update_custom_moves({'agent-0': 'FIRE', 'agent-1': 'FIRE'})
        self.env.execute_reservations()
        self.env.clean_map()
        expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                 ['@', ' ', ' ', ' ', ' ', '@'],
                                 ['@', ' ', ' ', 'A', 'A', '@'],
                                 ['@', ' ', 'P', ' ', 'P', '@'],
                                 ['@', ' ', ' ', 'A', ' ', '@'],
                                 ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(expected_map, self.env.map)

        # test that agents can walk into other agents if moves are de-conflicting
        # this only occurs stochastically so try it 50 times
        # TODO(ev) make this not stochastic
        self.env.agents['agent-0'].update_map_agent_rot('UP')
        self.env.update_moves({'agent-0': 'MOVE_DOWN'})
        for i in range(100):
            np.random.seed(i)
            self.env.execute_reservations()
            self.env.update_moves({'agent-0': 'MOVE_DOWN', 'agent-1': 'MOVE_LEFT'})
            self.env.execute_reservations()
            expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                     ['@', ' ', ' ', ' ', ' ', '@'],
                                     ['@', ' ', ' ', 'A', 'P', '@'],
                                     ['@', ' ', ' ', ' ', 'P', '@'],
                                     ['@', ' ', ' ', 'A', ' ', '@'],
                                     ['@', '@', '@', '@', '@', '@']])
            np.testing.assert_array_equal(expected_map, self.env.map)
            self.env.update_moves({'agent-0': 'MOVE_UP', 'agent-1': 'MOVE_RIGHT'})
            self.env.execute_reservations()

        # test that if two agents have a conflicting move then the tie is broken randomly
        num_agent_1 = 0.0
        num_agent_2 = 0.0
        for i in range(5000):
            self.env.reserved_slots.append([3, 2, 'P', 'agent-0'])
            self.env.reserved_slots.append([3, 4, 'P', 'agent-1'])
            self.env.execute_reservations()
            self.env.update_moves({'agent-0': 'MOVE_DOWN', 'agent-1': 'MOVE_UP'})
            self.env.execute_reservations()
            if self.env.agents['agent-0'].get_pos().tolist() == [3, 3]:
                num_agent_1 += 1
            else:
                num_agent_2 += 1
        agent_1_percent = num_agent_1 / (num_agent_1 + num_agent_2)
        within_bounds = (.48 < agent_1_percent) and (agent_1_percent < .52)
        self.assertTrue(within_bounds)

        # check that this works correctly with three agents
        self.add_agent('agent-2', [2, 3], 'UP', self.env, 3)
        num_agent_1 = 0.0
        other_agents = 0.0
        for i in range(10000):
            self.env.reserved_slots.append([3, 2, 'P', 'agent-0'])
            self.env.reserved_slots.append([3, 4, 'P', 'agent-1'])
            self.env.reserved_slots.append([2, 3, 'P', 'agent-2'])
            self.env.execute_reservations()
            self.env.update_moves({'agent-0': 'MOVE_DOWN', 'agent-1': 'MOVE_UP',
                                   'agent-2': 'MOVE_RIGHT'})

            self.env.execute_reservations()
            if self.env.agents['agent-2'].get_pos().tolist() == [3, 3]:
                num_agent_1 += 1
            else:
                other_agents += 1
        agent_1_percent = num_agent_1 / (num_agent_1 + other_agents)
        within_bounds = (.25 < agent_1_percent) and (agent_1_percent < .35)
        self.assertTrue(within_bounds)

        # you try to move into an agent that is in conflict with another agent
        # fifty percent of the time you should succeed
        percent_accomplished = 0
        percent_failed = 0
        for i in range(10000):
            self.env.reserved_slots.append([3, 2, 'P', 'agent-0'])
            self.env.reserved_slots.append([3, 4, 'P', 'agent-1'])
            self.env.reserved_slots.append([2, 2, 'P', 'agent-2'])
            self.env.execute_reservations()
            self.env.update_moves({'agent-0': 'MOVE_DOWN', 'agent-1': 'MOVE_UP',
                                   'agent-2': 'MOVE_RIGHT'})
            self.env.execute_reservations()
            if self.env.agents['agent-2'].get_pos().tolist() == [2, 2]:
                percent_failed += 1
            else:
                percent_accomplished += 1
        percent_success = percent_accomplished / (percent_accomplished + percent_failed)
        within_bounds = (.45 < percent_success) and (percent_success < .55)
        self.assertTrue(within_bounds)

    def test_beam_conflict(self):
        """Test that after the beam is fired, obscured apples and agents are returned"""
        self.env = HarvestEnv(ascii_map=MINI_HARVEST_MAP, num_agents=2)
        self.env.reset()

        # test that agents can't walk into other agents
        self.move_agent('agent-0', [4, 2])
        self.move_agent('agent-1', [4, 4])
        self.env.agents['agent-0'].update_map_agent_rot('UP')
        self.env.agents['agent-1'].update_map_agent_rot('UP')
        # test that if an agents firing beam hits another agent it gets covered
        self.env.update_custom_moves({'agent-1': 'FIRE'})
        self.env.execute_reservations()
        expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                 ['@', ' ', ' ', ' ', ' ', '@'],
                                 ['@', ' ', ' ', 'A', 'A', '@'],
                                 ['@', 'F', 'F', 'F', 'F', '@'],
                                 ['@', 'F', 'F', 'F', 'P', '@'],
                                 ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(expected_map, self.env.map)
        self.env.clean_map()
        expected_map = np.array([['@', '@', '@', '@', '@', '@'],
                                 ['@', ' ', ' ', ' ', ' ', '@'],
                                 ['@', ' ', ' ', 'A', 'A', '@'],
                                 ['@', ' ', ' ', 'A', 'A', '@'],
                                 ['@', ' ', 'P', 'A', 'P', '@'],
                                 ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(expected_map, self.env.map)

    def clear_agents(self):
        # FIXME(ev) this doesn't clear agent positions off the board
        self.env.agents = {}

    def add_agent(self, agent_id, start_pos, start_orientation, env, view_len):
        self.env.agents[agent_id] = HarvestAgent(agent_id, start_pos, start_orientation,
                                                 env, view_len)
        # FIXME(ev) just for now
        char = self.env.map[start_pos[0], start_pos[1]]
        self.env.hidden_cells.append([start_pos[0], start_pos[1], char])
        self.env.map[start_pos[0], start_pos[1]] = 'P'

    def move_agent(self, agent_id, new_pos):
        self.env.reserved_slots.append([new_pos[0], new_pos[1], 'P', agent_id])
        self.env.execute_reservations()

    def rotate_agent(self, agent_id, new_rot):
        self.env.agents[agent_id].update_map_agent_rot(new_rot)

    def construct_map(self, map, agent_id, start_pos, start_orientation):
        # overwrite the map for testing
        self.env = HarvestEnv(map, num_agents=0)
        self.env.reset()

        # replace the agents with agents with smaller views
        self.add_agent(agent_id, start_pos, start_orientation, self.env, 2)


class TestCleanupEnv(unittest.TestCase):
    def test_parameters(self):
        self.env = CleanupEnv(num_agents=0)
        self.assertEqual(self.env.potential_waste_area, 119)

    def test_reset(self):
        self.env = CleanupEnv(ascii_map=MINI_CLEANUP_MAP, num_agents=0)
        self.env.reset()
        # check that the map has no apples
        test_map = np.array([['@', '@', '@', '@', '@', '@'],
                             ['@', ' ', ' ', ' ', ' ', '@'],
                             ['@', 'H', ' ', ' ', ' ', '@'],
                             ['@', 'R', ' ', ' ', ' ', '@'],
                             ['@', 'S', ' ', ' ', ' ', '@'],
                             ['@', '@', '@', '@', '@', '@']])
        np.testing.assert_array_equal(self.env.map, test_map)

    # def test_firing(self):
    #     agent_id = 'agent-0'
    #     self.construct_map(TEST_MAP_1.copy(), agent_id, [3, 2], 'UP')
    #     import ipdb; ipdb.set_trace()
    #     # test basic firing with no rivers or streams or waste
    #     self.env.update_map({agent_id: 'FIRE'})
    #     self.env.execute_reservations()
    #     agent_view = self.env.agents[agent_id].get_state()
    #     expected_view = np.array(
    #         [['@'] + [' '] * 4,
    #          ['@'] + ['F'] * 2 + [' '] * 2,
    #          ['@'] + ['F'] + ['P'] + [' '] * 2,
    #          ['@'] + ['F'] * 2 + [' '] * 2,
    #          ['@'] + [' '] * 4]
    #     )
    #     np.testing.assert_array_equal(expected_view, agent_view)
    #
    #     self.env.clean_map()
    #
    #     expected_view = np.array(
    #         [['@'] + [' '] * 4,
    #          ['@'] + [' '] * 4,
    #          ['@'] + [' '] + ['P'] + [' '] * 2,
    #          ['@'] + [' '] * 4,
    #          ['@'] + [' '] * 4]
    #     )
    #     np.testing.assert_array_equal(expected_view, agent_view)

    def construct_map(self, map, agent_id, start_pos, start_orientation):
        # overwrite the map for testing
        self.env = CleanupEnv(map, num_agents=0)
        self.env.reset()
        self.clear_agents()

        # replace the agents with agents with smaller views
        self.add_agent(agent_id, start_pos, start_orientation, self.env, 2)
        # TODO(ev) hack for now, can't call render logic or else it will spawn apples
        self.move_agent(agent_id, start_pos)

    def clear_agents(self):
        # FIXME(ev) this doesn't clear agent positions off the board
        self.env.agents = {}

    def add_agent(self, agent_id, start_pos, start_orientation, env, view_len):
        self.env.agents[agent_id] = CleanupAgent(agent_id, start_pos, start_orientation,
                                                 env, view_len)

    def move_agent(self, agent_id, new_pos):
        self.env.reserved_slots.append([new_pos[0], new_pos[1], 'P', agent_id])
        self.env.execute_reservations()

    def rotate_agent(self, agent_id, new_rot):
        self.env.agents[agent_id].update_map_agent_rot(new_rot)


if __name__ == '__main__':
    unittest.main()
