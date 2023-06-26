import json

def sending_jsonObject(current_object):
    data={
        "employee_name":current_object.employee_name,
        "role":current_object.role,
        "mobile_number":current_object.mobile_number,
        "email_id":current_object.email_id,
        "location":current_object.location,
        }
    json_data =json.dumps(data)
    print(type(json_data))
    return json_data
