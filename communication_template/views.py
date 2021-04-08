from rest_framework.views import APIView
from rest_framework.response import Response
from communication_template.models import TemplateMaster
from communication_template.serializer import TemplateMasterSerializer

class TemplateListView(APIView):
    def get(self, request, *args, **kwargs):
        docs = TemplateMaster.objects.all()
        serializer = TemplateMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)

class CreateTemplateView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        data_serializer = TemplateMasterSerializer(data=data)
        data_serializer.is_valid(raise_exception=True)
        try:
            result_data = data_serializer.save()
            result_serializer = TemplateMasterSerializer(result_data)
        except:
            return Response(data = {"messege":"Constraint Violated"}, status=401)
        return Response(result_serializer.data, status=200)

class RetrievetTemplateView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        template = TemplateMaster.objects.get(template_id=id)
        serializer = TemplateMasterSerializer(template)
        return Response(serializer.data, status=200)

class UpdateTemplateView(APIView):
    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        template = TemplateMaster.objects.get(template_id=id)
        data = self.request.data
        serializer = TemplateMasterSerializer(template, data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.update(instance=template, validated_data=data)
            return Response(serializer.data, status=200)
        except:
            return Response(data = {"messege":"Constraint Violated"}, status=401)

class DeleteTemplateView(APIView):
    pass

