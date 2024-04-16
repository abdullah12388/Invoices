from django.test import TestCase
from system.models import *
from account.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, date

class TestModels(TestCase):
    
    def setUp(self):
        self.project = Project.objects.create(name='project1')
        self.vendor = Vendor.objects.create(name = 'Vendor')
        self.user = UserAccount.objects.create(
            first_name = 'Abdullah',
            last_name = 'Kamal',
            email = 'abdullah.mk96@yahoo.com',
            username = 'abdullah',
            password = make_password('As123123'),
            role = UserType.objects.create(type='Manager'),
            first_login = 1
        )
        self.product_uom = ProductUom.objects.create(name='meter')
        self.product = Product.objects.create(
            item = 1,
            product_id = 123456,
            description = 'Text Description',
            quantity = 50,
            uom = self.product_uom,
            delivery_date = '2024-04-02'
        )
        self.rfq_type = RFQType.objects.create(name='RFQ TYPE NAME')
        self.rfq_currency = RFQCurrency.objects.create(name='EGP')
        self.rfq = RFQ.objects.create(
            RFQ_ID = 100,
            project = self.project,
            vendor = self.vendor,
            ship_to_address = 'Address Description',
            bidder_id = 123456,
            type = self.rfq_type,
            submission_deadline = '2024-04-02 00:00:00.000',
            Quote_must_be_valid_until = '2024-04-02',
            currency = self.rfq_currency,
            Quotes_required_for_all_items = 'y',
            Bidder_can_change_submitted_quote = 'y',
            Bidder_can_add_items = 'y',
            Bidder_can_change_quantity = 'y',
            status = 's',
            user = self.user
        )
        self.vendor_user = UserAccount.objects.create(
            first_name = 'Ali',
            last_name = 'Kamal',
            email = 'abdullah.mohamed@globalts-eg.com',
            username = 'ali',
            password = make_password('As123123'),
            role = UserType.objects.create(type='vendor'),
            first_login = 1
        )
        self.vendor.users.add(self.vendor_user)
        self.quotation = Quotation.objects.create(
            RFQ = self.rfq,
            currency = self.rfq_currency,
            net_value = 1000,
            status = 'c',
            user = self.vendor_user
        )
        self.presales_user = UserAccount.objects.create(
            first_name = 'hassan',
            last_name = 'Kamal',
            email = 'hassan.mohamed@globalts-eg.com',
            username = 'hassan',
            password = make_password('As123123'),
            role = UserType.objects.create(type='presales'),
            first_login = 1
        )
        self.approve_quotation= ApprovedQuotation.objects.create(
            quotation = self.quotation,
            feedback = 'Quotation Approved',
            user = self.presales_user
        )
        self.reject_quotation= RejectedQuotation.objects.create(
            quotation = self.quotation,
            feedback = 'Quotation Rejected',
            user = self.presales_user
        )
        self.po_milestone = POMilestone.objects.create(
            precentage = 100,
            due = 30,
            description = 'Milestone 100% Description',
            amount = 10000,
            remaining = 10000
        )
        self.po = PurchaseOrder.objects.create(
            quotation = self.quotation,
            number = '123456789',
            contact_person = self.presales_user,
            total_value = 10000,
            remaining_value = 10000,
            currency = self.rfq_currency,
            shipping_terms = 'PO shipping terms',
            status = 'o'
        )    
        self.invoice_type = InvoiceType.objects.create(
            name = 'Invoice Type'
        )
        self.invoice_vat = InvoiceVat.objects.create(
            amount = 5
        )
        self.invoice_currency = InvoiceCurrency.objects.create(
            name = 'USD'
        )
        self.invoice = Invoice.objects.create(
            po = self.po,
            milestone = self.po_milestone,
            vendor = self.vendor,
            project = self.project,
            number = '123456789',
            date = datetime.now().date(),
            amount = 10000.000,
            payment_due = 30,
            bill_to = 'Ali Essam',
            type = self.invoice_type,
            currency = self.invoice_currency,
            vat =self.invoice_vat
        )
        self.invoice_submitted = SubmittedInvoice.objects.create(
            invoice = self.invoice,
            feedback = 'Invoice Submitted',
            status = 'p',
            user = self.vendor_user
        )
        self.invoice_pending = PendingInvoice.objects.create(
            invoice = self.invoice,
            feedback = 'Invoice Pending',
            user = self.vendor_user
        )
        self.invoice_approved = ApprovedInvoice.objects.create(
            invoice = self.invoice,
            feedback = 'Invoice Approved',
            user = self.vendor_user
        )
        self.invoice_rejected = RejectedInvoice.objects.create(
            invoice = self.invoice,
            feedback = 'Invoice Rejected',
            user = self.vendor_user
        )
        
    def test_Project_model_creation(self):
        self.assertEqual(self.project.name, 'project1')
    
    def test_Vendor_model_creation(self):
        self.assertEqual(self.vendor.name, 'Vendor')
        self.assertIsNotNone(self.vendor.timestamp)
        
    def test_vendor_users_model_relationship(self):
        self.vendor.users.add(self.user)
        self.assertIn(self.user, self.vendor.users.all())
        
    def test_vendor_projects_model_relationship(self):
        self.vendor.projects.add(self.project)
        self.assertIn(self.project, self.vendor.projects.all())
    
    def test_ProductUom_model_creation(self):
        self.assertEqual(self.product_uom.name, 'meter')
        self.assertIsNotNone(self.product_uom.timestamp)
    
    def test_Product_model_creation(self):
        self.assertEqual(self.product.item, 1)
        self.assertEqual(self.product.product_id, 123456)
        self.assertEqual(self.product.description, 'Text Description')
        self.assertEqual(self.product.quantity, 50)
        self.assertEqual(self.product.uom, self.product_uom)
        self.assertIsNone(self.product.category)
        self.assertEqual(self.product.delivery_date, '2024-04-02')
        self.assertIsNotNone(self.product.timestamp)
    
    def test_RFQType_model_creation(self):
        self.assertEqual(self.rfq_type.name, 'RFQ TYPE NAME')
        self.assertIsNotNone(self.rfq_type.timestamp)
        
    def test_RFQCurrency_model_creation(self):
        self.assertEqual(self.rfq_currency.name, 'EGP')
        self.assertIsNotNone(self.rfq_currency.timestamp)
    
    def test_RFQ_model_creation(self):
        self.assertEqual(self.rfq.RFQ_ID, 100)
        self.assertEqual(self.rfq.project, self.project)
        self.assertEqual(self.rfq.vendor, self.vendor)
        self.assertEqual(self.rfq.ship_to_address, 'Address Description')
        self.assertEqual(self.rfq.bidder_id, 123456)
        self.assertEqual(self.rfq.type, self.rfq_type)
        self.assertEqual(self.rfq.submission_deadline, '2024-04-02 00:00:00.000')
        self.assertEqual(self.rfq.Quote_must_be_valid_until, '2024-04-02')
        self.assertEqual(self.rfq.currency, self.rfq_currency)
        self.assertEqual(self.rfq.Quotes_required_for_all_items, 'y')
        self.assertEqual(self.rfq.Bidder_can_change_submitted_quote, 'y')
        self.assertEqual(self.rfq.Bidder_can_add_items, 'y')
        self.assertEqual(self.rfq.Bidder_can_change_quantity, 'y')
        self.assertEqual(self.rfq.status, 's')
        self.assertEqual(self.rfq.user, self.user)
        self.assertIsNotNone(self.rfq.timestamp)
    
    def test_RFQ_products_model_relationship(self):
        self.rfq.products.add(self.product)
        self.assertIn(self.product, self.rfq.products.all())
    
    def test_RFQFileHandler_model_creation(self):
        with open('D:/Invoices/Invoices/system/tests/test_file.pdf', 'rb') as file:
            test_file = SimpleUploadedFile('test_file.pdf', file.read(), content_type='application/pdf')
        
        rfq_file_handler = RFQFileHandler.objects.create(
            file = test_file,
            RFQ = self.rfq
        )
        self.assertIn('files/RFQ/', rfq_file_handler.file.name)
        # self.assertEqual(rfq_file_handler.file.name, 'files/RFQ/test_file.pdf')
        self.assertEqual(rfq_file_handler.RFQ, self.rfq)
        self.assertIsInstance(rfq_file_handler.timestamp, datetime)
        
    def test_RFQ_delete_related_files_signal(self):
        RFQ_delete_related_files(RFQ, self.rfq)
        self.assertEqual(RFQFileHandler.objects.filter(RFQ=self.rfq).exists(), False)
    
    def test_Quotation_model_creation(self):
        self.assertEqual(self.quotation.RFQ, self.rfq)
        self.assertEqual(self.quotation.currency, self.rfq_currency)
        self.assertEqual(self.quotation.net_value, 1000)
        self.assertEqual(self.quotation.status, 'c')
        self.assertEqual(self.quotation.user, self.vendor_user)
        self.assertIsNotNone(self.quotation.timestamp)
    
    def test_QuotationFileHandler_model_creation(self):
        with open('D:/Invoices/Invoices/system/tests/test_file.pdf', 'rb') as file:
            test_file = SimpleUploadedFile('test_file.pdf', file.read(), content_type='application/pdf')
        
        quotation_file_handler = QuotationFileHandler.objects.create(
            file = test_file,
            quotation = self.quotation
        )
        self.assertIn('files/Quotation/', quotation_file_handler.file.name)
        # self.assertEqual(rfq_file_handler.file.name, 'files/RFQ/test_file.pdf')
        self.assertEqual(quotation_file_handler.quotation, self.quotation)
        self.assertIsInstance(quotation_file_handler.timestamp, datetime)
        
    def test_Quotation_delete_related_files_signal(self):
        Quotation_delete_related_files(Quotation, self.quotation)
        self.assertEqual(QuotationFileHandler.objects.filter(quotation=self.quotation).exists(), False)
    
    def test_ApprovedQuotation_model_creation(self):
        self.assertEqual(self.approve_quotation.quotation, self.quotation)
        self.assertEqual(self.approve_quotation.feedback, 'Quotation Approved')
        self.assertEqual(self.approve_quotation.user, self.presales_user)
        self.assertIsInstance(self.approve_quotation.timestamp, datetime)
    
    def test_RejectedQuotation_model_creation(self):
        self.assertEqual(self.reject_quotation.quotation, self.quotation)
        self.assertEqual(self.reject_quotation.feedback, 'Quotation Rejected')
        self.assertEqual(self.reject_quotation.user, self.presales_user)
        self.assertIsInstance(self.reject_quotation.timestamp, datetime)
    
    def test_POMilestone_model_creation(self):
        self.assertEqual(self.po_milestone.precentage, 100)
        self.assertEqual(self.po_milestone.due, 30)
        self.assertEqual(self.po_milestone.description, 'Milestone 100% Description')
        self.assertEqual(self.po_milestone.amount, 10000)
        self.assertEqual(self.po_milestone.remaining, 10000)
        self.assertIsInstance(self.po_milestone.timestamp, datetime)

    def test_PurchaseOrder_model_creation(self):
        self.assertEqual(self.po.quotation, self.quotation)
        self.assertEqual(self.po.number, '123456789')
        self.assertEqual(self.po.contact_person, self.presales_user)
        self.assertEqual(self.po.total_value, 10000)
        self.assertEqual(self.po.remaining_value, 10000)
        self.assertEqual(self.po.currency, self.rfq_currency)
        self.assertEqual(self.po.shipping_terms, 'PO shipping terms')
        self.assertEqual(self.po.status, 'o')
        self.assertIsNotNone(self.po.timestamp)
        
    def test_PO_Milestones_model_relationship(self):
        self.po.milestones.add(self.po_milestone)
        self.assertIn(self.po_milestone, self.po.milestones.all())
    
    def test_POFileHandler_model_creation(self):
        with open('D:/Invoices/Invoices/system/tests/test_file.pdf', 'rb') as file:
            test_file = SimpleUploadedFile('test_file.pdf', file.read(), content_type='application/pdf')
        
        po_file_handler = POFileHandler.objects.create(
            file = test_file,
            po = self.po
        )
        self.assertIn('files/PO/', po_file_handler.file.name)
        # self.assertEqual(rfq_file_handler.file.name, 'files/RFQ/test_file.pdf')
        self.assertEqual(po_file_handler.po, self.po)
        self.assertIsInstance(po_file_handler.timestamp, datetime)
        
    def test_PO_delete_related_files_signal(self):
        PO_delete_related_files(PurchaseOrder, self.po)
        self.assertEqual(POFileHandler.objects.filter(po=self.po).exists(), False)
    
    def test_InvoiceType_model_creation(self):
        self.assertEqual(self.invoice_type.name, 'Invoice Type')
        self.assertIsInstance(self.invoice_type.timestamp, datetime)
    
    def test_InvoiceVat_model_creation(self):
        self.assertEqual(self.invoice_vat.amount, 5)
        self.assertIsInstance(self.invoice_vat.timestamp, datetime)
    
    def test_InvoiceCurrency_model_creation(self):
        self.assertEqual(self.invoice_currency.name, 'USD')
        self.assertIsInstance(self.invoice_currency.timestamp, datetime)

    def test_Invoice_model_creation(self):
        self.assertEqual(self.invoice.po, self.po)
        self.assertEqual(self.invoice.milestone, self.po_milestone)
        self.assertEqual(self.invoice.vendor, self.vendor)
        self.assertEqual(self.invoice.project, self.project)
        self.assertEqual(self.invoice.number, '123456789')
        self.assertIsInstance(self.invoice.date, date)
        self.assertEqual(self.invoice.amount, 10000.000)
        self.assertEqual(self.invoice.payment_due, 30)
        self.assertEqual(self.invoice.bill_to, 'Ali Essam')
        self.assertEqual(self.invoice.type, self.invoice_type)
        self.assertEqual(self.invoice.currency, self.invoice_currency)
        self.assertEqual(self.invoice.vat, self.invoice_vat)
        self.assertIsInstance(self.invoice.timestamp, datetime)

    def test_InvoiceFileHandler_model_creation(self):
        with open('D:/Invoices/Invoices/system/tests/test_file.pdf', 'rb') as file:
            test_file = SimpleUploadedFile('test_file.pdf', file.read(), content_type='application/pdf')
        
        invoice_file_handler = FileHandler.objects.create(
            file = test_file,
            invoice = self.invoice
        )
        self.assertIn('files/Invoices/', invoice_file_handler.file.name)
        # self.assertEqual(rfq_file_handler.file.name, 'files/RFQ/test_file.pdf')
        self.assertEqual(invoice_file_handler.invoice, self.invoice)
        self.assertIsInstance(invoice_file_handler.timestamp, datetime)
        
    def test_Invoice_delete_related_files_signal(self):
        delete_related_files(Invoice, self.invoice)
        self.assertEqual(FileHandler.objects.filter(invoice=self.invoice).exists(), False)

    def test_SubmittedInvoice_model_creation(self):
        self.assertEqual(self.invoice_submitted.invoice, self.invoice)
        self.assertEqual(self.invoice_submitted.feedback, 'Invoice Submitted')
        self.assertEqual(self.invoice_submitted.status, 'p')
        self.assertEqual(self.invoice_submitted.user, self.vendor_user)
        self.assertIsInstance(self.invoice_submitted.timestamp, datetime)

    def test_PendingInvoice_model_creation(self):
        self.assertEqual(self.invoice_pending.invoice, self.invoice)
        self.assertEqual(self.invoice_pending.feedback, 'Invoice Pending')
        self.assertEqual(self.invoice_pending.user, self.vendor_user)
        self.assertIsInstance(self.invoice_pending.timestamp, datetime)

    def test_ApprovedInvoice_model_creation(self):
        self.assertEqual(self.invoice_approved.invoice, self.invoice)
        self.assertEqual(self.invoice_approved.feedback, 'Invoice Approved')
        self.assertEqual(self.invoice_approved.user, self.vendor_user)
        self.assertIsInstance(self.invoice_approved.timestamp, datetime)

    def test_RejectedInvoice_model_creation(self):
        self.assertEqual(self.invoice_rejected.invoice, self.invoice)
        self.assertEqual(self.invoice_rejected.feedback, 'Invoice Rejected')
        self.assertEqual(self.invoice_rejected.user, self.vendor_user)
        self.assertIsInstance(self.invoice_rejected.timestamp, datetime)





    
    
    
    
    
    
    
    
    
    
    
    