
def db_answer_to_string(input_list: list, headers: list) -> str:
    out_string = '<table border="1" cellpadding="5" cellspacing="0">'
    out_string += '<tr>'
    for header in headers:
        out_string += f'<td align="center"><strong>{header}</strong></td>'
    out_string += '</tr>'
    for el in input_list:
        out_string += '<tr>'
        for field in el:
            out_string += f'<td>{field if field is not None else " - "}</td>'
        out_string += '</tr>'
    out_string += '</table>'
    return out_string


def paramaters_to_db_condition(parameters: dict) -> str:
    db_rules_on_query = ''  # if not have parameters return empty string
    if parameters:
        db_rules_on_query = ' WHERE ' + ' AND '.join(f'{key}=?' for key in parameters.keys())
    return db_rules_on_query
