from .models import *
import re

def MathExpressions_3(Correction_txt):
    print(Correction_txt)
    cleaned_string = Correction_txt.replace('```python', '').replace('```', '').strip()

    def parse_complex_string(s):
        # Remove unnecessary characters and clean the string
        s = s.strip()

        # Define a pattern to match each question block
        block_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')

        def parse_block(block):
            # Split by '], [' to separate question and choices
            parts = re.split(r'\], \[', block.strip('[]'))

            # Parse the question
            question = parts[0].strip('[]').split(', ', 1)
            question_id = question[0].strip()
            question_text = question[1].strip("'")

            # Parse the choices
            choices = []
            for part in parts[1:]:
                choice_parts = re.split(r',\s*', part.strip('[]'), 1)
                choice_id = choice_parts[0].strip()
                choice_text = choice_parts[1].strip("'")
                choices.append([choice_id, choice_text])

            return [[question_id, question_text]] + choices

        # Process each block to extract the questions and choices
        result = []
        for match in block_pattern.finditer(s):
            block = match.group(1)
            result.append(parse_block(block))

        return result

    parsed_array = parse_complex_string(cleaned_string)

    def clean_array(arr):
        for sublist in arr:
            for item in sublist:
                # Remove extra backslashes
                item[1] = re.sub(r"\\\\", r"\\", item[1])
                # Remove newline characters
                item[1] = item[1].replace('\\n', ' ')
        return arr
    
    clean_parsed_array = clean_array(parsed_array) 

    return clean_parsed_array


def MathExpressions_4(Correction):
    Correction_Parse = MathExpressions_3(Correction)
    print(Correction_Parse)
    for data in Correction_Parse:
        question = Question.objects.get(id=int(data[0][0]))
        question.Content = data[0][1]
        question.save()
        for elements in data[1:]:
            choice = Choice.objects.get(id=int(elements[0]))
            choice.Content = elements[1]
            choice.save()
