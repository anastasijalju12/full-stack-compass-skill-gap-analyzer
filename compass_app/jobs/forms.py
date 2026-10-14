from django.core.validators import RegexValidator
from django.db.models.functions import Now
from django.forms import ModelForm, Form

from careers.models import Application, Skill
from jobs.models import JobAd
from django import forms

class AddJobAdForm(ModelForm):
    class Meta:
        model = JobAd

        fields = ['name', 'description', 'type', 'location', 'application_deadline']

        labels = {
            'company': 'Company',
            'name': 'Position title',
            'description': 'Job / internship description',
            'type': 'Engagement type',
            'location': 'Location',
            'application_deadline': 'Application deadline',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control p-3 mb-3', 'placeholder': 'E.g. Junior Python Developer'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control p-3 mb-3', 'rows': 4, 'placeholder': 'Enter job ad details...'}),
            'type': forms.Select(attrs={'class': 'form-control p-3 mb-3'}),
            'location': forms.TextInput(
                attrs={'class': 'form-control p-3 mb-3', 'placeholder': 'E.g. Belgrade / Remote'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control p-3 mb-3', 'type': 'date'}),
        }

class ApplyForJobForm(Form):
    only_numbers_validator = RegexValidator(
        regex=r'^[\d+-]+$',
        message="The phone number may contain only digits and hyphens."
    )

    first_last_name = forms.CharField(max_length=200, label='Full name',
                                      error_messages={'required': ''}
)
    email = forms.EmailField(max_length=150, label='Email',
                             error_messages={'required': ''})
    contact_number = forms.CharField(
        validators=[only_numbers_validator],
        max_length=15,
        min_length=9,
        label='Phone',
        error_messages={'required': ''}
    )
    education = forms.CharField(max_length=200, label='Education', error_messages={'required': ''})

    skills = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        label='Skills', required=False)

    cv = forms.FileField(label='CV document', required=False)
    cover_message = forms.CharField(widget=forms.Textarea, label='Additional message for the employer',
                                    required=False)

    # skills from database
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.job_ad_id = kwargs.pop('job_ad_id', None)

        super().__init__(*args, **kwargs)
        skill_vals = (Skill.objects.
                      values_list('name', flat=True).distinct())
        self.fields['skills'].choices = [(v,v) for v in skill_vals]

    def save(self, commit, user_id, job_ad_id):
        education = self.cleaned_data['education']
        skills = ", ".join(self.cleaned_data['skills'])
        cover_message = self.cleaned_data['cover_message']

        # Getting the file from the cleaned form data
        cv_file = self.cleaned_data.get('cv')

        # Creating the object in the database
        application_data = Application(
            status='active',
            user_id=user_id,
            job_ad_id=job_ad_id,
            education=education,
            skills=skills,
            cover_message=cover_message,
        )

        # If the user actually attached a file, assign it through the model field
        # This way Django automatically uploads it to the "media/cvs/" folder and creates the path
        if cv_file:
            application_data.cv_path.save(cv_file.name, cv_file, save=False)

        # Finally saving the whole row to the database
        if commit:
            application_data.save()

        return application_data

    def clean(self):
        cleaned_data = super().clean()

        # Checking whether this user and job ad combination already exists in the database
        if self.user_id and self.job_ad_id:
            duplikat = Application.objects.filter(
                user_id=self.user_id,
                job_ad_id=self.job_ad_id
            ).exists()

            if duplikat:
                # Raises an error that is not tied to one field, but to the whole form
                raise forms.ValidationError("You have already applied for this job ad.")

        return cleaned_data