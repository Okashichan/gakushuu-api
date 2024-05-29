import random


def generate_quiz(questions_dict, quiz_size=10):
    if quiz_size > len(questions_dict):
        quiz_size = len(questions_dict)

    keys = list(questions_dict.keys())
    random.shuffle(keys)
    quiz_keys = keys[:quiz_size]

    quiz = []
    for key in quiz_keys:
        correct_answer = questions_dict[key]
        all_answers = list(questions_dict.values())
        wrong_answers = random.sample(
            [ans for ans in all_answers if ans != correct_answer], 3)

        options = wrong_answers + [correct_answer]
        random.shuffle(options)

        unique_options = list(set(options))
        while len(unique_options) < 4:
            remaining_wrong_answers = [
                ans for ans in all_answers if ans != correct_answer and ans not in unique_options]
            if remaining_wrong_answers:
                new_answer = random.choice(remaining_wrong_answers)
                unique_options.append(new_answer)
            unique_options = list(set(unique_options))

        random.shuffle(unique_options)
        quiz.append((key, correct_answer, unique_options))

    return quiz
