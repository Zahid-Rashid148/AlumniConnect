from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, AlumniProfile, MentorshipRequest, Message, Post


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    branch = forms.CharField(max_length=100)
    year = forms.IntegerField(min_value=1, max_value=5)
    roll_number = forms.CharField(max_length=20, required=False)
    skills = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Python, Django, React...'}),
        required=False
    )
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.status = 'pending'
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                branch=self.cleaned_data['branch'],
                year=self.cleaned_data['year'],
                roll_number=self.cleaned_data.get('roll_number', ''),
                skills=self.cleaned_data.get('skills', ''),
            )
            user.bio = self.cleaned_data.get('bio', '')
            user.save()
        return user


class AlumniRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    company = forms.CharField(max_length=200)
    role = forms.CharField(max_length=100, label='Job Title')
    experience_years = forms.IntegerField(min_value=0, max_value=50)
    graduation_year = forms.IntegerField(min_value=1970, max_value=2030)
    branch = forms.CharField(max_length=100)
    domain = forms.CharField(max_length=100, required=False)
    skills = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Leadership, ML, Finance...'}),
        required=False
    )
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    linkedin = forms.URLField(required=False)
    is_open_to_mentor = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'alumni'
        user.status = 'pending'
        user.bio = self.cleaned_data.get('bio', '')
        user.linkedin = self.cleaned_data.get('linkedin', '')
        if commit:
            user.save()
            AlumniProfile.objects.create(
                user=user,
                company=self.cleaned_data['company'],
                role=self.cleaned_data['role'],
                experience_years=self.cleaned_data['experience_years'],
                graduation_year=self.cleaned_data['graduation_year'],
                branch=self.cleaned_data['branch'],
                domain=self.cleaned_data.get('domain', ''),
                skills=self.cleaned_data.get('skills', ''),
                is_open_to_mentor=self.cleaned_data.get('is_open_to_mentor', True),
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['message', 'goals']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Introduce yourself and why you want this mentor...'}),
            'goals': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What do you hope to achieve from this mentorship?'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Type your message...',
                'class': 'message-input'
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post_type', 'content', 'company', 'location', 'deadline', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Job/Internship Title'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe the opportunity...'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country or Remote'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://apply.example.com'}),
        }


class StudentProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = StudentProfile
        fields = ['branch', 'year', 'roll_number', 'cgpa', 'skills']
    
    avatar = forms.ImageField(required=False)


class AlumniProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    linkedin = forms.URLField(required=False)

    class Meta:
        model = AlumniProfile
        fields = ['company', 'role', 'experience_years', 'graduation_year', 'branch', 'domain', 'skills', 'is_open_to_mentor']

    avatar = forms.ImageField(required=False)
