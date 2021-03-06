from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.sites import site
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import CreateView
from django.views.generic.edit import ModelFormMixin

from jamsession.models import DataSetDefinition
from jamsession.forms.admin import DataDefAdminForm


@site.admin_view
def dashboard(request):
    """
    Dashboard view for Jamsession app.
    """
    context = {
        'title': "Jamsession Administration",
    }
    return render_to_response(
        'jamsession/admin/dashboard.html',
        context,
        context_instance=RequestContext(request))


object_types = {
    'datasetdefinition': (DataSetDefinition, DataDefAdminForm)
}


class AdminCreateView(CreateView):
    def get_form_kwargs(self):
        return super(ModelFormMixin, self).get_form_kwargs()

    def _construct_object_dictionary(self, obj):
        obj_dict = {}
        keys = [key for key in dir(obj) if not key.startswith('_')]
        for key in keys:
            attr = getattr(obj, key)
            if not callable(attr):
                obj_dict[key] = attr
        return obj_dict

    def get_success_url(self):
        if self.success_url:
            url = self.success_url % \
                self._construct_object_dictionary(self.object)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url


@site.admin_view
def create_object(request, object_type):
    klass, form_klass = object_types.get(object_type, None)
    if not klass:
        raise Http404("Content type %s not found" % object_type)

    context = {
        'title': 'Add %s' % klass.verbose_name,
        'klass': klass,
        'add': True,
        'obj': None,
    }
    view = AdminCreateView()
    view.template_name = 'jamsession/admin/create_object.html'
    view.form_class = form_klass
    view.success_url = reverse("jamsession:admin-edit-object",
                            kwargs=dict(object_type=object_type,
                                        object_id="%(id)s")
    )
    view.request = request
    print view.get_form_kwargs()
    return view.dispatch(request)

    return generic_create_object(request,
                                 form_class=form_class,
                                 template_name=template_name,
                                 extra_context=context,
                                 post_save_redirect=post_save_url)


def edit_object(request, object_type, object_id):
    pass
