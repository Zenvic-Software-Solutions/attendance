from .customer import (
    CentreWriteSerializer,
    CentreReadSerializer,
    CustomerReadSerializer,CustomerWriteSerializer,CustomerViewSerializer,PhoneSerializer,
    CustomerLoanReadSerializer,
    NomineeLoanReadSerializer,
)

from .loan import LoanReadSerializer,LoanWriteSerializer,LoanViewSerializer
from .payment import LoanNextDueSerializer,PaymentDueSerializer,CollectionSerializer
from .reports import LoanReportSerializer, DailyReportSerializer, CenterReportSerializer, CustomerReportSerializer