from unittest.mock import MagicMock


class FakeDBConnectionHandler:
    def __init__(self, session):
        self.session = session

    def get_session(self):
        return self.session



def get_error_msg(exc_info, field):
    errors = exc_info.value.errors()
    for error in errors:
        if error['loc'][-1] == field:
            return error['msg']
    return None


async def _call_handler(handler, exception):
    return await handler(MagicMock(), exception)
