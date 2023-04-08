from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, BaseRegisterForm
from .forms import PostForm
from .filter import PostFilter
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class PostList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'news.html'
    context_object_name = 'post_news'
    paginate_by = 50

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  #вписываем фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый пост
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'onenews'
    queryset = Post.objects.all()


class PostCreateView(CreateView):   # создание поста
    template_name = 'post_add.html'
    form_class = PostForm


class PostUpdateView(UpdateView):   # редактирование поста
    template_name = 'post_edit.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте редактирования
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления поста
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'post_delete'


class PostSearch(ListView):   #поиск поста
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_news'
    paginate_by = 50

    def get_queryset(self):  # получаем обычный запрос
        queryset = super().get_queryset()  # используем наш класс фильтрации
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
