from django_downloadview import ObjectDownloadView

from demoproject.object.models import Document

#: Serve ``file`` attribute of ``Document`` model.
default_file_view = ObjectDownloadView.as_view(model=Document)

#: Serve ``another_file`` attribute of ``Document`` model.
another_file_view = ObjectDownloadView.as_view(
    model=Document, file_field="another_file"
)

#: Serve ``file`` attribute of ``Document`` model, using client-side filename
#: from model.
deserialized_basename_view = ObjectDownloadView.as_view(
    model=Document, basename_field="basename"
)

#: Serve ``file`` attribute of ``Document`` model, inline (not as attachment).
inline_file_view = ObjectDownloadView.as_view(model=Document, attachment=False)
