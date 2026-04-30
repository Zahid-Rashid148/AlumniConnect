from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from .models import User, StudentProfile, AlumniProfile, MentorshipRequest, Message, Post, Notification
from .forms import (
    StudentRegistrationForm, AlumniRegistrationForm, LoginForm,
    MentorshipRequestForm, MessageForm, PostForm,
    StudentProfileUpdateForm, AlumniProfileUpdateForm
)


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    stats = {
        'total_alumni': User.objects.filter(role='alumni', status='approved').count(),
        'total_students': User.objects.filter(role='student', status='approved').count(),
        'total_mentorships': MentorshipRequest.objects.filter(status='accepted').count(),
        'total_posts': Post.objects.filter(is_active=True).count(),
    }
    recent_posts = Post.objects.filter(is_active=True).select_related('author')[:3]
    return render(request, 'home.html', {'stats': stats, 'recent_posts': recent_posts})


# ─── AUTH VIEWS ─────────────────────────────────────────────────────────────

def login_student(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user and user.role == 'student':
                if user.status == 'approved':
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.display_name}!')
                    return redirect('dashboard')
                elif user.status == 'pending':
                    messages.warning(request, 'Your account is pending admin approval.')
                else:
                    messages.error(request, 'Your account has been rejected.')
            else:
                messages.error(request, 'Invalid credentials or not a student account.')
    return render(request, 'auth/login_student.html', {'form': form})


def login_alumni(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user and user.role == 'alumni':
                if user.status == 'approved':
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.display_name}!')
                    return redirect('dashboard')
                elif user.status == 'pending':
                    messages.warning(request, 'Your account is pending admin approval.')
                else:
                    messages.error(request, 'Your account has been rejected.')
            else:
                messages.error(request, 'Invalid credentials or not an alumni account.')
    return render(request, 'auth/login_alumni.html', {'form': form})


def login_admin(request):
    if request.user.is_authenticated and request.user.role == 'admin':
        return redirect('admin_dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user and (user.role == 'admin' or user.is_superuser):
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid admin credentials.')
    return render(request, 'auth/login_admin.html', {'form': form})


def register_student(request):
    form = StudentRegistrationForm()
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration submitted! Please wait for admin approval.')
            return redirect('login_student')
    return render(request, 'auth/register_student.html', {'form': form})


def register_alumni(request):
    form = AlumniRegistrationForm()
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration submitted! Please wait for admin approval.')
            return redirect('login_alumni')
    return render(request, 'auth/register_alumni.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ─── DASHBOARD ──────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin' or user.is_superuser:
        return redirect('admin_dashboard')
    elif user.role == 'student':
        return student_dashboard(request)
    elif user.role == 'alumni':
        return alumni_dashboard(request)
    return redirect('home')


def student_dashboard(request):
    user = request.user
    my_requests = MentorshipRequest.objects.filter(student=user).select_related('alumni')
    accepted_mentors = my_requests.filter(status='accepted')
    pending_requests = my_requests.filter(status='pending')
    recent_posts = Post.objects.filter(is_active=True).select_related('author')[:5]
    alumni_list = User.objects.filter(role='alumni', status='approved').select_related('alumni_profile')[:6]
    unread_messages = Message.objects.filter(receiver=user, is_read=False).count()
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]

    context = {
        'user': user,
        'my_requests': my_requests,
        'accepted_mentors': accepted_mentors,
        'pending_requests': pending_requests,
        'recent_posts': recent_posts,
        'alumni_list': alumni_list,
        'unread_messages': unread_messages,
        'notifications': notifications,
    }
    return render(request, 'dashboard/student.html', context)


def alumni_dashboard(request):
    user = request.user
    received_requests = MentorshipRequest.objects.filter(alumni=user).select_related('student')
    pending_requests = received_requests.filter(status='pending')
    accepted_students = received_requests.filter(status='accepted')
    my_posts = Post.objects.filter(author=user)
    unread_messages = Message.objects.filter(receiver=user, is_read=False).count()
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]

    context = {
        'user': user,
        'received_requests': received_requests,
        'pending_requests': pending_requests,
        'accepted_students': accepted_students,
        'my_posts': my_posts,
        'unread_messages': unread_messages,
        'notifications': notifications,
    }
    return render(request, 'dashboard/alumni.html', context)


@login_required
def admin_dashboard(request):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('dashboard')

    pending_users = User.objects.filter(status='pending')
    all_students = User.objects.filter(role='student')
    all_alumni = User.objects.filter(role='alumni')
    all_mentorships = MentorshipRequest.objects.all().select_related('student', 'alumni')
    all_posts = Post.objects.all().select_related('author')

    stats = {
        'pending': pending_users.count(),
        'students': all_students.count(),
        'alumni': all_alumni.count(),
        'mentorships': all_mentorships.filter(status='accepted').count(),
        'posts': all_posts.count(),
    }

    context = {
        'pending_users': pending_users,
        'all_students': all_students,
        'all_alumni': all_alumni,
        'all_mentorships': all_mentorships,
        'stats': stats,
    }
    return render(request, 'dashboard/admin.html', context)


# ─── ADMIN ACTIONS ──────────────────────────────────────────────────────────

@login_required
def approve_user(request, user_id):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    user.status = 'approved'
    user.save()
    Notification.objects.create(
        user=user,
        notif_type='account_approved',
        title='Account Approved',
        message='Your account has been approved by the admin. Welcome aboard!',
        link='/dashboard/'
    )
    messages.success(request, f'{user.display_name} approved successfully.')
    return redirect('admin_dashboard')


@login_required
def reject_user(request, user_id):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    user.status = 'rejected'
    user.save()
    messages.warning(request, f'{user.display_name} has been rejected.')
    return redirect('admin_dashboard')


# ─── ALUMNI LIST ────────────────────────────────────────────────────────────

@login_required
def alumni_list(request):
    alumni = User.objects.filter(role='alumni', status='approved').select_related('alumni_profile')
    search = request.GET.get('q', '')
    domain = request.GET.get('domain', '')
    if search:
        alumni = alumni.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(alumni_profile__company__icontains=search) |
            Q(alumni_profile__skills__icontains=search)
        )
    if domain:
        alumni = alumni.filter(alumni_profile__domain__icontains=domain)

    # Build enriched list with request status attached
    my_requests = {}
    if request.user.role == 'student':
        my_requests = {
            r.alumni_id: r.status
            for r in MentorshipRequest.objects.filter(student=request.user)
        }

    # Attach status directly to each alumni object
    alumni_with_status = []
    for alum in alumni:
        alumni_with_status.append({
            'user': alum,
            'request_status': my_requests.get(alum.id, None),
        })

    context = {
        'alumni_with_status': alumni_with_status,
        'search': search,
        'domain': domain,
    }
    return render(request, 'alumni_list.html', context)


# ─── MENTORSHIP ─────────────────────────────────────────────────────────────

@login_required
def send_mentorship_request(request, alumni_id):
    if request.user.role != 'student':
        messages.error(request, 'Only students can send mentorship requests.')
        return redirect('alumni_list')

    alumni = get_object_or_404(User, id=alumni_id, role='alumni')

    if MentorshipRequest.objects.filter(student=request.user, alumni=alumni).exists():
        messages.warning(request, 'You already sent a request to this alumni.')
        return redirect('alumni_list')

    form = MentorshipRequestForm()
    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.student = request.user
            req.alumni = alumni
            req.save()
            Notification.objects.create(
                user=alumni,
                notif_type='mentorship_request',
                title='New Mentorship Request',
                message=f'{request.user.display_name} wants you as a mentor.',
                link='/dashboard/'
            )
            messages.success(request, f'Mentorship request sent to {alumni.display_name}!')
            return redirect('alumni_list')

    return render(request, 'mentorship_request.html', {'form': form, 'alumni': alumni})


@login_required
def handle_mentorship_request(request, request_id, action):
    if request.user.role != 'alumni':
        return redirect('dashboard')

    mentorship_req = get_object_or_404(MentorshipRequest, id=request_id, alumni=request.user)

    if action == 'accept':
        mentorship_req.status = 'accepted'
        mentorship_req.save()
        Notification.objects.create(
            user=mentorship_req.student,
            notif_type='mentorship_accepted',
            title='Mentorship Request Accepted!',
            message=f'{request.user.display_name} accepted your mentorship request!',
            link='/messages/'
        )
        messages.success(request, f'You accepted {mentorship_req.student.display_name} as your mentee.')
    elif action == 'reject':
        mentorship_req.status = 'rejected'
        mentorship_req.save()
        Notification.objects.create(
            user=mentorship_req.student,
            notif_type='mentorship_rejected',
            title='Mentorship Request Update',
            message=f'Your mentorship request to {request.user.display_name} was not accepted at this time.',
            link='/alumni/'
        )
        messages.info(request, f'Request from {mentorship_req.student.display_name} rejected.')

    return redirect('dashboard')


# ─── MESSAGING ──────────────────────────────────────────────────────────────

@login_required
def inbox(request):
    user = request.user

    sent_to = Message.objects.filter(sender=user).values_list('receiver_id', flat=True)
    received_from = Message.objects.filter(receiver=user).values_list('sender_id', flat=True)
    chat_user_ids = set(list(sent_to) + list(received_from))
    chat_users = User.objects.filter(id__in=chat_user_ids)

    # Build enriched list with unread count attached
    chat_list = []
    for cu in chat_users:
        unread = Message.objects.filter(sender=cu, receiver=user, is_read=False).count()
        last_msg = Message.objects.filter(
            Q(sender=user, receiver=cu) | Q(sender=cu, receiver=user)
        ).order_by('-created_at').first()
        chat_list.append({
            'user': cu,
            'unread': unread,
            'last_message': last_msg,
        })

    # Sort by latest message first
    chat_list.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else 0, reverse=True)

    return render(request, 'inbox.html', {'chat_list': chat_list})


@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    user = request.user

    # Check if they're allowed to chat (accepted mentorship)
    can_chat = False
    if user.role == 'student' and other_user.role == 'alumni':
        can_chat = MentorshipRequest.objects.filter(
            student=user, alumni=other_user, status='accepted'
        ).exists()
    elif user.role == 'alumni' and other_user.role == 'student':
        can_chat = MentorshipRequest.objects.filter(
            student=other_user, alumni=user, status='accepted'
        ).exists()
    elif user.role == 'admin' or user.is_superuser:
        can_chat = True

    if not can_chat:
        messages.error(request, 'You can only chat with accepted mentors/mentees.')
        return redirect('inbox')

    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=user, is_read=False).update(is_read=True)

    all_messages = Message.objects.filter(
        Q(sender=user, receiver=other_user) |
        Q(sender=other_user, receiver=user)
    ).order_by('created_at')

    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = user
            msg.receiver = other_user
            msg.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'ok',
                    'message': msg.content,
                    'time': msg.created_at.strftime('%H:%M'),
                    'sender': user.display_name,
                })
            return redirect('chat', user_id=user_id)

    context = {
        'other_user': other_user,
        'messages': all_messages,
        'form': form,
    }
    return render(request, 'chat.html', context)


# ─── POSTS ──────────────────────────────────────────────────────────────────

@login_required
def posts_list(request):
    posts = Post.objects.filter(is_active=True).select_related('author')
    post_type = request.GET.get('type', '')
    if post_type:
        posts = posts.filter(post_type=post_type)
    return render(request, 'posts.html', {'posts': posts, 'post_type': post_type})


@login_required
def create_post(request):
    if request.user.role != 'alumni':
        messages.error(request, 'Only alumni can create posts.')
        return redirect('posts_list')

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('dashboard')

    return render(request, 'create_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('dashboard')


# ─── PROFILE ────────────────────────────────────────────────────────────────

@login_required
def profile(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user

    context = {'profile_user': profile_user}

    if profile_user.role == 'student':
        try:
            context['student_profile'] = profile_user.student_profile
        except StudentProfile.DoesNotExist:
            pass
    elif profile_user.role == 'alumni':
        try:
            context['alumni_profile'] = profile_user.alumni_profile
            context['posts'] = Post.objects.filter(author=profile_user, is_active=True)
        except AlumniProfile.DoesNotExist:
            pass

    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if user.role == 'student':
        try:
            sp = user.student_profile
        except StudentProfile.DoesNotExist:
            sp = None

        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'phone': user.phone,
        }
        form = StudentProfileUpdateForm(instance=sp, initial=initial)
        if request.method == 'POST':
            form = StudentProfileUpdateForm(request.POST, instance=sp)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.bio = form.cleaned_data.get('bio', '')
                user.phone = form.cleaned_data.get('phone', '')
                # Handle avatar upload
                if request.FILES.get('avatar'):
                    user.avatar = request.FILES['avatar']
                user.save()
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('profile')

    elif user.role == 'alumni':
        try:
            ap = user.alumni_profile
        except AlumniProfile.DoesNotExist:
            ap = None

        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'linkedin': user.linkedin,
        }
        form = AlumniProfileUpdateForm(instance=ap, initial=initial)
        if request.method == 'POST':
            form = AlumniProfileUpdateForm(request.POST, instance=ap)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.bio = form.cleaned_data.get('bio', '')
                user.linkedin = form.cleaned_data.get('linkedin', '')
                # Handle avatar upload
                if request.FILES.get('avatar'):
                    user.avatar = request.FILES['avatar']
                user.save()
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('profile')
    else:
        return redirect('dashboard')

    return render(request, 'edit_profile.html', {'form': form})


# ─── NOTIFICATIONS ──────────────────────────────────────────────────────────

@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifs})


@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'ok'})
