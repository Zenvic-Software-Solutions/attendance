from apps.BASE.views import AppAPIView

class ActiveStatusChange(AppAPIView):
    def post(self, request, *args, **kwargs):
        uuid = request.data.get("uuid")
        model_name = request.data.get("model")

        if not uuid or not model_name:
            return self.send_error_response({"error": "Both 'uuid' and 'model' are required."})
        
        try:
            from django.apps import apps
            model = apps.get_model(app_label='CMS', model_name=model_name)
        except LookupError:
            return self.send_error_response({"error": f"Model '{model_name}' does not exist."})

        try:
            obj = model.objects.get(uuid=uuid)
            obj.is_active = not obj.is_active 
            print(obj.is_active)
            obj.save()
        except model.DoesNotExist:
            return self.send_error_response({"error": f"No object found with uuid '{uuid}' in model '{model_name}'."})
        except AttributeError:
            return self.send_error_response({"error": "The model does not have a 'status' field."})
        except Exception as e:
            return self.send_error_response({"error": str(e)})

        return self.send_response({"message": "Active status changed successfully."})


class ArchieveStatusChange(AppAPIView):
    def post(self, request, *args, **kwargs):
        uuid = request.data.get("uuid")
        model_name = request.data.get("model")

        if not uuid or not model_name:
            return self.send_error_response({"error": "Both 'uuid' and 'model' are required."})
        
        try:
            from django.apps import apps
            model = apps.get_model(app_label='CMS', model_name=model_name)
        except LookupError:
            return self.send_error_response({"error": f"Model '{model_name}' does not exist."})

        try:
            obj = model.objects.get(uuid=uuid)
            obj.is_deleted = not obj.is_deleted 
            obj.save()
        except model.DoesNotExist:
            return self.send_error_response({"error": f"No object found with uuid '{uuid}' in model '{model_name}'."})
        except AttributeError:
            return self.send_error_response({"error": "The model does not have a 'status' field."})
        except Exception as e:
            return self.send_error_response({"error": str(e)})

        return self.send_response({"message": "Deleted status changed successfully."})
