import hashlib
import time
import datetime
import random
import string
import binascii
from models.model_survey import Survey, Translation, Question, Option
from models.model_submit import SurveyResponse
from initialize.redis_config import redis_client

def generate_unique_url():
    while True:
        url = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        url_hash = binascii.crc32(url.encode())
        if not redis_client.getbit('url_bitmap', url_hash):
            return url, url_hash

from fastapi import HTTPException

def controller_create_survey(data):
    try:
        # Validate survey data
        if 'default_lan' not in data or not data['default_lan']:
            raise HTTPException(status_code=400, detail="Survey must have a default language")
        
        if 'translation' not in data or data['default_lan'] not in data['translation']:
            raise HTTPException(status_code=400, detail="Default language must be present in translations")
        
        if 'question' not in data or not (1 <= len(data['question']) <= 10):
            raise HTTPException(status_code=400, detail="Survey must have between 1 and 10 questions")
        
        if not any(q['choice_type'] == 'CSAT' for q in data['question']):
            raise HTTPException(status_code=400, detail="Survey must have at least one CSAT question")

        url, url_hash = generate_unique_url()
        translations = [
            Translation(language=lang, translations=trans)
            for lang, trans in data['translation'].items()
        ]
        
        questions = [
            Question(
                id=q['id'],
                title=q['title'],
                choice_type=q['choice_type'],
                number_op=q.get('number_op'),
                required=q['required'],
                options=[Option(id=opt['id'], title=opt['title']) for opt in q['options']],
                max_selection=q.get('max_selection')
            )
            for q in data['question']
        ]
        
        survey = Survey(
            id=url,
            default_lan=data['default_lan'],
            translation=translations,
            questions=questions
        )
        
        survey.save()
        
        # Set the bitmap after successfully creating the survey
        redis_client.setbit('url_bitmap', url_hash, 1)

        saved_survey = Survey.objects(id=url).first() 
        
        survey_data = {
            "survey_id": str(survey.id),
            "created_at": datetime.datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        }
        
        redis_client.setex(f"url:{url}", 30 * 24 * 60 * 60, str(saved_survey))
        
        return {
            "survey_id": f"filum/s/{url}",
            "created_at": survey_data["created_at"],
            "time": survey_data["time"]
        }
    
    except HTTPException as e:
        raise e  # Giữ nguyên lỗi nếu là HTTPException
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create survey: {str(e)}")


def controller_get_visual(survey_id):
    try:
        # Retrieve survey responses from the database
        responses = SurveyResponse.objects(survey_id=survey_id)
        
        # Initialize counters for each question type
        question_totals = {}
        
        for response in responses:
            for answer in response.answers:
                if answer.choice_type in ['CSAT', 'single', 'multi']:
                    if answer.question_id not in question_totals:
                        question_totals[answer.question_id] = {
                            "question_id": answer.question_id,
                            "choice_type": answer.choice_type,
                            "total": 0
                        }
                    question_totals[answer.question_id]["total"] += answer.counter
        
        # Prepare the response data
        report_data = {
            "survey_id": survey_id,
            "answers": list(question_totals.values())
        }
        
        return report_data
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Failed to generate report: {e}")