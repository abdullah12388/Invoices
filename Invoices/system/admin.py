from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]

@admin.register(ItemUom)
class ItemUomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'number',
        'description',
        'quantity',
        'uom',
        'unit_price',
        'amount',
        'timestamp',
    ]
    
@admin.register(InvoiceType)
class InvoiceTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]
    
@admin.register(InvoiceVat)
class InvoiceVatAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'amount',
        'timestamp',
    ]
    
@admin.register(InvoiceCurrency)
class InvoiceCurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]
    
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'po',
        'milestone',
        'vendor',
        'project',
        'number',
        'date',
        'payment_due',
        'bill_to',
        'type',
        'currency',
        'vat',
        'timestamp',
    ]
    
@admin.register(FileHandler)
class FileHandlerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file',
        'invoice',
        'timestamp',
    ]
    
@admin.register(SubmittedInvoice)
class SubmittedInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'invoice',
        'feedback',
        'user',
        'timestamp',
    ]

@admin.register(PendingInvoice)
class SubmittedInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'invoice',
        'feedback',
        'user',
        'timestamp',
    ]

@admin.register(ApprovedInvoice)
class ApprovedInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'invoice',
        'feedback',
        'user',
        'timestamp',
    ]

@admin.register(RejectedInvoice)
class RejectedInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'invoice',
        'feedback',
        'user',
        'timestamp',
    ]
    
@admin.register(ProductUom)
class ProductUomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]
    
# @admin.register(ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'name',
#         'timestamp',
#     ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'item',
        'product_id',
        'description',
        'quantity',
        'uom',
        'category',
        'delivery_date',
        'timestamp',
    ]

@admin.register(RFQType)
class RFQTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]

@admin.register(RFQCurrency)
class RFQCurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'timestamp',
    ]

@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'RFQ_ID',
        'project',
        'vendor',
        'ship_to_address',
        'bidder_id',
        'type',
        'submission_deadline',
        'Quote_must_be_valid_until',
        'currency',
        'Quotes_required_for_all_items',
        'Bidder_can_change_submitted_quote',
        'Bidder_can_add_items',
        'Bidder_can_change_quantity',
        'status',
        'user',
        'timestamp',
    ]
    
@admin.register(RFQFileHandler)
class RFQFileHandlerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file',
        'RFQ',
        'timestamp',
    ]

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'RFQ',
        'net_value',
        'currency',
        'status',
        'user',
        'timestamp',
    ]
    
    
@admin.register(QuotationFileHandler)
class QuotationFileHandlerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file',
        'quotation',
        'timestamp',
    ]


@admin.register(ApprovedQuotation)
class ApprovedQuotationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'quotation',
        'feedback',
        'user',
        'timestamp',
    ]


@admin.register(RejectedQuotation)
class RejectedQuotationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'quotation',
        'feedback',
        'user',
        'timestamp',
    ]


@admin.register(POMilestone)
class POMilestoneAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'precentage',
        'due',
        'description',
        'amount',
        'remaining',
        'timestamp',
    ]


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'number',
        'contact_person',
        'total_value',
        'currency',
        'shipping_terms',
        'timestamp',
    ]

@admin.register(POFileHandler)
class POFileHandlerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file',
        'po',
        'timestamp',
    ]