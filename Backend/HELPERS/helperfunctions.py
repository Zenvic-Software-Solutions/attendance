import requests
from datetime import datetime, timezone

from apps.BASE.views import AppAPIView 

def time_since(created_at):
    """
    Calculate the time elapsed since the given `created_at` datetime.
    
    Args:
        created_at (datetime): The datetime object to calculate time since.
        
    Returns:
        str: A human-readable string representing the time since `created_at`.
    """
    if not isinstance(created_at, datetime):
        raise ValueError("created_at must be a datetime object.")

    now = datetime.now(timezone.utc)
    delta = now - created_at

    days = delta.days
    seconds = delta.seconds

    if days > 365:
        years = days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif days > 30:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif days > 0:
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif seconds > 3600:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds > 60:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"



def get_city_by_pincode(pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data[0]['Status'] == 'Success':
            post_offices = data[0]['PostOffice']
            if post_offices:
                for office in post_offices:
                    # print(f"City: {office['Division']}, State: {office['State']}, District: {office['District']}")
                    data ={
                        "city": office['Division'],
                        "district": office['District'],
                        "state": office['State'],
                    }
                    return data
            else:
                return {"detail":"No post offices found for this PIN code."}
        else:
            return {"error":"Invalid PIN code."}
    else:
        return {"detail":"Failed to fetch data."}

# pincode = "627501" 
# print(get_city_by_pincode(pincode))


from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key())


# class GetNextInvoiceIDView(AppAPIView):
#     """
#     A view to fetch the next invoice ID.
#     """
#     def get(self, request, *args, **kwargs):
#         try:
#             invoice_id = ""
#             last_invoice = Invoice.objects.all().order_by("id").last()
#             if last_invoice:
#                 last_invoice_id = last_invoice.invoice_id
#                 invoice_number = int(last_invoice_id.split("SDT")[-1]) + 1
#                 invoice_id = f"SDT{invoice_number:04d}"  # Format the invoice ID
#             else:
#                 invoice_id = "SDT0001"  # Start from the first invoice ID if none exist
#             return self.send_response({"next_invoice_id": invoice_id})
#         except Exception as e:
#             return self.send_error_response({"error": str(e)})
