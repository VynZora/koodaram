from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("service-single/", views.service_single, name="service_single"),
    path("trips/", views.trips, name="trips"),
    path("trip-single/", views.trip_single, name="trip_single"),
    path("team/", views.team, name="team"),
    path("team-single/", views.team_single, name="team_single"),
    path("pricing/", views.pricing, name="pricing"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("image-gallery/", views.image_gallery, name="image_gallery"),
    path("video-gallery/", views.video_gallery, name="video_gallery"),
    path("faqs/", views.faqs, name="faqs"),
    path("404/", views.page_not_found, name="page_not_found"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_single, name="blog_single"),
    path("contact/", views.contact, name="contact"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("dashboard/blogs/", views.admin_blog_list, name="admin_blog_list"),
    path("dashboard/blogs/create/", views.blog_create, name="blog_create"),
    path("dashboard/blogs/<int:pk>/edit/", views.blog_update, name="blog_update"),
    path("dashboard/blogs/<int:pk>/delete/", views.blog_delete, name="blog_delete"),

    path("dashboard/gallery/", views.gallery_images, name="list_image"),
    path("dashboard/gallery/add/", views.add_image, name="add_image"),
    path("dashboard/gallery/<int:image_id>/delete/", views.delete_image, name="delete_image"),

    path("dashboard/categories/", views.category_list, name="category_list"),
    path("dashboard/categories/add/", views.add_category, name="add_category"),
    path("dashboard/categories/<int:pk>/edit/", views.update_category, name="update_category"),
    path("dashboard/categories/<int:pk>/delete/", views.delete_category, name="delete_category"),

    path("dashboard/testimonials/", views.testimonial_list, name="review_list"),
    path("dashboard/testimonials/add/", views.testimonial_create, name="testimonial_create"),
    path("dashboard/testimonials/<int:pk>/edit/", views.testimonial_update, name="testimonial_update"),
    path("dashboard/testimonials/<int:pk>/delete/", views.testimonial_delete, name="testimonial_delete"),

    path("dashboard/contacts/", views.view_contacts, name="view_contacts"),
    path("dashboard/contacts/<int:pk>/delete/", views.delete_contact, name="delete_contact"),
]
