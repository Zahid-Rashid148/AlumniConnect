"""
AlumniConnect® — Sample Data Seed Script
Run: python seed_data.py  (from project root with Django env active)
OR:  python manage.py shell < seed_data.py
"""

import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumniconnect.settings')
django.setup()

from mainapp.models import User, StudentProfile, AlumniProfile, MentorshipRequest, Post, Notification

print("🌱 Seeding AlumniConnect® sample data...")

# ── Clear existing (optional) ────────────────────────────────
# Uncomment to reset:
# User.objects.filter(is_superuser=False).delete()

# ── Admin User ───────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@alumniconnect.com',
        password='admin123',
        first_name='System',
        last_name='Admin',
        role='admin',
        status='approved',
    )
    print(f"  ✅ Admin created: admin / admin123")
else:
    print("  ⏭  Admin already exists")

# ── Alumni ───────────────────────────────────────────────────
alumni_data = [
    {
        'username': 'priya_sharma',
        'first_name': 'Priya',
        'last_name': 'Sharma',
        'email': 'priya@google.com',
        'bio': 'Senior ML Engineer at Google with a passion for making AI accessible. Love helping students navigate careers in tech.',
        'linkedin': 'https://linkedin.com/in/priyasharma',
        'profile': {
            'company': 'Google',
            'role': 'Senior ML Engineer',
            'experience_years': 7,
            'graduation_year': 2017,
            'branch': 'Computer Science',
            'domain': 'Artificial Intelligence',
            'skills': 'Machine Learning, Python, TensorFlow, System Design, Leadership',
            'is_open_to_mentor': True,
        }
    },
    {
        'username': 'arjun_kapoor',
        'first_name': 'Arjun',
        'last_name': 'Kapoor',
        'email': 'arjun@stripe.com',
        'bio': 'Product Manager at Stripe. Built fintech products used by millions. Happy to mentor students interested in PM or fintech.',
        'linkedin': 'https://linkedin.com/in/arjunkapoor',
        'profile': {
            'company': 'Stripe',
            'role': 'Senior Product Manager',
            'experience_years': 6,
            'graduation_year': 2018,
            'branch': 'Electronics',
            'domain': 'Product Management',
            'skills': 'Product Strategy, Fintech, Data Analysis, Roadmapping, User Research',
            'is_open_to_mentor': True,
        }
    },
    {
        'username': 'sneha_nair',
        'first_name': 'Sneha',
        'last_name': 'Nair',
        'email': 'sneha@amazon.com',
        'bio': 'SDE-III at Amazon working on distributed systems. Competitive programmer turned engineer. Open to guiding students on DSA and interviews.',
        'linkedin': '',
        'profile': {
            'company': 'Amazon',
            'role': 'SDE-III',
            'experience_years': 5,
            'graduation_year': 2019,
            'branch': 'Computer Science',
            'domain': 'Backend Engineering',
            'skills': 'Java, Distributed Systems, AWS, Data Structures, Algorithms',
            'is_open_to_mentor': True,
        }
    },
    {
        'username': 'rahul_mehta',
        'first_name': 'Rahul',
        'last_name': 'Mehta',
        'email': 'rahul@mckinsey.com',
        'bio': 'Consultant at McKinsey. MBA from IIM-A. Helping students navigate consulting, MBA applications, and career transitions.',
        'linkedin': 'https://linkedin.com/in/rahulmehta',
        'profile': {
            'company': 'McKinsey & Company',
            'role': 'Associate Consultant',
            'experience_years': 4,
            'graduation_year': 2020,
            'branch': 'Mechanical',
            'domain': 'Management Consulting',
            'skills': 'Business Strategy, Data Analysis, Presentation, Problem Solving, Excel',
            'is_open_to_mentor': False,
        }
    },
]

created_alumni = []
for a in alumni_data:
    if not User.objects.filter(username=a['username']).exists():
        user = User.objects.create_user(
            username=a['username'],
            email=a['email'],
            password='password123',
            first_name=a['first_name'],
            last_name=a['last_name'],
            role='alumni',
            status='approved',
            bio=a['bio'],
            linkedin=a.get('linkedin', ''),
        )
        AlumniProfile.objects.create(user=user, **a['profile'])
        created_alumni.append(user)
        print(f"  ✅ Alumni: {user.display_name} ({a['username']} / password123)")
    else:
        created_alumni.append(User.objects.get(username=a['username']))
        print(f"  ⏭  Alumni {a['username']} already exists")

# ── Students ─────────────────────────────────────────────────
student_data = [
    {
        'username': 'aarav_singh',
        'first_name': 'Aarav',
        'last_name': 'Singh',
        'email': 'aarav@college.edu',
        'bio': 'Final year CS student passionate about ML and open-source. Looking for guidance on breaking into FAANG.',
        'profile': {
            'branch': 'Computer Science',
            'year': 4,
            'roll_number': 'CS2021001',
            'cgpa': 8.7,
            'skills': 'Python, Machine Learning, Django, React, Git',
        }
    },
    {
        'username': 'divya_reddy',
        'first_name': 'Divya',
        'last_name': 'Reddy',
        'email': 'divya@college.edu',
        'bio': 'Second year student interested in product management and entrepreneurship. Building a student marketplace app.',
        'profile': {
            'branch': 'Information Technology',
            'year': 2,
            'roll_number': 'IT2023045',
            'cgpa': 9.1,
            'skills': 'Product Design, Figma, JavaScript, Market Research',
        }
    },
    {
        'username': 'karan_patel',
        'first_name': 'Karan',
        'last_name': 'Patel',
        'email': 'karan@college.edu',
        'bio': 'Third year Mechanical student considering a switch to consulting or core engineering. Strong analytical background.',
        'profile': {
            'branch': 'Mechanical Engineering',
            'year': 3,
            'roll_number': 'ME2022018',
            'cgpa': 7.9,
            'skills': 'CAD, MATLAB, Data Analysis, Excel, Problem Solving',
        }
    },
]

created_students = []
for s in student_data:
    if not User.objects.filter(username=s['username']).exists():
        user = User.objects.create_user(
            username=s['username'],
            email=s['email'],
            password='password123',
            first_name=s['first_name'],
            last_name=s['last_name'],
            role='student',
            status='approved',
            bio=s['bio'],
        )
        StudentProfile.objects.create(user=user, **s['profile'])
        created_students.append(user)
        print(f"  ✅ Student: {user.display_name} ({s['username']} / password123)")
    else:
        created_students.append(User.objects.get(username=s['username']))
        print(f"  ⏭  Student {s['username']} already exists")

# ── Mentorship Requests ──────────────────────────────────────
if created_students and created_alumni:
    reqs = [
        (created_students[0], created_alumni[0], 'accepted', "Hi Priya! I'm Aarav, a final year CS student deeply interested in ML. I've been following your work at Google and would love guidance on breaking into AI roles.", "I want to understand the path to ML engineering at top companies and get guidance on my final year project."),
        (created_students[0], created_alumni[1], 'pending', "Hello Arjun! I'm a CS student exploring product management as a career. Your transition from engineering to PM is inspiring. Would love your guidance!", "Learn how to build a portfolio for PM roles and understand product thinking."),
        (created_students[1], created_alumni[1], 'accepted', "Hi Arjun! I'm building a student marketplace and could really use guidance from someone who's worked in fintech product. Would love your mentorship!", "Understand product-market fit, MVP strategy, and how to approach users."),
        (created_students[2], created_alumni[3], 'pending', "Hello Rahul! I'm a Mechanical student considering consulting after graduation. Your journey to McKinsey is very inspiring. Could you guide me?", "Prepare for consulting interviews and understand the consulting career path."),
    ]
    for student, alumni, status, msg, goals in reqs:
        if not MentorshipRequest.objects.filter(student=student, alumni=alumni).exists():
            MentorshipRequest.objects.create(
                student=student,
                alumni=alumni,
                status=status,
                message=msg,
                goals=goals,
            )
            print(f"  ✅ Request: {student.display_name} → {alumni.display_name} ({status})")

# ── Sample Posts ─────────────────────────────────────────────
if created_alumni:
    posts_data = [
        {
            'author': created_alumni[0],
            'title': 'Google Summer of Code 2025 — Applications Open',
            'post_type': 'internship',
            'content': 'Google Summer of Code is now accepting applications! Work on open-source projects for 3 months under the guidance of experienced mentors. Great stipend and amazing learning experience. Ideal for students with programming experience.',
            'company': 'Google',
            'location': 'Remote',
            'deadline': None,
            'link': 'https://summerofcode.withgoogle.com',
        },
        {
            'author': created_alumni[1],
            'title': 'Product Manager Intern — Fintech Startup (YC W25)',
            'post_type': 'internship',
            'content': 'We\'re hiring PM interns at our YC-backed fintech startup. You\'ll work directly with the founding team on product strategy, user research, and roadmapping. Looking for driven students with strong analytical skills and genuine interest in fintech.',
            'company': 'Razorpay (via referral)',
            'location': 'Bangalore',
            'deadline': None,
            'link': '',
        },
        {
            'author': created_alumni[2],
            'title': 'SDE Intern — Amazon Hyderabad (PPO Opportunity)',
            'post_type': 'internship',
            'content': 'Amazon Hyderabad is hiring SDE interns for Summer 2025. Strong DSA skills required. 6-month internship with pre-placement offer consideration. Competitive stipend. I can refer deserving candidates — DM me after applying.',
            'company': 'Amazon',
            'location': 'Hyderabad',
            'deadline': None,
            'link': 'https://amazon.jobs',
        },
        {
            'author': created_alumni[0],
            'title': 'Free Workshop: Breaking Into AI — Resume & Portfolio Review',
            'post_type': 'event',
            'content': 'I\'m hosting a free online workshop for students interested in AI/ML careers. We\'ll cover: building your ML portfolio, what FAANG ML teams look for, common mistakes in applications, and live resume review. Open to all years.',
            'company': 'Google',
            'location': 'Online (Zoom)',
            'deadline': None,
            'link': '',
        },
    ]

    for p in posts_data:
        if not Post.objects.filter(title=p['title']).exists():
            Post.objects.create(**p)
            print(f"  ✅ Post: {p['title'][:50]}")

print("\n✨ Seeding complete! Summary:")
print(f"   👤 Admin:    admin / admin123")
print(f"   🎓 Students: aarav_singh, divya_reddy, karan_patel (password: password123)")
print(f"   💼 Alumni:   priya_sharma, arjun_kapoor, sneha_nair, rahul_mehta (password: password123)")
print(f"\n   🚀 Run: python manage.py runserver")
print(f"   🌐 Open: http://127.0.0.1:8000")
