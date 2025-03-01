import unittest
from fastapi.testclient import TestClient
from main import app
from models.model_survey import Survey
from models.model_submit import SurveyResponse
from initialize.redis_config import redis_client

client = TestClient(app)

class TestSurvey(unittest.TestCase):

    def setUp(self):
        # Clear the database and cache before each test
        Survey.objects.delete()
        SurveyResponse.objects.delete()
        redis_client.flushall()

    def test_create_survey_success(self):
        data = {
            "default_lan": "vietnam",
            "translation": {
                "vietnam": {
                    "question_1_title": "Đây là title của question 1 (CSAT)",
                    "question_2_title": "Đây là title của question 2 (Văn bản)",
                    "question_3_title": "Đây là title của question 3 (Đơn)",
                    "question_4_title": "Đây là title của question 4 (Đa)",
                    "question_1_an_1": "Đây là đáp án 1 của q1",
                    "question_1_an_2": "Đây là đáp án 2 của q1",
                    "question_1_an_3": "Đây là đáp án 3 của q1",
                    "question_1_an_4": "Đây là đáp án 4 của q1",
                    "question_1_an_5": "Đây là đáp án 5 của q1",
                    "question_3_an_1": "Đây là đáp án 1 của q3",
                    "question_3_an_2": "Đây là đáp án 2 của q3",
                    "question_4_an_1": "Đây là đáp án 1 của q4",
                    "question_4_an_2": "Đây là đáp án 2 của q4",
                    "question_4_an_3": "Đây là đáp án 3 của q4"
                },
                "us": {
                    "question_1_title": "This is the title of question 1 (CSAT)",
                    "question_2_title": "This is the title of question 2 (Text)",
                    "question_3_title": "This is the title of question 3 (Single)",
                    "question_4_title": "This is the title of question 4 (Multi)",
                    "question_1_an_1": "This is answer 1 of q1",
                    "question_1_an_2": "This is answer 2 of q1",
                    "question_1_an_3": "This is answer 3 of q1",
                    "question_1_an_4": "This is answer 4 of q1",
                    "question_1_an_5": "This is answer 5 of q1",
                    "question_3_an_1": "This is answer 1 of q3",
                    "question_3_an_2": "This is answer 2 of q3",
                    "question_4_an_1": "This is answer 1 of q4",
                    "question_4_an_2": "This is answer 2 of q4",
                    "question_4_an_3": "This is answer 3 of q4"
                }
            },
            "question": [
                {
                    "id": 1,
                    "title": "question_1_title",
                    "choice_type": "CSAT",
                    "number_op": 5,
                    "required": True,
                    "options": [
                        {"id": 1, "title": "question_1_an_1"},
                        {"id": 2, "title": "question_1_an_2"},
                        {"id": 3, "title": "question_1_an_3"},
                        {"id": 4, "title": "question_1_an_4"},
                        {"id": 5, "title": "question_1_an_5"}
                    ],
                    "max_selection": None
                },
                {
                    "id": 2,
                    "title": "question_2_title",
                    "choice_type": "text",
                    "number_op": None,
                    "required": False,
                    "options": [],
                    "max_selection": None
                },
                {
                    "id": 3,
                    "title": "question_3_title",
                    "choice_type": "single",
                    "number_op": None,
                    "required": True,
                    "options": [
                        {"id": 1, "title": "question_3_an_1"},
                        {"id": 2, "title": "question_3_an_2"}
                    ],
                    "max_selection": None
                },
                {
                    "id": 4,
                    "title": "question_4_title",
                    "choice_type": "multi",
                    "number_op": None,
                    "required": False,
                    "options": [
                        {"id": 1, "title": "question_4_an_1"},
                        {"id": 2, "title": "question_4_an_2"},
                        {"id": 3, "title": "question_4_an_3"}
                    ],
                    "max_selection": 2
                }
            ]
        }
        response = client.post("/filum/survey", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("survey_id", response.json())

    def test_create_survey_fail_no_csat(self):
        data = {
            "default_lan": "vietnam",
            "translation": {
                "vietnam": {
                    "question_2_title": "Đây là title của question 2 (Văn bản)",
                    "question_3_title": "Đây là title của question 3 (Đơn)",
                    "question_4_title": "Đây là title của question 4 (Đa)",
                    "question_3_an_1": "Đây là đáp án 1 của q3",
                    "question_3_an_2": "Đây là đáp án 2 của q3",
                    "question_4_an_1": "Đây là đáp án 1 của q4",
                    "question_4_an_2": "Đây là đáp án 2 của q4",
                    "question_4_an_3": "Đây là đáp án 3 của q4"
                },
                "us": {
                    "question_2_title": "This is the title of question 2 (Text)",
                    "question_3_title": "This is the title of question 3 (Single)",
                    "question_4_title": "This is the title of question 4 (Multi)",
                    "question_3_an_1": "This is answer 1 of q3",
                    "question_3_an_2": "This is answer 2 of q3",
                    "question_4_an_1": "This is answer 1 of q4",
                    "question_4_an_2": "This is answer 2 of q4",
                    "question_4_an_3": "This is answer 3 of q4"
                }
            },
            "question": [
                {
                    "id": 2,
                    "title": "question_2_title",
                    "choice_type": "text",
                    "number_op": None,
                    "required": False,
                    "options": [],
                    "max_selection": None
                },
                {
                    "id": 3,
                    "title": "question_3_title",
                    "choice_type": "single",
                    "number_op": None,
                    "required": True,
                    "options": [
                        {"id": 1, "title": "question_3_an_1"},
                        {"id": 2, "title": "question_3_an_2"}
                    ],
                    "max_selection": None
                },
                {
                    "id": 4,
                    "title": "question_4_title",
                    "choice_type": "multi",
                    "number_op": None,
                    "required": False,
                    "options": [
                        {"id": 1, "title": "question_4_an_1"},
                        {"id": 2, "title": "question_4_an_2"},
                        {"id": 3, "title": "question_4_an_3"}
                    ],
                    "max_selection": 2
                }
            ]
        }
        response = client.post("/filum/survey", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Survey must have at least one CSAT question")

    def test_create_survey_fail_no_default_language(self):
        data = {
            "translation": {
                "vietnam": {
                    "question_1_title": "Đây là title của question 1 (CSAT)",
                    "question_2_title": "Đây là title của question 2 (Văn bản)",
                    "question_3_title": "Đây là title của question 3 (Đơn)",
                    "question_4_title": "Đây là title của question 4 (Đa)",
                    "question_1_an_1": "Đây là đáp án 1 của q1",
                    "question_1_an_2": "Đây là đáp án 2 của q1",
                    "question_1_an_3": "Đây là đáp án 3 của q1",
                    "question_1_an_4": "Đây là đáp án 4 của q1",
                    "question_1_an_5": "Đây là đáp án 5 của q1",
                    "question_3_an_1": "Đây là đáp án 1 của q3",
                    "question_3_an_2": "Đây là đáp án 2 của q3",
                    "question_4_an_1": "Đây là đáp án 1 của q4",
                    "question_4_an_2": "Đây là đáp án 2 của q4",
                    "question_4_an_3": "Đây là đáp án 3 của q4"
                },
                "us": {
                    "question_1_title": "This is the title of question 1 (CSAT)",
                    "question_2_title": "This is the title of question 2 (Text)",
                    "question_3_title": "This is the title of question 3 (Single)",
                    "question_4_title": "This is the title of question 4 (Multi)",
                    "question_1_an_1": "This is answer 1 of q1",
                    "question_1_an_2": "This is answer 2 of q1",
                    "question_1_an_3": "This is answer 3 of q1",
                    "question_1_an_4": "This is answer 4 of q1",
                    "question_1_an_5": "This is answer 5 of q1",
                    "question_3_an_1": "This is answer 1 of q3",
                    "question_3_an_2": "This is answer 2 of q3",
                    "question_4_an_1": "This is answer 1 of q4",
                    "question_4_an_2": "This is answer 2 of q4",
                    "question_4_an_3": "This is answer 3 of q4"
                }
            },
            "question": [
                {
                    "id": 1,
                    "title": "question_1_title",
                    "choice_type": "CSAT",
                    "number_op": 5,
                    "required": True,
                    "options": [
                        {"id": 1, "title": "question_1_an_1"},
                        {"id": 2, "title": "question_1_an_2"},
                        {"id": 3, "title": "question_1_an_3"},
                        {"id": 4, "title": "question_1_an_4"},
                        {"id": 5, "title": "question_1_an_5"}
                    ],
                    "max_selection": None
                },
                {
                    "id": 2,
                    "title": "question_2_title",
                    "choice_type": "text",
                    "number_op": None,
                    "required": False,
                    "options": [],
                    "max_selection": None
                },
                {
                    "id": 3,
                    "title": "question_3_title",
                    "choice_type": "single",
                    "number_op": None,
                    "required": True,
                    "options": [
                        {"id": 1, "title": "question_3_an_1"},
                        {"id": 2, "title": "question_3_an_2"}
                    ],
                    "max_selection": None
                },
                {
                    "id": 4,
                    "title": "question_4_title",
                    "choice_type": "multi",
                    "number_op": None,
                    "required": False,
                    "options": [
                        {"id": 1, "title": "question_4_an_1"},
                        {"id": 2, "title": "question_4_an_2"},
                        {"id": 3, "title": "question_4_an_3"}
                    ],
                    "max_selection": 2
                }
            ]
        }
        response = client.post("/filum/survey", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Survey must have a default language")

    def test_create_survey_fail_no_questions(self):
        data = {
            "default_lan": "vietnam",
            "translation": {
                "vietnam": {
                    "question_1_title": "Đây là title của question 1 (CSAT)",
                    "question_2_title": "Đây là title của question 2 (Văn bản)",
                    "question_3_title": "Đây là title của question 3 (Đơn)",
                    "question_4_title": "Đây là title của question 4 (Đa)",
                    "question_1_an_1": "Đây là đáp án 1 của q1",
                    "question_1_an_2": "Đây là đáp án 2 của q1",
                    "question_1_an_3": "Đây là đáp án 3 của q1",
                    "question_1_an_4": "Đây là đáp án 4 của q1",
                    "question_1_an_5": "Đây là đáp án 5 của q1",
                    "question_3_an_1": "Đây là đáp án 1 của q3",
                    "question_3_an_2": "Đây là đáp án 2 của q3",
                    "question_4_an_1": "Đây là đáp án 1 của q4",
                    "question_4_an_2": "Đây là đáp án 2 của q4",
                    "question_4_an_3": "Đây là đáp án 3 của q4"
                },
                "us": {
                    "question_1_title": "This is the title of question 1 (CSAT)",
                    "question_2_title": "This is the title of question 2 (Text)",
                    "question_3_title": "This is the title of question 3 (Single)",
                    "question_4_title": "This is the title of question 4 (Multi)",
                    "question_1_an_1": "This is answer 1 of q1",
                    "question_1_an_2": "This is answer 2 of q1",
                    "question_1_an_3": "This is answer 3 of q1",
                    "question_1_an_4": "This is answer 4 of q1",
                    "question_1_an_5": "This is answer 5 of q1",
                    "question_3_an_1": "This is answer 1 of q3",
                    "question_3_an_2": "This is answer 2 of q3",
                    "question_4_an_1": "This is answer 1 of q4",
                    "question_4_an_2": "This is answer 2 of q4",
                    "question_4_an_3": "This is answer 3 of q4"
                }
            },
            "question": []
        }
        response = client.post("/filum/survey", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Survey must have between 1 and 10 questions")

    def test_submit_survey_fail_required_question_not_answered(self):
        # Create a survey first
        survey_data = {
            "default_lan": "vietnam",
            "translation": {
                "vietnam": {
                    "question_1_title": "Đây là title của question 1 (CSAT)",
                    "question_2_title": "Đây là title của question 2 (Văn bản)",
                    "question_3_title": "Đây là title của question 3 (Đơn)",
                    "question_4_title": "Đây là title của question 4 (Đa)",
                    "question_1_an_1": "Đây là đáp án 1 của q1",
                    "question_1_an_2": "Đây là đáp án 2 của q1",
                    "question_1_an_3": "Đây là đáp án 3 của q1",
                    "question_1_an_4": "Đây là đáp án 4 của q1",
                    "question_1_an_5": "Đây là đáp án 5 của q1",
                    "question_3_an_1": "Đây là đáp án 1 của q3",
                    "question_3_an_2": "Đây là đáp án 2 của q3",
                    "question_4_an_1": "Đây là đáp án 1 của q4",
                    "question_4_an_2": "Đây là đáp án 2 của q4",
                    "question_4_an_3": "Đây là đáp án 3 của q4"
                },
                "us": {
                    "question_1_title": "This is the title of question 1 (CSAT)",
                    "question_2_title": "This is the title of question 2 (Text)",
                    "question_3_title": "This is the title of question 3 (Single)",
                    "question_4_title": "This is the title of question 4 (Multi)",
                    "question_1_an_1": "This is answer 1 of q1",
                    "question_1_an_2": "This is answer 2 of q1",
                    "question_1_an_3": "This is answer 3 of q1",
                    "question_1_an_4": "This is answer 4 of q1",
                    "question_1_an_5": "This is answer 5 of q1",
                    "question_3_an_1": "This is answer 1 of q3",
                    "question_3_an_2": "This is answer 2 of q3",
                    "question_4_an_1": "This is answer 1 of q4",
                    "question_4_an_2": "This is answer 2 of q4",
                    "question_4_an_3": "This is answer 3 of q4"
                }
            },
            "question": [
                {
                    "id": 1,
                    "title": "question_1_title",
                    "choice_type": "CSAT",
                    "number_op": 5,
                    "required": True,
                    "options": [
                        {"id": 1, "title": "question_1_an_1"},
                        {"id": 2, "title": "question_1_an_2"},
                        {"id": 3, "title": "question_1_an_3"},
                        {"id": 4, "title": "question_1_an_4"},
                        {"id": 5, "title": "question_1_an_5"}
                    ],
                    "max_selection": None
                },
                {
                    "id": 2,
                    "title": "question_2_title",
                    "choice_type": "text",
                    "number_op": None,
                    "required": False,
                    "options": [],
                    "max_selection": None
                },
                {
                    "id": 3,
                    "title": "question_3_title",
                    "choice_type": "single",
                    "number_op": None,
                    "required": True,
                    "options": [
                        {"id": 1, "title": "question_3_an_1"},
                        {"id": 2, "title": "question_3_an_2"}
                    ],
                    "max_selection": None
                },
                {
                    "id": 4,
                    "title": "question_4_title",
                    "choice_type": "multi",
                    "number_op": None,
                    "required": False,
                    "options": [
                        {"id": 1, "title": "question_4_an_1"},
                        {"id": 2, "title": "question_4_an_2"},
                        {"id": 3, "title": "question_4_an_3"}
                    ],
                    "max_selection": 2
                }
            ]
        }
        survey_response = client.post("/filum/survey", json=survey_data)
        survey_id = survey_response.json()["survey_id"]

        # Submit a survey response without answering required questions
        response_data = {
            "email":"Kinghuynh@gmail.com",
    "name":"Huynh Bao King",
    "phone":"0381231312312",
    "language": "vietnam",
    "submitted_at": "2025-02-28T12:34:56Z",
            "answers": [
                {
                    "question_id": 2,
                    "answer_id": None
                },
                {
                    "question_id": 3,
                    "answer_id": None
                }
            ]
        }
        response = client.post(f"{survey_id}", json=response_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "You must complete all required questions")

if __name__ == '__main__':
    unittest.main()
