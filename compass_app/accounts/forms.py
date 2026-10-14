"""
Author: Sofija Nikolic, index: 2023/0603

Django forms for login, user and company registration, and password
reset, with validation of username/email uniqueness. All fields use
the Bootstrap 'form-control' class to match the prototype design.
"""

from django import forms

from .models import User, Company


class LoginForm(forms.Form):
    """Login form - used for both users and companies."""

    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
    )


def _username_taken(username):
    """Checks whether the username is already taken in the User or Company table.

    Returns: bool - True if the username is already in use.
    """
    return User.objects.filter(username=username).exists() or Company.objects.filter(username=username).exists()


def _email_taken(email):
    """Checks whether the email is already registered in the User or Company table.

    Returns: bool - True if the email is already in use.
    """
    return User.objects.filter(email=email).exists() or Company.objects.filter(email=email).exists()


class UserRegistrationForm(forms.Form):
    """Form for registering a new user (a person looking for a job)."""

    first_name = forms.CharField(
        label="First name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
    )
    last_name = forms.CharField(
        label="Last name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
    )
    username = forms.CharField(
        label="Username", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a username', 'id': 'id_username'}),
    )
    email = forms.EmailField(
        label="Email", max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
    )
    contact = forms.CharField(
        label="Contact", max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a password'}),
        min_length=8,
    )
    password_confirm = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password'}),
    )

    def clean_username(self):
        """Validates that the username is not already taken."""
        username = self.cleaned_data['username']
        if _username_taken(username):
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """Validates that the email is not already registered."""
        email = self.cleaned_data['email']
        if _email_taken(email):
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        """Validates that the entered password and confirmation match."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class CompanyRegistrationForm(forms.Form):
    """Form for registering a new company (employer)."""

    name = forms.CharField(
        label="Company name", max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the company name'}),
    )
    username = forms.CharField(
        label="Username", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a username', 'id': 'id_username'}),
    )
    email = forms.EmailField(
        label="Email", max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter a contact email'}),
    )
    industry = forms.CharField(
        label="Industry", max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter the company's industry"}),
    )
    contact = forms.CharField(
        label="Contact", max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a phone number'}),
    )
    description = forms.CharField(
        label="Description", required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'A short description of the company', 'rows': 3}),
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a password'}),
        min_length=8,
    )
    password_confirm = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password'}),
    )

    def clean_username(self):
        """Validates that the username is not already taken."""
        username = self.cleaned_data['username']
        if _username_taken(username):
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """Validates that the email is not already registered."""
        email = self.cleaned_data['email']
        if _email_taken(email):
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        """Validates that the entered password and confirmation match."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class ForgotPasswordForm(forms.Form):
    """Form for entering an email when requesting a password reset."""

    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
    )


class SetNewPasswordForm(forms.Form):
    """Form for entering a new password after clicking the reset link."""

    password = forms.CharField(
        label="New password", min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a new password'}),
    )
    password_confirm = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password'}),
    )

    def clean(self):
        """Validates that the new password and confirmation match."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """Form for editing one's own profile (user).

    Does not include a password field - that is changed through the
    separate password reset flow.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'contact']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'Email',
            'contact': 'Contact',
        }

    def clean_username(self):
        """Validates that the username is not taken by another account."""
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists() or \
           Company.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """Validates that the email is not taken by another account."""
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists() or \
           Company.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class CompanyProfileForm(forms.ModelForm):
    """Form for editing one's own profile (company).

    Does not include a password field - that is changed through the
    separate password reset flow.
    """

    class Meta:
        model = Company
        fields = ['name', 'username', 'email', 'industry', 'contact', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Name',
            'username': 'Username',
            'email': 'Email',
            'industry': 'Industry',
            'contact': 'Contact',
            'description': 'Description',
        }

    def clean_username(self):
        """Validates that the username is not taken by another account."""
        username = self.cleaned_data['username']
        if Company.objects.exclude(pk=self.instance.pk).filter(username=username).exists() or \
           User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """Validates that the email is not taken by another account."""
        email = self.cleaned_data['email']
        if Company.objects.exclude(pk=self.instance.pk).filter(email=email).exists() or \
           User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
