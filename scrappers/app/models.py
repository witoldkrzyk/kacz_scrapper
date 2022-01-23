from django.db import models


class Source(models.Model):
    id = models.BigAutoField(primary_key=True)
    tin = models.ForeignKey('Tins', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    document_type = models.CharField(max_length=255, blank=True, null=True)
    number_id = models.CharField(max_length=255, blank=True, null=True)
    sell_for = models.CharField(max_length=255, blank=True, null=True)
    is_exists = models.BooleanField(default=False)
    start_ts = models.DateTimeField(blank=True, null=True)
    parsing_ts = models.DateTimeField(blank=True, null=True)


class Tins(models.Model):
    id = models.BigAutoField(primary_key=True)
    tin = models.CharField(max_length=255, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tin