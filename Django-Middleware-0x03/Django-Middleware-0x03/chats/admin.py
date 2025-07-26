from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Property,
    Booking,
    Payment,
    Review,
    Conversation,
    Message,
)

User = get_user_model()

# =========================
# Custom User Admin
# =========================

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)

# =========================
# Register Other Models
# =========================

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'location', 'price_per_night', 'created_at')
    search_fields = ('name', 'location', 'host__email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'property', 'user', 'status', 'start_date', 'end_date', 'total_price')
    list_filter = ('status',)
    search_fields = ('booking_id', 'property__name', 'user__email')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'property', 'user', 'rating', 'created_at')
    search_fields = ('property__name', 'user__email')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    filter_horizontal = ('participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'sent_at')
    search_fields = ('sender__email', 'conversation__conversation_id')
