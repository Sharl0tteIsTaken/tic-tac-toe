
grid:str = '\
  7 | 8 | 9 \n.\
 -----------\n.\
  4 | 5 | 6 \n.\
 -----------\n.\
  1 | 2 | 3 \n'

symbols = ['X', 'O']
allow_input = [str(x) for x in range(1, 10)]
horizon = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
verical = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
greet_text = """

Welcome to tic tac toe, 
this is a two player game, on a grid of 3x3,
player alternately places 'X' and 'O',
get a line with same symbol wins the round.
X goes first, player alternately goes first.

Tip: Game will display
right: number that can be placed,
left:  current state of the board.\n"""


class bcolors:
    """
    color the text in terminal.
    
    rules:
    can be used in f-string
    put color codes before, and ENDC after text
    
    examples:
    `f"{bcolors.HEADER}colored text{bcolors.ENDC}"`
    `f"{bcolors.WARNING}colored text{bcolors.ENDC}"`
    """
    # cite: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def tester_decor(func):
    """
    this is a test decorator, used to assist debug, abandand because of will cause weird return value.
    """
    def wrapper(*args, **kwargs):
        print(f"executing: {func.__name__}")
        func(*args, **kwargs)
        print(f"execute end of: {func.__name__}")
    wrapper.__name__ = func.__name__
    return wrapper


class ShowMaker():
    """
    2-player based tic tac toe game,
    organizer of the game, with not much customization to save time.
    
    Functions:
    ----
    new_game() shows greet text, and setup everything, 
    player_input() ask players to place X and O alternately.
    """
    def __init__(self) -> None:
        self.playing = True
        self._iswinner = False
        self._round = 0
        self._p1_score = 0
        self._p2_score = 0
        self._setup_new_game()
        
    def _setup_new_game(self) -> None:
        """
        set current player alternately,
        resets _placed, _grid, _placeable_grid, the state of playing:bool and _iswinner:bool.
        
        in-game grid on the left is _grid, right is _placeable_grid.
        """
        if self._round % 2 == 0:
            self._current_player = False # use True as 1 and False as 0
        else:
            self._current_player = True
        self._placed:dict[int, str] = {
            1: ' ', 2: ' ', 3: ' ',
            4: ' ', 5: ' ', 6: ' ',
            7: ' ', 8: ' ', 9: ' ',
        }
        self._grid:str = grid
        self._placeable_grid:str = grid
        self.playing = True
        self._iswinner = False

    def new_game(self) -> None:
        """
        setup new game with greet text and shows grid.
        """
        print(greet_text)
        self._setup_new_game()
        self._show_grid()
        
    def player_input(self) -> None:
        """
        ask the current player to choose a position to place the represent mark,
        will restrain players to only enter letters thats allowed and unique,
        then pass the position to _place(), _end_check(),
        lastly change the current player.
        """
        user_input = input(f'player {int(self._current_player)+1}({symbols[self._current_player]}) marks: ')
        if self._placeable(user_input):
            self._show_grid()
            self._end_check(user_input)
            self._draw_check()
            self._current_player = not self._current_player

    def _placeable(self, position:str) -> bool:
        """
        return True if position is in allow_input and is unique(haven't been pass in during this round).
        
        Args:
            position (str): user input

        Returns:
            False: if position is not in allow_input or is not unique
            Ture: if position is in allow_input and is unique
        """
        if position not in allow_input:
            print(f"{bcolors.WARNING}user input '{position}' is not allowed.\naccept numbers 1 ~ 9.{bcolors.ENDC}")
            return False
        placeable = [k for k in self._placed.keys() if self._placed[k] == " "]
        if int(position) not in placeable:
            print(f"{bcolors.WARNING}position '{position}' is occupied,\npick another position.{bcolors.ENDC}")
            return False
        self._update_grid(position)
        return True

    def _update_grid(self, position:str) -> None:
        """
        update the grid with position(allowed and unique), also updates: 
        _grid: position will be replaced by players represent symbol
        _placeable_grid: position will be replaced by ' '
        _placed: store relationship between position and symbol
        
        Args:
            position (str): user input
        """
        symbol = symbols[self._current_player]
        self._placed[int(position)] = symbol
        self._grid = self._grid.replace(position, symbol)
        self._placeable_grid = self._placeable_grid.replace(position, " ")
        
    def _show_grid(self) -> None:
        """
        modify the grid to current state of the game, and print it out after format.
        """
        grid = self._grid
        for num in range(1, 10):
            grid = grid.replace(str(num), " ")
        grid = grid.replace('\n', '')
        split_grid:list[str] = grid.split('.')
        split_placeable_grid:list[str] = self._placeable_grid.split('.')
        print("="*28)
        print(" tic tac toe  |   placeable")
        for num in range(len(split_grid)):
            print(f"{split_grid[num]}  | {split_placeable_grid[num]}", end='')
        print("="*28, '\n')
        
    def _draw_check(self) -> None:
        """
        check if there's any position empty,
        if none, game is draw and round is ended,
        lastly print player scores.
        """
        if " " not in self._placed.values() and not self._iswinner:
            print("draw.")
            self.playing = False
            self._round = self._round + 1
            self._show_score()
        
    def _end_check(self, user_input:str) -> None:
        """
        check if the current placement at the position will result a winner,
        if Ture, show the winning line's position in grid with highlighted text,
        and print position of the line.
        
        Args:
            user_input (str): user input
        """
        if user_input == "5":
            self._win_con_5()
            return None
        num:int = int(user_input)
        idx_x = (num-1) // 3
        idx_y = (num-1) % 3
        x = horizon[idx_x]
        y = verical[idx_y]
        positions = [x, y]
        win_con:list[list[int]] = []
        for pos in positions:
            # '-' -> '|' shape check
            if self._placed[pos[0]] == self._placed[pos[1]] and self._placed[pos[1]] == self._placed[pos[2]]:
                win_con.append([pos[0], pos[1], pos[2]])
        input_num = int(user_input)
        if input_num % 2 != 0:
            if self._placed[input_num] == self._placed[5] and self._placed[5] == self._placed[10-input_num]:
                # 'X' shape check on corner place
                win_con.append([input_num, 5, 10-input_num])
        self._show_win_positions(win_con)
        self._show_highlighted_grid(win_con)
        
    def _win_con_5(self) -> None:
        """
        only tests if the current placement at the position 5 will result a winner,
        if Ture, show the winning line's position in grid with highlighted text, 
        and print position of the line.
        """
        left = 1
        mid = 5
        right = 9
        win_con = []
        for step in range(4):
            if self._placed[left+step] == self._placed[mid] and self._placed[mid] == self._placed[right-step]:
                win_con.append([left+step, mid, right-step])
        self._show_win_positions(win_con)
        self._show_highlighted_grid(win_con)
    
    def _show_win_positions(self, con:list[str] | list[int] | list[list[int]]) -> None:
        """
        takes winning line(s)'s position as input, 
        print the positions after format.

        Args:
            con (list[str] | list[int] | list[list[int]]): winning condition(winning line), 
            there can be one or many winning line
        """
        if con == []:
            return None
        elif type(con[0]) != list:
            con = [con] # type: ignore
        print(f'player {int(self._current_player)+1}({symbols[self._current_player]}) wins with position: ', end='')
        print(*con, sep=', ')
        
    def _show_highlighted_grid(self, win_con:list[str] | list[int] | list[list[int]]) -> None:
        """
        takes winning line(s)'s position as input, 
        print the grid with highlighted winning line.

        Args:
            win_con (list[str] | list[int] | list[list[int]]):  winning condition(winning line), 
            there can be one or many winning line
        """
        if win_con == []:
            return None
        self.playing = False
        self._iswinner = True
        self._round = self._round + 1
        if type(win_con[0]) == list:
            align = []
            for line in win_con:
                for pos in line: # type: ignore
                    align.append(str(pos))
        else:
            align = [str(pos) for pos in win_con]
        hl_grid:str = grid.replace(".", "")
        for num in range(1, 10):
            hl_grid = hl_grid.replace(str(num), f"【{num}】")
        for position in self._placed:
            if str(position) in align:
                hl_grid = hl_grid.replace(f"【{str(position)}】", f"{bcolors.WARNING}{self._placed[position]}{bcolors.ENDC}")
            else:
                hl_grid = hl_grid.replace(f"【{str(position)}】", self._placed[position])
        layers = hl_grid.split('\n')[:-1]
        print("-"*28)
        for layer in layers:
            print(f"        {layer}")
        print("-"*28)
        if self._current_player:
            self._p2_score = self._p2_score + 1
        else:
            self._p1_score = self._p1_score + 1
        self._show_score()
        
    def _show_score(self):
        """
        print players score after format.
        """
        print('~'*17)
        print('     score')
        print(f" player 1(X):  {self._p1_score}")
        print(f" player 2(O):  {self._p2_score}")
        print('~'*17)
        
