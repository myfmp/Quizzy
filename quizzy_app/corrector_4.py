from .models import *

def upload_correction_to_db(corrections):
    # Save the corrections to the database
    for correction in corrections:
        if isinstance(correction, list) and len(correction) > 1:
            for choices in correction[1:]:
                try:
                    if isinstance(choices, list) and len(choices) >= 3:
                        choice = Choice.objects.get(id=int(choices[0]))
                        choice.Correction = choices[2] == 'true'
                        choice.save()
                except Choice.DoesNotExist:
                    print(f"Choice with id {choices[0]} does not exist.")
                except Exception as e:
                    print(f"Error processing choice: {e}")