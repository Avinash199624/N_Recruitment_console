from job_posting.models import UserJobPositions
from rest_framework import serializers

class ApplicantJobPositionsSerializer(serializers.ModelSerializer):

    notification_id = serializers.SerializerMethodField(
        method_name="get_notification_id", read_only=True
    )

    description = serializers.SerializerMethodField(
        method_name="get_description", read_only=True
    )

    date_of_application = serializers.SerializerMethodField(
        method_name="get_date_of_application", read_only=True
    )

    date_of_closing = serializers.SerializerMethodField(
        method_name="get_date_of_closing", read_only=True
    )

    hiring_status = serializers.SerializerMethodField(
        method_name="get_hiring_status", read_only=True
    )

    class Meta:
        model = UserJobPositions
        fields = (
            "id",
            "notification_id",
            "description",
            "date_of_application",
            "date_of_closing",
            "hiring_status",
        )

    def get_notification_id(self,obj):
        notification_id = obj.job_posting.notification_id
        return notification_id

    def get_description(self,obj):
        description = obj.position.position.position_name
        return description

    def get_date_of_application(self,obj):
        date_of_application = obj.date_of_application
        return date_of_application

    def get_date_of_closing(self,obj):
        date_of_closing = obj.date_of_closing
        return date_of_closing

    def get_hiring_status(self,obj):
        hiring_status = obj.applied_job_status
        return hiring_status