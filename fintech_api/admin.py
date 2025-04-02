from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Wallet, Invoice, VirtualCard, VirtualAccount, Transaction, Notification

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'two_factor_enabled', 'created_at')
    list_filter = ('is_active', 'is_staff', 'two_factor_enabled', 'created_at')
    
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('2FA Settings'), {'fields': ('two_factor_enabled', 'otpauth_url', 'otp_base32', 'qr_code', 'login_otp', 'login_otp_used', 'otp_created_at')}),
        (_('Important Dates'), {'fields': ('created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'two_factor_enabled'),
        }),
    )
    
    model = CustomUser
    
    # Override formfield_for_dbfield to make some fields read-only where appropriate
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['created_at', 'updated_at', 'otp_created_at']
        if obj:  # Editing an existing user
            readonly_fields.append('email')  # Prevent email changes after creation
        return readonly_fields

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'balance', 'created_at')
    list_filter = ('currency',)
    search_fields = ('user__email',)
    ordering = ('-created_at',)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'wallet', 'amount', 'currency', 'recipient', 'status', 'created_at')
    list_filter = ('status', 'currency')
    search_fields = ('user__email', 'recipient')
    ordering = ('-created_at',)

class VirtualCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number_last_four', 'expiry_date', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'card_number')
    ordering = ('-created_at',)

    def card_number_last_four(self, obj):
        return obj.card_number[-4:]
    card_number_last_four.short_description = 'Card Number (Last 4)'

class VirtualAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'currency', 'balance', 'is_active', 'created_at')
    list_filter = ('currency', 'is_active')
    search_fields = ('user__email', 'account_number')
    ordering = ('-created_at',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'wallet', 'amount', 'currency', 'transaction_type', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'currency')
    search_fields = ('user__email', 'description')
    ordering = ('-created_at',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__email', 'message')
    ordering = ('-created_at',)

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(VirtualCard, VirtualCardAdmin)
admin.site.register(VirtualAccount, VirtualAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Notification, NotificationAdmin)
