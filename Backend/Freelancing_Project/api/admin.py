from django.contrib import admin
from .models import User, Project, Proposal

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_freelancer', 'is_client']
    search_fields = ['username', 'email']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'budget','department']
    search_fields = ['title', 'client__username','department']
    list_filter = ['budget','department']

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['project', 'freelancer','client', 'bid_amount']
    search_fields = ['project__title', 'freelancer__username']
    list_filter = ['bid_amount']
