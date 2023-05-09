import os
import random
import re
import pathlib

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
PATH = APP_PATH + '/section/'
print(PATH)
def standardize_string(word: str) -> str:
    word = word.strip().lower()
    return re.sub("\s+", " ", word)
    
    
def choose_section() -> int:
    sections = os.listdir(PATH)
    sections.sort()
    for i, section in enumerate(sections):
        temp = section.split(".")[0]
        print(temp)
        sections[i] = temp
    sections = [int(section.split("_")[1]) for section in sections]
    number_section = input("Choose section (q to quit): ")
    
    while True:
        if number_section == "q":
            return
        if not number_section.isdigit():
            print("Input must be an integer")
            number_section = input("Choose section (q to quit): ")
        elif int(number_section) not in sections:
            print(f"There is no section_{number_section}")
            number_section = input("Choose section (q to quit): ")
        else: 
            break
    return number_section


def read_data(number_section: int) -> dict[str, str]:
    if number_section is None:
        return
    section = {}
    with open(PATH+f'section_{number_section}.txt', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(": ")
            key = line[0]
            value = line[1]
            section[key] = value
        
    num_words = input("Choose number of words to test: ")
    while True:
        num_words = standardize_string(num_words)
        if not num_words.isdigit() or int(num_words) > 30:
            print("Invalid input!")
            num_words = input("Enter your choice: ")
        else:
            break
    
    return section, int(num_words)
            

def get_random_words(section: dict[str, str], num_words: int) -> list[str]:
    if section is None:
        return
    return random.sample(list(section.values()), num_words)


def check_multi_choice(input_answer: str, answer: str) -> bool:
    if input_answer == answer:
        return True
    
    choices = [a for a in answer.split(" ") if "/" in a][0]
    list_choices = choices.split("/")
    for choice in list_choices:
        if input_answer == answer.replace(choices, choice):
            return True
    return False

def calc_score(input_answer: str, answer: str) -> int:
    score = 0
    if "/" in answer:
        check = check_multi_choice(input_answer, answer)
        if check:
            print('Correct!')
            score += 1
        else:
            print(f"Incorrect! The correct word is: {answer}")
    elif input_answer == answer:
        print('Correct!')
        score += 1
    else:
        print(f"Incorrect! The correct word is: {answer}")
            
    return score

def test(rand_words: str, section: dict[str, str]):
    if rand_words is None:
        return
    
    meaning = list(section.values())
    keys = list(section.keys())

    correct = 0
    for word in rand_words:
        input_answer = input(word+" (q to quit): ")
        input_answer = standardize_string(input_answer)
        
        if input_answer == 'q':
            break
        answer = keys[meaning.index(word)].lower()
        correct += calc_score(input_answer, answer)
        
    if correct == len(rand_words):
        print("All the words are correct, well done!")
    else:
        print(f"Score: {correct}")

def learn():
    number_section = choose_section()
    section, num_words = read_data(number_section)
    rand_words = get_random_words(section, num_words)
    test(rand_words, section)
    
def run():
    print("0 to preview vocab")
    print("1 to test")
    print("q to quit")
    choice = input("Enter your choice: ")
    while True:
        if choice == "q":
            break
        if not choice.isdigit() or int(choice) > 1:
            print("Invalid value!")
            choice = input("Enter your choice: ")
            continue
        else:
            break
        
    if choice == "1":
        learn()
    else:
        pass

    
    
if __name__ == "__main__":
    run()