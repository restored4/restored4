import numpy as np

# global variables
BOARD_ROWS = 5
BOARD_COLS = 5
START = (1, 0)
OBSTACLE_STATES = [(2, 2), (2, 3), (2, 4), (3, 2)]
WIN_STATE = (4, 4)
JUMP_HERE = (1, 3)
STATE_AFTER_JUMP = (3, 3)
DETERMINISTIC = True
OUTPUT_INFO = True
TOTAL_REWARD = 0
MAXIMUM_STEPS = 40
NO_OF_EPISODES = 0
DEBUG = True

class State:
    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.board[2, 2] = -1
        self.board[2, 3] = -1
        self.board[2, 4] = -1
        self.board[3, 2] = -1
        self.board[3, 3] = 5
        self.board[START] = 1
        self.board[WIN_STATE] = 10
        self.board[STATE_AFTER_JUMP] = 5
        self.state = state
        self.initial_state = state
        self.isEnd = False
        self.determine = DETERMINISTIC

    def giveReward(self):
        if self.state == WIN_STATE:
            return 10
        elif self.initial_state == JUMP_HERE and self.state == STATE_AFTER_JUMP:
            print("give +5")
            return 5
        else:
            return -1

    # def obstacleFunc(self, state): # Describing the obstacles
    #     return ((state == (2, 2))
    #                     or (state == (2, 3))
    #                     or (state == (2, 4))
    #                     or (state == (3, 2)))

    def isEndFunc(self, steps):
        if (self.state == WIN_STATE
                or steps >= MAXIMUM_STEPS):
            if self.state == WIN_STATE:
                if OUTPUT_INFO:
                    print('WINNING STATE REACHED:', WIN_STATE)
            if steps >= MAXIMUM_STEPS:
                if OUTPUT_INFO:
                    print('MAXIMUM NO OF STEPS REACHED:', MAXIMUM_STEPS)
            self.isEnd = True

    def probabilityOfAction(self, action):

        choice_action = ""
        as_expected = "yes"

        if action == "North":
            choice_action = np.random.choice(["North", "West", "East"], p=[0.8, 0.1, 0.1])
            if choice_action != action:
                as_expected = "no"

        if action == "South":
            choice_action = np.random.choice(["South", "West", "East"], p=[0.8, 0.1, 0.1])
            if choice_action != action:
                as_expected = "no"

        if action == "West":
            choice_action = np.random.choice(["West", "North", "South"], p=[0.8, 0.1, 0.1])
            if choice_action != action:
                as_expected = "no"

        if action == "East":
            choice_action = np.random.choice(["East", "North", "South"], p=[0.8, 0.1, 0.1])
            if choice_action != action:
                as_expected = "no"
        if DEBUG:
            print("probOfAction => ", "choice_action:", choice_action, "- actionRespected:", as_expected)
        return choice_action, as_expected

    def nextPosition(self, action):
        """
        action: North, South, West, East
        -------------
        0 | 1 | 2| 3| 4|
        1 |
        2 |
        3 |
        4 |
        return board next state
        """
        if self.determine:
            if action == "North":
                next_state = (self.state[0] - 1, self.state[1])
            elif action == "South":
                next_state = (self.state[0] + 1, self.state[1])
            elif action == "West":
                next_state = (self.state[0], self.state[1] - 1)
            elif action == "jump":
                next_state = (self.state[0] + 2, self.state[1])
            else:
                next_state = (self.state[0], self.state[1] + 1)  # This action is for East movement

        # Checking whether next state is legal
        if (next_state[0] >= 0) and (next_state[0] <= 4):
            if (next_state[1] >= 0) and (next_state[1] <= 4):
                if next_state not in OBSTACLE_STATES:
                    return next_state
        return self.state

    def showBoard(self):
        self.board[self.state] = 1
        print("Board Environment showing agent A at state (1, 0):")
        print('    0   1   2   3   4')
        print(' -----------------------')
        for i in range(0, BOARD_ROWS):
            out = str(i) + ' | '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'A'
                if self.board[i, j] == 10:
                    token = '*'
                if self.board[i, j] == -1:
                    token = 'w'
                if self.board[i, j] == 5:
                    token = '0'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
            print(out)
        print(' -----------------')
        # print(self.board)


# Agent (player) coding
class Agent:
    def __init__(self):
        self.states = []
        self.actions = ["North", "West", "East", "South"]
        self.State = State()
        self.isEnd = self.State.isEnd
        self.lr = 0.3  # Agent's learning rate
        self.exp_rate = 0.3  # Agent's epsilon value
        self.decay_gamma = 1  # Agent's discount factor
        # initial state rewards
        self.Q_values = {}
        self.episode_reward = 0

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.Q_values[(i, j)] = 0
        print(self.Q_values)

    def complete_episode(self):
        global NO_OF_EPISODES
        global TOTAL_REWARD
        new = NO_OF_EPISODES + 1
        if NO_OF_EPISODES >= 30:
            NO_OF_EPISODES = 0
        else:
            new
        # print("Number 0f Episodes:", new)
        TOTAL_REWARD += self.episode_reward
        self.episode_reward = 0



    def chooseAction(self):
        # choose action with most expected value
        max_next_reward = 0
        action = ""
        # For the agent to be able to jump:
        if self.State.state == JUMP_HERE:
            action = self.actions + ["jump"]

        if np.random.uniform(0, 1) <= self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                current_position = self.State.state
                next_reward = self.Q_values[self.State.nextPosition(a)]
                print(next_reward, )
                if next_reward >= max_next_reward:
                    action = a
                    max_next_reward = next_reward
        return action

    def takeAction(self, action):
        position = self.State.nextPosition(action)  # Updating state
        return State(state=position)

    def reset(self):
        self.states = []
        self.State = State()
        self.isEnd = self.State.isEnd

    def play(self, rounds=10):
        i = 0
        while i < rounds:
            # to the end of game back propagate reward
            if self.State.isEnd:
                # back propagate
                reward = self.State.giveReward()
                self.Q_values[self.State.state] = reward

                self.episode_reward = reward
                self.complete_episode()
                print("End of Game Reward:", reward)


                # print(self.Q_values)

                for s in reversed(self.states):
                    reward = self.Q_values[s] + self.lr * (reward - self.Q_values[s])
                    self.Q_values[s] = round(reward, 3)
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                # append trace
                self.states.append(self.State.nextPosition(action))
                print("current position {} action {}".format(self.State.state, action))
                # by taking the action, it reaches the next state
                self.State = self.takeAction(action)
                # mark is end
                self.State.isEndFunc(0)
                print("Next state:", self.State.state)
                print("---------------------")
                self.isEnd = self.State.isEnd


    def showValues(self):
        for i in range(0, BOARD_ROWS):
            print('----------------------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += str(self.Q_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------------------')


if __name__ == "__main__":
    ag = Agent()
    st = State()
    st.showBoard()
    ag.play(100)
    ag.showValues()
