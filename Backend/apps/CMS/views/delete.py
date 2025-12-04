from rest_framework.views import APIView
from apps.CMS.models import Loan,Customer
from rest_framework.response import Response

class DeleteAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        uuid = request.data.get("uuid")

        if not uuid:
            return Response({"error": "UUID is required"}, status=400)

        # List of models to check
        models_to_check = [Customer, Loan]

        deleted = False

        for model in models_to_check:
            try:
                obj = model.objects.get(uuid=uuid)
                obj.is_deleted == True
                obj.save()
                return Response({
                    "message": f"{model.__name__} deleted successfully"
                }, status=200)
            except model.DoesNotExist:
                continue

        if not deleted:
            return Response({"error": "Object not found"}, status=404)
