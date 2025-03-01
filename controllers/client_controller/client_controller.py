from initialize.redis_config import redis_client
from models.model_survey import Survey
from models.model_submit import SurveyResponse, Answer
import binascii
import json
from datetime import datetime

def create_client_survey_controller(survey_id, data):
    try:
        # Check if survey exists in bitmap
        url_hash = binascii.crc32(survey_id.encode())
        if not redis_client.getbit('url_bitmap', url_hash):
            return {"error": "Survey not found"}
        
        # Retrieve survey from database to validate required questions
        survey = Survey.objects(id=survey_id).first()
        if not survey:
            return {"error": "Survey not found in database"}
        
        # Validate required questions
        required_questions = {q.id for q in survey.questions if q.required}
        answered_questions = {ans['question_id'] for ans in data['answers']}
        if not required_questions.issubset(answered_questions):
            return {"error": "You must complete all required questions"}
        
        # Validate max_selection
        for ans in data['answers']:
            question = next((q for q in survey.questions if q.id == ans['question_id']), None)
            if question and question.max_selection is not None:
                if ans.get('num_selection', 0) > question.max_selection:
                    return {"error": f"Question {ans['question_id']} exceeds max selection limit"}
        
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
    except Exception as e:
        return {"error": f"Failed to submit survey response: {e}"}

def controller_get_survey_from_cache(survey_id):
    try:
        cached_survey = redis_client.get(f"url:{survey_id}")
        if cached_survey:
            return json.loads(cached_survey.decode('utf-8'))
        else:
            return None
    except Exception as e:
        return {"error": f"Failed to retrieve survey from cache: {e}"}

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
            return {"error": "Survey not found"}
        
        # If found in bitmap, retrieve from database
        survey = Survey.objects(id=survey_id).first()
        if survey:
            return json.loads(survey.to_json())
        else:
            return {"error": "Survey not found in database"}
    except Exception as e:
        return {"error": f"Failed to retrieve survey: {e}"}