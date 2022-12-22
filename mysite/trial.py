import init_django
from datacenter.models import Customer, Resource

customer_name = 'customer_8'
customer = Customer.objects.get(pk=customer_name)

print(customer.customer_secret)