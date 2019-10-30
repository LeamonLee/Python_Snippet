from django import forms
from django.utils.safestring import mark_safe

class DateTimePickerForm(forms.Form):
    start_date = forms.DateField(label=mark_safe("<strong>Start_date -</strong>"), widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker',
                                    "placeholder":"Ex:2018-12-1"
                                }, format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))
    end_date = forms.DateField(label=mark_safe("<strong>End_date -</strong>"), widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker',
                                    "placeholder":"Ex:2018-12-2"
                                }, format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))
    # start_date = forms.DateField(label=mark_safe("<strong>Start_date - </strong>"), widget=forms.DateInput(attrs=
    #                             {
    #                                 'class':'datepicker',
    #                                 "placeholder":"Ex:2018-12-1"
    #                             }))
    # end_date = forms.DateField(label=mark_safe("<strong>End_date - </strong>"), widget=forms.DateInput(attrs=
    #                             {
    #                                 'class':'datepicker',
    #                                 "placeholder":"Ex:2018-12-2"
    #                             }))

    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(DateTimePickerForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['style'] = 'display:inline;'
        self.fields['end_date'].widget.attrs['style']  = 'display:inline;'


    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        # if start_date == 'cc':
        #     raise forms.ValidationError('username exsite!')
        print("validating start_date...")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        # if endt_date == 'cc':
        #     raise forms.ValidationError('username exsite!')
        print("validating end_date...")
        return end_date

    def clean(self):
        cleaned_data = self.cleaned_data
        # pwd = cleaned_data['password']
        # pwd2 = cleaned_data['password1']
        # print(pwd, pwd2)
        # if pwd != pwd2:
        #     raise forms.ValidationError('the password you input is not same')
        print("Final validation...")
        return cleaned_data