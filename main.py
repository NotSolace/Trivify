from __future__ import annotations
from dataclasses import dataclass

from typing import Optional, List, Dict

from requests import Session
from random import choice, shuffle, sample

from time import sleep
from os import system

QUESTIONS = 5 # The maximum amount of questions is 50 (https://opentdb.com/api_config.php)
MULTIPLE_ANSWERS = True

@dataclass
class QuestionClass:
    question: str
    answer: str
    difficulty: str
    incorrect_answers: Optional[Dict]

class Trivia:
    questions: List[QuestionClass]
    session: Session

    def __init__(self) -> None:
        self.session = Session()
        self.questions = self.get_questions()

        self.correct_answers = 0
        self.incorrect_answers = 0

    def get_questions(self) -> List[QuestionClass]:
        response = self.session.get(
            url=(
                f"https://opentdb.com/api.php"
                f"?amount={QUESTIONS}"
                f"&type=multiple" if MULTIPLE_ANSWERS else "&type=boolean"
            )
        ) 
        
        return [
            QuestionClass(
                question=result.get("question", ""),
                answer=result.get("correct_answer", ""),
                difficulty=result.get("difficulty", ""),
                incorrect_answers=result.get("incorrect_answers", [])
            )
            for result in response.json().get("results", [])
        ]

    def start_quiz(self):
        for index, question in enumerate(self.questions, start=1):
            system("cls||clear")
            
            print(f'{index}. {question.question.replace('&quot;', '"').replace('&#039', "'").replace('&amp;', '&')} | Difficulty: {question.difficulty}')

            if MULTIPLE_ANSWERS:
                print(f'[ANSWERS] ' + ', '.join(
                    sample([question.answer] + question.incorrect_answers, len(question.incorrect_answers) + 1) # type: ignore
                )) # type: ignore

            answer = input("[YOU] Your answer: ")

            if answer.lower() == question.answer.lower():
                print(f'[BOT] Correct answer.')
                self.correct_answers += 1
            else:
                print(f'[ANSWER] {question.answer}')
                print(f'[BOT] Incorrect answer.')
                self.incorrect_answers += 1

            sleep(0.85)
        
        system("cls||clear")
        print(f'You have reached the end of your {QUESTIONS} questions trivia.')
        print(f'Correct Answers: {self.correct_answers}\nIncorrect Answers: {self.incorrect_answers}\nSkill Level: {self.calculate_level()}')
    
    def calculate_level(self) -> str:
        skill = round((self.correct_answers / (self.correct_answers + self.incorrect_answers)) * 100)
        
        if skill > 75:
            return 'Platinum'
        if skill < 75 and skill > 50:
            return 'Gold'
        if skill < 50 and skill > 25:
            return 'Silver'
        if skill < 25 and skill > 1:
            return 'Bronze'
        else:
            return 'Unknown'

if __name__ == "__main__":
    TriviaClass = Trivia()
    TriviaClass.start_quiz()