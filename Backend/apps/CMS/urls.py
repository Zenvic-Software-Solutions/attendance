from rest_framework.routers import SimpleRouter
from django.urls import path
from apps.BASE.views import get_upload_api_view
#Bulk-Upload-Files
from HELPERS import BulkFileUploadView, ActiveStatusChange, ArchieveStatusChange
from apps.CMS.views import (
    CentreListAPIView,
    CentreCUDAPIView,
    CustomerListAPIView,
    CustomerCUDAPIView,
    LoanListAPIView,
    LoanCUDAPIView,
    LoanViewAPI,
    CustomerRetrieveAPIView,
    Dashboard,
    LoanNextDueListAPIView,
    PaymentListAPIView,
    PhoneAPIVIEW,
    PaymentCreateAPIView,
    ReportsAPIView,
    NomineeLoanAPIVIew,
    CustomerLoanAPIVIew,
    LoanReportExportAPIView,
    PaymentReportExportAPIView,
    TodayPaymentReportExportAPIView,
    LoanBulkUploadAPIView,
    LoanBulkDownloadSampleAPIView,
    DeleteAPIView,
    CollectionAPIView,
    PaymentReportAPIView,
    
)
from apps.CMS.models import ProofDocument,LoanBill

app_name = "cms"
API_URL_PREFIX = "api/"

router = SimpleRouter()
router.register("centre/cud",CentreCUDAPIView,basename="centre-cud")
router.register("customer/cud",CustomerCUDAPIView,basename="customer-cud")
router.register("loan/list",LoanListAPIView,basename="loan-list")
router.register("loan/cud",LoanCUDAPIView,basename="loan-cud")
# router.register("payment/list",PaymentListAPIView,basename="payment-list")
router.register("loan/next-due-list", LoanNextDueListAPIView, basename="loan-next-due-list")

urlpatterns = [
    path("proof/image/",get_upload_api_view(ProofDocument).as_view()),
    path("bill/image/",get_upload_api_view(LoanBill).as_view()),
    path("loan/retrieve/<uuid>/",LoanViewAPI.as_view({'get':'list'})),
    path("customer/list/",CustomerListAPIView.as_view({'get':'list'})),
    path("centre/list/",CentreListAPIView.as_view({'get':'list'})),
    path("customer/retrieve/<uuid>/",CustomerRetrieveAPIView.as_view({'get':'list'})),
    path("customer/loan/<uuid>/",CustomerLoanAPIVIew.as_view({'get':'list'})),
    path("nominee/loan/<uuid>/",NomineeLoanAPIVIew.as_view({'get':'list'})),
    path("phone/list/",PhoneAPIVIEW.as_view({'get':'list'})),
    path("payment/list/<uuid>/",PaymentListAPIView.as_view({'get':'list'})),
    path("collection/list/",CollectionAPIView.as_view({'get':'list'})),
    path("dashboard/",Dashboard.as_view()),
    path("report/payment/export/", PaymentReportExportAPIView.as_view(), name="payment-report-export"),
    path("report/payment/today/export/", TodayPaymentReportExportAPIView.as_view(), name="today-payment-report"),
    path("report/payment/", PaymentReportAPIView.as_view(), name="payment-report"),
    path("loan/bulk-upload/", LoanBulkUploadAPIView.as_view()),
    
    path("loan/bulk/sample/", LoanBulkDownloadSampleAPIView.as_view(), name="loan-bulk-sample"),
    path("reports/loan/", LoanReportExportAPIView.as_view(), name="loan-report"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("reports/", ReportsAPIView.as_view(), name="reports"),
    path("delete/",DeleteAPIView.as_view())
    
   
] + router.urls
