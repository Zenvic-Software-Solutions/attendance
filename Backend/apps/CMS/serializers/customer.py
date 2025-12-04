from apps.ACCESS.models import User
from apps.BASE.serializers import ReadOnlySerializer,WriteOnlySerializer,read_serializer
from apps.CMS.models import Customer,ProofDocument,Centre,Loan
from rest_framework import serializers


class CentreReadSerializer(ReadOnlySerializer):
    class Meta(ReadOnlySerializer.Meta):
        model = Centre
        fields = [
            "id",
            "uuid",
            "identity"
        ]

class CentreWriteSerializer(WriteOnlySerializer):
    class Meta(WriteOnlySerializer.Meta):
        model = Centre
        fields = [
            "identity"
        ]


class CustomerReadSerializer(ReadOnlySerializer):
    centre_details = read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")
    class Meta(WriteOnlySerializer.Meta):
        model = Customer
        fields = [
            "id",
            "uuid",
            "identity",
            "phone_number",
            "aadhar_no",
            "centre", 
            "centre_details", 
        ]


class CustomerViewSerializer(ReadOnlySerializer):
    centre_details = read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")
    proof_image_details = read_serializer(ProofDocument,meta_fields=["id","uuid","file"])(source="proof_image",many=True)
    class Meta(WriteOnlySerializer.Meta):
        model = Customer
        fields = [
            "id",
            "uuid",
            "user",
            "identity",
            "phone_number",
            "address",
            "aadhar_no",
            "centre_details",
            "proof_image_details"
        ]
        


class CustomerWriteSerializer(WriteOnlySerializer):
    aadhar_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    proof_image = serializers.ListField(required=False)

    class Meta(WriteOnlySerializer.Meta):
        model = Customer
        fields = [
            "id",
            "identity",
            "phone_number",
            "address",
            "aadhar_no",
            "centre",
            "proof_image",
        ]

    def validate(self, attrs):
        # default values
        attrs["aadhar_no"] = attrs.get("aadhar_no") or None
        attrs["proof_image"] = attrs.get("proof_image") or []

        # unique phone check
        phone_number = attrs.get("phone_number")
        user = self.context["request"].user

        if phone_number:
            exists = Customer.objects.filter(
                user=user,                        
                phone_number=phone_number
            ).exclude(
                pk=self.instance.pk if self.instance else None
            ).exists()

            if exists:
                raise serializers.ValidationError({
                    "error": ["Phone number already exists."]
                })



        return attrs



class PhoneSerializer(ReadOnlySerializer):
    class Meta(WriteOnlySerializer.Meta):
        model = Customer
        fields = [
            "id",
            "uuid",
            "phone_number"
        ]






class CustomerLoanReadSerializer(ReadOnlySerializer): 
    customer_details = read_serializer(Customer,meta_fields=["id","uuid","identity","phone_number","address"],
                            init_fields_config={"centre_details":read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")})(source="customer")
    class Meta(ReadOnlySerializer.Meta):
        model = Loan
        fields = [
            "id",
            "uuid",
            "loan_title",
            "customer_details",
            "principal_amount",
            "interest_amount",
            "balance",
        ]

class NomineeLoanReadSerializer(ReadOnlySerializer):
    
    nominee_details = read_serializer(Customer,meta_fields=["id","uuid","identity","phone_number","address"],
                            init_fields_config={"centre_details":read_serializer(Centre,meta_fields=["id","uuid","identity"])(source="centre")})(source="nominee")
    class Meta(ReadOnlySerializer.Meta):
        model = Loan
        fields = [
            "id",
            "uuid",
            "loan_title",
            "nominee_details",
            "principal_amount",
            "interest_amount",
            "balance",
        ]