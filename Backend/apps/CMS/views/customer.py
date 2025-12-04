from apps.BASE.views import AppAPIView, ListAPIViewSet, CUDAPIViewSet
from apps.CMS.models import Centre, Customer,Loan
from apps.CMS.serializers import (
    CentreWriteSerializer,
    CentreReadSerializer,
    CustomerReadSerializer, CustomerWriteSerializer, CustomerViewSerializer,
    PhoneSerializer,
    NomineeLoanReadSerializer,
    CustomerLoanReadSerializer
)
from apps.BASE.permissions import AuthenticatedAPIMixin, NonAuthenticatedAPIMixin
from apps.BASE.pagination import CommonPagination
class CentreListAPIView(ListAPIViewSet):
    search_fields = ["identity"]
    pagination_class = CommonPagination
    def get_queryset(self):
        user =self.request.user
        return Centre.objects.filter(user =user)
    serializer_class = CentreReadSerializer


class CentreCUDAPIView(AuthenticatedAPIMixin,CUDAPIViewSet):
    # permission_classes = [AuthenticatedAPIMixin]
    queryset = Centre.objects.all()
    serializer_class = CentreWriteSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerListAPIView(ListAPIViewSet):
    # def get_queryset(self):
    #     user = self.request.user
    #     return Customer.objects.filter(user=user)
    search_fields = [
        "identity",
        "phone_number",
        "aadhar_no",
        "centre__identity",
    ]
    
    filterset_fields = ["centre"]

    def get_queryset(self):
        user = self.request.user

        # Only customers who actually purchased a loan
        purchased_customer_ids = Loan.objects.filter(
            user=user
        ).values_list("customer_id", flat=True)

        return Customer.objects.filter(
            user=user,
            id__in=purchased_customer_ids
        )
    serializer_class = CustomerReadSerializer


class CustomerCUDAPIView(AuthenticatedAPIMixin, CUDAPIViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerRetrieveAPIView(ListAPIViewSet):
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        return Customer.objects.filter(uuid=uuid)

    serializer_class = CustomerViewSerializer


class PhoneAPIVIEW(ListAPIViewSet):
    search_fields = ["phone_number", "identity"]
    filterset_fields = ["phone_number"]
    
    pagination_class = CommonPagination
    
    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(user=user)

    serializer_class = PhoneSerializer



class CustomerLoanAPIVIew(ListAPIViewSet):
    serializer_class = CustomerLoanReadSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        customer = Customer.objects.get(uuid =uuid)
        return Loan.objects.filter(customer =customer)
class NomineeLoanAPIVIew(ListAPIViewSet):
    serializer_class = NomineeLoanReadSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        nominee = Customer.objects.get(uuid =uuid)
        return Loan.objects.filter(nominee =nominee)