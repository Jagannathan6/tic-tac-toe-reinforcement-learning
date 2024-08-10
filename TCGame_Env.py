from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    #responsible to find whether the tic tac toe game is complete
    def current_state_sum(self, current_state, num1, num2, num3):
        #print(num1, ' ',  num2, ' ', num3)
        #print(current_state[num1], ' ',  current_state[num2], ' ', current_state[num3])

        if (current_state[num1] + current_state[num2] + current_state[num3] == 15):
            return True
        else:
            return False


    def __init__(self):
        """initialise the board"""

        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, current_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        #print('current state in winning', current_state)
        #Passes all the combinations of how a match can be completed.
        if ( self.current_state_sum(current_state,0,1,2) or self.current_state_sum(current_state,3,4,5) or self.current_state_sum(current_state,6,7,8) or
             self.current_state_sum(current_state,0,3,6) or self.current_state_sum(current_state,1,4,7) or self.current_state_sum(current_state,2,5,8) or
             self.current_state_sum(current_state,2,4,6) or self.current_state_sum(current_state,0,5,8) ):
            return True
        else:
            return False




    def is_terminal(self, current_state):
        # Terminal state could be winning state or when the board is filled up
        #print('is_terminal ', current_state)

        if self.is_winning(current_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(current_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, current_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(current_state) if np.isnan(val)]


    def allowed_values(self, current_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in current_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, current_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(current_state), self.allowed_values(current_state)[0])
        env_actions = product(self.allowed_positions(current_state), self.allowed_values(current_state)[1])
        return (agent_actions, env_actions)



    def state_transition(self, current_state, current_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        new_state = []
        for i in current_state:
            new_state.append(i)
        #print('current action ', current_action[0])
        #print('current action ', current_action[1])
        new_state[current_action[0]] = current_action[1]
        return new_state



    def step(self, current_state, current_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        new_state = self.state_transition(current_state, current_action) #Move the state fom one to another
        terminal_state , result = self.is_terminal(new_state) #Find whwther the application has reached the end state
        if terminal_state:
            # Coe comes in a if loop if the turn is from Agent
            if result == "Win":
                reward = 10  #Provide the reward as 10 to agent as it has won the match
                game_state = "Game is won by the Agent" # Message that Agrnt has won the match
            else:
                reward = 0 #If the game enbds in a tie, noone gets a point
                game_state = "Game ends in a Tie" #Message that game has ended in a tie
            return (new_state, reward, terminal_state, game_state)
        else:
            agent_actions, environment_action = self.action_space(new_state)
            new_values = []
            for positions, values in enumerate(environment_action):
                new_values.append(values)
            new_action = random.choice(new_values)
            latest_state = self.state_transition(new_state, new_action) #Move the state fom one to another
            terminal_state, result = self.is_terminal(latest_state) #Find whwther the application has reached the end state
            if terminal_state:
                if result == "Win":
                    reward = 10 #Provide the reward as 10 to Environment as it has won the match
                    game_state = "Game is won by the Environment" # Message that Environment has won the match
                else:
                    reward = 0 #If the game enbds in a tie, noone gets a point
                    game_state = "Game ends in a Tie" #Message that game has ended in a tie
            else:
                reward = -1
                game_state = "Resume" # There is still scope to continue the match. Please continue
            return (latest_state, reward, terminal_state, game_state)


    def reset(self):
        return self.state
