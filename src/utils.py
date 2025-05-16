from typing import Any, Callable, Iterable


class Utils:
    '''Utility functions, mainly for the UI'''
    def __init__(self) -> None:
        pass

    def display_message(self, message: str):
        print(message)

        
    def display_menu(self, prompt: str, options: dict[int, str]):
        print(prompt)
        for key, label in options.items():
            print(f"    {key}. {label}")

    def display_table(self, title: str, header: str, data: Iterable, format_row: list[Callable[[Any], str]]):
        print(title)
        print(header)

        for index, item in enumerate(data, start=1):
            values = [str(index)] + [fmt(item) for fmt in format_row]
            print(" | ".join(values))
    
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