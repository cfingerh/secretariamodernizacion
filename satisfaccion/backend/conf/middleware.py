from threading import current_thread
_requests = {}


def get_username():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t]

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _requests[current_thread()] = request
        response = self.get_response(request)

        return response