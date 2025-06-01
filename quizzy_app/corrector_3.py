from .models import *
import re

# Function to upload the corrected array into the database
def parse_correction_into_array(cleaned_string):
    def parse_complex_string(s):
        s = s.strip()
        block_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')

        def parse_block(block):
            parts = re.split(r'\], \[', block.strip('[]'))
            question = parts[0].strip('[]').split(', ')
            question_id = question[0].strip().strip("'")
            question_text = question[1].strip().strip("'")
            
            choices = []
            for part in parts[1:]:
                choice_parts = re.split(r',\s*', part.strip('[]'))
                choice_id = choice_parts[0].strip().strip("'")
                choice_text = choice_parts[1].strip().strip("'")
                choice_extra = choice_parts[2].strip().strip("'") if len(choice_parts) > 2 else ''
                choices.append([choice_id, choice_text, choice_extra])
            
            return [[question_id, question_text]] + choices
        
        result = []
        for match in block_pattern.finditer(s):
            block = match.group(1)
            result.append(parse_block(block))
        
        return result

    corrections = parse_complex_string(cleaned_string)

    return corrections


