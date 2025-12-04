from apps.BASE.views import ListAPIViewSet,CUDAPIViewSet
from apps.CMS.models import Loan
from apps.CMS.serializers import LoanReadSerializer,LoanWriteSerializer,LoanViewSerializer
from apps.BASE.permissions import AuthenticatedAPIMixin

class LoanListAPIView(AuthenticatedAPIMixin, ListAPIViewSet):
    search_fields = ["loan_title","customer__identity"]
    filterset_fields = ["customer__centre"]
    serializer_class = LoanReadSerializer
    # queryset = Loan.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(user=user)




class LoanCUDAPIView(AuthenticatedAPIMixin,CUDAPIViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LoanViewAPI(ListAPIViewSet):
    # permission_classes = [AuthenticatedAPIMixin]
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        return Loan.objects.filter(uuid=uuid)
    serializer_class = LoanViewSerializer

