from rest_framework import serializers
from django.db import transaction
from communication_template.models import TemplateMaster,TemplateType

class TemplateTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateType
        fields = (
            "temp_type",
        )

class TemplateMasterSerializer(serializers.ModelSerializer):

    type = TemplateTypeSerializer(required=False)

    class Meta:
        model = TemplateMaster

        fields = (
            "template_id",
            "template_name",
            "subject",
            "body",
            "is_active",
            "is_deleted",
            "type",
        )

    def save(self):
        with transaction.atomic():
            type_data = dict(self.data['type'])
            type = TemplateType.objects.get(temp_type__exact = type_data['temp_type'])
            template = TemplateMaster.objects.create(
                template_name = self.data['template_name'],
                subject = self.data['subject'],
                body = self.data['body'],
                is_active = self.data['is_active'],
            )
            template.type = type
            template.save()
            return template


    def update(self, instance, validated_data):
        print("Instance",instance)
        print("Validated_data",validated_data['type']['temp_type'])

        if instance:
            instance.template_name = (
                validated_data['template_name'] if validated_data['template_name'] else instance.template_name
            )
            instance.subject = (
                validated_data['subject'] if validated_data['subject'] else instance.subject
            )
            instance.body = (
                validated_data['body'] if validated_data['body'] else instance.body
            )
            instance.is_active = (
                validated_data['is_active'] if validated_data['is_active'] else instance.is_active
            )
            instance.is_deleted = (
                validated_data['is_deleted'] if validated_data['is_deleted'] else instance.is_deleted
            )
            temp_type = validated_data['type']['temp_type']
            type = TemplateType.objects.get(temp_type__exact=temp_type)

            instance.type = type
            instance.save()