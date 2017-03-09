"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return calc_move_diff_from_center(game, player)

def calc_ratio_of_moves(game, player):
    """A hueristic which takes the simple ratio of player and opponent moves
    as a scoring metric.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    player_factor = 1
    opp_factor = 1
    player_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if not opp_moves:
        return float("inf")
    elif not player_moves:
        return float("-inf")
    else:
        return float(player_factor * len(player_moves) / (opp_factor * len(opp_moves)))

def calc_move_diff_with_spaces(game, player):
    """A hueristic which takes the difference between player and opponent moves
    as a scoring metric. The method applies proportional weight factor for
    opponent moves based on the number of open spaces remaining in the game
    state.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    player_factor = 1
    opp_factor = 2
    player_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    open_spaces = len(game.get_blank_spaces())
    total_spaces = game.width * game.height
    if not opp_moves:
        return float("inf")
    elif not player_moves:
        return float("-inf")
    else:
        return float(player_factor * len(player_moves) * (total_spaces / open_spaces) - opp_factor * len(opp_moves))

def calc_move_diff_from_center(game, player):
    """A hueristic which weights values depending on their proximity to the center
    of the board. Center positions are favored over openings on the ouside of the
    board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    player_factor = 1
    opp_factor = 2
    board_center = (math.floor(game.width / 2), math.floor(game.height / 2))
    player_moves = game.get_legal_moves(player)
    player_score = 0
    for move in player_moves:
        if move == (3, 3):
            player_score += 1
        else:
            player_score += 1 - math.sqrt((board_center[0] - move[0]) ** 2 + (board_center[1] - move[1]) ** 2) / game.width
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_score = 0
    for move in opp_moves:
        if move == (3, 3):
            opp_score += 1
        else:
            opp_score += 1 - math.sqrt((board_center[0] - move[0]) ** 2 + (board_center[1] - move[1]) ** 2) / game.width
    if not opp_moves:
        return float("inf")
    elif not player_moves:
        return float("-inf")
    else:
        return float(player_factor * player_score - opp_factor * opp_score)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=3):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            # print('No available moves')
            return (-1, -1)

        if self.iterative:
            # Start searching at first level to find the best move so far
            curr_depth = 1
            best_move_overall = (-1, -1)
            best_score_overall = float("-inf")
            while True:
                # Iteratively deepen the search by increasing the search limit by 1
                # each round. Terminates when timeout or solution found
                try:
                    if self.method == 'minimax':
                        best_round_score, best_round_move = self.minimax(game, curr_depth)
                    elif self.method == 'alphabeta':
                        best_round_score, best_round_move = self.alphabeta(game, curr_depth)
                    if best_score_overall < best_round_score:
                        best_move_overall = best_round_move
                        best_score_overall = best_round_score
                    curr_depth += 1
                except Timeout:
                    # Handle any actions required at timeout, if necessary
                    # print('Iterative deepening timeout')
                    break
        else:
            best_move_overall = (-1, -1)
            try:
                # The try/except block will automatically catch the exception
                # raised by the search method when the timer gets close to expiring
                if self.method == 'minimax':
                    best_score_overall, best_move_overall = self.minimax(game, self.search_depth)
                elif self.method == 'alphabeta':
                    best_score_overall, best_move_overall = self.alphabeta(game, self.search_depth)

            except Timeout:
                # Handle any actions required at timeout, if necessary
                # print('Search function timeout')
                pass
        # Return the best move from the last completed search iteration
        return best_move_overall

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        possible_moves = game.get_legal_moves()

        if depth == 0 or not possible_moves:
            score_diff = self.score(game, self)
            return score_diff, (-1, -1)

        overall_best_move = (-1, -1)
        highest_move_diff = float("-inf") if maximizing_player else float("inf")

        for next_move in possible_moves:
            temp_board = game.forecast_move(next_move)
            curr_move_diff, curr_best_move = self.minimax(temp_board, depth - 1, not maximizing_player)
            if maximizing_player:
                if curr_move_diff > highest_move_diff:
                    highest_move_diff = curr_move_diff
                    overall_best_move = next_move
            else:
                if curr_move_diff < highest_move_diff:
                    highest_move_diff = curr_move_diff
                    overall_best_move = next_move
        return highest_move_diff, overall_best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        possible_moves = game.get_legal_moves()

        if depth == 0 or not possible_moves:
            score_diff = self.score(game, self)
            return score_diff, (-1, -1)

        overall_best_move = (-1, -1)
        highest_move_diff = float("-inf") if maximizing_player else float("inf")

        for next_move in possible_moves:
            temp_board = game.forecast_move(next_move)
            curr_move_diff, curr_best_move = self.alphabeta(temp_board, depth - 1, alpha, beta, not maximizing_player)
            if maximizing_player:
                if curr_move_diff > highest_move_diff:
                    highest_move_diff = curr_move_diff
                    overall_best_move = next_move
                if highest_move_diff >= beta:
                    return curr_move_diff, next_move
                alpha = max(alpha, curr_move_diff)
            else:
                if curr_move_diff < highest_move_diff:
                    highest_move_diff = curr_move_diff
                    overall_best_move = next_move, overall_best_move
                if highest_move_diff <= alpha:
                    return curr_move_diff, next_move
                beta = min(beta, curr_move_diff)
        return highest_move_diff, overall_best_move
