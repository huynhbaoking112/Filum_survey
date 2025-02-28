def create_client_survey_controller(survey_id, data):
    return {"message": "Create from client",
            "data": data 
            }


def read_client_survey_controller(survey_id):
    return {"message" : "Read from client "}