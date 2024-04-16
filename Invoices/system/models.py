from django.db import models
from account.models import *
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)


class Vendor(models.Model):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(UserAccount, related_name='VendorUsers', blank=True, null=True)
    projects = models.ManyToManyField(Project, related_name='VendorProjects', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ProductUom(models.Model):
    name = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)


# class ProductCategory(models.Model):
#     name = models.CharField(max_length=256)
#     timestamp = models.DateTimeField(auto_now_add=True)
    

class Product(models.Model):
    item = models.PositiveBigIntegerField()
    product_id = models.CharField(max_length=256)
    description = models.TextField()
    quantity = models.PositiveBigIntegerField()
    uom = models.ForeignKey(ProductUom, on_delete=models.CASCADE)
    category = models.CharField(max_length=256, blank=True, null=True)
    delivery_date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)


class RFQType(models.Model):
    name = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)


class RFQCurrency(models.Model):
    name = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)


RFQ_status_choices = [
    ('s', 'Sent'),
    ('v', 'Viewed'),
    ('r', 'Replyed'),
]

RFQ_QuotesRequiredForAllItems = [
    ('y', 'Yes'),
    ('n', 'No'),
]
RFQ_BidderCanChangeSubmittedQuote = [
    ('y', 'Yes'),
    ('n', 'No'),
]
RFQ_BidderCanAddItems = [
    ('y', 'Yes'),
    ('n', 'No'),
]
RFQ_BidderCanChangeQuantity = [
    ('y', 'Yes'),
    ('n', 'No'),
]


class RFQ(models.Model):
    RFQ_ID = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    ship_to_address = models.TextField()
    bidder_id = models.CharField(max_length=256)
    type = models.ForeignKey(RFQType, on_delete=models.CASCADE)
    submission_deadline = models.DateTimeField()
    Quote_must_be_valid_until = models.DateField()
    currency = models.ForeignKey(RFQCurrency, on_delete=models.CASCADE)
    Quotes_required_for_all_items = models.CharField(max_length=10, choices=RFQ_QuotesRequiredForAllItems)
    Bidder_can_change_submitted_quote = models.CharField(max_length=10, choices=RFQ_BidderCanChangeSubmittedQuote)
    Bidder_can_add_items = models.CharField(max_length=10, choices=RFQ_BidderCanAddItems)
    Bidder_can_change_quantity = models.CharField(max_length=10, choices=RFQ_BidderCanChangeQuantity)
    products = models.ManyToManyField(Product, related_name='RFQProduct')
    status = models.CharField(max_length=50, choices=RFQ_status_choices, default=RFQ_status_choices[0][0])
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class RFQFileHandler(models.Model):
    file = models.FileField(upload_to='files/RFQ/')
    RFQ = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='RFQfiles')
    timestamp = models.DateTimeField(auto_now_add=True)



@receiver(pre_delete, sender=RFQ)
def RFQ_delete_related_files(sender, instance, **kwargs):
    """
    Signal handler to delete all related FileHandler objects and their associated files.
    """
    file_handlers = instance.RFQfiles.all()
    for file_handler in file_handlers:
        file_path = file_handler.file.path
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        file_handler.delete()



Quotation_status_choices = [
    ('c', 'Created'),
    ('a', 'Approved'),
    ('r', 'Rejected'),
]

class Quotation(models.Model):
    RFQ = models.ForeignKey(RFQ, on_delete=models.CASCADE)
    currency = models.ForeignKey(RFQCurrency, on_delete=models.CASCADE)
    net_value = models.PositiveBigIntegerField()
    status = models.CharField(max_length=256, choices=Quotation_status_choices, default=Quotation_status_choices[0][0])
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class QuotationFileHandler(models.Model):
    file = models.FileField(upload_to='files/Quotation/')
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='Quotationfiles')
    timestamp = models.DateTimeField(auto_now_add=True)
    

@receiver(pre_delete, sender=Quotation)
def Quotation_delete_related_files(sender, instance, **kwargs):
    """
    Signal handler to delete all related FileHandler objects and their associated files.
    """
    file_handlers = instance.Quotationfiles.all()
    for file_handler in file_handlers:
        file_path = file_handler.file.path
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        file_handler.delete()
        

class ApprovedQuotation(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    feedback = models.TextField(default='Quotation Approved')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class RejectedQuotation(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    feedback = models.TextField(default='Quotation Rejected')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    

class POMilestone(models.Model):
    precentage = models.PositiveBigIntegerField()
    due = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField()
    amount = models.FloatField(blank=True, null=True)
    remaining = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



PO_status_choices = [
    ('o', 'Opened'),
    ('c', 'Closed'),
]


class PurchaseOrder(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    number = models.CharField(max_length=256)
    contact_person = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    total_value = models.FloatField()
    remaining_value = models.FloatField()
    currency = models.ForeignKey(RFQCurrency, on_delete=models.CASCADE)
    shipping_terms = models.TextField()
    milestones = models.ManyToManyField(POMilestone, related_name='POMilestones')
    status = models.CharField(max_length=256, choices=PO_status_choices, default=PO_status_choices[0][0])
    timestamp = models.DateTimeField(auto_now_add=True)


class POFileHandler(models.Model):
    file = models.FileField(upload_to='files/PO/')
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='POfiles')
    timestamp = models.DateTimeField(auto_now_add=True)
    

@receiver(pre_delete, sender=PurchaseOrder)
def PO_delete_related_files(sender, instance, **kwargs):
    """
    Signal handler to delete all related FileHandler objects and their associated files.
    """
    file_handlers = instance.POfiles.all()
    for file_handler in file_handlers:
        file_path = file_handler.file.path
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        file_handler.delete()



# class ItemUom(models.Model):
#     name = models.CharField(max_length=10)
#     timestamp = models.DateTimeField(auto_now_add=True)
    

# class Item(models.Model):    
#     number = models.CharField(max_length=256)
#     description = models.TextField()
#     quantity = models.FloatField()
#     uom = models.ForeignKey(ItemUom, on_delete=models.CASCADE)
#     unit_price = models.FloatField()
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)


class InvoiceType(models.Model):
    name = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)


class InvoiceVat(models.Model):
    amount = models.PositiveBigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class InvoiceCurrency(models.Model):
    name = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    milestone = models.ForeignKey(POMilestone, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    number = models.CharField(max_length=256)
    date = models.DateField()
    amount = models.FloatField()
    payment_due = models.PositiveBigIntegerField()
    bill_to = models.CharField(max_length=256)
    type = models.ForeignKey(InvoiceType, on_delete=models.CASCADE)
    currency = models.ForeignKey(InvoiceCurrency, on_delete=models.CASCADE)
    vat = models.ForeignKey(InvoiceVat, on_delete=models.CASCADE)
    # items = models.ManyToManyField(Item, related_name='InvoiceItems')
    timestamp = models.DateTimeField(auto_now_add=True)


class FileHandler(models.Model):
    file = models.FileField(upload_to='files/Invoices/')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoicefiles')
    timestamp = models.DateTimeField(auto_now_add=True)



@receiver(pre_delete, sender=Invoice)
def delete_related_files(sender, instance, **kwargs):
    """
    Signal handler to delete all related FileHandler objects and their associated files.
    """
    file_handlers = instance.invoicefiles.all()
    for file_handler in file_handlers:
        file_path = file_handler.file.path
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        file_handler.delete()


status_choices = [
    ('p', 'Pending'),
    ('a', 'Approved'),
    ('r', 'Rejected'),
]

class SubmittedInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    feedback = models.TextField(default='Invoice Submitted')
    status = models.CharField(max_length=50, choices=status_choices, default=status_choices[0][0])
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class PendingInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    feedback = models.TextField(default='Invoice Pending')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class ApprovedInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    feedback = models.TextField(default='Invoice Approved')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class RejectedInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    feedback = models.TextField(default='Invoice Rejected')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



