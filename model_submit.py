from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, BooleanField, DateTimeField

class Answer(EmbeddedDocument):
    question_id = IntField(required=True)
    choice_type = StringField(required=True, choices=['CSAT', 'text', 'single', 'multi'])
    answer = StringField()  # Dùng cho câu hỏi dạng text 
    answer_id = IntField()  # Dùng cho câu hỏi single-choice hoặc CSAT
    answer_ids = ListField(IntField())  # Dùng cho câu hỏi multi-choice
    max_selection = IntField()  # Số lượng tối đa lựa chọn
    num_selection = IntField()  # Số lượng lựa chọn thực tế của người dùng
    required = BooleanField(default=False)  # Câu hỏi có bắt buộc không
    counter = IntField(default = 1)

class SurveyResponse(Document):
    survey_id = StringField(required=True)  # Có thể dùng ReferenceField(Survey) nếu muốn liên kết
    email = StringField(required=True)
    name = StringField(required=True)
    phone = StringField(required=True)
    language = StringField(required=True)
    submitted_at = DateTimeField(required=True)
    answers = ListField(EmbeddedDocumentField(Answer))

    meta = {'collection': 'survey_responses'}  # Định nghĩa collection trong MongoDB
