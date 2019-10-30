from django.shortcuts import render, get_object_or_404, redirect
from .models import Attendance
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import DateTimePickerForm

# Create your views here.

def attendance_list(request):
    context = {
        'Attendances': Attendance.objects.all()
    }
    return render(request, 'attendances/data_list.html', context)


class AttendanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Attendance
    template_name = 'attendances/attendance_list2.html'     # <app>/<model>_<viewtype>.html
    # context_object_name = 'Attendances'                   # The default of context_object_name is "object_list" or "attendance_list"
    ordering = ['-date']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        print("DateTime GET form validating... ")
        return super(AttendanceListView, self).get(request, *args, **kwargs)
        # context = self.get_queryset()
        # return render(request, self.template_name, {'context': context})
    
    def get_queryset(self, **kwargs):
        print("Processing get_queryset... ")
        
        # context = super().get_context_data(**kwargs)
        # DTPForm = context["date_picker_form"]
        DTPForm = DateTimePickerForm(self.request.GET)
        
        start_date = self.request.GET.get('start_date', "")
        end_date = self.request.GET.get('end_date', "")
        print(f"start_date: {start_date}, end_date: {end_date}")
        if DTPForm.is_valid() and start_date != "" and end_date != "":
            print("DTPForm is valid!!!")
            return Attendance.objects.filter(date__range=(start_date, end_date)).order_by('-date')
        else:
            print("Either start_date or end_date is invalid... ")
            return Attendance.objects.all().order_by("-date")
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context["date_picker_form"] = DateTimePickerForm(self.request.GET)
        else:
            context["date_picker_form"] = DateTimePickerForm()
        return context

    def test_func(self):
        # print("------------- Form Testing Func ------------- ")
        return True


class UserAttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendances/user_attendance3.html'      # <app>/<model>_<viewtype>.html
    # context_object_name = 'Attendances'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        filtered_Attendance = Attendance.objects.filter(user=user).order_by('-date')

        DTPForm = DateTimePickerForm(self.request.GET)
        
        start_date = self.request.GET.get('start_date', "")
        end_date = self.request.GET.get('end_date', "")
        
        if DTPForm.is_valid() and start_date != "" and end_date != "":
            return filtered_Attendance.filter(date__range=(start_date, end_date)).order_by('-date')
        else:
            return filtered_Attendance.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context["date_picker_form"] = DateTimePickerForm(self.request.GET)
        else:
            context["date_picker_form"] = DateTimePickerForm()
        return context