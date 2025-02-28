from mongoengine import Document, StringField, BooleanField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, MapField

class Option(EmbeddedDocument):
    id = IntField(required=True)
    title = StringField(required=True)

class Question(EmbeddedDocument):
    id = IntField(required=True)
    title = StringField(required=True)
    choice_type = StringField(required=True, choices=['CSAT', 'text', 'single', 'multi'])
    number_op = IntField()
    required = BooleanField(default=False)
    options = ListField(EmbeddedDocumentField(Option))
    max_selection = IntField()

class Translation(EmbeddedDocument):
    language = StringField(required=True)
    translations = MapField(StringField(), required=True)

class Survey(Document):
    default_lan = StringField(required=True)
    translation = ListField(EmbeddedDocumentField(Translation), required=True)
    questions = ListField(EmbeddedDocumentField(Question))
