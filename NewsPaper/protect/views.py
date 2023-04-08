from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class MyView(PermissionRequiredMixin.View):
    permission_required = ('news.view_post',
                           'news.add_post',
                           'news.delete_post',
                           'news.change_post')


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
