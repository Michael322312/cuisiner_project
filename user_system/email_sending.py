from django.core.mail import send_mail

def send_hello():
    send_mail(
        "Hello!!",
        "Here is the message.",
        "cuisinersender@gmail.com",
        ["zomisha0808@gmail.com"],
        fail_silently=False,
    )

