from apps.BASE.models import BaseModel,MAX_CHAR_FIELD_LENGTH,DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
from apps.ACCESS.models import User
from django.db import models

class Centre(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    identity =  models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)



class ProofDocument(BaseModel):
    file = models.ImageField(upload_to="files/proof/images")



class Customer(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    identity = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    phone_number = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH)
    address = models.TextField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    aadhar_no = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    centre = models.ForeignKey(Centre,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    proof_image = models.ManyToManyField(ProofDocument,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "phone_number"], name="unique_user_phone"
            )
        ]