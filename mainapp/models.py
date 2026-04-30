from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('admin', 'Admin'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_approved(self):
        return self.status == 'approved'

    @property
    def display_name(self):
        return self.get_full_name() or self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    branch = models.CharField(max_length=100)
    year = models.IntegerField()
    roll_number = models.CharField(max_length=20, blank=True)
    cgpa = models.FloatField(blank=True, null=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')

    def __str__(self):
        return f"{self.user.display_name} - {self.branch} Year {self.year}"

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    graduation_year = models.IntegerField()
    branch = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    is_open_to_mentor = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.display_name} at {self.company}"

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class MentorshipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    alumni = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField()
    goals = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    response_note = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'alumni']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.display_name} → {self.alumni.display_name} ({self.status})"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.display_name} → {self.receiver.display_name}: {self.content[:50]}"


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('job', 'Job'),
        ('internship', 'Internship'),
        ('event', 'Event'),
        ('general', 'General'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    post_type = models.CharField(max_length=15, choices=POST_TYPE_CHOICES, default='general')
    content = models.TextField()
    company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(blank=True, null=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.post_type.upper()}] {self.title} by {self.author.display_name}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('mentorship_request', 'Mentorship Request'),
        ('mentorship_accepted', 'Mentorship Accepted'),
        ('mentorship_rejected', 'Mentorship Rejected'),
        ('new_message', 'New Message'),
        ('account_approved', 'Account Approved'),
        ('new_post', 'New Post'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif for {self.user.username}: {self.title}"
