from initialize.redis_config import redis_client
from models.model_survey import Survey
from models.model_submit import SurveyResponse, Answer
import binascii
import json
from fastapi import HTTPException
from datetime import datetime

def create_client_survey_controller(survey_id, data):
    try:
        # Check if survey exists in bitmap
        url_hash = binascii.crc32(survey_id.encode())
        if not redis_client.getbit('url_bitmap', url_hash):
            raise HTTPException(status_code=404, detail="Survey not found")
        
        # Retrieve survey from database to validate required questions
        survey = Survey.objects(id=survey_id).first()
        if not survey:
            raise HTTPException(status_code=404, detail="Survey not found in database")
        
        # Validate required questions
        required_questions = {q.id for q in survey.questions if q.required}
        answered_questions = {ans['question_id'] for ans in data['answers']}
        if not required_questions.issubset(answered_questions):
            raise HTTPException(status_code=400, detail="You must complete all required questions")
        
        # Validate max_selection
        for ans in data['answers']:
            question = next((q for q in survey.questions if q.id == ans['question_id']), None)
            if question and question.max_selection is not None:
                if ans.get('num_selection', 0) > question.max_selection:
                    raise HTTPException(status_code=400, detail=f"Question {ans['question_id']} exceeds max selection limit")
        
        # Create SurveyResponse object
        answers = [
            Answer(
                question_id=ans['question_id'],
                choice_type=ans['choice_type'],
                answer=ans.get('answer'),
                answer_id=ans.get('answer_id'),
                answer_ids=ans.get('answer_ids', []),
                num_selection=ans.get('num_selection'),
            )
            for ans in data['answers']
        ]
        
        survey_response = SurveyResponse(
            survey_id=survey_id,
            email=data['email'],
            name=data['name'],
            phone=data['phone'],
            language=data['language'],
            submitted_at=datetime.strptime(data['submitted_at'], "%Y-%m-%dT%H:%M:%SZ"),
            answers=answers
        )
        
        survey_response.save()
        
        return {"message": "Survey response submitted successfully"}
    except HTTPException as e:
        raise e  # Giữ nguyên mã lỗi nếu đã là HTTPException

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit survey response: {e}")

def controller_get_survey_from_cache(survey_id):
    try:
        cached_survey = redis_client.get(f"url:{survey_id}")
        if cached_survey:
            return json.loads(cached_survey.decode('utf-8'))
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve survey from cache: {e}")

def read_client_survey_controller(survey_id):
    try:
        # Check cache first
        survey_data = controller_get_survey_from_cache(survey_id)
        if survey_data:
            print(survey_data)
            return survey_data
        
        # If not found in cache, check bitmap
        url_hash = binascii.crc32(survey_id.encode())
        if not redis_client.getbit('url_bitmap', url_hash):
            raise HTTPException(status_code=404, detail="Survey not found")
        
        # If found in bitmap, retrieve from database
        survey = Survey.objects(id=survey_id).first()
        if survey:
            return json.loads(survey.to_json())
        else:
            raise HTTPException(status_code=404, detail="Survey not found")
    except HTTPException as e:
        raise e  # Giữ nguyên mã lỗi nếu đã là HTTPException

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit survey response: {e}")

def read_client_survey_lan(survey_id, lan):
    try:
        # Check if survey exists in bitmap
        url_hash = binascii.crc32(survey_id.encode())
        if not redis_client.getbit('url_bitmap', url_hash):
            raise HTTPException(status_code=404, detail="Survey not found")
        
        # Retrieve survey from database
        survey = Survey.objects(id=survey_id).first()
        if not survey:
            raise HTTPException(status_code=404, detail="Survey not found in database")
        
        # Check if the requested language exists in translations
        translation = next((t for t in survey.translation if t.language == lan), None)
        if not translation:
            raise HTTPException(status_code=404, detail="Translation not found for the requested language")
        
        # Prepare the response data
        translated_questions = []
        for question in survey.questions:
            translated_question = {
                "id": question.id,
                "title": translation.translations.get(question.title, question.title),
                "choice_type": question.choice_type,
                "number_op": question.number_op,
                "required": question.required,
                "options": [
                    {
                        "id": option.id,
                        "title": translation.translations.get(option.title, option.title)
                    }
                    for option in question.options
                ],
                "max_selection": question.max_selection
            }
            translated_questions.append(translated_question)
        
        response_data = {
            "question": translated_questions
        }
        
        return response_data
    except HTTPException as e:
        raise e  # Giữ nguyên mã lỗi nếu đã là HTTPException

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve survey: {e}")

