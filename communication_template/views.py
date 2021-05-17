from rest_framework.views import APIView
from rest_framework.response import Response
from communication_template.models import CommunicationMaster
from communication_template.serializer import CommunicationMasterSerializer

class CommunicationTemplateListView(APIView):
    def get(self, request, *args, **kwargs):
        docs = CommunicationMaster.objects.filter(is_deleted=False)
        serializer = CommunicationMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)

class CreateCommunicationTemplateView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        data_serializer = CommunicationMasterSerializer(data=data)
        data_serializer.is_valid(raise_exception=True)
        try:
            result_data = data_serializer.save(validated_data=data)
            result_serializer = CommunicationMasterSerializer(result_data)
            return Response(result_serializer.data, status=200)
        except:
            return Response(data={"message": "Constraint Violated"}, status=400)

class RetrievetCommunicationTemplateView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        template = CommunicationMaster.objects.get(communication_id=id, is_deleted=False)
        serializer = CommunicationMasterSerializer(template)
        return Response(serializer.data, status=200)

class UpdateCommunicationTemplateView(APIView):
    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        template = CommunicationMaster.objects.get(communication_id=id)
        data = self.request.data
        serializer = CommunicationMasterSerializer(template, data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.update(instance=template, validated_data=data)
            return Response(serializer.data, status=200)
        except:
            return Response(data = {"messege":"Constraint Violated"}, status=401)


class DeleteCommunicationTemplateView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            template = CommunicationMaster.objects.get(communication_id=id)
            template.is_deleted = True
            template.save()
            return Response(data={"message": "Record Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

