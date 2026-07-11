from rest_framework.throttling import SimpleRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginThrottle(SimpleRateThrottle):
    scope = 'login'

    def get_cache_key(self, request, view):
        return self.get_ident(request)

class ThrottledLoginView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]
