from django.contrib import admin
from .models import Problem
from django.utils.html import format_html
from django.urls import reverse


class ProblemAdmin(admin.ModelAdmin):

    list_display = ["id", "title", "start"]
    # search_fields = ["id", "audit_unit__id"]

    def start(self, obj):
        """Add column to start services"""
        return format_html(
            '<a class="button" href="{}">Start</a>&ensp;<a class="button" href="{}">Stop</a>',
            reverse("fedota:start_problem", args=[obj.pk]),
            reverse("fedota:stop_problem", args=[obj.pk]),
        )

    start.short_description = "Actions"
    start.allow_tags = True

admin.site.register(Problem, ProblemAdmin)