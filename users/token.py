from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, token_arg, timestamp):
        user = token_arg[0]
        if "home" in token_arg[1]:
            user_req_for = user.home_permission
        elif "content" in token_arg[1]:
            user_req_for = user.content_permission
        
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active) + six.text_type(user_req_for)
        )
        
account_activation_token = TokenGenerator()