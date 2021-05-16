from django.contrib import admin

# Register your models here.
from matmgmt.models import BelPartNumber, Inventory,  PartMaster, StockIssue, StoreLocation, Reservation


admin.site.register(BelPartNumber)
admin.site.register(PartMaster)
admin.site.register(Inventory)
admin.site.register(Reservation)
admin.site.register(StoreLocation)
admin.site.register(StockIssue)
