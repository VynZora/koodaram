from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogForm, ContactForm, TestimonialForm, ActivityForm, CampingPackageForm
from .models import Blog, Category, ContactMessage, GalleryImage, Testimonial, Activity, CampingPackage


def home(request):
    testimonials = list(Testimonial.objects.all()[:8])
    if testimonials and len(testimonials) < 3:
        repeat_count = (3 + len(testimonials) - 1) // len(testimonials)
        testimonials = (testimonials * repeat_count)[:3]

    blogs = Blog.objects.all()[:3]
    packages = CampingPackage.objects.all()[:4]
    activities = Activity.objects.all()[:4]
    
    context = {
        "testimonials": testimonials, 
        "blogs": blogs,
        "packages": packages,
        "activities": activities
    }
    return render(request, "frontend/index.html", context)


def about(request):
    testimonials = list(Testimonial.objects.all()[:8])
    if testimonials and len(testimonials) < 3:
        repeat_count = (3 + len(testimonials) - 1) // len(testimonials)
        testimonials = (testimonials * repeat_count)[:3]
    return render(request, "frontend/about.html", {"testimonials": testimonials})


def blog(request):
    blog_queryset = Blog.objects.all()
    paginator = Paginator(blog_queryset, 6)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    return render(request, "frontend/blog.html", {"blogs": blogs})


def blog_single(request, slug):
    blog_post = get_object_or_404(Blog, slug=slug)
    recent_blogs = Blog.objects.exclude(slug=slug)[:4]
    context = {"blog": blog_post, "recent_blogs": recent_blogs}
    return render(request, "frontend/blog-single.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully. We will contact you soon.")
            return redirect("contact")
        messages.error(request, "Please check the form and try again.")
    return render(request, "frontend/contact.html", {"form": form})


def services(request):
    return render(request, "frontend/services.html")


def service_single(request):
    return render(request, "frontend/service-single.html")


def trips(request):
    return render(request, "frontend/trips.html")


def trip_single(request):
    return render(request, "frontend/trip-single.html")


def team(request):
    return render(request, "frontend/team.html")


def team_single(request):
    return render(request, "frontend/team-single.html")


def pricing(request):
    return render(request, "frontend/pricing.html")


def testimonials(request):
    return render(request, "frontend/testimonials.html")


def image_gallery(request):
    categories = Category.objects.filter(images__isnull=False).distinct().order_by("name")
    gallery_images = GalleryImage.objects.select_related("category").order_by("-uploaded_at")
    context = {"categories": categories, "gallery_images": gallery_images}
    return render(request, "frontend/image-gallery.html", context)


def video_gallery(request):
    return render(request, "frontend/video-gallery.html")


def faqs(request):
    return render(request, "frontend/faqs.html")


def page_not_found(request, exception=None):
    return render(request, "frontend/404.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, "authenticate/login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("admin_dashboard")

        messages.error(request, "Invalid credentials or unauthorized access.")

    return render(request, "authenticate/login.html")


@login_required(login_url="admin_login")
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")


import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta

@login_required(login_url="admin_login")
def admin_dashboard(request):
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 1. Total Stats
    stats = {
        'total_projects': Blog.objects.count(), # Assuming Portfolio Projects means Blogs based on the URL in template
        'projects_this_month': Blog.objects.filter(created_at__gte=month_start).count(),
        'total_services': Category.objects.count(), # Assuming Categories map to Services
        'total_inquiries': ContactMessage.objects.filter(service_type__isnull=False).count() if hasattr(ContactMessage, 'service_type') else 0, # Since service_type might not exist, failing gracefully
        'total_contacts': ContactMessage.objects.count(),
        'total_packages': CampingPackage.objects.count()
    }

    # 2. Recent Lists
    recent_projects = Blog.objects.all().order_by('-created_at')[:4]
    recent_contacts = ContactMessage.objects.all().order_by('-created_at')[:4]
    recent_packages = CampingPackage.objects.all().order_by('-created_at')[:4]
    # Inquiries fallback if no dedicated model
    recent_inquiries = ContactMessage.objects.all().order_by('-created_at')[:4] if not hasattr(ContactMessage, 'service_type') else ContactMessage.objects.exclude(service_type__isnull=True).order_by('-created_at')[:4]

    # 3. Chart Data (Projects over last 6 months)
    month_labels = []
    month_counts = []
    for i in range(5, -1, -1):
        target_month = now - relativedelta(months=i)
        label = target_month.strftime('%b')
        month_labels.append(label)
        
        count = Blog.objects.filter(
            created_at__year=target_month.year,
            created_at__month=target_month.month
        ).count()
        month_counts.append(count)
        
    # 4. Service Distribution (Doughnut Chart)
    service_labels = []
    service_counts = []
    for category in Category.objects.all()[:6]: # Limit to top 6 categories for visual fit
        service_labels.append(category.name)
        # Using GalleryImage count as a proxy for category size since there is no direct service linkage
        service_counts.append(category.images.count())
        
    if not service_labels: # Fallback if empty to load chart cleanly
        service_labels = ['No Data']
        service_counts = [1]

    context = {
        'stats': stats,
        'recent_projects': recent_projects,
        'recent_contacts': recent_contacts,
        'recent_inquiries': recent_inquiries,
        'recent_packages': recent_packages,
        'month_labels': month_labels,
        'month_counts': month_counts,
        'service_labels': service_labels,
        'service_counts': service_counts,
    }

    return render(request, "admin_pages/dashboard.html", context)



# ==========================================
# 6. BLOGS (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def admin_blog_list(request):  # RENAMED from blog_list to fix URL error
    blogs_qs = Blog.objects.all().order_by("-created_at")
    paginator = Paginator(blogs_qs, 6)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    return render(request, "admin_pages/blog_list.html", {"blogs": blogs})

@login_required(login_url="admin_login")
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post created!")
            return redirect("admin_blog_list")
    else:
        form = BlogForm()
    return render(request, "admin_pages/create_blog.html", {"form": form})

@login_required(login_url="admin_login")
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated!")
            return redirect("admin_blog_list")
    else:
        form = BlogForm(instance=blog)
    return render(request, "admin_pages/create_blog.html", {"form": form, "blog": blog})

@login_required(login_url="admin_login")
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted.")
    return redirect("admin_blog_list")


# ==========================================
# 7. GALLERY (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def gallery_images(request):
    categories = Category.objects.all().prefetch_related("images")
    category_pages = {}
    for category in categories:
        images_qs = category.images.all().order_by("-uploaded_at")
        paginator = Paginator(images_qs, 8)
        page_number = request.GET.get(f"page_{category.id}", 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        category_pages[category.id] = page_obj

    return render(
        request, "admin_pages/image_list.html",
        {"categories": categories, "category_pages": category_pages},
    )

@login_required(login_url="admin_login")
def add_image(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        files = request.FILES.getlist("images")
        for file in files:
            GalleryImage.objects.create(
                category=category,
                title=file.name,
                image=file,
            )
        messages.success(request, "Images uploaded successfully!")
        return redirect("list_image")

    return render(request, "admin_pages/add_image.html", {"categories": categories})

@login_required(login_url="admin_login")
def delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    if request.method == "POST":
        image.delete()
        messages.success(request, "Image deleted successfully!")
        return redirect("list_image")
    return render(request, "admin_pages/image_list.html", {"image": image})


@login_required(login_url="admin_login")
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)
    return render(request, "admin_pages/category_list.html", {"categories": categories})


@login_required(login_url="admin_login")
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Category created successfully!")
            return redirect("category_list")
    return render(request, "admin_pages/add_category.html")


@login_required(login_url="admin_login")
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect("category_list")
    return redirect("category_list")


@login_required(login_url="admin_login")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("category_list")
    return redirect("category_list")


# ==========================================
# 8. TESTIMONIALS (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def testimonial_list(request):
    testimonials_list = Testimonial.objects.all().order_by(Lower("name"))
    paginator = Paginator(testimonials_list, 6)
    page_number = request.GET.get("page")
    testimonials = paginator.get_page(page_number)
    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})


@login_required(login_url="admin_login")
def testimonial_create(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully!")
            return redirect("review_list")
    else:
        form = TestimonialForm()
    return render(request, "admin_pages/create_review.html", {"form": form})


@login_required(login_url="admin_login")
def testimonial_update(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully!")
            return redirect("review_list")
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, "admin_pages/review_list.html", {"form": form, "testimonial": testimonial})


@login_required(login_url="admin_login")
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully!")
        return redirect("review_list")
    return render(request, "admin_pages/review_list.html", {"testimonial": testimonial})


# ==========================================
# 9. CONTACTS & INQUIRIES (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def view_contacts(request):
    contacts = ContactMessage.objects.all().order_by("-created_at")
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "admin_pages/view_contacts.html", {"contacts": page_obj})

@login_required(login_url="admin_login")
def delete_contact(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        contact.delete()
    return redirect("view_contacts")


# ==========================================
# 10. ACTIVITIES (FRONTEND)
# ==========================================

def activity_list(request):
    # Fetch activities, ordered by newest first
    activities_qs = Activity.objects.all().order_by("-created_at")
    paginator = Paginator(activities_qs, 9)
    page_number = request.GET.get("page")
    activities = paginator.get_page(page_number)
    return render(request, "frontend/activities.html", {"activities": activities})


def activity_single(request, slug):
    activity = get_object_or_404(Activity, slug=slug)
    # Optional: fetch other recent activities for a sidebar
    recent_activities = Activity.objects.exclude(slug=slug)[:3]
    context = {"activity": activity, "recent_activities": recent_activities}
    return render(request, "frontend/activity-single.html", context)


# ==========================================
# 11. ACTIVITIES (ADMIN DASHBOARD)
# ==========================================

@login_required(login_url="admin_login")
def admin_activity_list(request):
    activities_qs = Activity.objects.all().order_by("-created_at")
    paginator = Paginator(activities_qs, 10)
    page_number = request.GET.get("page")
    activities = paginator.get_page(page_number)
    return render(request, "admin_pages/activity_list.html", {"activities": activities})


@login_required(login_url="admin_login")
def activity_create(request):
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity created successfully!")
            return redirect("admin_activity_list")
    else:
        form = ActivityForm()
    return render(request, "admin_pages/create_activity.html", {"form": form})


@login_required(login_url="admin_login")
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully!")
            return redirect("admin_activity_list")
    else:
        form = ActivityForm(instance=activity)
    # Reusing the create template for editing is common practice
    return render(request, "admin_pages/create_activity.html", {"form": form, "activity": activity})


@login_required(login_url="admin_login")
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        activity.delete()
        messages.success(request, "Activity deleted successfully!")
    return redirect("admin_activity_list")


# ==========================================
# 12. CAMPING PACKAGES (FRONTEND)
# ==========================================

def services(request):
    packages_qs = CampingPackage.objects.all().order_by("-created_at")
    paginator = Paginator(packages_qs, 9)
    page_number = request.GET.get("page")
    packages = paginator.get_page(page_number)
    return render(request, "frontend/services.html", {"packages": packages})


def service_single(request, slug):
    package = get_object_or_404(CampingPackage, slug=slug)
    recent_packages = CampingPackage.objects.exclude(slug=slug).order_by("-created_at")[:5]
    return render(request, "frontend/service-single.html", {"package": package, "recent_packages": recent_packages})


# ==========================================
# 13. CAMPING PACKAGES (ADMIN DASHBOARD)
# ==========================================

@login_required(login_url="admin_login")
def admin_camping_package_list(request):
    packages_qs = CampingPackage.objects.all().order_by("-created_at")
    paginator = Paginator(packages_qs, 10)
    page_number = request.GET.get("page")
    packages = paginator.get_page(page_number)
    return render(request, "admin_pages/camping_package_list.html", {"packages": packages})


@login_required(login_url="admin_login")
def camping_package_create(request):
    if request.method == "POST":
        form = CampingPackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Camping Package created successfully!")
            return redirect("admin_camping_package_list")
    else:
        form = CampingPackageForm()
    return render(request, "admin_pages/create_camping_package.html", {"form": form})


@login_required(login_url="admin_login")
def camping_package_update(request, pk):
    package = get_object_or_404(CampingPackage, pk=pk)
    if request.method == "POST":
        form = CampingPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Camping Package updated successfully!")
            return redirect("admin_camping_package_list")
    else:
        form = CampingPackageForm(instance=package)
    return render(request, "admin_pages/create_camping_package.html", {"form": form, "package": package})


@login_required(login_url="admin_login")
def camping_package_delete(request, pk):
    package = get_object_or_404(CampingPackage, pk=pk)
    if request.method == "POST":
        package.delete()
        messages.success(request, "Camping Package deleted successfully!")
    return redirect("admin_camping_package_list")