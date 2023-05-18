from django.core.mail import send_mail 


def send_activation_code(email, activation_code):
    message = f'Hello, you have registered in our site. Please go throgh account activation please. Your code: {activation_code}'
    send_mail(
        'Activation for user in Site <site name>', message, 'settings@mail.com',[email]
    )

def send_verification_code(email, verification):
    message = f'Hello, '
    