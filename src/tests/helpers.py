def get_error_msg(exc_info, field):
    errors = exc_info.value.errors()
    for error in errors:
        if error['loc'][-1] == field:
            return error['msg']
    return None
