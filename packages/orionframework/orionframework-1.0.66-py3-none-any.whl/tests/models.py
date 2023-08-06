from orionframework.media.document.models import AbstractDocument
from orionframework.media.image.models import AbstractImage
from orionframework.media.cloud_document.models import AbstractCloudDocument


class Image(AbstractImage):
    pass


class Document(AbstractDocument):
    pass


class CloudDocument(AbstractCloudDocument):
    pass
