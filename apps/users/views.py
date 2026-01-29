from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        # Redirect doctors to admin, and patients to their dashboard
        if self.request.user.is_doctor or self.request.user.is_staff:
            return '/admin/'
        return reverse_lazy('patient_dashboard')