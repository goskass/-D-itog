from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Ad, Response
from .forms import AdCreationForm, DateFilterForm, CategoryFilterForm, UserFilterForm
from .forms import ResponseForm
from django.contrib import messages


class AdListView(ListView):
    model = Ad
    template_name = 'ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 3


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    template_name = 'ad_create.html'
    form_class = AdCreationForm
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    template_name = 'ad_update.html'
    form_class = AdCreationForm
    success_url = reverse_lazy('ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user or self.request.user.is_superuser

class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user or self.request.user.is_superuser


class CreateResponseView(LoginRequiredMixin, View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        form = ResponseForm()
        return render(request, 'response.html', {'form': form, 'ad': ad, 'response_user': request.user})

    def post(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.ad = ad
            response.save()
            response.send_notification_email()
            messages.success(request, 'Отклик успешно отправлен!')
            return redirect('ad_detail', pk=ad_id)
        return render(request, 'response.html', {'form': form, 'ad': ad, 'response_user': request.user})


class PrivateResponseListView(ListView):
    template_name = 'private_responses.html'
    context_object_name = 'responses'
    ordering = ['-created_at']
    paginate_by = 1

    def get_queryset(self):
        user_ads = Ad.objects.filter(user=self.request.user)
        queryset = Response.objects.filter(ad__in=user_ads).order_by('-created_at')

        date_filter = self.request.GET.get('date')
        if date_filter:
            try:
                date_filter = timezone.datetime.strptime(date_filter, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date=date_filter)
            except ValueError:
                pass

        ad_filter = self.request.GET.get('ad')
        if ad_filter:
            queryset = queryset.filter(ad_id=ad_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_ads'] = Ad.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            response_id = request.POST.get('delete')

            response = Response.objects.get(pk=response_id)
            response.delete()
            messages.success(request, 'Отклик успешно удален.')
        elif 'accept' in request.POST:
            response_id = request.POST.get('accept')
            response = Response.objects.get(pk=response_id)
            response.is_approved = True
            response.save()

            recipient_email = response.user.email
            recipient_username = response.user.username
            subject = 'Ваш отклик был принят'
            context = {'ad_title': response.ad.title, 'user_email': recipient_email}
            html_message = render_to_string('email/notification_email.html', context)
            plain_message = strip_tags(html_message)

            send_mail(subject, plain_message, 'goskazon@yandex.ru', [recipient_email], html_message=html_message)

            messages.success(request, 'Отклик успешно принят.')

        return redirect('private_responses')

class AdSearchView(ListView):
    template_name = 'search_ads.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 5
    model = Ad

    def get_queryset(self):
        queryset = super().get_queryset()
        date_filter = self.request.GET.get('created_at')
        category_filter = self.request.GET.get('category')
        user_filter = self.request.GET.get('user')
        filters = Q()
        if date_filter:
            filters &= Q(created_at=date_filter)
        if category_filter:
            filters &= Q(category=category_filter)
        if user_filter:
            filters &= Q(user__username=user_filter)

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_form'] = DateFilterForm()
        context['category_form'] = CategoryFilterForm()
        context['user_form'] = UserFilterForm()
        return context


