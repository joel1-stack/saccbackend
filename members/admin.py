from django.contrib import admin
from .models import Member, MemberDocument


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_number', 'user', 'national_id', 'status', 'membership_fee_paid', 'registration_date']
    list_filter = ['status', 'membership_fee_paid', 'registration_date']
    search_fields = ['member_number', 'user__username', 'user__email', 'national_id']
    readonly_fields = ['member_number', 'registration_date', 'updated_at']


@admin.register(MemberDocument)
class MemberDocumentAdmin(admin.ModelAdmin):
    list_display = ['member', 'document_type', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['member__member_number', 'member__user__username']