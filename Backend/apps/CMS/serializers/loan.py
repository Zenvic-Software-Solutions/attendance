from apps.CMS.models import Loan,Customer,LoanBill,Centre
from apps.ACCESS.models import User
from apps.BASE.serializers import ReadOnlySerializer,WriteOnlySerializer,read_serializer



class LoanReadSerializer(ReadOnlySerializer):
    customer_details = read_serializer(Customer,meta_fields=["id","uuid","identity","phone_number","address"],
                            init_fields_config={"centre_details":read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")})(source="customer")
    # centre_details=read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")
    nominee_details = read_serializer(Customer,meta_fields=["id","uuid","identity"])(source="nominee")
    class Meta(ReadOnlySerializer.Meta):
        model = Loan
        fields = [
            "id",
            "uuid",
            "loan_id",
            "loan_title",
            "customer_details",
            "principal_amount",
            "interest_amount",
            "nominee_details",
            "balance",
        ]
class LoanViewSerializer(ReadOnlySerializer):
    bill_image_details = read_serializer(LoanBill,meta_fields=["id","uuid","file"])(source="bill_image",many=True)
    customer_details = read_serializer(Customer,meta_fields=["id","uuid","identity","phone_number","address"],
                            init_fields_config={"centre_details":read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")})(source="customer")
    nominee_details = read_serializer(Customer,meta_fields=["id","uuid","identity","phone_number","address"],
                            init_fields_config={"centre_details":read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")})(source="nominee")
    
    # centre_details=read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")
    class Meta(ReadOnlySerializer.Meta):
        model = Loan
        fields = [
            "id",
            "uuid",
            "loan_id",
            "loan_title",
            "customer_details",
            "nominee_details",
            "principal_amount",
            "interest_amount",
            "balance",
            "total_week",
            "balance_week",
            "initiated_date",
            "loan_date",
            # "due_date",
            "bill_image_details",
            # "centre_details",
            # "created_at",
        ]


class LoanWriteSerializer(WriteOnlySerializer):
    class Meta(WriteOnlySerializer.Meta):
        model = Loan
        fields = [
            "loan_title",
            "principal_amount",
            "interest_amount",
            "initiated_date",
            # "due_date",
            "balance",
            "customer",
            "nominee",
            "total_week",
            "balance_week",
            "bill_image",
            "loan_date"
        ]
