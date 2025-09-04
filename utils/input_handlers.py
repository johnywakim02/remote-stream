def input_yes_no(question: str, default: bool = True) -> bool:
    response: str = input(f"{question} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    while response not in {"y", "n", ""}:
        response = input(f"Input invalid. \n{question} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    if response == "":
        return default
    return response == "y"

def input_positive_int(question: str) -> int:
    while True:
        response = input(f"{question}: ").strip()
        if response.isdigit() and int(response) > 0:
            return int(response)
        print("Input invalid. Please enter a positive whole number.")

def input_from_range_int(question: str, possible_answers: set[int]) -> int:
    while True:
        response = input(f"{question} Available options {sorted(possible_answers)}: ").strip()
        if not response.isdigit():
            print("Please enter a valid number.")
            continue

        response_int = int(response)
        if response_int not in possible_answers:
            print("Please choose one of the available options.")
            continue

        return response_int


