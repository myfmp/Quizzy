from .models import *
from django.db.models import IntegerField
from django.db.models.functions import Cast

def score(quizz_id, user_answers):

    def compare_arrays(array1, array2):
        # Create a dictionary from the second array for quick lookup
        dict_array2 = {item[0]: item[1] for item in array2 if isinstance(item, list)}

        result = [array1[0]]  # Start with the first element of array1
        exact_match = True  # Initialize exact match flag

        for item in array1[1:]:
            if isinstance(item, list):
                key = item[0]
                value1 = item[1]
                
                if key in dict_array2:
                    value2 = dict_array2[key]
                    
                    if value1 == False and value2 == False:
                        status = 'neutral'
                    elif value1 == True and value2 == True:
                        status = 'correct'
                    elif value1 == True and value2 == False:
                        status = 'negative'
                        exact_match = False
                    elif value1 == False and value2 == True:
                        status = 'corrected'
                        exact_match = False
                else:
                    # Key not found in the second array, so default to neutral
                    status = 'neutral'
                    exact_match = False
                
                result.append([key, status])
            else:
                exact_match = False
        
        return result, exact_match
    
    correction = []
    tmp = []
    result = []
    score_counter = 0  # Initialize score counter

    # Collecting questions and choices
    Questions = Question.objects.filter(Quizz_id=quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
    for question in Questions:
        tmp = [str(question.id)]
        Choices = Choice.objects.filter(Question_id=question.id)
        for choice in Choices:
            tmp.append([str(choice.id), choice.Correction])
        correction.append(tmp)

    for bloc_1, bloc_2 in zip(user_answers, correction):
        results, exact_match = compare_arrays(bloc_1, bloc_2)
        result.append(results)
        if exact_match:
            score_counter += 1  # Increment score if there is an exact match

    return result, score_counter
