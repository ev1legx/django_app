import time
from django.http import JsonResponse

class SimpleThrottleMiddlewareNoCache:
    def __init__(self, get_response):
        self.get_response = get_response
        self.visits = {}
        self.wait_time = 1  # интервал между запросами в секундах

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')

        if not ip:
            # Если IP не найден — пропускаем без ограничения
            return self.get_response(request)

        now = time.time()
        last_visit = self.visits.get(ip)

        if last_visit and (now - last_visit) < self.wait_time:
            return JsonResponse(
                {"error": "Too many requests. Please wait before trying again."},
                status=429
            )

        self.visits[ip] = now

        response = self.get_response(request)
        return response