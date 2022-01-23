from django.contrib import admin
from app.models import Source, Tins


@admin.register(Source)
class Source(admin.ModelAdmin):
    list_display = ('company_name', 'total_amount', 'company_address', 'document_type',
                    'number_id', 'sell_for', 'is_exists', 'start_ts', 'parsing_ts')


@admin.register(Tins)
class Tins(admin.ModelAdmin):
    pass