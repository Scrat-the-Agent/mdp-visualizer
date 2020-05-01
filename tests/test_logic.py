import pytest
from random import randint

from mdp_visualizer.logic.gameLogic import GameLogic, GameParams
from mdp_visualizer.logic.actions_objects_list import Modes, Actions


def take_random_action(logic, max_action=None):
    return randint(0, max_action if max_action else (logic.n_actions - 1))


def test_board_steps():
    num_logics = 20
    num_steps = 1000

    for i in range(num_logics):
        params = GameParams(game_mode=Modes.IAMRLAGENT, game_height=3, game_width=4,
                            scrat_random=True,
                            hippo_random=True, hippo_move_prob=1,
                            watermelon_random=True, watermelon_move_prob=1)
        logic = GameLogic(params)

        for j in range(num_steps):
            prev_scrat_pos = logic.scrat_position
            prev_hippo_pos = logic.hippo_position
            prev_watermelon_pos = logic.watermelon_position

            action = take_random_action(logic)
            logic.step(action)

            new_scrat_pos = logic.scrat_position
            new_hippo_pos = logic.hippo_position
            new_watermelon_pos = logic.watermelon_position

            assert 0 <= abs(new_scrat_pos[0] - prev_scrat_pos[0]) + abs(new_scrat_pos[1] - prev_scrat_pos[1]) <= 1
            assert 0 <= abs(new_hippo_pos[0] - prev_hippo_pos[0]) + abs(new_hippo_pos[1] - prev_hippo_pos[1]) <= 1
            assert 0 <= abs(new_watermelon_pos[0] - prev_watermelon_pos[0]) +\
                abs(new_watermelon_pos[1] - prev_watermelon_pos[1]) <= 1

        logic.full_reset()


def test_watermelon_hippo_actions():
    num_logics = 20
    num_steps = 1000

    # Fully mobile Hippo and Watermelon
    params = GameParams(game_mode=Modes.IAMRLAGENT, game_height=3, game_width=4,
                        scrat_random=True,
                        hippo_random=True, hippo_move_prob=0,
                        watermelon_random=True, watermelon_move_prob=0)
    logic = GameLogic(params)

    for i in range(num_logics):
        for j in range(num_steps):
            if logic.scrat_position == logic.watermelon_position and not logic.scrat_carrying_watermelon:
                action = Actions.TAKE.value
            elif logic.scrat_position == logic.hippo_position and logic.scrat_carrying_watermelon:
                action = Actions.PUT_FEED.value
            else:
                action = take_random_action(logic, max_action=3)

            _, _, done, _ = logic.step(action)

            assert logic.scrat_carrying_watermelon == logic.watermelon.is_taken
            assert logic.hippo_is_fed == logic.watermelon.is_eaten

            if done:
                print(f"Done {j}!")
                break

        assert done
        logic.full_reset()


def test_with_lava():
    num_logics = 20
    num_steps = 1000

    # Mobile Hippo and Watermelon with lava
    # Scrat doesn't take the Watermelon and feed the Hippo. Done can be only reached in only 1 lava.
    params = GameParams(game_mode=Modes.IAMRLAGENT, game_height=5, game_width=6,
                        scrat_random=True,
                        hippo_random=True, hippo_move_prob=1,
                        watermelon_random=True, watermelon_move_prob=1,
                        lava_random=1, lava_is_terminal=True)
    logic = GameLogic(params)

    for i in range(num_logics):
        for j in range(num_steps):
            action = take_random_action(logic, max_action=3)

            _, _, done, _ = logic.step(action)

            assert logic.hippo_position not in logic.lava_cells
            assert logic.watermelon_position not in logic.lava_cells
            assert logic.full_reward <= 0

            if done:
                print(f"Lava! Scrat position: {logic.scrat_position}, lava_cells: {logic.lava_cells}")
                assert logic.scrat_position in logic.lava_cells
                break

        logic.full_reset()
