from orionframework.media.serializers import AbstractMediaSerializer
from orionframework.media.settings import CloudDocument


class CloudDocumentSerializer(AbstractMediaSerializer):
    class Meta:
        model = CloudDocument
        exclude = ["parent_type", "parent_id"]
