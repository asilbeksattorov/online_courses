from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import models
from .models import Subject, Course, Module, Topic, Text, Video, Image, File, Comment
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from course.forms import VideoForm, CommentForm
from .forms import RegistrationForm
from django.views.generic.edit import FormView
from django.db.models import Avg



class HomeView(TemplateView):
    template_name = 'course/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['courses'] = Course.objects.all().order_by('-created')
        return context


class SubjectDetailView(View):
    def get(self, request, slug):
        subject = get_object_or_404(Subject, slug=slug)
        courses = Course.objects.filter(subject=subject)

        paginator = Paginator(courses, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'subject': subject,
            'courses': page_obj
        }
        return render(request, 'course/subject_detail.html', context)





class CoursesListView(ListView):
    model = Course
    template_name = 'course/course.html'
    context_object_name = 'courses'
    paginate_by = 6

    def get_queryset(self):
        return Course.objects.all().order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            course.student_count = course.modules.count()
            course.total_duration = course.duration
            course.average_rating = round(Comment.objects.filter(video_id__in=course.modules.values_list('topics__object_id', flat=True)).aggregate(Avg('rating'))['rating__avg'] or 0, 1)
            course.comment_count = Comment.objects.filter(video_id__in=course.modules.values_list('topics__object_id', flat=True)).count()
        return context




class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.modules.all()
        return context


@method_decorator(login_required, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    fields = ['title', 'overview', 'duration', 'price', 'subject', 'image']
    template_name = 'course/course_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    fields = ['title', 'overview', 'duration', 'price', 'subject', 'image']
    template_name = 'course/course_form.html'
    success_url = reverse_lazy('index')


@method_decorator(login_required, name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy('index')


class ModuleDetailView(DetailView):
    model = Module
    template_name = 'course/module_detail.html'
    context_object_name = 'module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = self.object.topics.all()
        return context


class TopicDetailView(View):
    def get(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        return render(request, 'course/topic_detail.html', {'topic': topic, 'item': topic.item})


# Optional: content (Text, Video, Image, File) detail views
class ContentDetailView(View):
    def get(self, request, model_name, pk):
        model = {
            'text': Text,
            'video': Video,
            'image': Image,
            'file': File
        }.get(model_name)

        if not model:
            return redirect('index')

        content_object = get_object_or_404(model, pk=pk)
        return render(request, 'course/content_detail.html', {'item': content_object})







class AddNewVideoView(CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'course/add-new-video.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, "New video added successfully.")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VideoUpdateView(UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'course/update.html'
    success_url = reverse_lazy('index')  # update to correct redirect if needed

    def form_valid(self, form):
        messages.success(self.request, "Video updated successfully.")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return super().get_object(queryset)


@method_decorator(login_required, name='dispatch')
class VideoDeleteView(DeleteView):
    model = Video
    template_name = 'course/delete_confirm/delete-confirm-video.html'
    context_object_name = 'video'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Video deleted.")
        return super().delete(request, *args, **kwargs)


class VideoDetailView(DetailView):
    model = Video
    template_name = 'course/video-detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['subjects'] = Subject.objects.all()  # like categories
        context['comments'] = Comment.objects.filter(
            video_id=self.object, parent__isnull=True
        ).order_by('-rating')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video_id = self.object
            comment.user_id = request.user
            comment.save()
            messages.success(request, "Your comment has been posted.")
            return redirect('video_detail', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)




class RegisterView(FormView):
    template_name = 'course/about.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account successfully created!")
        return super().form_valid(form)



class TeacherView(TemplateView):
    template_name = 'course/teacher.html'
    from django.views.generic import TemplateView


class TeacherView(TemplateView):
    template_name = 'course/teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = [
            {"img": "1", "name": "Abror Nazirov", "title": "Python Backend"},
            {"img": "2", "name": "Rashid Qilichev", "title": "React JS Frontend"},
            {"img": "3", "name": "Oydin Ergasheva", "title": "Flutter"},
            {"img": "4", "name": "Alibek Davronov", "title": "React Native"},
        ]
        return context
