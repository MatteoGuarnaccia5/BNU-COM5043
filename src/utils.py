from typing import Callable


class Utils:
    '''Utility functions, mainly for the UI'''
    def __init__(self) -> None:
        pass


    def display_menu():
        pass
    
    def validate_user_intput(self, prompt: str, lower_bound: int, upper_bound: int, error_msg: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value <= lower_bound or value >= upper_bound:
                    print(error_msg)
                    continue
                return value
            except ValueError:
                print("Invalid input. Please try again.")