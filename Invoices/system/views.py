import json
import os
from django.shortcuts import render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, Sum, Max, Min
from django.db import connection
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime, timedelta, time
from .decorators import is_user_login
from collections import Counter, defaultdict
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.core.serializers import serialize
from django.conf import settings
# for E-mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Create your views here.

####################### VENDOR ###########################################
@is_user_login
def VendorDashboardView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    # t_invoice = Invoice.objects.count()
    t_invoice = SubmittedInvoice.objects.filter(user=user_obj).count()
    p_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[0][0]).count()
    a_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[1][0]).count()
    r_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[2][0]).count()
    context = {
        'user': user_obj,
        # 't_invoice': t_invoice,
        't_invoice': t_invoice,
        'p_invoice': p_invoice,
        'a_invoice': a_invoice,
        'r_invoice': r_invoice
    }
    return render(request, 'VendorDashboard.html', context)


@is_user_login
def VendorInvoicesStatusColumnChartApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        filter = request.GET.get('filter', None)
        from_value = request.GET.get('from', None)
        to_value = request.GET.get('to', None)
        current_date = datetime.now().date()
        filters_query = Q()
        if from_value:
            if filter == 'per_time':
                filters_query &= (Q(timestamp__date=current_date) & Q(timestamp__time__gte=from_value))
            if filter == 'per_day':
                filters_query &= Q(timestamp__date__gte=from_value)
            if filter == 'per_month':
                year_from, month_from = map(int, from_value.split('-'))
                filters_query &= (Q(timestamp__year__gt=year_from) | (Q(timestamp__year=year_from) & Q(timestamp__month__gte=month_from)))
            if filter == 'per_year':
                filters_query &= Q(timestamp__year__gte=from_value)
        if to_value:
            if filter == 'per_time':
                filters_query &= (Q(timestamp__date=current_date) & Q(timestamp__time__lte=to_value))
            if filter == 'per_day':
                filters_query &= Q(timestamp__date__lte=to_value)
            if filter == 'per_month':
                year_to, month_to = map(int, to_value.split('-'))
                filters_query &= (Q(timestamp__year__lt=year_to) | (Q(timestamp__year=year_to) & Q(timestamp__month__lte=month_to)))
                # print(year_to, month_to, filters_query)
            if filter == 'per_year':
                filters_query &= Q(timestamp__year__lte=to_value)
        p_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[0][0]).filter(filters_query).count()
        a_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[1][0]).filter(filters_query).count()
        r_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[2][0]).filter(filters_query).count()
        # print(p_invoice, a_invoice, r_invoice)
    else:
        p_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[0][0]).count()
        a_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[1][0]).count()
        r_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[2][0]).count()
    data = [
        ['Pending', p_invoice, p_invoice, '#343a40'],
        ['Approved', a_invoice, a_invoice, '#28a745'],
        ['Rejected', r_invoice, r_invoice, '#dc3545'],
    ]
    return JsonResponse(data=data, safe=False)


@is_user_login
def VendorInvoicesStatusPieChartApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    p_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[0][0]).count()
    a_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[1][0]).count()
    r_invoice = SubmittedInvoice.objects.filter(user=user_obj, status=status_choices[2][0]).count()
    data = [
        ['Pending', p_invoice],
        ['Approved', a_invoice],
        ['Rejected', r_invoice],
    ]
    return JsonResponse(data=data, safe=False)




@is_user_login
def VendorPendingRFQView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        vendor = cursor.execute(f"SELECT DISTINCT [vendor_id] FROM [Invoices].[dbo].[system_vendor_users] WHERE [useraccount_id] = {user_obj.id}")
        vendor_results = vendor.fetchall()

        RFQ_ID = cursor.execute(f"SELECT DISTINCT [RFQ_ID] FROM [Invoices].[dbo].[system_rfq] WHERE [vendor_id] = {vendor_results[0][0]} AND [status] != 'r'")
        RFQ_ID_results = RFQ_ID.fetchall()
        project = cursor.execute(f"""SELECT DISTINCT p.[id], p.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_project] as p
                                WHERE srfq.project_id = p.id and [vendor_id] = {vendor_results[0][0]}""")
        project_results = project.fetchall()
        bidder_id = cursor.execute(f"SELECT DISTINCT [bidder_id] FROM [Invoices].[dbo].[system_rfq] WHERE [vendor_id] = {vendor_results[0][0]}")
        bidder_id_results = bidder_id.fetchall()
        RFQ_type = cursor.execute(f"""SELECT DISTINCT t.[id], t.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqtype] as t
                                WHERE srfq.type_id = t.id and [vendor_id] = {vendor_results[0][0]}""")
        RFQ_type_results = RFQ_type.fetchall()
        RFQ_currency = cursor.execute(f"""SELECT DISTINCT c.[id], c.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqcurrency] as c
                                WHERE srfq.currency_id = c.id and [vendor_id] = {vendor_results[0][0]}""")
        RFQ_currency_results = RFQ_currency.fetchall()
        product_id = cursor.execute(f"""SELECT sp.[id], sp.[product_id] FROM [Invoices].[dbo].[system_rfq_products] as srfqp
                                join [Invoices].[dbo].[system_rfq] as srfq on srfqp.rfq_id = srfq.id
                                join [Invoices].[dbo].[system_product] as sp on srfqp.product_id = sp.id
                                where srfq.vendor_id = {vendor_results[0][0]}""")
        product_id_results = product_id.fetchall()
    context = {
        'user': user_obj,
        'RFQ_ID_results': RFQ_ID_results,
        'project_results': project_results,
        'bidder_id_results': bidder_id_results,
        'RFQ_type_results': RFQ_type_results,
        'RFQ_currency_results': RFQ_currency_results,
        'RFQ_qrfai_results': RFQ_QuotesRequiredForAllItems,
        'RFQ_bccsq_results': RFQ_BidderCanChangeSubmittedQuote,
        'RFQ_bcai_results': RFQ_BidderCanAddItems,
        'RFQ_bccq_results': RFQ_BidderCanChangeQuantity,
        'product_id_results': product_id_results,
    }
    return render(request, 'VendorRFQToDo.html', context)


@is_user_login
def VendorRFQToDoTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        vendor_obj = Vendor.objects.get(users=user_obj)
        RFQ_ID = request.GET.get('RFQ_ID', None)
        project = request.GET.get('project', None)
        Bidder_ID = request.GET.get('Bidder_ID', None)
        RFQ_Type = request.GET.get('RFQ_Type', None)
        eqc = request.GET.get('eqc', None)
        qrfai = request.GET.get('qrfai', None)
        bccsq = request.GET.get('bccsq', None)
        bcai = request.GET.get('bcai', None)
        bccq = request.GET.get('bccq', None)
        Product_ID = request.GET.get('Product_ID', None)
        sd_from = request.GET.get('sd_from', None)
        sd_to = request.GET.get('sd_to', None)
        qmbvu_from = request.GET.get('qmbvu_from', None)
        qmbvu_to = request.GET.get('qmbvu_to', None)

        print(request.GET)
        RFQ_list = RFQ.objects.select_related('project', 'vendor', 'type', 'currency')\
            .filter(vendor=vendor_obj)\
                .exclude(status=RFQ_status_choices[2][0])
                
        if RFQ_ID:
            RFQ_list = RFQ_list.filter(RFQ_ID=RFQ_ID)
        if project:
            RFQ_list = RFQ_list.filter(project_id=project)
        if Bidder_ID:
            RFQ_list = RFQ_list.filter(bidder_id=Bidder_ID)
        if RFQ_Type:
            RFQ_list = RFQ_list.filter(type_id=RFQ_Type)
        if eqc:
            RFQ_list = RFQ_list.filter(currency_id=eqc)
        if qrfai:
            RFQ_list = RFQ_list.filter(Quotes_required_for_all_items=qrfai)
        if bccsq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_submitted_quote=bccsq)
        if bcai:
            RFQ_list = RFQ_list.filter(Bidder_can_add_items=bcai)
        if bccq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_quantity=bccq)
        if Product_ID:
            product_obj = Product.objects.get(id=Product_ID)
            RFQ_list = RFQ_list.filter(products=product_obj)
        if sd_from:
            RFQ_list = RFQ_list.filter(submission_deadline__gte=sd_from)
        if sd_to:
            RFQ_list = RFQ_list.filter(submission_deadline__lte=sd_to)
        if qmbvu_from:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__gte=qmbvu_from)
        if qmbvu_to:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__lte=qmbvu_to)
        # print(RFQ_list[0].status)
        RFQs = [
            {
                "id": rfqlst.id,
                "RFQ_ID": rfqlst.RFQ_ID,
                "vendor": rfqlst.vendor.name,
                "project": rfqlst.project.name,
                "submission_deadline": date_time_formatter(rfqlst.submission_deadline)
            }
            for rfqlst in RFQ_list
        ]
        return JsonResponse(data=RFQs, safe=False)


@is_user_login
def VendorRFQToDoDetailsApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        RFQ_details = RFQ.objects.select_related('project', 'vendor', 'type', 'currency', 'user')\
            .get(RFQ_ID=RFQ_ID)
        RFQ_details.status = RFQ_status_choices[1][0]
        RFQ_details.save()
        # print(invoice_details.invoice.items.first().number)
        products_list = RFQ_details.products.select_related('uom')
        products = []
        products_count = RFQ_details.products.count()
        for product in products_list:
            products.append(
                {
                'item_number': product.item,
                'product_id': product.product_id,
                'description': product.description,
                'quantity': product.quantity,
                'uom': product.uom.name,
                'category': product.category,
                'dd_sp': product.delivery_date,
                }
            )
        
        fhs = RFQFileHandler.objects.filter(RFQ=RFQ_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)
        
        # send emails
        sender = settings.EMAIL_USER
        receiver = [RFQ_details.user.email]
        subject = f"RFQ {RFQ_details.RFQ_ID} | Follow Up"
        message = f"""Dear {RFQ_details.user.first_name},

I hope this find you well.
You need to know that the Request For Quotation (RFQ)
With the following details:
RFQ ID:   {RFQ_details.RFQ_ID}
Project:   {RFQ_details.project.name}
Vendor:   {RFQ_details.vendor.name}

Has Been Viewed By:
Name:   {user_obj.first_name} {user_obj.last_name}
E-Mail:   {user_obj.email}

The whole details will be found in our web portal, waiting for you
To check it out.
Link:   http://127.0.0.1:8000/

*Note: This E-Mail is auto generated from our system, Just for your notification.

Best Regards,
Invoices Management System (IMS)
                        """
        # print([rec.email for rec in receivers_list])
        # send_email(
        #     sender,
        #     receiver,
        #     subject,
        #     message
        # )
        
        RFQ_obj = {
            'id': RFQ_details.id,
            'vendor': RFQ_details.vendor.name,
            'RFQ_ID': RFQ_details.RFQ_ID,
            'project_name': RFQ_details.project.name,
            'ship_to_address': RFQ_details.ship_to_address,
            'bidder_id': RFQ_details.bidder_id,
            'submission_deadline': date_time_formatter(RFQ_details.submission_deadline),
            'qmbvu': RFQ_details.Quote_must_be_valid_until,
            'RFQ_Type': RFQ_details.type.name,
            'eqc': RFQ_details.currency.name,
            'qrfai': 'Yes' if RFQ_details.Quotes_required_for_all_items == 'y' else 'No',
            'bccsq': 'Yes' if RFQ_details.Bidder_can_change_submitted_quote == 'y' else 'No',
            'bcai': 'Yes' if RFQ_details.Bidder_can_add_items == 'y' else 'No',
            'bccq': 'Yes' if RFQ_details.Bidder_can_change_quantity == 'y' else 'No',
            'products': products,
            'products_count':products_count,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=RFQ_obj, safe=False)


def VendorRFQToDoCreateQuoteApi(request):
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        RFQ_details = RFQ.objects.select_related('project', 'vendor', 'type', 'currency')\
            .get(RFQ_ID=RFQ_ID)
        currencies = RFQCurrency.objects.all()
        RFQ_obj = {
            'RFQ_ID': RFQ_details.RFQ_ID,
            'submission_deadline': date_time_formatter(RFQ_details.submission_deadline),
            'qmbvu': RFQ_details.Quote_must_be_valid_until,
            'RFQ_Type': RFQ_details.type.name,
            'eqc': RFQ_details.currency.name,
            'currencies': [[cur.id, cur.name] for cur in currencies],
        }
        # RFQ_details.status = RFQ_status_choices[2][0]
        # RFQ_details.save()
        return JsonResponse(data=RFQ_obj, safe=False)


@is_user_login
def VendorRFQToDoCreateQuoteSubmitApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.POST:
        print(request.POST)
        # RFQ creation
        RFQ_ID = request.POST.get('RFQ_ID', None)
        total_net_value = request.POST.get('total_net_value', None)
        currency = request.POST.get('currency', None)
        
        RFQ_obj = RFQ.objects.get(RFQ_ID=RFQ_ID)
        RFQCurrnecy_obj = RFQCurrency.objects.get(id=currency)
        
        Quotation_obj = Quotation.objects.create(
            RFQ = RFQ_obj,
            currency = RFQCurrnecy_obj,
            net_value = total_net_value,
            status = Quotation_status_choices[0][0],
            user = user_obj
        )
        
        RFQ_obj.status = RFQ_status_choices[2][0]
        RFQ_obj.save()
        
        if request.FILES:
            files = request.FILES.getlist('filepond')
            for file in files:
                QuotationFileHandler.objects.create(
                    file=file,
                    quotation=Quotation_obj,
                )
        
        # send emails
        sender = settings.EMAIL_USER
        receiver = [RFQ_obj.user.email]
        subject = f"RFQ {RFQ_obj.RFQ_ID} | New Quotation"
        message = f"""Dear {RFQ_obj.user.first_name},

I hope this find you well.
You need to know that there is a new Quotation
with the following details:
Quote ID:   {Quotation_obj.id}
RFQ ID:   {RFQ_obj.RFQ_ID}
Project:   {RFQ_obj.project.name}
Vendor:   {RFQ_obj.vendor.name}

Has Been Created By:
Name:   {user_obj.first_name} {user_obj.last_name}
E-Mail:   {user_obj.email}

The whole details will be found in our web portal, waiting for you
To check it out.
Link:   http://127.0.0.1:8000/

*Note: This E-Mail is auto generated from our system, Just for your notification.

Best Regards,
Invoices Management System (IMS)
                        """
        # print([rec.email for rec in receivers_list])
        # send_email(
        #     sender,
        #     receiver,
        #     subject,
        #     message
        # )
            
        data = {
            'status': 'added',
        }
        return JsonResponse(data=data, safe=False)
    





@is_user_login
def VendorDoneRFQView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        vendor = cursor.execute(f"SELECT DISTINCT [vendor_id] FROM [Invoices].[dbo].[system_vendor_users] WHERE [useraccount_id] = {user_obj.id}")
        vendor_results = vendor.fetchall()

        # Quotation_ID = cursor.execute(f"""SELECT DISTINCT sq.[id] FROM [Invoices].[dbo].[system_quotation] AS sq
        #                         JOIN [Invoices].[dbo].[system_rfq] AS srfq ON srfq.[id] = sq.[RFQ_id]
        #                         WHERE srfq.[vendor_id] = {vendor_results[0][0]}""")
        # Quotation_ID_results = Quotation_ID.fetchall()
        RFQ_ID = cursor.execute(f"SELECT DISTINCT [RFQ_ID] FROM [Invoices].[dbo].[system_rfq] WHERE [vendor_id] = {vendor_results[0][0]} AND [status] = 'r'")
        RFQ_ID_results = RFQ_ID.fetchall()
        project = cursor.execute(f"""SELECT DISTINCT p.[id], p.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_project] as p
                                WHERE srfq.project_id = p.id and [vendor_id] = {vendor_results[0][0]} AND srfq.[status] = 'r'""")
        project_results = project.fetchall()
        bidder_id = cursor.execute(f"SELECT DISTINCT [bidder_id] FROM [Invoices].[dbo].[system_rfq] WHERE [vendor_id] = {vendor_results[0][0]} AND [status] = 'r'")
        bidder_id_results = bidder_id.fetchall()
        RFQ_type = cursor.execute(f"""SELECT DISTINCT t.[id], t.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqtype] as t
                                WHERE srfq.type_id = t.id and [vendor_id] = {vendor_results[0][0]} AND srfq.[status] = 'r'""")
        RFQ_type_results = RFQ_type.fetchall()
        RFQ_currency = cursor.execute(f"""SELECT DISTINCT c.[id], c.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqcurrency] as c
                                WHERE srfq.currency_id = c.id and [vendor_id] = {vendor_results[0][0]} AND srfq.[status] = 'r'""")
        RFQ_currency_results = RFQ_currency.fetchall()
        product_id = cursor.execute(f"""SELECT sp.[id], sp.[product_id] FROM [Invoices].[dbo].[system_rfq_products] as srfqp
                                join [Invoices].[dbo].[system_rfq] as srfq on srfqp.rfq_id = srfq.id
                                join [Invoices].[dbo].[system_product] as sp on srfqp.product_id = sp.id
                                where srfq.vendor_id = {vendor_results[0][0]} AND srfq.[status] = 'r'""")
        product_id_results = product_id.fetchall()
    context = {
        'user': user_obj,
        # 'Quotation_ID_results': Quotation_ID_results,
        'RFQ_ID_results': RFQ_ID_results,
        'project_results': project_results,
        'bidder_id_results': bidder_id_results,
        'RFQ_type_results': RFQ_type_results,
        'RFQ_currency_results': RFQ_currency_results,
        'RFQ_qrfai_results': RFQ_QuotesRequiredForAllItems,
        'RFQ_bccsq_results': RFQ_BidderCanChangeSubmittedQuote,
        'RFQ_bcai_results': RFQ_BidderCanAddItems,
        'RFQ_bccq_results': RFQ_BidderCanChangeQuantity,
        'product_id_results': product_id_results,
    }
    return render(request, 'VendorRFQDone.html', context)


@is_user_login
def VendorRFQDoneTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        vendor_obj = Vendor.objects.get(users=user_obj)
        RFQ_ID = request.GET.get('RFQ_ID', None)
        project = request.GET.get('project', None)
        Bidder_ID = request.GET.get('Bidder_ID', None)
        RFQ_Type = request.GET.get('RFQ_Type', None)
        eqc = request.GET.get('eqc', None)
        qrfai = request.GET.get('qrfai', None)
        bccsq = request.GET.get('bccsq', None)
        bcai = request.GET.get('bcai', None)
        bccq = request.GET.get('bccq', None)
        Product_ID = request.GET.get('Product_ID', None)
        sd_from = request.GET.get('sd_from', None)
        sd_to = request.GET.get('sd_to', None)
        qmbvu_from = request.GET.get('qmbvu_from', None)
        qmbvu_to = request.GET.get('qmbvu_to', None)

        print(request.GET)
        RFQ_list = RFQ.objects.select_related('project', 'vendor', 'type', 'currency')\
            .filter(vendor=vendor_obj, status=RFQ_status_choices[2][0])
                
        if RFQ_ID:
            RFQ_list = RFQ_list.filter(RFQ_ID=RFQ_ID)
        if project:
            RFQ_list = RFQ_list.filter(project_id=project)
        if Bidder_ID:
            RFQ_list = RFQ_list.filter(bidder_id=Bidder_ID)
        if RFQ_Type:
            RFQ_list = RFQ_list.filter(type_id=RFQ_Type)
        if eqc:
            RFQ_list = RFQ_list.filter(currency_id=eqc)
        if qrfai:
            RFQ_list = RFQ_list.filter(Quotes_required_for_all_items=qrfai)
        if bccsq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_submitted_quote=bccsq)
        if bcai:
            RFQ_list = RFQ_list.filter(Bidder_can_add_items=bcai)
        if bccq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_quantity=bccq)
        if Product_ID:
            product_obj = Product.objects.get(id=Product_ID)
            RFQ_list = RFQ_list.filter(products=product_obj)
        if sd_from:
            RFQ_list = RFQ_list.filter(submission_deadline__gte=sd_from)
        if sd_to:
            RFQ_list = RFQ_list.filter(submission_deadline__lte=sd_to)
        if qmbvu_from:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__gte=qmbvu_from)
        if qmbvu_to:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__lte=qmbvu_to)
        # print(RFQ_list[0].status)
        
        RFQs = [
            {
                "id": rfqlst.id,
                "RFQ_ID": rfqlst.RFQ_ID,
                "vendor": rfqlst.vendor.name,
                "project": rfqlst.project.name,
                "submission_deadline": date_time_formatter(rfqlst.submission_deadline),
                "quotation": Quotation.objects.filter(RFQ=rfqlst).count(),
            }
            for rfqlst in RFQ_list
        ]
        return JsonResponse(data=RFQs, safe=False)


@is_user_login
def VendorRFQDoneDetailsApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        RFQ_details = RFQ.objects.select_related('project', 'vendor', 'type', 'currency', 'user')\
            .get(RFQ_ID=RFQ_ID)
        # RFQ_details.status = RFQ_status_choices[1][0]
        # RFQ_details.save()
        # print(invoice_details.invoice.items.first().number)
        products_list = RFQ_details.products.select_related('uom')
        products = []
        products_count = RFQ_details.products.count()
        for product in products_list:
            products.append(
                {
                'item_number': product.item,
                'product_id': product.product_id,
                'description': product.description,
                'quantity': product.quantity,
                'uom': product.uom.name,
                'category': product.category,
                'dd_sp': product.delivery_date,
                }
            )
        
        fhs = RFQFileHandler.objects.filter(RFQ=RFQ_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)
        
        RFQ_obj = {
            'id': RFQ_details.id,
            'vendor': RFQ_details.vendor.name,
            'RFQ_ID': RFQ_details.RFQ_ID,
            'project_name': RFQ_details.project.name,
            'ship_to_address': RFQ_details.ship_to_address,
            'bidder_id': RFQ_details.bidder_id,
            'submission_deadline': date_time_formatter(RFQ_details.submission_deadline),
            'qmbvu': RFQ_details.Quote_must_be_valid_until,
            'RFQ_Type': RFQ_details.type.name,
            'eqc': RFQ_details.currency.name,
            'qrfai': 'Yes' if RFQ_details.Quotes_required_for_all_items == 'y' else 'No',
            'bccsq': 'Yes' if RFQ_details.Bidder_can_change_submitted_quote == 'y' else 'No',
            'bcai': 'Yes' if RFQ_details.Bidder_can_add_items == 'y' else 'No',
            'bccq': 'Yes' if RFQ_details.Bidder_can_change_quantity == 'y' else 'No',
            'products': products,
            'products_count':products_count,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=RFQ_obj, safe=False)


def VendorRFQDoneCreateQuoteApi(request):
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        RFQ_details = RFQ.objects.select_related('project', 'vendor', 'type', 'currency')\
            .get(RFQ_ID=RFQ_ID)
        currencies = RFQCurrency.objects.all()
        RFQ_obj = {
            'RFQ_ID': RFQ_details.RFQ_ID,
            'submission_deadline': date_time_formatter(RFQ_details.submission_deadline),
            'qmbvu': RFQ_details.Quote_must_be_valid_until,
            'RFQ_Type': RFQ_details.type.name,
            'eqc': RFQ_details.currency.name,
            'currencies': [[cur.id, cur.name] for cur in currencies],
        }
        # RFQ_details.status = RFQ_status_choices[2][0]
        # RFQ_details.save()
        return JsonResponse(data=RFQ_obj, safe=False)


@is_user_login
def VendorRFQDoneCreateQuoteSubmitApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.POST:
        # print(request.POST)
        # RFQ creation
        RFQ_ID = request.POST.get('RFQ_ID', None)
        total_net_value = request.POST.get('total_net_value', None)
        currency = request.POST.get('currency', None)
        
        RFQ_obj = RFQ.objects.get(RFQ_ID=RFQ_ID)
        RFQCurrnecy_obj = RFQCurrency.objects.get(id=currency)
        
        Quotation_obj = Quotation.objects.create(
            RFQ = RFQ_obj,
            currency = RFQCurrnecy_obj,
            net_value = total_net_value,
            status = Quotation_status_choices[0][0],
            user = user_obj
        )
        
        if request.FILES:
            files = request.FILES.getlist('filepond')
            for file in files:
                QuotationFileHandler.objects.create(
                    file=file,
                    quotation=Quotation_obj,
                )
        
                # send emails
            sender = settings.EMAIL_USER
            receiver = [RFQ_obj.user.email]
            subject = f"RFQ {RFQ_obj.RFQ_ID} | New Quotation"
            message = f"""Dear {RFQ_obj.user.first_name},

I hope this find you well.
You need to know that there is a new Quotation
with the following details:
Quote ID:   {Quotation_obj.id}
RFQ ID:   {RFQ_obj.RFQ_ID}
Project:   {RFQ_obj.project.name}
Vendor:   {RFQ_obj.vendor.name}

Has Been Created By:
Name:   {user_obj.first_name} {user_obj.last_name}
E-Mail:   {user_obj.email}

The whole details will be found in our web portal, waiting for you
To check it out.
Link:   http://127.0.0.1:8000/

*Note: This E-Mail is auto generated from our system, Just for your notification.

Best Regards,
Invoices Management System (IMS)
                        """
        # print([rec.email for rec in receivers_list])
        # send_email(
        #     sender,
        #     receiver,
        #     subject,
        #     message
        # )
        data = {
            'status': 'added',
        }
        return JsonResponse(data=data, safe=False)
    




@is_user_login
def VendorQuotationView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        vendor = cursor.execute(f"SELECT DISTINCT [vendor_id] FROM [Invoices].[dbo].[system_vendor_users] WHERE [useraccount_id] = {user_obj.id}")
        vendor_results = vendor.fetchall()

        Quotation_ID = cursor.execute(f"""SELECT DISTINCT sq.[id] FROM [Invoices].[dbo].[system_quotation] AS sq
                                JOIN [Invoices].[dbo].[system_rfq] AS srfq ON srfq.[id] = sq.[RFQ_id]
                                WHERE srfq.[vendor_id] = {vendor_results[0][0]}""")
        Quotation_ID_results = Quotation_ID.fetchall()
        RFQ_ID = cursor.execute(f"SELECT DISTINCT [RFQ_ID] FROM [Invoices].[dbo].[system_rfq] WHERE [vendor_id] = {vendor_results[0][0]} AND [status] = 'r'")
        RFQ_ID_results = RFQ_ID.fetchall()
        currency = cursor.execute(f"""SELECT DISTINCT cr.[id], cr.[name] FROM [Invoices].[dbo].[system_quotation] AS sq, [Invoices].[dbo].[system_rfqcurrency] as cr
                                WHERE sq.[currency_id] = cr.[id]""")
        currency_results = currency.fetchall()
        user = cursor.execute(f"""SELECT DISTINCT sq.[user_id], CONCAT(aua.first_name, ' ', aua.last_name) FROM [Invoices].[dbo].[system_quotation] AS sq
                                JOIN [Invoices].[dbo].[system_rfq] AS srfq ON srfq.[id] = sq.[RFQ_id]
                                JOIN [Invoices].[dbo].[account_useraccount] AS aua ON aua.[id] = sq.[user_id]
                                WHERE srfq.[vendor_id] = {vendor_results[0][0]}""")
        user_results = user.fetchall()
    context = {
        'user': user_obj,
        'Quotation_ID_results': Quotation_ID_results,
        'RFQ_ID_results': RFQ_ID_results,
        'Status': Quotation_status_choices,
        'currency_results': currency_results,
        'user_results': user_results,
    }
    return render(request, 'VendorQuotation.html', context)

@is_user_login
def VendorQuotationTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        vendor_obj = Vendor.objects.get(users=user_obj)
        quotation = request.GET.get('quotation', None)
        RFQ_ID = request.GET.get('RFQ_ID', None)
        status = request.GET.get('status', None)
        currency = request.GET.get('currency', None)
        user = request.GET.get('user', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)

        print(request.GET)
        Quotation_list = Quotation.objects.select_related('RFQ', 'RFQ__vendor', 'user', 'currency')\
            .filter(RFQ__vendor=vendor_obj)
                
        if quotation:
            Quotation_list = Quotation_list.filter(id=quotation)
        if RFQ_ID:
            Quotation_list = Quotation_list.filter(RFQ__RFQ_ID=RFQ_ID)
        if status:
            Quotation_list = Quotation_list.filter(status=status)
        if currency:
            Quotation_list = Quotation_list.filter(currency_id=currency)
        if user:
            Quotation_list = Quotation_list.filter(user=user)
        if timestamp_from:
            Quotation_list = Quotation_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            Quotation_list = Quotation_list.filter(timestamp__lte=timestamp_to)
        # print(Quotation_list[0].status)

        Quotations = [
            {
                "id": ql.id,
                "RFQ_ID": ql.RFQ.RFQ_ID,
                "currency": ql.currency.name,
                "net_value": ql.net_value,
                "status": 'Created' if ql.status == 'c' else 'Approved' if ql.status == 'a' else 'Rejected',
                "user": f'{ql.user.first_name} {ql.user.last_name}',
                "timestamp": date_time_formatter(ql.timestamp),
            }
            for ql in Quotation_list
        ]
        return JsonResponse(data=Quotations, safe=False)


def VendorQuoteDetailsApi(request):
    if request.GET:
        Quote_ID = request.GET.get('Quote_ID', None)
        Quotation_details = Quotation.objects.select_related('RFQ', 'RFQ__type', 'currency', 'user')\
            .get(id=Quote_ID)

        fhs = QuotationFileHandler.objects.filter(quotation=Quotation_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
            
        Quotation_obj = {
            'RFQ_ID': Quotation_details.RFQ.RFQ_ID,
            'submission_deadline': date_time_formatter(Quotation_details.RFQ.submission_deadline),
            'qmbvu': Quotation_details.RFQ.Quote_must_be_valid_until,
            'RFQ_Type': Quotation_details.RFQ.type.name,
            'eqc': Quotation_details.currency.name,
            'net_value': Quotation_details.net_value,
            'currency': Quotation_details.currency.name,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=Quotation_obj, safe=False)




# Vendor PO
@is_user_login
def VendorPOView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        quotation_id = cursor.execute(f"SELECT DISTINCT [quotation_id] FROM [Invoices].[dbo].[system_purchaseorder]")
        quotation_id_results = quotation_id.fetchall()
        PO_number = cursor.execute(f"SELECT DISTINCT [id], [number] FROM [Invoices].[dbo].[system_purchaseorder]")
        PO_number_results = PO_number.fetchall()
        submitted_user = cursor.execute(f"""SELECT DISTINCT u.[id], CONCAT(u.[first_name], ' ', u.[last_name]) FROM [Invoices].[dbo].[system_purchaseorder] as spo, [Invoices].[dbo].[account_useraccount] as u
                                WHERE spo.[contact_person_id] = u.id""")
        submitted_user_results = submitted_user.fetchall()
        PO_currency = cursor.execute(f"""SELECT DISTINCT c.[id], c.[name] FROM [Invoices].[dbo].[system_purchaseorder] as spo, [Invoices].[dbo].[system_rfqcurrency] as c
                                WHERE spo.currency_id = c.id""")
        PO_currency_results = PO_currency.fetchall()
        milestones = cursor.execute(f"""SELECT DISTINCT sm.[id], sm.[precentage] FROM [Invoices].[dbo].[system_purchaseorder_milestones] as spom
                                join [Invoices].[dbo].[system_purchaseorder] as spo on spom.purchaseorder_id = spo.id
                                join [Invoices].[dbo].[system_pomilestone] as sm on spom.pomilestone_id = sm.id""")
        milestones_results = milestones.fetchall()
    context = {
        'user': user_obj,
        'quotation_id_results': quotation_id_results,
        'PO_number_results': PO_number_results,
        'submitted_user_results': submitted_user_results,
        'PO_currency_results': PO_currency_results,
        'milestones_results': milestones_results,
        'status_results': PO_status_choices,
    }
    return render(request, 'VendorPO.html', context)

@is_user_login
def VendorPOTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        quotation = request.GET.get('quotation', None)
        PO_number = request.GET.get('PO_number', None)
        user = request.GET.get('user', None)
        currency = request.GET.get('currency', None)
        milestone = request.GET.get('milestone', None)
        status = request.GET.get('status', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)

    
        print(request.GET)
        PO_list = PurchaseOrder.objects.select_related('quotation', 'contact_person', 'currency')
                
        if quotation:
            PO_list = PO_list.filter(quotation_id=quotation)
        if PO_number:
            PO_list = PO_list.filter(id=PO_number)
        if user:
            PO_list = PO_list.filter(contact_person_id=user)
        if currency:
            PO_list = PO_list.filter(currency_id=currency)
        if milestone:
            milestone_obj = POMilestone.objects.get(id=milestone)
            PO_list = PO_list.filter(milestones=milestone_obj)
        if status:
            PO_list = PO_list.filter(status=status)
        if timestamp_from:
            PO_list = PO_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            PO_list = PO_list.filter(timestamp__lte=timestamp_to)

        # print(RFQ_list[0].status)
        POs = [
            {
                "id": polst.id,
                "number": polst.number,
                "quotation": polst.quotation.id,
                "total_value": polst.total_value,
                "currency": polst.currency.name,
                "milestones": polst.milestones.count(),
                "contact_person": f"{polst.contact_person.first_name} {polst.contact_person.last_name}",
                "status": 'Opened' if polst.status == 'o' else 'Closed',
                "timestamp": date_time_formatter(polst.timestamp),
            }
            for polst in PO_list
        ]
        return JsonResponse(data=POs, safe=False)

def VendorPODetailsApi(request):
    if request.GET:
        PO_id = request.GET.get('PO_id', None)
        PO_obj = PurchaseOrder.objects.select_related('quotation', 'contact_person', 'currency')\
            .get(id=PO_id)
        milestones_list = PO_obj.milestones.all()
        milestones = []
        milestones_count = PO_obj.milestones.count()
        for milestone in milestones_list:
            milestones.append(
                {
                'id': milestone.id,
                'precentage': f'{milestone.precentage} %',
                'due': f'{0 if not milestone.due else milestone.due} Days',
                'description': milestone.description,
                'amount': milestone.amount,
                'timestamp': date_time_formatter(milestone.timestamp)
                }
            )
        fhs = POFileHandler.objects.filter(po=PO_obj)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)

        RFQ_obj = {
            'PO_id': PO_obj.id,
            'PO_number': PO_obj.number,
            'quotation': PO_obj.quotation.id,
            'total_value': PO_obj.total_value,
            'currency': PO_obj.currency.name,
            'contact_person': f'{PO_obj.contact_person.first_name} {PO_obj.contact_person.last_name}',
            'status': 'Opened' if PO_obj.status == 'o' else 'Closed',
            'timestamp': date_time_formatter(PO_obj.timestamp),
            'shipping_terms': PO_obj.shipping_terms,
            'total_milestones': milestones_count,
            'milestones':milestones,
            'total_files': attachments_count,
            'attachments': attachments,
        }
        return JsonResponse(data=RFQ_obj, safe=False)




@is_user_login
def NewInvoiceView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        PO = cursor.execute(f"""SELECT DISTINCT spo.[id], spo.[number]
                                FROM [Invoices].[dbo].[system_purchaseorder] AS spo
                                    ,[Invoices].[dbo].[system_quotation] AS sq
                                    ,[Invoices].[dbo].[system_rfq] AS srfq
                                    ,[Invoices].[dbo].[system_vendor] AS sv
                                    ,[Invoices].[dbo].[system_vendor_users] AS svu
                                WHERE
                                    spo.quotation_id = sq.id AND
                                    sq.RFQ_id = srfq.id AND
                                    srfq.vendor_id = sv.id AND
                                    svu.vendor_id = sv.id AND
                                    svu.useraccount_id = {user_obj.id} AND
                                    spo.status = 'o'""")
        PO_results = PO.fetchall()
        vendor = cursor.execute(f"""SELECT DISTINCT sv.id, sv.name FROM [Invoices].[dbo].[system_vendor_users] AS svu, [Invoices].[dbo].[system_vendor] AS sv
                                WHERE svu.vendor_id = sv.id AND svu.useraccount_id = {user_obj.id}""")
        vendor_results = vendor.fetchone()
        type = cursor.execute("SELECT DISTINCT [id], [name] FROM [Invoices].[dbo].[system_invoicetype]")
        type_results = type.fetchall()
        currency = cursor.execute("SELECT DISTINCT [id], [name] FROM [Invoices].[dbo].[system_invoicecurrency]")
        currency_results = currency.fetchall()
        vat = cursor.execute("SELECT DISTINCT [id], [amount] FROM [Invoices].[dbo].[system_invoicevat]")
        vat_results = vat.fetchall()
        uom = cursor.execute("SELECT DISTINCT [id],[name] FROM [Invoices].[dbo].[system_itemuom]")
        uom_results = uom.fetchall()
    context = {
        'user': user_obj,
        'PO_results': PO_results,
        'vendor': vendor_results,
        # 'vendor': [user_obj.id, user_obj.username.upper()],
        'types': type_results,
        'currencies': currency_results,
        'vats': vat_results,
        'uoms': uom_results,
    }
    return render(request, 'NewInvoice.html', context)
  
@is_user_login
def NewInvoicePODetailsApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        # print(request.GET)
        # invoice creation
        PO_ID = request.GET.get('PO_ID', None)
        PO_obj = PurchaseOrder.objects.select_related('quotation', 'quotation__RFQ', 'quotation__RFQ__project').get(id=PO_ID)
        milestones = PO_obj.milestones.all()
        milestones_list = []
        for milestone in milestones:
            # print(milestone.precentage)
            milestones_list.append([
                milestone.id,
                milestone.precentage,
                f'{milestone.description}',
                format((milestone.amount if milestone.amount else 0) - (milestone.remaining if milestone.remaining else 0), '.3f'),
                format((milestone.remaining if milestone.remaining else 0), '.3f'),
                format((milestone.amount if milestone.amount else 0), '.3f'),
            ])
        data = {
            'payed': format((PO_obj.total_value - PO_obj.remaining_value), '.3f'),
            'remaining': format(PO_obj.remaining_value, '.3f'),
            'total': format(PO_obj.total_value, '.3f'),
            'milestones': milestones_list,
            'projects': [PO_obj.quotation.RFQ.project.id, PO_obj.quotation.RFQ.project.name],
        }
        return JsonResponse(data=data, safe=False)


@is_user_login
def NewInvoiceSubmitApi(request):
    if request.POST:
        user_token = request.session['user_token']
        user_obj = Token.objects.get(token=user_token).user
        # print(request.POST)
        # invoice creation
        po = request.POST.get('po', None)
        milestone = request.POST.get('milestone', None)
        vendor = request.POST.get('vendor', None)
        project = request.POST.get('project', None)
        number = request.POST.get('number', None)
        date = request.POST.get('date', None)
        payment_due = request.POST.get('due', None)
        bill_to = request.POST.get('bill_to', None)
        type = request.POST.get('type', None)
        currency = request.POST.get('currency', None)
        vat = request.POST.get('vat', None)
        
        check_invoice = SubmittedInvoice.objects.select_related('invoice')\
                            .filter(invoice__number=number)
        
        if check_invoice.exists():
            check_invoice_status = check_invoice.filter(Q(status=status_choices[0][0]) | Q(status=status_choices[1][0])).exists()
            if check_invoice_status:
                data = {
                    'status': "Error: The provided invoice number is not unique.",
                }
                return JsonResponse(data=data, safe=False)
            else:
                invoice_obj = Invoice.objects.create(
                    po_id=po,
                    milestone_id=milestone,
                    vendor_id=vendor,
                    project_id=project,
                    number=number,
                    date=date,
                    payment_due=payment_due,
                    bill_to=bill_to,
                    type_id=type,
                    currency_id=currency,
                    vat_id=vat,
                )

                # items creation
                items_list = request.POST.getlist('items', None)
                for item in items_list:
                    item_dict = json.loads(item)
                    uom_obj = ItemUom.objects.get(name=item_dict.get('uom'))
                    item_obj = Item.objects.create(
                        number = item_dict.get('number'),
                        description = item_dict.get('description'),
                        quantity = item_dict.get('quantity'),
                        uom = uom_obj,
                        unit_price = item_dict.get('unit_price'),
                        amount = item_dict.get('amount'),
                    )
                    invoice_obj.items.add(item_obj)
                
                # files creation
                if request.FILES:
                    # print(request.FILES.getlist('filepond'))
                    files = request.FILES.getlist('filepond')
                    for file in files:
                        FileHandler.objects.create(
                            file=file,
                            invoice=invoice_obj,
                        )
                SubmittedInvoice.objects.create(
                    invoice=invoice_obj,
                    feedback='Submitted',
                    user=user_obj,
                )
                PendingInvoice.objects.create(
                    invoice=invoice_obj,
                    feedback='Pending',
                    user=user_obj,
                )
                data = {
                    'status': 'added',
                }
                return JsonResponse(data=data, safe=False)
        else:
            invoice_obj = Invoice.objects.create(
                po_id=po,
                milestone_id=milestone,
                vendor_id=vendor,
                project_id=project,
                number=number,
                date=date,
                payment_due=payment_due,
                bill_to=bill_to,
                type_id=type,
                currency_id=currency,
                vat_id=vat,
            )

            # items creation
            items_list = request.POST.getlist('items', None)
            for item in items_list:
                item_dict = json.loads(item)
                uom_obj = ItemUom.objects.get(name=item_dict.get('uom'))
                item_obj = Item.objects.create(
                    number = item_dict.get('number'),
                    description = item_dict.get('description'),
                    quantity = item_dict.get('quantity'),
                    uom = uom_obj,
                    unit_price = item_dict.get('unit_price'),
                    amount = item_dict.get('amount'),
                )
                invoice_obj.items.add(item_obj)
            
            # files creation
            if request.FILES:
                # print(request.FILES.getlist('filepond'))
                files = request.FILES.getlist('filepond')
                for file in files:
                    FileHandler.objects.create(
                        file=file,
                        invoice=invoice_obj,
                    )
            SubmittedInvoice.objects.create(
                invoice=invoice_obj,
                feedback='Submitted',
                user=user_obj,
            )
            PendingInvoice.objects.create(
                invoice=invoice_obj,
                feedback='Pending',
                user=user_obj,
            )
            data = {
                'status': 'added',
            }
            return JsonResponse(data=data, safe=False)



@is_user_login
def VendorDoneInvoicesView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        number = cursor.execute(f"""SELECT DISTINCT si.[number]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu
                                WHERE si.vendor_id = svu.vendor_id AND svu.useraccount_id = {user_obj.id}""")
        number_results = number.fetchall()
        po = cursor.execute(f"""SELECT DISTINCT spo.[id], spo.[number]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu, [Invoices].[dbo].[system_purchaseorder] AS spo
                                WHERE si.po_id = spo.id AND si.vendor_id = svu.vendor_id AND svu.useraccount_id = {user_obj.id}""")
        po_results = po.fetchall()
        due = cursor.execute(f"""SELECT DISTINCT si.[payment_due]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu
                                WHERE si.vendor_id = svu.vendor_id AND svu.useraccount_id = {user_obj.id}""")
        due_results = due.fetchall()
        bill_to = cursor.execute(f"""SELECT DISTINCT si.[bill_to]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu
                                WHERE si.vendor_id = svu.vendor_id AND svu.useraccount_id = {user_obj.id}""")
        bill_to_results = bill_to.fetchall()
        project_name = cursor.execute(f"""SELECT DISTINCT sp.[id], sp.[name]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu, [Invoices].[dbo].[system_project] AS sp
                                WHERE si.vendor_id = svu.vendor_id AND si.project_id = sp.id AND svu.useraccount_id = {user_obj.id}""")
        project_name_results = project_name.fetchall()
        milestone = cursor.execute(f"""SELECT DISTINCT spom.[id], spom.[precentage]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu, [Invoices].[dbo].[system_pomilestone] AS spom
                                WHERE si.vendor_id = svu.vendor_id AND si.milestone_id = spom.id AND svu.useraccount_id = {user_obj.id}""")
        milestone_results = milestone.fetchall()
        item = cursor.execute(f"""SELECT DISTINCT sitm.[id], sitm.[number] 
                                FROM [Invoices].[dbo].[system_invoice_items] as sii
                                    ,[Invoices].[dbo].[system_invoice] as sinvo
                                    ,[Invoices].[dbo].[system_item] as sitm
                                    ,[Invoices].[dbo].[system_vendor_users] AS svu
                                WHERE sii.invoice_id = sinvo.id
                                    AND sii.item_id = sitm.id
                                    AND sinvo.vendor_id = svu.vendor_id
                                    AND svu.useraccount_id = {user_obj.id}""")
        item_results = item.fetchall()
        type = cursor.execute(f"""SELECT DISTINCT sinvot.[id], sinvot.[name]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu, [Invoices].[dbo].[system_invoicetype] AS sinvot
                                WHERE si.vendor_id = svu.vendor_id AND si.type_id = sinvot.id AND svu.useraccount_id = {user_obj.id}""")
        type_results = type.fetchall()
        currency = cursor.execute(f"""SELECT DISTINCT sinvoc.[id], sinvoc.[name]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu, [Invoices].[dbo].[system_invoicecurrency] AS sinvoc
                                WHERE si.vendor_id = svu.vendor_id AND si.currency_id = sinvoc.id AND svu.useraccount_id = {user_obj.id}""")
        currency_results = currency.fetchall()
        vat = cursor.execute(f"""SELECT DISTINCT sinvov.[id], sinvov.[amount]
                                FROM [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor_users] AS svu, [Invoices].[dbo].[system_invoicevat] AS sinvov
                                WHERE si.vendor_id = svu.vendor_id AND si.currency_id = sinvov.id AND svu.useraccount_id = {user_obj.id}""")
        vat_results = vat.fetchall()
    context = {
        'user': user_obj,
        'number_results': number_results,
        'po_results': po_results,
        'due_results': due_results,
        'bill_to_results': bill_to_results,
        'project_name_results': project_name_results,
        'milestone_results': milestone_results,
        'item_results': item_results,
        'currency_results': currency_results,
        'type_results': type_results,
        'vat_results': vat_results,
        'status_results': status_choices,
    }
    return render(request, 'VendorInvoicesDone.html', context)


@is_user_login
def VendorInvoicesDoneTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        number = request.GET.get('number', None)
        date = request.GET.get('date', None)
        po = request.GET.get('po', None)
        due = request.GET.get('due', None)
        bill_to = request.GET.get('bill_to', None)
        project_name = request.GET.get('project_name', None)
        type = request.GET.get('type', None)
        milestone = request.GET.get('milestone', None)
        item = request.GET.get('item', None)
        vat = request.GET.get('vat', None)
        currency = request.GET.get('currency', None)
        status = request.GET.get('status', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)
        
        invoices_list = SubmittedInvoice.objects\
            .select_related('invoice',
                            'invoice__po',
                            'invoice__milestone',
                            'invoice__vendor',
                            'invoice__project',
                            'invoice__type',
                            'invoice__vat',
                            'invoice__currency')\
            .filter(user=user_obj, invoice__vendor__users=user_obj)
        
        if number:
            invoices_list = invoices_list.filter(invoice__number=number)
        if date:
            invoices_list = invoices_list.filter(invoice__date=date)
        if po:
            invoices_list = invoices_list.filter(invoice__po_id=po)
        if due:
            invoices_list = invoices_list.filter(invoice__payment_due=due)
        if bill_to:
            invoices_list = invoices_list.filter(invoice__bill_to=bill_to)
        if project_name:
            invoices_list = invoices_list.filter(invoice__project_id=project_name)
        if type:
            invoices_list = invoices_list.filter(invoice__type_id=type)
        if milestone:
            invoices_list = invoices_list.filter(invoice__milestone_id=milestone)
        if item:
            invoices_list = invoices_list.filter(invoice__items=item)
        if vat:
            invoices_list = invoices_list.filter(invoice__vat_id=vat)
        if currency:
            invoices_list = invoices_list.filter(invoice__currency_id=currency)
        if status:
            invoices_list = invoices_list.filter(status=status)
        if timestamp_from:
            invoices_list = invoices_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            invoices_list = invoices_list.filter(timestamp__lte=timestamp_to)
        invoices = [
            {
                "id": invlst.id,
                "invoice_id": invlst.invoice.id,
                "vendor": invlst.invoice.vendor.name,
                "date": invlst.invoice.date,
                "po": invlst.invoice.po.number,
                "bill_to": invlst.invoice.bill_to,
                "user": f"{invlst.user.first_name} {invlst.user.last_name}",
                "timestamp": date_time_formatter(invlst.timestamp),
                "status": dict(status_choices).get(invlst.status)
            }
            for invlst in invoices_list
        ]
        return JsonResponse(data=invoices, safe=False)
    

def VendorInvoicesDoneDetailsApi(request):
    if request.GET:
        submitted_id = request.GET.get('id', None)
        invoice_details = SubmittedInvoice.objects\
                            .select_related(
                                'invoice',
                                'invoice__po',
                                'invoice__milestone',
                                'invoice__vendor',
                                'invoice__project',
                                'invoice__type',
                                'invoice__vat',
                                'invoice__currency')\
                            .get(id=submitted_id)
        items_list = invoice_details.invoice.items.select_related('uom')
        items = []
        items_count = invoice_details.invoice.items.count()
        items_total_amount = 0
        for item in items_list:
            items_total_amount += int(item.amount)
            items.append(
                {
                'number': item.number,
                'description': item.description,
                'quantity': item.quantity,
                'uom': item.uom.name,
                'unit_price': item.unit_price,
                'amount': item.amount,
                }
            )
        
        fhs = FileHandler.objects.filter(invoice=invoice_details.invoice)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        invoice = {
            'invoice_id': invoice_details.invoice.id,
            'vendor': invoice_details.invoice.vendor.name,
            'number': invoice_details.invoice.number,
            'date': invoice_details.invoice.date,
            'po': invoice_details.invoice.po.number,
            'payment_due': invoice_details.invoice.payment_due,
            'bill_to': invoice_details.invoice.bill_to,
            'project_name': invoice_details.invoice.project.name,
            'type': invoice_details.invoice.type.name,
            'milestone': invoice_details.invoice.milestone.precentage,
            'milestone_description': invoice_details.invoice.milestone.description,
            'items': items,
            'items_count':items_count,
            'items_total_amount':items_total_amount,
            'vat': invoice_details.invoice.vat.amount,
            'vat_amount': (items_total_amount * invoice_details.invoice.vat.amount)/100,
            'invoice_total': items_total_amount+((items_total_amount * invoice_details.invoice.vat.amount)/100),
            'currency': invoice_details.invoice.currency.name,
            'invoice_timestamp': date_time_formatter(invoice_details.invoice.timestamp),
            'invoice_attachments': attachments,
            'invoice_attachments_count': attachments_count,
            'status': invoice_details.status,
            
            'submitted_id': invoice_details.id,
            'feedback': invoice_details.feedback,
            'user': f"{invoice_details.user.first_name} {invoice_details.user.last_name}",
            'submitted_timestamp': date_time_formatter(invoice_details.timestamp),
        }
        # if invoice_details.status == 'a':
        #     approved_user = ApprovedInvoice.objects.get(invoice=invoice_details.invoice).user
        #     approved_timeStamp = ApprovedInvoice.objects.get(invoice=invoice_details.invoice).timestamp
        #     invoice['approved_user'] = f"{approved_user.first_name} {approved_user.last_name}"
        #     invoice['approved_timeStamp'] = date_time_formatter(approved_timeStamp)
        # if invoice_details.status == 'r':
        #     rejected_user = RejectedInvoice.objects.get(invoice=invoice_details.invoice).user
        #     rejected_timeStamp = RejectedInvoice.objects.get(invoice=invoice_details.invoice).timestamp
        #     invoice['rejected_user'] = f"{rejected_user.first_name} {rejected_user.last_name}"
        #     invoice['rejected_timeStamp'] = date_time_formatter(rejected_timeStamp)
        if invoice_details.status == 'a':
            approved_obj = ApprovedInvoice.objects.get(invoice=invoice_details.invoice)
            invoice['approved_user'] = f"{approved_obj.user.first_name} {approved_obj.user.last_name}"
            invoice['approved_timeStamp'] = date_time_formatter(approved_obj.timestamp)
            invoice['approved_feedback'] = approved_obj.feedback
        if invoice_details.status == 'r':
            rejected_obj = RejectedInvoice.objects.get(invoice=invoice_details.invoice)
            invoice['rejected_user'] = f"{rejected_obj.user.first_name} {rejected_obj.user.last_name}"
            invoice['rejected_timeStamp'] = date_time_formatter(rejected_obj.timestamp)
            invoice['rejected_feedback'] = rejected_obj.feedback
        return JsonResponse(data=invoice, safe=False)
    
    




############################## PROCUREMENT ########################################################

# Dashboard
@is_user_login
def ProcurementDashboardView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    # t_invoice = Invoice.objects.count()
    t_invoice = SubmittedInvoice.objects.count()
    p_invoice = PendingInvoice.objects.count()
    a_invoice = ApprovedInvoice.objects.count()
    r_invoice = RejectedInvoice.objects.count()
    context = {
        'user': user_obj,
        # 't_invoice': t_invoice,
        't_invoice': t_invoice,
        'p_invoice': p_invoice,
        'a_invoice': a_invoice,
        'r_invoice': r_invoice
    }
    return render(request, 'ProcurementDashboard.html', context)

def ProcurementInvoicesStatusColumnChartApi(request):
    if request.GET:
        filter = request.GET.get('filter', None)
        from_value = request.GET.get('from', None)
        to_value = request.GET.get('to', None)
        current_date = datetime.now().date()
        filters_query = Q()
        if from_value:
            if filter == 'per_time':
                filters_query &= (Q(timestamp__date=current_date) & Q(timestamp__time__gte=from_value))
            if filter == 'per_day':
                filters_query &= Q(timestamp__date__gte=from_value)
            if filter == 'per_month':
                year_from, month_from = map(int, from_value.split('-'))
                filters_query &= (Q(timestamp__year__gt=year_from) | (Q(timestamp__year=year_from) & Q(timestamp__month__gte=month_from)))
            if filter == 'per_year':
                filters_query &= Q(timestamp__year__gte=from_value)
        if to_value:
            if filter == 'per_time':
                filters_query &= (Q(timestamp__date=current_date) & Q(timestamp__time__lte=to_value))
            if filter == 'per_day':
                filters_query &= Q(timestamp__date__lte=to_value)
            if filter == 'per_month':
                year_to, month_to = map(int, to_value.split('-'))
                filters_query &= (Q(timestamp__year__lt=year_to) | (Q(timestamp__year=year_to) & Q(timestamp__month__lte=month_to)))
                # print(year_to, month_to, filters_query)
            if filter == 'per_year':
                filters_query &= Q(timestamp__year__lte=to_value)
        p_invoice = PendingInvoice.objects.filter(filters_query).count()
        a_invoice = ApprovedInvoice.objects.filter(filters_query).count()
        r_invoice = RejectedInvoice.objects.filter(filters_query).count()
        # print(p_invoice, a_invoice, r_invoice)
    else:
        p_invoice = PendingInvoice.objects.count()
        a_invoice = ApprovedInvoice.objects.count()
        r_invoice = RejectedInvoice.objects.count()
    data = [
        ['Pending', p_invoice, p_invoice, '#343a40'],
        ['Approved', a_invoice, a_invoice, '#28a745'],
        ['Rejected', r_invoice, r_invoice, '#dc3545'],
    ]
    return JsonResponse(data=data, safe=False)

def ProcurementInvoicesStatusPieChartApi(request):
    p_invoice = PendingInvoice.objects.count()
    a_invoice = ApprovedInvoice.objects.count()
    r_invoice = RejectedInvoice.objects.count()
    data = [
        ['Pending', p_invoice],
        ['Approved', a_invoice],
        ['Rejected', r_invoice],
    ]
    return JsonResponse(data=data, safe=False)


# RFQ
@is_user_login
def ProcurementCreatedRFQView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        RFQ_ID = cursor.execute(f"SELECT DISTINCT [RFQ_ID] FROM [Invoices].[dbo].[system_rfq]")
        RFQ_ID_results = RFQ_ID.fetchall()
        vendor = cursor.execute(f"SELECT DISTINCT [id], [name] FROM [Invoices].[dbo].[system_vendor]")
        vendor_results = vendor.fetchall()
        project = cursor.execute(f"""SELECT DISTINCT p.[id], p.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_project] as p
                                WHERE srfq.project_id = p.id""")
        project_results = project.fetchall()
        bidder_id = cursor.execute(f"SELECT DISTINCT [bidder_id] FROM [Invoices].[dbo].[system_rfq]")
        bidder_id_results = bidder_id.fetchall()
        RFQ_type = cursor.execute(f"""SELECT DISTINCT t.[id], t.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqtype] as t
                                WHERE srfq.type_id = t.id""")
        RFQ_type_results = RFQ_type.fetchall()
        RFQ_currency = cursor.execute(f"""SELECT DISTINCT c.[id], c.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqcurrency] as c
                                WHERE srfq.currency_id = c.id""")
        RFQ_currency_results = RFQ_currency.fetchall()
        product_id = cursor.execute(f"""SELECT sp.[id], sp.[product_id] FROM [Invoices].[dbo].[system_rfq_products] as srfqp
                                join [Invoices].[dbo].[system_rfq] as srfq on srfqp.rfq_id = srfq.id
                                join [Invoices].[dbo].[system_product] as sp on srfqp.product_id = sp.id""")
        product_id_results = product_id.fetchall()
        user = cursor.execute(f"""SELECT DISTINCT u.[id], CONCAT(u.[first_name], ' ', u.[last_name]) FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[account_useraccount] as u
                                WHERE srfq.user_id = u.id""")
        user_results = user.fetchall()
    context = {
        'user': user_obj,
        'vendor_results': vendor_results,
        'RFQ_ID_results': RFQ_ID_results,
        'project_results': project_results,
        'bidder_id_results': bidder_id_results,
        'RFQ_type_results': RFQ_type_results,
        'RFQ_currency_results': RFQ_currency_results,
        'RFQ_qrfai_results': RFQ_QuotesRequiredForAllItems,
        'RFQ_bccsq_results': RFQ_BidderCanChangeSubmittedQuote,
        'RFQ_bcai_results': RFQ_BidderCanAddItems,
        'RFQ_bccq_results': RFQ_BidderCanChangeQuantity,
        'product_id_results': product_id_results,
        'RFQ_status': RFQ_status_choices,
        'user_results': user_results,
    }
    return render(request, 'ProcurementRFQCreated.html', context)

@is_user_login
def ProcurementCreatedRFQTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        project = request.GET.get('project', None)
        vendor = request.GET.get('vendor', None)
        Bidder_ID = request.GET.get('Bidder_ID', None)
        RFQ_Type = request.GET.get('RFQ_Type', None)
        eqc = request.GET.get('eqc', None)
        qrfai = request.GET.get('qrfai', None)
        bccsq = request.GET.get('bccsq', None)
        bcai = request.GET.get('bcai', None)
        bccq = request.GET.get('bccq', None)
        Product_ID = request.GET.get('Product_ID', None)
        status = request.GET.get('status', None)
        user = request.GET.get('user', None)
        sd_from = request.GET.get('sd_from', None)
        sd_to = request.GET.get('sd_to', None)
        qmbvu_from = request.GET.get('qmbvu_from', None)
        qmbvu_to = request.GET.get('qmbvu_to', None)

        print(request.GET)
        RFQ_list = RFQ.objects.select_related('project', 'vendor', 'type', 'currency', 'user')
                
        if RFQ_ID:
            RFQ_list = RFQ_list.filter(RFQ_ID=RFQ_ID)
        if project:
            RFQ_list = RFQ_list.filter(project_id=project)
        if vendor:
            RFQ_list = RFQ_list.filter(vendor_id=vendor)
        if Bidder_ID:
            RFQ_list = RFQ_list.filter(bidder_id=Bidder_ID)
        if RFQ_Type:
            RFQ_list = RFQ_list.filter(type_id=RFQ_Type)
        if eqc:
            RFQ_list = RFQ_list.filter(currency_id=eqc)
        if qrfai:
            RFQ_list = RFQ_list.filter(Quotes_required_for_all_items=qrfai)
        if bccsq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_submitted_quote=bccsq)
        if bcai:
            RFQ_list = RFQ_list.filter(Bidder_can_add_items=bcai)
        if bccq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_quantity=bccq)
        if Product_ID:
            product_obj = Product.objects.get(id=Product_ID)
            RFQ_list = RFQ_list.filter(products=product_obj)
        if status:
            RFQ_list = RFQ_list.filter(status=status)
        if user:
            RFQ_list = RFQ_list.filter(user_id=user)
        if sd_from:
            RFQ_list = RFQ_list.filter(submission_deadline__gte=sd_from)
        if sd_to:
            RFQ_list = RFQ_list.filter(submission_deadline__lte=sd_to)
        if qmbvu_from:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__gte=qmbvu_from)
        if qmbvu_to:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__lte=qmbvu_to)
        # print(RFQ_list[0].status)
        RFQs = [
            {
                "id": rfqlst.id,
                "RFQ_ID": rfqlst.RFQ_ID,
                "vendor": rfqlst.vendor.name,
                "project": rfqlst.project.name,
                "submission_deadline": date_time_formatter(rfqlst.submission_deadline),
                "status": 'Sent' if rfqlst.status == 's' else 'Viewed' if rfqlst.status == 'v' else 'Replyed',
                "user": f"{rfqlst.user.first_name} {rfqlst.user.last_name}",
                "quotation": Quotation.objects.filter(RFQ=rfqlst).count(),
            }
            for rfqlst in RFQ_list
        ]
        return JsonResponse(data=RFQs, safe=False)

def ProcurementCreatedRFQDetailsApi(request):
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        RFQ_details = RFQ.objects.select_related('project', 'vendor', 'type', 'currency', 'user')\
            .get(RFQ_ID=RFQ_ID)
        products_list = RFQ_details.products.select_related('uom')
        products = []
        products_count = RFQ_details.products.count()
        for product in products_list:
            products.append(
                {
                'item_number': product.item,
                'product_id': product.product_id,
                'description': product.description,
                'quantity': product.quantity,
                'uom': product.uom.name,
                'category': product.category,
                'dd_sp': product.delivery_date,
                }
            )
        
        fhs = RFQFileHandler.objects.filter(RFQ=RFQ_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)

        RFQ_obj = {
            'id': RFQ_details.id,
            'vendor': RFQ_details.vendor.name,
            'RFQ_ID': RFQ_details.RFQ_ID,
            'project_name': RFQ_details.project.name,
            'ship_to_address': RFQ_details.ship_to_address,
            'bidder_id': RFQ_details.bidder_id,
            'submission_deadline': date_time_formatter(RFQ_details.submission_deadline),
            'qmbvu': RFQ_details.Quote_must_be_valid_until,
            'RFQ_Type': RFQ_details.type.name,
            'eqc': RFQ_details.currency.name,
            'qrfai': 'Yes' if RFQ_details.Quotes_required_for_all_items == 'y' else 'No',
            'bccsq': 'Yes' if RFQ_details.Bidder_can_change_submitted_quote == 'y' else 'No',
            'bcai': 'Yes' if RFQ_details.Bidder_can_add_items == 'y' else 'No',
            'bccq': 'Yes' if RFQ_details.Bidder_can_change_quantity == 'y' else 'No',
            'products': products,
            'products_count':products_count,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=RFQ_obj, safe=False)


# Quotation
@is_user_login
def ProcurementQuotationDoneView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        Quotation_ID = cursor.execute(f"""SELECT DISTINCT [id] FROM [Invoices].[dbo].[system_quotation]""")
        Quotation_ID_results = Quotation_ID.fetchall()
        RFQ_ID = cursor.execute(f"""SELECT DISTINCT srfq.[RFQ_ID] FROM [Invoices].[dbo].[system_quotation] AS sq, [Invoices].[dbo].[system_rfq] AS srfq
                                WHERE sq.[RFQ_id] = srfq.[id]""")
        RFQ_ID_results = RFQ_ID.fetchall()
        currency = cursor.execute(f"""SELECT DISTINCT cr.[id], cr.[name] FROM [Invoices].[dbo].[system_quotation] AS sq, [Invoices].[dbo].[system_rfqcurrency] as cr
                                WHERE sq.[currency_id] = cr.[id]""")
        currency_results = currency.fetchall()
        user = cursor.execute(f"""SELECT DISTINCT sq.[user_id], CONCAT(aua.first_name, ' ', aua.last_name) FROM [Invoices].[dbo].[system_quotation] AS sq
                                JOIN [Invoices].[dbo].[account_useraccount] AS aua ON aua.[id] = sq.[user_id]""")
        user_results = user.fetchall()
    context = {
        'user': user_obj,
        'Quotation_ID_results': Quotation_ID_results,
        'RFQ_ID_results': RFQ_ID_results,
        'Status': Quotation_status_choices,
        'currency_results': currency_results,
        'user_results': user_results,
    }
    return render(request, 'ProcurementQuotationDone.html', context)

def ProcurementQuotationDoneTableApi(request):
    if request.GET:
        quotation = request.GET.get('quotation', None)
        RFQ_ID = request.GET.get('RFQ_ID', None)
        status = request.GET.get('status', None)
        currency = request.GET.get('currency', None)
        user = request.GET.get('user', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)

        # print(request.GET)
        Quotation_list = Quotation.objects.select_related('RFQ', 'RFQ__vendor', 'user', 'currency')
                
        if quotation:
            Quotation_list = Quotation_list.filter(id=quotation)
        if RFQ_ID:
            Quotation_list = Quotation_list.filter(RFQ__RFQ_ID=RFQ_ID)
        if status:
            Quotation_list = Quotation_list.filter(status=status)
        if currency:
            Quotation_list = Quotation_list.filter(currency_id=currency)
        if user:
            Quotation_list = Quotation_list.filter(user=user)
        if timestamp_from:
            Quotation_list = Quotation_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            Quotation_list = Quotation_list.filter(timestamp__lte=timestamp_to)
        # print(Quotation_list[0].status)

        Quotations = [
            {
                "id": ql.id,
                "RFQ_ID": ql.RFQ.RFQ_ID,
                "currency": ql.currency.name,
                "net_value": ql.net_value,
                "status": 'Created' if ql.status == 'c' else 'Approved' if ql.status == 'a' else 'Rejected',
                "user": f'{ql.user.first_name} {ql.user.last_name}',
                "timestamp": date_time_formatter(ql.timestamp),
            }
            for ql in Quotation_list
        ]
        return JsonResponse(data=Quotations, safe=False)

def ProcurementQuotationDoneDetailsApi(request):
    if request.GET:
        Quote_ID = request.GET.get('Quote_ID', None)
        Quotation_details = Quotation.objects.select_related('RFQ', 'RFQ__type', 'currency', 'user')\
            .get(id=Quote_ID)

        fhs = QuotationFileHandler.objects.filter(quotation=Quotation_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
            
        Quotation_obj = {
            'RFQ_ID': Quotation_details.RFQ.RFQ_ID,
            'submission_deadline': date_time_formatter(Quotation_details.RFQ.submission_deadline),
            'qmbvu': Quotation_details.RFQ.Quote_must_be_valid_until,
            'RFQ_Type': Quotation_details.RFQ.type.name,
            'eqc': Quotation_details.currency.name,
            'net_value': Quotation_details.net_value,
            'currency': Quotation_details.currency.name,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=Quotation_obj, safe=False)




# Purchase Order
# New
@is_user_login
def ProcurementNewPOView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    quotations = Quotation.objects.select_related('RFQ').filter(status=Quotation_status_choices[1][0])
    currencies = RFQCurrency.objects.all()
    context = {
        'user': user_obj,
        'quotations': quotations,
        'currencies': currencies,
    }
    return render(request, 'ProcurementPONew.html', context)

@is_user_login
def ProcurementNewPOSubmitApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.POST:
        print(request.POST)
        # RFQ creation
        quotation = request.POST.get('quotation', None)
        po = request.POST.get('po', None)
        contact_person = request.POST.get('contact_person', None)
        total_value = request.POST.get('total_value', None)
        currency = request.POST.get('currency', None)
        shipping_terms = request.POST.get('shipping_terms', None)
        
        check_PO = PurchaseOrder.objects.select_related('Quotation')\
            .filter(quotation_id=quotation, number=po, status=PO_status_choices[0][0])
        
        if check_PO.exists():
            data = {
                'status': "Error: The provided PO number is not unique.",
            }
            return JsonResponse(data=data, safe=False)
        else:
            PO_obj = PurchaseOrder.objects.create(
                quotation_id = quotation,
                number = po,
                contact_person = user_obj,
                total_value = total_value,
                remaining_value = total_value,
                currency_id = currency,
                shipping_terms = shipping_terms,
                status = PO_status_choices[0][0]
            )

            # items creation
            milestones_list = request.POST.getlist('milestones', None)
            for milestone in milestones_list:
                milestone_dict = json.loads(milestone)
                milestone_obj = POMilestone.objects.create(
                    precentage = int(milestone_dict.get('precentage')),
                    due = milestone_dict.get('due'),
                    description = milestone_dict.get('description'),
                    amount = milestone_dict.get('amount'),
                    remaining = milestone_dict.get('amount')
                )
                PO_obj.milestones.add(milestone_obj)

            # files creation
            if request.FILES:
                # print(request.FILES.getlist('filepond'))
                files = request.FILES.getlist('filepond')
                for file in files:
                    POFileHandler.objects.create(
                        file=file,
                        po=PO_obj,
                    )
                    
            # send emails
            sender = settings.EMAIL_USER
            receivers_list = PO_obj.quotation.RFQ.vendor.users.all()
            receiver = [rec.email for rec in receivers_list]
            subject = 'P.O. | New'
            message = f"""Dear {PO_obj.quotation.RFQ.vendor.name},

I hope this find you well.
You need to know that there is a new Purchase Order (P.O.)
Created right now with the following details:

RFQ ID:   {PO_obj.quotation.RFQ.RFQ_ID}
Quotation ID:   {PO_obj.quotation.id}
P.O. Number:   {PO_obj.number}

The whole details will be found in our web portal, waiting for you
To check it out.
Link:   http://127.0.0.1:8000/

*Note: This E-Mail is auto generated from our system, Just for your notification.

Best Regards,
Invoices Management System (IMS)
                        """
            send_email(
                sender,
                receiver,
                subject,
                message
            )
            data = {
                'status': 'added',
            }
            return JsonResponse(data=data, safe=False)

# Created
@is_user_login
def ProcurementCreatedPOView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        quotation_id = cursor.execute(f"SELECT DISTINCT [quotation_id] FROM [Invoices].[dbo].[system_purchaseorder]")
        quotation_id_results = quotation_id.fetchall()
        PO_number = cursor.execute(f"SELECT DISTINCT [id], [number] FROM [Invoices].[dbo].[system_purchaseorder]")
        PO_number_results = PO_number.fetchall()
        submitted_user = cursor.execute(f"""SELECT DISTINCT u.[id], CONCAT(u.[first_name], ' ', u.[last_name]) FROM [Invoices].[dbo].[system_purchaseorder] as spo, [Invoices].[dbo].[account_useraccount] as u
                                WHERE spo.[contact_person_id] = u.id""")
        submitted_user_results = submitted_user.fetchall()
        PO_currency = cursor.execute(f"""SELECT DISTINCT c.[id], c.[name] FROM [Invoices].[dbo].[system_purchaseorder] as spo, [Invoices].[dbo].[system_rfqcurrency] as c
                                WHERE spo.currency_id = c.id""")
        PO_currency_results = PO_currency.fetchall()
        milestones = cursor.execute(f"""SELECT DISTINCT sm.[id], sm.[precentage] FROM [Invoices].[dbo].[system_purchaseorder_milestones] as spom
                                join [Invoices].[dbo].[system_purchaseorder] as spo on spom.purchaseorder_id = spo.id
                                join [Invoices].[dbo].[system_pomilestone] as sm on spom.pomilestone_id = sm.id""")
        milestones_results = milestones.fetchall()
    context = {
        'user': user_obj,
        'quotation_id_results': quotation_id_results,
        'PO_number_results': PO_number_results,
        'submitted_user_results': submitted_user_results,
        'PO_currency_results': PO_currency_results,
        'milestones_results': milestones_results,
        'status_results': PO_status_choices,
    }
    return render(request, 'ProcurementPOCreated.html', context)

@is_user_login
def ProcurementCreatedPOTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        quotation = request.GET.get('quotation', None)
        PO_number = request.GET.get('PO_number', None)
        user = request.GET.get('user', None)
        currency = request.GET.get('currency', None)
        milestone = request.GET.get('milestone', None)
        status = request.GET.get('status', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)

    
        print(request.GET)
        PO_list = PurchaseOrder.objects.select_related('quotation', 'contact_person', 'currency')
                
        if quotation:
            PO_list = PO_list.filter(quotation_id=quotation)
        if PO_number:
            PO_list = PO_list.filter(id=PO_number)
        if user:
            PO_list = PO_list.filter(contact_person_id=user)
        if currency:
            PO_list = PO_list.filter(currency_id=currency)
        if milestone:
            milestone_obj = POMilestone.objects.get(id=milestone)
            PO_list = PO_list.filter(milestones=milestone_obj)
        if status:
            PO_list = PO_list.filter(status=status)
        if timestamp_from:
            PO_list = PO_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            PO_list = PO_list.filter(timestamp__lte=timestamp_to)

        # print(RFQ_list[0].status)
        POs = [
            {
                "id": polst.id,
                "number": polst.number,
                "quotation": polst.quotation.id,
                "total_value": polst.total_value,
                "currency": polst.currency.name,
                "milestones": polst.milestones.count(),
                "contact_person": f"{polst.contact_person.first_name} {polst.contact_person.last_name}",
                "status": 'Opened' if polst.status == 'o' else 'Closed',
                "timestamp": date_time_formatter(polst.timestamp),
            }
            for polst in PO_list
        ]
        return JsonResponse(data=POs, safe=False)

def ProcurementCreatedPODetailsApi(request):
    if request.GET:
        PO_id = request.GET.get('PO_id', None)
        PO_obj = PurchaseOrder.objects.select_related('quotation', 'contact_person', 'currency')\
            .get(id=PO_id)
        milestones_list = PO_obj.milestones.all()
        milestones = []
        milestones_count = PO_obj.milestones.count()
        for milestone in milestones_list:
            milestones.append(
                {
                'id': milestone.id,
                'precentage': f'{milestone.precentage} %',
                'due': f'{0 if not milestone.due else milestone.due} Days',
                'description': milestone.description,
                'amount': milestone.amount,
                'timestamp': date_time_formatter(milestone.timestamp)
                }
            )
        fhs = POFileHandler.objects.filter(po=PO_obj)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)

        RFQ_obj = {
            'PO_id': PO_obj.id,
            'PO_number': PO_obj.number,
            'quotation': PO_obj.quotation.id,
            'total_value': PO_obj.total_value,
            'currency': PO_obj.currency.name,
            'contact_person': f'{PO_obj.contact_person.first_name} {PO_obj.contact_person.last_name}',
            'status': 'Opened' if PO_obj.status == 'o' else 'Closed',
            'timestamp': date_time_formatter(PO_obj.timestamp),
            'shipping_terms': PO_obj.shipping_terms,
            'total_milestones': milestones_count,
            'milestones':milestones,
            'total_files': attachments_count,
            'attachments': attachments,
        }
        return JsonResponse(data=RFQ_obj, safe=False)


@is_user_login
def ProcurementPendingInvoicesView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        vendor = cursor.execute(f"""SELECT DISTINCT sv.[id], sv.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor] AS sv
                                WHERE ssi.invoice_id = si.id AND si.vendor_id = sv.id AND ssi.status = 'p'""")
        vendor_results = vendor.fetchall()
        number = cursor.execute(f"""SELECT DISTINCT si.[number]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si
                                WHERE ssi.invoice_id = si.id AND ssi.status = 'p'""")
        number_results = number.fetchall()
        po = cursor.execute(f"""SELECT DISTINCT spo.[id], spo.[number]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_purchaseorder] AS spo
                                WHERE ssi.invoice_id = si.id AND si.po_id = spo.id AND ssi.status = 'p'""")
        po_results = po.fetchall()
        due = cursor.execute(f"""SELECT DISTINCT si.[payment_due]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si
                                WHERE ssi.invoice_id = si.id AND ssi.status = 'p'""")
        due_results = due.fetchall()
        bill_to = cursor.execute(f"""SELECT DISTINCT si.[bill_to]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si
                                WHERE ssi.invoice_id = si.id AND ssi.status = 'p'""")
        bill_to_results = bill_to.fetchall()
        project_name = cursor.execute(f"""SELECT DISTINCT sp.[id], sp.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_project] AS sp
                                WHERE ssi.invoice_id = si.id AND si.project_id = sp.id AND ssi.status = 'p'""")
        project_name_results = project_name.fetchall()
        milestone = cursor.execute(f"""SELECT DISTINCT spom.[id], spom.[precentage]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_pomilestone] AS spom
                                WHERE ssi.invoice_id = si.id AND si.milestone_id = spom.id AND ssi.status = 'p'""")
        milestone_results = milestone.fetchall()
        item = cursor.execute(f"""SELECT DISTINCT sitm.[id], sitm.[number]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi
                                    ,[Invoices].[dbo].[system_invoice] AS sinvo
                                    ,[Invoices].[dbo].[system_invoice_items] AS sii
                                    ,[Invoices].[dbo].[system_item] AS sitm
                                WHERE ssi.invoice_id = sinvo.id 
                                    AND sii.invoice_id = sinvo.id 
                                    AND sii.item_id = sitm.id
                                    AND ssi.status = 'p'""")
        item_results = item.fetchall()
        currency = cursor.execute(f"""SELECT DISTINCT sic.[id], sic.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_invoicecurrency] AS sic
                                WHERE ssi.invoice_id = si.id AND si.currency_id = sic.id AND ssi.status = 'p'""")
        currency_results = currency.fetchall()
        type = cursor.execute(f"""SELECT DISTINCT sit.[id], sit.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_invoicetype] AS sit
                                WHERE ssi.invoice_id = si.id AND si.type_id = sit.id AND ssi.status = 'p'""")
        type_results = type.fetchall()
        vat = cursor.execute(f"""SELECT DISTINCT siv.[id], siv.[amount]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_invoicevat] AS siv
                                WHERE ssi.invoice_id = si.id AND si.vat_id = siv.id AND ssi.status = 'p'""")
        vat_results = vat.fetchall()
        submitted_user = cursor.execute('''SELECT DISTINCT [user_id], ([first_name]+' '+[last_name]) as full_name FROM [Invoices].[dbo].[system_pendinginvoice], [Invoices].[dbo].[account_useraccount]
                            WHERE [Invoices].[dbo].[system_pendinginvoice].[user_id] = [Invoices].[dbo].[account_useraccount].[id]''')
        submitted_user_results = submitted_user.fetchall()
    context = {
        'user': user_obj,
        'vendor_results': vendor_results,
        'number_results': number_results,
        'po_results': po_results,
        'due_results': due_results,
        'bill_to_results': bill_to_results,
        'project_name_results': project_name_results,
        'milestone_results': milestone_results,
        'item_results': item_results,
        'currency_results': currency_results,
        'type_results': type_results,
        'vat_results': vat_results,
        'submitted_user_results': submitted_user_results,
    }
    return render(request, 'ProcurementInvoicesToDo.html', context)


def ProcurementInvoicesToDoTableApi(request):
    if request.GET:
        vendor = request.GET.get('vendor', None)
        number = request.GET.get('number', None)
        date = request.GET.get('date', None)
        po = request.GET.get('po', None)
        due = request.GET.get('due', None)
        bill_to = request.GET.get('bill_to', None)
        project_name = request.GET.get('project_name', None)
        type = request.GET.get('type', None)
        milestone = request.GET.get('milestone', None)
        item = request.GET.get('item', None)
        vat = request.GET.get('vat', None)
        currency = request.GET.get('currency', None)
        user = request.GET.get('user', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)
        # print(engineer, technicion, station, ticket, task, vdatefrom, vdateto, rdatefrom, rdateto)
        # time_sheet_list = TimeSheet.objects.filter(area_manager_status=None).order_by('-id')
        invoices_list = PendingInvoice.objects\
            .select_related('invoice',
                            'invoice__po',
                            'invoice__milestone',
                            'invoice__vendor',
                            'invoice__project',
                            'invoice__type',
                            'invoice__vat',
                            'invoice__currency')
        if vendor:
            invoices_list = invoices_list.filter(invoice__vendor_id=vendor)
        if number:
            invoices_list = invoices_list.filter(invoice__number=number)
        if date:
            invoices_list = invoices_list.filter(invoice__date=date)
        if po:
            invoices_list = invoices_list.filter(invoice__po_id=po)
        if due:
            invoices_list = invoices_list.filter(invoice__payment_due=due)
        if bill_to:
            invoices_list = invoices_list.filter(invoice__bill_to=bill_to)
        if project_name:
            invoices_list = invoices_list.filter(invoice__project_id=project_name)
        if type:
            invoices_list = invoices_list.filter(invoice__type_id=type)
        if milestone:
            invoices_list = invoices_list.filter(invoice__milestone_id=milestone)
        if item:
            invoices_list = invoices_list.filter(invoice__items=item)
        if vat:
            invoices_list = invoices_list.filter(invoice__vat_id=vat)
        if currency:
            invoices_list = invoices_list.filter(invoice__currency_id=currency)
        if user:
            invoices_list = invoices_list.filter(user_id=user)
        if timestamp_from:
            invoices_list = invoices_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            invoices_list = invoices_list.filter(timestamp__lte=timestamp_to)
        # print(invoices_list.count())
        invoices = [
            {
                "id": invlst.id,
                "invoice_id": invlst.invoice.id,
                "vendor": invlst.invoice.vendor.name,
                "date": invlst.invoice.date,
                "po": invlst.invoice.po.number,
                "bill_to": invlst.invoice.bill_to,
                "user": f"{invlst.user.first_name} {invlst.user.last_name}",
                "timestamp": date_time_formatter(invlst.timestamp)
            }
            for invlst in invoices_list
        ]
        return JsonResponse(data=invoices, safe=False)
    

def ProcurementInvoicesToDoDetailsApi(request):
    if request.GET:
        submitted_id = request.GET.get('id', None)
        invoice_details = PendingInvoice.objects\
                            .select_related('invoice',
                                'invoice__po',
                                'invoice__milestone',
                                'invoice__vendor',
                                'invoice__project',
                                'invoice__type',
                                'invoice__vat',
                                'invoice__currency')\
                            .get(id=submitted_id)
        # print(invoice_details.invoice.items.first().number)
        items_list = invoice_details.invoice.items.select_related('uom')
        items = []
        items_count = invoice_details.invoice.items.count()
        items_total_amount = 0
        for item in items_list:
            items_total_amount += int(item.amount)
            items.append(
                {
                'number': item.number,
                'description': item.description,
                'quantity': item.quantity,
                'uom': item.uom.name,
                'unit_price': item.unit_price,
                'amount': item.amount,
                }
            )
        
        fhs = FileHandler.objects.filter(invoice=invoice_details.invoice)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)
        invoice = {
            'invoice_id': invoice_details.invoice.id,
            'vendor': invoice_details.invoice.vendor.name,
            'number': invoice_details.invoice.number,
            'date': invoice_details.invoice.date,
            'po': invoice_details.invoice.po.number,
            'payment_due': invoice_details.invoice.payment_due,
            'bill_to': invoice_details.invoice.bill_to,
            'project_name': invoice_details.invoice.project.name,
            'type': invoice_details.invoice.type.name,
            'milestone': invoice_details.invoice.milestone.precentage,
            'milestone_description': invoice_details.invoice.milestone.description,
            'items': items,
            'items_count':items_count,
            'items_total_amount':items_total_amount,
            'vat': invoice_details.invoice.vat.amount,
            'vat_amount': (items_total_amount * invoice_details.invoice.vat.amount)/100,
            'invoice_total': items_total_amount+((items_total_amount * invoice_details.invoice.vat.amount)/100),
            'currency': invoice_details.invoice.currency.name,
            'invoice_timestamp': date_time_formatter(invoice_details.invoice.timestamp),
            'invoice_attachments': attachments,
            'invoice_attachments_count': attachments_count,
            
            'submitted_id': invoice_details.id,
            'feedback': invoice_details.feedback,
            'user': f"{invoice_details.user.first_name} {invoice_details.user.last_name}",
            'submitted_timestamp': date_time_formatter(invoice_details.timestamp),
        }
        return JsonResponse(data=invoice, safe=False)
    

@is_user_login
def ProcurementInvoicesToDoApproveApi(request):
    if request.GET:
        try:
            user_token = request.session['user_token']
            user_obj = Token.objects.get(token=user_token).user
            invoice_id = request.GET.get('invoice_id', None)
            feedback = request.GET.get('feedback', None)
            submit_obj = SubmittedInvoice.objects.get(invoice_id=invoice_id)
            submit_obj.status = status_choices[1][0]
            submit_obj.feedback = feedback
            submit_obj.save()
            PendingInvoice.objects.filter(invoice_id=invoice_id).delete()
            
            invoice_obj = Invoice.objects.select_related('po', 'vat').get(id=invoice_id)
            invoice_items = invoice_obj.items.all()
            invoice_amount = 0
            for item in invoice_items:
                invoice_amount += float(item.amount)
            invoice_vat = (invoice_amount * invoice_obj.vat.amount) / 100
            invoice_total = invoice_amount + invoice_vat
            
            po_obj = invoice_obj.po
            if int((po_obj.remaining_value) - (invoice_total)) > 0:
                po_obj.remaining_value = (po_obj.remaining_value) - (invoice_total)
                po_obj.save()
            elif int((po_obj.remaining_value) - (invoice_total)) == 0:
                po_obj.remaining_value = (po_obj.remaining_value) - (invoice_total)
                po_obj.status = PO_status_choices[1][0]
                po_obj.save()
            else:
                print('Case Will Never Happend!...')
            po_payed = invoice_total
            for milestone in po_obj.milestones.all():
                if milestone.remaining == 0:
                    continue
                else:
                    check_value = milestone.remaining - po_payed
                    if check_value > 0:
                        milestone.remaining = check_value
                    else:
                        po_payed = po_payed - milestone.remaining
                        milestone.remaining = 0
                    milestone.save()
            if feedback:
                ApprovedInvoice.objects.create(
                    invoice_id=invoice_id,
                    feedback=feedback,
                    user=user_obj,
                )
            else:
                ApprovedInvoice.objects.create(
                    invoice_id=invoice_id,
                    user=user_obj,
                )
            return JsonResponse(data={'status': 'Approved'}, safe=False)
        except SubmittedInvoice.DoesNotExist as ex:
            print(ex)


@is_user_login
def ProcurementInvoicesToDoRejectApi(request):
    if request.GET:
        try:
            user_token = request.session['user_token']
            user_obj = Token.objects.get(token=user_token).user
            invoice_id = request.GET.get('invoice_id', None)
            feedback = request.GET.get('feedback', None)
            submit_obj = SubmittedInvoice.objects.get(invoice_id=invoice_id)
            submit_obj.status = status_choices[2][0]
            submit_obj.feedback = feedback
            submit_obj.save()
            PendingInvoice.objects.filter(invoice_id=invoice_id).delete()
            if feedback:
                RejectedInvoice.objects.create(
                    invoice_id=invoice_id,
                    feedback=feedback,
                    user=user_obj,
                )
            else:
                RejectedInvoice.objects.create(
                    invoice_id=invoice_id,
                    user=user_obj,
                )
            return JsonResponse(data={'status': 'Rejected'}, safe=False)
        except SubmittedInvoice.DoesNotExist as ex:
            print(ex)


    
@is_user_login
def ProcurementDoneInvoicesView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        vendor = cursor.execute(f"""SELECT DISTINCT sv.[id], sv.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_vendor] AS sv
                                WHERE ssi.invoice_id = si.id AND si.vendor_id = sv.id""")
        vendor_results = vendor.fetchall()
        number = cursor.execute(f"""SELECT DISTINCT si.[number]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si
                                WHERE ssi.invoice_id = si.id""")
        number_results = number.fetchall()
        po = cursor.execute(f"""SELECT DISTINCT spo.[id], spo.[number]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_purchaseorder] AS spo
                                WHERE ssi.invoice_id = si.id AND si.po_id = spo.id""")
        po_results = po.fetchall()
        due = cursor.execute(f"""SELECT DISTINCT si.[payment_due]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si
                                WHERE ssi.invoice_id = si.id""")
        due_results = due.fetchall()
        bill_to = cursor.execute(f"""SELECT DISTINCT si.[bill_to]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si
                                WHERE ssi.invoice_id = si.id""")
        bill_to_results = bill_to.fetchall()
        project_name = cursor.execute(f"""SELECT DISTINCT sp.[id], sp.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_project] AS sp
                                WHERE ssi.invoice_id = si.id AND si.project_id = sp.id""")
        project_name_results = project_name.fetchall()
        milestone = cursor.execute(f"""SELECT DISTINCT spom.[id], spom.[precentage]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_pomilestone] AS spom
                                WHERE ssi.invoice_id = si.id AND si.milestone_id = spom.id""")
        milestone_results = milestone.fetchall()
        item = cursor.execute(f"""SELECT DISTINCT sitm.[id], sitm.[number]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi
                                    ,[Invoices].[dbo].[system_invoice] AS sinvo
                                    ,[Invoices].[dbo].[system_invoice_items] AS sii
                                    ,[Invoices].[dbo].[system_item] AS sitm
                                WHERE ssi.invoice_id = sinvo.id 
                                    AND sii.invoice_id = sinvo.id 
                                    AND sii.item_id = sitm.id
                                   """)
        item_results = item.fetchall()
        currency = cursor.execute(f"""SELECT DISTINCT sic.[id], sic.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_invoicecurrency] AS sic
                                WHERE ssi.invoice_id = si.id AND si.currency_id = sic.id""")
        currency_results = currency.fetchall()
        type = cursor.execute(f"""SELECT DISTINCT sit.[id], sit.[name]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_invoicetype] AS sit
                                WHERE ssi.invoice_id = si.id AND si.type_id = sit.id""")
        type_results = type.fetchall()
        vat = cursor.execute(f"""SELECT DISTINCT siv.[id], siv.[amount]
                                FROM [Invoices].[dbo].[system_submittedinvoice] AS ssi, [Invoices].[dbo].[system_invoice] AS si, [Invoices].[dbo].[system_invoicevat] AS siv
                                WHERE ssi.invoice_id = si.id AND si.vat_id = siv.id""")
        vat_results = vat.fetchall()
        submitted_user = cursor.execute('''SELECT DISTINCT [user_id], ([first_name]+' '+[last_name]) as full_name FROM [Invoices].[dbo].[system_pendinginvoice], [Invoices].[dbo].[account_useraccount]
                            WHERE [Invoices].[dbo].[system_pendinginvoice].[user_id] = [Invoices].[dbo].[account_useraccount].[id]''')
        submitted_user_results = submitted_user.fetchall()
    context = {
        'user': user_obj,
        'vendor_results': vendor_results,
        'number_results': number_results,
        'po_results': po_results,
        'due_results': due_results,
        'bill_to_results': bill_to_results,
        'project_name_results': project_name_results,
        'milestone_results': milestone_results,
        'item_results': item_results,
        'currency_results': currency_results,
        'type_results': type_results,
        'vat_results': vat_results,
        'submitted_user_results': submitted_user_results,
        'status_results': status_choices,
    }
    return render(request, 'ProcurementInvoicesDone.html', context)


def ProcurementInvoicesDoneTableApi(request):
    if request.GET:
        vendor = request.GET.get('vendor', None)
        number = request.GET.get('number', None)
        date = request.GET.get('date', None)
        po = request.GET.get('po', None)
        due = request.GET.get('due', None)
        bill_to = request.GET.get('bill_to', None)
        project_name = request.GET.get('project_name', None)
        type = request.GET.get('type', None)
        milestone = request.GET.get('milestone', None)
        item = request.GET.get('item', None)
        vat = request.GET.get('vat', None)
        currency = request.GET.get('currency', None)
        user = request.GET.get('user', None)
        status = request.GET.get('status', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)
        # print(engineer, technicion, station, ticket, task, vdatefrom, vdateto, rdatefrom, rdateto)
        # time_sheet_list = TimeSheet.objects.filter(area_manager_status=None).order_by('-id')
        
        invoices_list = SubmittedInvoice.objects\
            .select_related('invoice',
                            'invoice__po',
                            'invoice__milestone',
                            'invoice__vendor',
                            'invoice__project',
                            'invoice__type',
                            'invoice__vat',
                            'invoice__currency')
        if vendor:
            invoices_list = invoices_list.filter(invoice__vendor_id=vendor)
        if number:
            invoices_list = invoices_list.filter(invoice__number=number)
        if date:
            invoices_list = invoices_list.filter(invoice__date=date)
        if po:
            invoices_list = invoices_list.filter(invoice__po_id=po)
        if due:
            invoices_list = invoices_list.filter(invoice__payment_due=due)
        if bill_to:
            invoices_list = invoices_list.filter(invoice__bill_to=bill_to)
        if project_name:
            invoices_list = invoices_list.filter(invoice__project_id=project_name)
        if type:
            invoices_list = invoices_list.filter(invoice__type_id=type)
        if milestone:
            invoices_list = invoices_list.filter(invoice__milestone_id=milestone)
        if item:
            invoices_list = invoices_list.filter(invoice__items=item)
        if vat:
            invoices_list = invoices_list.filter(invoice__vat_id=vat)
        if currency:
            invoices_list = invoices_list.filter(invoice__currency_id=currency)
        if user:
            invoices_list = invoices_list.filter(user_id=user)
        if status:
            invoices_list = invoices_list.filter(status=status)
        if timestamp_from:
            invoices_list = invoices_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            invoices_list = invoices_list.filter(timestamp__lte=timestamp_to)
        # print(invoices_list.count())
        invoices = [
            {
                "id": invlst.id,
                "invoice_id": invlst.invoice.id,
                "vendor": invlst.invoice.vendor.name,
                "date": invlst.invoice.date,
                "po": invlst.invoice.po.number,
                "bill_to": invlst.invoice.bill_to,
                "user": f"{invlst.user.first_name} {invlst.user.last_name}",
                "timestamp": date_time_formatter(invlst.timestamp),
                "status": dict(status_choices).get(invlst.status)
            }
            for invlst in invoices_list
        ]
        return JsonResponse(data=invoices, safe=False)
    

def ProcurementInvoicesDoneDetailsApi(request):
    if request.GET:
        submitted_id = request.GET.get('id', None)
        invoice_details = SubmittedInvoice.objects\
                            .select_related('invoice',
                                'invoice__po',
                                'invoice__milestone',
                                'invoice__vendor',
                                'invoice__project',
                                'invoice__type',
                                'invoice__vat',
                                'invoice__currency')\
                            .get(id=submitted_id)
        # print(invoice_details.invoice.items.first().number)
        items_list = invoice_details.invoice.items.select_related('uom')
        items = []
        items_count = invoice_details.invoice.items.count()
        items_total_amount = 0
        for item in items_list:
            items_total_amount += int(item.amount)
            items.append(
                {
                'number': item.number,
                'description': item.description,
                'quantity': item.quantity,
                'uom': item.uom.name,
                'unit_price': item.unit_price,
                'amount': item.amount,
                }
            )
        
        fhs = FileHandler.objects.filter(invoice=invoice_details.invoice)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)
        invoice = {
            'invoice_id': invoice_details.invoice.id,
            'vendor': invoice_details.invoice.vendor.name,
            'number': invoice_details.invoice.number,
            'date': invoice_details.invoice.date,
            'po': invoice_details.invoice.po.number,
            'payment_due': invoice_details.invoice.payment_due,
            'bill_to': invoice_details.invoice.bill_to,
            'project_name': invoice_details.invoice.project.name,
            'type': invoice_details.invoice.type.name,
            'milestone': invoice_details.invoice.milestone.precentage,
            'milestone_description': invoice_details.invoice.milestone.description,
            'items': items,
            'items_count':items_count,
            'items_total_amount':items_total_amount,
            'vat': invoice_details.invoice.vat.amount,
            'vat_amount': (items_total_amount * invoice_details.invoice.vat.amount)/100,
            'invoice_total': items_total_amount+((items_total_amount * invoice_details.invoice.vat.amount)/100),
            'currency': invoice_details.invoice.currency.name,
            'invoice_timestamp': date_time_formatter(invoice_details.invoice.timestamp),
            'invoice_attachments': attachments,
            'invoice_attachments_count': attachments_count,
            'status': invoice_details.status,
            
            'submitted_id': invoice_details.id,
            'feedback': invoice_details.feedback,
            'user': f"{invoice_details.user.first_name} {invoice_details.user.last_name}",
            'submitted_timestamp': date_time_formatter(invoice_details.timestamp),
        }
        if invoice_details.status == 'a':
            approved_obj = ApprovedInvoice.objects.get(invoice=invoice_details.invoice)
            invoice['approved_user'] = f"{approved_obj.user.first_name} {approved_obj.user.last_name}"
            invoice['approved_timeStamp'] = date_time_formatter(approved_obj.timestamp)
            invoice['approved_feedback'] = approved_obj.feedback
        if invoice_details.status == 'r':
            rejected_obj = RejectedInvoice.objects.get(invoice=invoice_details.invoice)
            invoice['rejected_user'] = f"{rejected_obj.user.first_name} {rejected_obj.user.last_name}"
            invoice['rejected_timeStamp'] = date_time_formatter(rejected_obj.timestamp)
            invoice['rejected_feedback'] = rejected_obj.feedback
        return JsonResponse(data=invoice, safe=False)
    

@is_user_login
def ProcurementNewVendorView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    vendors = Vendor.objects.all()
    vendors_list = []
    for ven in vendors:
        vic = SubmittedInvoice.objects.filter(invoice__vendor__name=ven.name).count()
        vendors_list.append(
            [ven.name.upper(), vic, ven.users.all()]
        )
    context = {
        'user': user_obj,
        'vendor': vendors_list,
    }
    return render(request, 'ProcurementNewVendor.html', context)


@is_user_login
def ProcurementNewVendorApi(request):
    if request.POST:
        vendor_name = request.POST.get('vendor_name', None)
        check_name = Vendor.objects.filter(name=vendor_name).exists()
        if check_name:
            return HttpResponseRedirect('/system/Invoices/ProcurementNewVendor/?vendor=exists')
        else:
            Vendor.objects.create(
                name=vendor_name
            )
            return HttpResponseRedirect('/system/Invoices/ProcurementNewVendor/?vendor=added')


@is_user_login
def ProcurementNewVendorUserApi(request):
    if request.POST:
        firstName = request.POST.get('firstName', None)
        lastName = request.POST.get('lastName', None)
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        vendor = request.POST.get('vendor', None)
        print(vendor)
        check_name = UserAccount.objects.filter(username=username).exists()
        if check_name:
            return HttpResponseRedirect('/system/Invoices/ProcurementNewVendor/?user=exists')
        else:
            user_obj = UserAccount.objects.create(
                first_name= firstName,
                last_name= lastName if lastName else 'Company',
                email= email if email else 'example@example.com',
                username= username,
                password= make_password(password) if password else make_password('As123123'),
                role_id= 1,
            )
            vendor_obj = Vendor.objects.get(name=vendor)
            print(vendor_obj)
            vendor_obj.users.add(user_obj)
            vendor_obj.save()
            return HttpResponseRedirect('/system/Invoices/ProcurementNewVendor/?user=added')

  
# @is_user_login
# def NewInvoiceVendorView(request):
#     if request.POST:
#         vendor = request.POST.get('vendor', None)
#         check_name = Vendor.objects.filter(name=vendor).exists()
#         if check_name:
#             return HttpResponseRedirect('/system/Invoices/NewVendor/?fail=true')
#         else:
#             Vendor.objects.create(name=vendor)
#             return HttpResponseRedirect('/system/Invoices/NewVendor/?done=true')
#     user_token = request.session['user_token']
#     user_obj = Token.objects.get(token=user_token).user
#     with connection.cursor() as cursor:
#         vendor = cursor.execute(""" SELECT v.name, COUNT(si.status) AS StatusCount
#                                     FROM [Invoices].[dbo].[system_vendor] AS v
#                                     LEFT JOIN [Invoices].[dbo].[system_invoice] AS i ON v.id = i.vendor_id
#                                     LEFT JOIN [Invoices].[dbo].[system_submittedinvoice] AS si ON i.id = si.invoice_id
#                                     GROUP BY v.id, v.name;""")
#         vendor_results = vendor.fetchall()
#     context = {
#         'user': user_obj,
#         'vendor': vendor_results,
#     }
#     return render(request, 'NewVendor.html', context)
  




######################################## MANAGER ###############################################


@is_user_login
def ManagerDashboardView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    # t_invoice = Invoice.objects.count()
    t_invoice = SubmittedInvoice.objects.count()
    p_invoice = PendingInvoice.objects.count()
    a_invoice = ApprovedInvoice.objects.count()
    r_invoice = RejectedInvoice.objects.count()
    context = {
        'user': user_obj,
        # 't_invoice': t_invoice,
        't_invoice': t_invoice,
        'p_invoice': p_invoice,
        'a_invoice': a_invoice,
        'r_invoice': r_invoice
    }
    return render(request, 'ManagerDashboard.html', context)


def ManagerInvoicesStatusColumnChartApi(request):
    if request.GET:
        filter = request.GET.get('filter', None)
        from_value = request.GET.get('from', None)
        to_value = request.GET.get('to', None)
        current_date = datetime.now().date()
        filters_query = Q()
        if from_value:
            if filter == 'per_time':
                filters_query &= (Q(timestamp__date=current_date) & Q(timestamp__time__gte=from_value))
            if filter == 'per_day':
                filters_query &= Q(timestamp__date__gte=from_value)
            if filter == 'per_month':
                year_from, month_from = map(int, from_value.split('-'))
                filters_query &= (Q(timestamp__year__gt=year_from) | (Q(timestamp__year=year_from) & Q(timestamp__month__gte=month_from)))
            if filter == 'per_year':
                filters_query &= Q(timestamp__year__gte=from_value)
        if to_value:
            if filter == 'per_time':
                filters_query &= (Q(timestamp__date=current_date) & Q(timestamp__time__lte=to_value))
            if filter == 'per_day':
                filters_query &= Q(timestamp__date__lte=to_value)
            if filter == 'per_month':
                year_to, month_to = map(int, to_value.split('-'))
                filters_query &= (Q(timestamp__year__lt=year_to) | (Q(timestamp__year=year_to) & Q(timestamp__month__lte=month_to)))
                # print(year_to, month_to, filters_query)
            if filter == 'per_year':
                filters_query &= Q(timestamp__year__lte=to_value)
        p_invoice = PendingInvoice.objects.filter(filters_query).count()
        a_invoice = ApprovedInvoice.objects.filter(filters_query).count()
        r_invoice = RejectedInvoice.objects.filter(filters_query).count()
        # print(p_invoice, a_invoice, r_invoice)
    else:
        p_invoice = PendingInvoice.objects.count()
        a_invoice = ApprovedInvoice.objects.count()
        r_invoice = RejectedInvoice.objects.count()
    data = [
        ['Pending', p_invoice, p_invoice, '#343a40'],
        ['Approved', a_invoice, a_invoice, '#28a745'],
        ['Rejected', r_invoice, r_invoice, '#dc3545'],
    ]
    return JsonResponse(data=data, safe=False)


def ManagerInvoicesStatusPieChartApi(request):
    p_invoice = PendingInvoice.objects.count()
    a_invoice = ApprovedInvoice.objects.count()
    r_invoice = RejectedInvoice.objects.count()
    data = [
        ['Pending', p_invoice],
        ['Approved', a_invoice],
        ['Rejected', r_invoice],
    ]
    return JsonResponse(data=data, safe=False)


    
@is_user_login
def ManagerDoneInvoicesView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        vendor = cursor.execute("SELECT DISTINCT [vendor] FROM [Invoices].[dbo].[system_invoice]")
        vendor_results = vendor.fetchall()
        number = cursor.execute("SELECT DISTINCT [number] FROM [Invoices].[dbo].[system_invoice]")
        number_results = number.fetchall()
        po = cursor.execute("SELECT DISTINCT [po] FROM [Invoices].[dbo].[system_invoice]")
        po_results = po.fetchall()
        due = cursor.execute("SELECT DISTINCT [payment_due] FROM [Invoices].[dbo].[system_invoice]")
        due_results = due.fetchall()
        bill_to = cursor.execute("SELECT DISTINCT [bill_to] FROM [Invoices].[dbo].[system_invoice]")
        bill_to_results = bill_to.fetchall()
        project_name = cursor.execute("SELECT DISTINCT [project_name] FROM [Invoices].[dbo].[system_invoice]")
        project_name_results = project_name.fetchall()
        milestone = cursor.execute("SELECT DISTINCT [milestone] FROM [Invoices].[dbo].[system_invoice]")
        milestone_results = milestone.fetchall()
        item = cursor.execute("SELECT DISTINCT [id], [number] FROM [Invoices].[dbo].[system_item]")
        item_results = item.fetchall()
        currency = cursor.execute("SELECT DISTINCT [id], [name] FROM [Invoices].[dbo].[system_invoicecurrency]")
        currency_results = currency.fetchall()
        type = cursor.execute("SELECT DISTINCT [id], [name] FROM [Invoices].[dbo].[system_invoicetype]")
        type_results = type.fetchall()
        vat = cursor.execute("SELECT DISTINCT [id], [amount] FROM [Invoices].[dbo].[system_invoicevat]")
        vat_results = vat.fetchall()
        submitted_user = cursor.execute('''SELECT DISTINCT [user_id], ([first_name]+' '+[last_name]) as full_name FROM [Invoices].[dbo].[system_submittedinvoice], [Invoices].[dbo].[account_useraccount]
                            WHERE [Invoices].[dbo].[system_submittedinvoice].[user_id] = [Invoices].[dbo].[account_useraccount].[id]''')
        submitted_user_results = submitted_user.fetchall()
    context = {
        'user': user_obj,
        'vendor_results': vendor_results,
        'number_results': number_results,
        'po_results': po_results,
        'due_results': due_results,
        'bill_to_results': bill_to_results,
        'project_name_results': project_name_results,
        'milestone_results': milestone_results,
        'item_results': item_results,
        'currency_results': currency_results,
        'type_results': type_results,
        'vat_results': vat_results,
        'submitted_user_results': submitted_user_results,
        'status_results': status_choices,
    }
    return render(request, 'ManagerInvoicesDone.html', context)


def ManagerInvoicesDoneTableApi(request):
    if request.GET:
        vendor = request.GET.get('vendor', None)
        number = request.GET.get('number', None)
        date = request.GET.get('date', None)
        po = request.GET.get('po', None)
        due = request.GET.get('due', None)
        bill_to = request.GET.get('bill_to', None)
        project_name = request.GET.get('project_name', None)
        type = request.GET.get('type', None)
        milestone = request.GET.get('milestone', None)
        item = request.GET.get('item', None)
        vat = request.GET.get('vat', None)
        currency = request.GET.get('currency', None)
        user = request.GET.get('user', None)
        status = request.GET.get('status', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)
        # print(engineer, technicion, station, ticket, task, vdatefrom, vdateto, rdatefrom, rdateto)
        # time_sheet_list = TimeSheet.objects.filter(area_manager_status=None).order_by('-id')
        
        invoices_list = SubmittedInvoice.objects\
            .select_related('invoice',
                            'invoice__type',
                            'invoice__vat',
                            'invoice__currency')
        
        if vendor:
            invoices_list = invoices_list.filter(invoice__vendor=vendor)
        if number:
            invoices_list = invoices_list.filter(invoice__number=number)
        if date:
            invoices_list = invoices_list.filter(invoice__date=date)
        if po:
            invoices_list = invoices_list.filter(invoice__po=po)
        if due:
            invoices_list = invoices_list.filter(invoice__payment_due=due)
        if bill_to:
            invoices_list = invoices_list.filter(invoice__bill_to=bill_to)
        if project_name:
            invoices_list = invoices_list.filter(invoice__project_name=project_name)
        if type:
            invoices_list = invoices_list.filter(invoice__type__id=type)
        if milestone:
            invoices_list = invoices_list.filter(invoice__milestone=milestone)
        if item:
            invoices_list = invoices_list.filter(invoice__items=item)
        if vat:
            invoices_list = invoices_list.filter(invoice__vat__id=vat)
        if currency:
            invoices_list = invoices_list.filter(invoice__currency__id=currency)
        if user:
            invoices_list = invoices_list.filter(user__id=user)
        if status:
            invoices_list = invoices_list.filter(status=status)
        if timestamp_from:
            invoices_list = invoices_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            invoices_list = invoices_list.filter(timestamp__lte=timestamp_to)
        # print(invoices_list.count())
        invoices = [
            {
                "id": invlst.id,
                "invoice_id": invlst.invoice.id,
                "vendor": invlst.invoice.vendor,
                "date": invlst.invoice.date,
                "po": invlst.invoice.po,
                "bill_to": invlst.invoice.bill_to,
                "user": f"{invlst.user.first_name} {invlst.user.last_name}",
                "timestamp": date_time_formatter(invlst.timestamp),
                "status": dict(status_choices).get(invlst.status)
            }
            for invlst in invoices_list
        ]
        return JsonResponse(data=invoices, safe=False)
    

def ManagerInvoicesDoneDetailsApi(request):
    if request.GET:
        submitted_id = request.GET.get('id', None)
        invoice_details = SubmittedInvoice.objects.select_related('invoice', 'invoice__type',
                                'invoice__vat', 'invoice__currency')\
                            .get(id=submitted_id)
        # print(invoice_details.invoice.items.first().number)
        items_list = invoice_details.invoice.items.select_related('uom')
        items = []
        items_count = invoice_details.invoice.items.count()
        items_total_amount = 0
        for item in items_list:
            items_total_amount += int(item.amount)
            items.append(
                {
                'number': item.number,
                'description': item.description,
                'quantity': item.quantity,
                'uom': item.uom.name,
                'unit_price': item.unit_price,
                'amount': item.amount,
                }
            )
        
        fhs = FileHandler.objects.filter(invoice=invoice_details.invoice)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)
        invoice = {
            'invoice_id': invoice_details.invoice.id,
            'vendor': invoice_details.invoice.vendor,
            'number': invoice_details.invoice.number,
            'date': invoice_details.invoice.date,
            'po': invoice_details.invoice.po,
            'payment_due': invoice_details.invoice.payment_due,
            'bill_to': invoice_details.invoice.bill_to,
            'project_name': invoice_details.invoice.project_name,
            'type': invoice_details.invoice.type.name,
            'milestone': invoice_details.invoice.milestone,
            'items': items,
            'items_count':items_count,
            'items_total_amount':items_total_amount,
            'vat': invoice_details.invoice.vat.amount,
            'vat_amount': (items_total_amount * invoice_details.invoice.vat.amount)/100,
            'invoice_total': items_total_amount+((items_total_amount * invoice_details.invoice.vat.amount)/100),
            'currency': invoice_details.invoice.currency.name,
            'invoice_timestamp': date_time_formatter(invoice_details.invoice.timestamp),
            'invoice_attachments': attachments,
            'invoice_attachments_count': attachments_count,
            'status': invoice_details.status,
            
            'submitted_id': invoice_details.id,
            'feedback': invoice_details.feedback,
            'user': f"{invoice_details.user.first_name} {invoice_details.user.last_name}",
            'submitted_timestamp': date_time_formatter(invoice_details.timestamp),
        }
        if invoice_details.status == 'a':
            approved_obj = ApprovedInvoice.objects.get(invoice=invoice_details.invoice)
            invoice['approved_user'] = f"{approved_obj.user.first_name} {approved_obj.user.last_name}"
            invoice['approved_timeStamp'] = date_time_formatter(approved_obj.timestamp)
            invoice['approved_feedback'] = approved_obj.feedback
        if invoice_details.status == 'r':
            rejected_obj = RejectedInvoice.objects.get(invoice=invoice_details.invoice)
            invoice['rejected_user'] = f"{rejected_obj.user.first_name} {rejected_obj.user.last_name}"
            invoice['rejected_timeStamp'] = date_time_formatter(rejected_obj.timestamp)
            invoice['rejected_feedback'] = rejected_obj.feedback
        return JsonResponse(data=invoice, safe=False)
    


############################## PRESALES ########################################################


@is_user_login
def PresalesDashboardView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    # t_invoice = Invoice.objects.count()
    t_invoice = SubmittedInvoice.objects.count()
    p_invoice = PendingInvoice.objects.count()
    a_invoice = ApprovedInvoice.objects.count()
    r_invoice = RejectedInvoice.objects.count()
    context = {
        'user': user_obj,
        # 't_invoice': t_invoice,
        't_invoice': t_invoice,
        'p_invoice': p_invoice,
        'a_invoice': a_invoice,
        'r_invoice': r_invoice
    }
    return render(request, 'PresalesDashboard.html', context)


@is_user_login
def PresalesNewProjectView(request):
    if request.POST:
        project_name = request.POST.get('project_name', None)
        check_project = Project.objects.filter(name=project_name).exists()
        if check_project:
            return HttpResponseRedirect('/system/PresalesProject/New/?project=exists')
        else:
            Project.objects.create(
                name=project_name
            )
            return HttpResponseRedirect('/system/PresalesProject/New/?project=added')
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    projects = Project.objects.all()
    project_list = []
    for project in projects:
        vendors = Vendor.objects.filter(projects=project)
        project_list.append(
            [project.name, vendors.count(), vendors.all()]
        )
    context = {
        'user': user_obj,
        'projects': project_list,
    }
    return render(request, 'PresalesNewProject.html', context)


@is_user_login
def PresalesNewRFQView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    projects = Project.objects.all()
    vendors = Vendor.objects.only('id', 'name')
    RFQ_types = RFQType.objects.all()
    RFQ_currency = RFQCurrency.objects.all()
    product_uom = ProductUom.objects.all()
    context = {
        'user': user_obj,
        'projects': projects,
        'vendors': vendors,
        'RFQ_types': RFQ_types,
        'RFQ_currency': RFQ_currency,
        'product_uom': product_uom,
        'qrfai': RFQ_QuotesRequiredForAllItems,
        'bccsq': RFQ_BidderCanChangeSubmittedQuote,
        'bcai': RFQ_BidderCanAddItems,
        'bccq': RFQ_BidderCanChangeQuantity,
    }
    return render(request, 'PresalesRFQNew.html', context)


@is_user_login
def PresalesNewRFQSubmitApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.POST:
        print(request.POST)
        # RFQ creation
        RFQ_ID = request.POST.get('RFQ_ID', None)
        vendor = request.POST.get('vendor', None)
        project = request.POST.get('project', None)
        ship_to_address = request.POST.get('ship_to_address', None)
        Bidder_ID = request.POST.get('Bidder_ID', None)
        # submission_deadline = request.POST.get('submission_deadline', None)
        qmbvu = request.POST.get('qmbvu', None)
        RFQ_type = request.POST.get('RFQ_type', None)
        eqc = request.POST.get('eqc', None)
        qrfai = request.POST.get('qrfai', None)
        bccsq = request.POST.get('bccsq', None)
        bcai = request.POST.get('bcai', None)
        bccq = request.POST.get('bccq', None)
        
        check_RFQ = RFQ.objects.select_related('vendor', 'project').filter(RFQ_ID=RFQ_ID, vendor_id=vendor, project_id=project)
        
        if check_RFQ.exists():
            data = {
                'status': "Error: The provided invoice number is not unique.",
            }
            return JsonResponse(data=data, safe=False)
        else:
            vendor_obj = Vendor.objects.get(id=vendor)
            project_obj = Project.objects.get(id=project)
            vendor_obj.projects.add(project_obj)
            RFQ_obj = RFQ.objects.create(
                RFQ_ID = RFQ_ID,
                project = project_obj,
                vendor = vendor_obj,
                ship_to_address = ship_to_address,
                bidder_id = Bidder_ID,
                type_id = RFQ_type,
                submission_deadline = datetime.now(),
                Quote_must_be_valid_until = qmbvu,
                currency_id = eqc,
                Quotes_required_for_all_items = qrfai,
                Bidder_can_change_submitted_quote = bccsq,
                Bidder_can_add_items = bcai,
                Bidder_can_change_quantity = bccq,
                status = RFQ_status_choices[0][0],
                user = user_obj,
            )

            # items creation
            products_list = request.POST.getlist('products', None)
            for product in products_list:
                product_dict = json.loads(product)
                uom_obj = ProductUom.objects.get(name=product_dict.get('uom'))
                product_obj = Product.objects.create(
                    item = int(product_dict.get('item_number')),
                    product_id = product_dict.get('product_id'),
                    description = product_dict.get('description'),
                    quantity = int(product_dict.get('quantity')),
                    uom = uom_obj,
                    category = product_dict.get('category'),
                    # delivery_date = datetime.strptime(product_dict.get('dd_sp'), '%d/%m/%Y').date()
                    delivery_date = datetime.strptime(product_dict.get('dd_sp'), '%Y-%m-%d').date()
                )
                RFQ_obj.products.add(product_obj)

            # files creation
            if request.FILES:
                # print(request.FILES.getlist('filepond'))
                files = request.FILES.getlist('filepond')
                for file in files:
                    RFQFileHandler.objects.create(
                        file=file,
                        RFQ=RFQ_obj,
                    )
                    
            # send emails
            sender = user_obj.email
            receivers_list = RFQ_obj.vendor.users.all()
            receiver = [rec.email for rec in receivers_list]
            subject = 'New Request For Quotation'
            message = f"""Dear {RFQ_obj.vendor.name},

I hope this find you well.
You need to know that there is a new Request For Quotation (RFQ)
Created right now with the following details:

RFQ ID:   {RFQ_obj.RFQ_ID}
Project:   {RFQ_obj.project.name}

The whole details will be found in our web portal, waiting for you
To check it out.
Link:   http://127.0.0.1:8000/

*Note: This E-Mail is auto generated from our system, Just for your notification.

Best Regards,
Invoices Management System (IMS)
                        """
            # print([rec.email for rec in receivers_list])
            # send_email(
            #     sender,
            #     receiver,
            #     subject,
            #     message
            # )
            data = {
                'status': 'added',
            }
            return JsonResponse(data=data, safe=False)


@is_user_login
def PresalesCreatedRFQView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        RFQ_ID = cursor.execute(f"SELECT DISTINCT [RFQ_ID] FROM [Invoices].[dbo].[system_rfq]")
        RFQ_ID_results = RFQ_ID.fetchall()
        vendor = cursor.execute(f"SELECT DISTINCT [id], [name] FROM [Invoices].[dbo].[system_vendor]")
        vendor_results = vendor.fetchall()
        project = cursor.execute(f"""SELECT DISTINCT p.[id], p.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_project] as p
                                WHERE srfq.project_id = p.id""")
        project_results = project.fetchall()
        bidder_id = cursor.execute(f"SELECT DISTINCT [bidder_id] FROM [Invoices].[dbo].[system_rfq]")
        bidder_id_results = bidder_id.fetchall()
        RFQ_type = cursor.execute(f"""SELECT DISTINCT t.[id], t.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqtype] as t
                                WHERE srfq.type_id = t.id""")
        RFQ_type_results = RFQ_type.fetchall()
        RFQ_currency = cursor.execute(f"""SELECT DISTINCT c.[id], c.[name] FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[system_rfqcurrency] as c
                                WHERE srfq.currency_id = c.id""")
        RFQ_currency_results = RFQ_currency.fetchall()
        product_id = cursor.execute(f"""SELECT sp.[id], sp.[product_id] FROM [Invoices].[dbo].[system_rfq_products] as srfqp
                                join [Invoices].[dbo].[system_rfq] as srfq on srfqp.rfq_id = srfq.id
                                join [Invoices].[dbo].[system_product] as sp on srfqp.product_id = sp.id""")
        product_id_results = product_id.fetchall()
        user = cursor.execute(f"""SELECT DISTINCT u.[id], CONCAT(u.[first_name], ' ', u.[last_name]) FROM [Invoices].[dbo].[system_rfq] as srfq, [Invoices].[dbo].[account_useraccount] as u
                                WHERE srfq.user_id = u.id""")
        user_results = user.fetchall()
    context = {
        'user': user_obj,
        'vendor_results': vendor_results,
        'RFQ_ID_results': RFQ_ID_results,
        'project_results': project_results,
        'bidder_id_results': bidder_id_results,
        'RFQ_type_results': RFQ_type_results,
        'RFQ_currency_results': RFQ_currency_results,
        'RFQ_qrfai_results': RFQ_QuotesRequiredForAllItems,
        'RFQ_bccsq_results': RFQ_BidderCanChangeSubmittedQuote,
        'RFQ_bcai_results': RFQ_BidderCanAddItems,
        'RFQ_bccq_results': RFQ_BidderCanChangeQuantity,
        'product_id_results': product_id_results,
        'RFQ_status': RFQ_status_choices,
        'user_results': user_results,
    }
    return render(request, 'PresalesRFQCreated.html', context)


@is_user_login
def PresalesCreatedRFQTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        project = request.GET.get('project', None)
        vendor = request.GET.get('vendor', None)
        Bidder_ID = request.GET.get('Bidder_ID', None)
        RFQ_Type = request.GET.get('RFQ_Type', None)
        eqc = request.GET.get('eqc', None)
        qrfai = request.GET.get('qrfai', None)
        bccsq = request.GET.get('bccsq', None)
        bcai = request.GET.get('bcai', None)
        bccq = request.GET.get('bccq', None)
        Product_ID = request.GET.get('Product_ID', None)
        status = request.GET.get('status', None)
        user = request.GET.get('user', None)
        sd_from = request.GET.get('sd_from', None)
        sd_to = request.GET.get('sd_to', None)
        qmbvu_from = request.GET.get('qmbvu_from', None)
        qmbvu_to = request.GET.get('qmbvu_to', None)

        print(request.GET)
        RFQ_list = RFQ.objects.select_related('project', 'vendor', 'type', 'currency', 'user')
                
        if RFQ_ID:
            RFQ_list = RFQ_list.filter(RFQ_ID=RFQ_ID)
        if project:
            RFQ_list = RFQ_list.filter(project_id=project)
        if vendor:
            RFQ_list = RFQ_list.filter(vendor_id=vendor)
        if Bidder_ID:
            RFQ_list = RFQ_list.filter(bidder_id=Bidder_ID)
        if RFQ_Type:
            RFQ_list = RFQ_list.filter(type_id=RFQ_Type)
        if eqc:
            RFQ_list = RFQ_list.filter(currency_id=eqc)
        if qrfai:
            RFQ_list = RFQ_list.filter(Quotes_required_for_all_items=qrfai)
        if bccsq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_submitted_quote=bccsq)
        if bcai:
            RFQ_list = RFQ_list.filter(Bidder_can_add_items=bcai)
        if bccq:
            RFQ_list = RFQ_list.filter(Bidder_can_change_quantity=bccq)
        if Product_ID:
            product_obj = Product.objects.get(id=Product_ID)
            RFQ_list = RFQ_list.filter(products=product_obj)
        if status:
            RFQ_list = RFQ_list.filter(status=status)
        if user:
            RFQ_list = RFQ_list.filter(user_id=user)
        if sd_from:
            RFQ_list = RFQ_list.filter(submission_deadline__gte=sd_from)
        if sd_to:
            RFQ_list = RFQ_list.filter(submission_deadline__lte=sd_to)
        if qmbvu_from:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__gte=qmbvu_from)
        if qmbvu_to:
            RFQ_list = RFQ_list.filter(Quote_must_be_valid_until__lte=qmbvu_to)
        # print(RFQ_list[0].status)
        RFQs = [
            {
                "id": rfqlst.id,
                "RFQ_ID": rfqlst.RFQ_ID,
                "vendor": rfqlst.vendor.name,
                "project": rfqlst.project.name,
                "submission_deadline": date_time_formatter(rfqlst.submission_deadline),
                "status": 'Sent' if rfqlst.status == 's' else 'Viewed' if rfqlst.status == 'v' else 'Replyed',
                "user": f"{rfqlst.user.first_name} {rfqlst.user.last_name}",
                "quotation": Quotation.objects.filter(RFQ=rfqlst).count(),
            }
            for rfqlst in RFQ_list
        ]
        return JsonResponse(data=RFQs, safe=False)


def PresalesCreatedRFQDetailsApi(request):
    if request.GET:
        RFQ_ID = request.GET.get('RFQ_ID', None)
        RFQ_details = RFQ.objects.select_related('project', 'vendor', 'type', 'currency', 'user')\
            .get(RFQ_ID=RFQ_ID)
        products_list = RFQ_details.products.select_related('uom')
        products = []
        products_count = RFQ_details.products.count()
        for product in products_list:
            products.append(
                {
                'item_number': product.item,
                'product_id': product.product_id,
                'description': product.description,
                'quantity': product.quantity,
                'uom': product.uom.name,
                'category': product.category,
                'dd_sp': product.delivery_date,
                }
            )
        
        fhs = RFQFileHandler.objects.filter(RFQ=RFQ_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
        # print(attachments)

        RFQ_obj = {
            'id': RFQ_details.id,
            'vendor': RFQ_details.vendor.name,
            'RFQ_ID': RFQ_details.RFQ_ID,
            'project_name': RFQ_details.project.name,
            'ship_to_address': RFQ_details.ship_to_address,
            'bidder_id': RFQ_details.bidder_id,
            'submission_deadline': date_time_formatter(RFQ_details.submission_deadline),
            'qmbvu': RFQ_details.Quote_must_be_valid_until,
            'RFQ_Type': RFQ_details.type.name,
            'eqc': RFQ_details.currency.name,
            'qrfai': 'Yes' if RFQ_details.Quotes_required_for_all_items == 'y' else 'No',
            'bccsq': 'Yes' if RFQ_details.Bidder_can_change_submitted_quote == 'y' else 'No',
            'bcai': 'Yes' if RFQ_details.Bidder_can_add_items == 'y' else 'No',
            'bccq': 'Yes' if RFQ_details.Bidder_can_change_quantity == 'y' else 'No',
            'products': products,
            'products_count':products_count,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=RFQ_obj, safe=False)




@is_user_login
def PresalesQuotationToDoView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        Quotation_ID = cursor.execute(f"""SELECT DISTINCT [id] FROM [Invoices].[dbo].[system_quotation] WHERE [status] = 'c'""")
        Quotation_ID_results = Quotation_ID.fetchall()
        RFQ_ID = cursor.execute(f"""SELECT DISTINCT srfq.[RFQ_ID] FROM [Invoices].[dbo].[system_quotation] AS sq, [Invoices].[dbo].[system_rfq] AS srfq
                                WHERE sq.[RFQ_id] = srfq.[id] AND sq.[status] = 'c'""")
        RFQ_ID_results = RFQ_ID.fetchall()
        currency = cursor.execute(f"""SELECT DISTINCT cr.[id], cr.[name] FROM [Invoices].[dbo].[system_quotation] AS sq, [Invoices].[dbo].[system_rfqcurrency] as cr
                                WHERE sq.[currency_id] = cr.[id]""")
        currency_results = currency.fetchall()
        user = cursor.execute(f"""SELECT DISTINCT sq.[user_id], CONCAT(aua.first_name, ' ', aua.last_name) FROM [Invoices].[dbo].[system_quotation] AS sq
                                JOIN [Invoices].[dbo].[account_useraccount] AS aua ON aua.[id] = sq.[user_id]
                                WHERE sq.[status] = 'c'""")
        user_results = user.fetchall()
    context = {
        'user': user_obj,
        'Quotation_ID_results': Quotation_ID_results,
        'RFQ_ID_results': RFQ_ID_results,
        # 'Status': Quotation_status_choices,
        'currency_results': currency_results,
        'user_results': user_results,
    }
    return render(request, 'PresalesQuotationToDo.html', context)


@is_user_login
def PresalesQuotationToDoTableApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        quotation = request.GET.get('quotation', None)
        RFQ_ID = request.GET.get('RFQ_ID', None)
        status = request.GET.get('status', None)
        currency = request.GET.get('currency', None)
        user = request.GET.get('user', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)

        print(request.GET)
        Quotation_list = Quotation.objects.select_related('RFQ', 'RFQ__vendor', 'user', 'currency')\
            .filter(status=Quotation_status_choices[0][0])
                
        if quotation:
            Quotation_list = Quotation_list.filter(id=quotation)
        if RFQ_ID:
            Quotation_list = Quotation_list.filter(RFQ__RFQ_ID=RFQ_ID)
        if status:
            Quotation_list = Quotation_list.filter(status=status)
        if currency:
            Quotation_list = Quotation_list.filter(currency_id=currency)
        if user:
            Quotation_list = Quotation_list.filter(user=user)
        if timestamp_from:
            Quotation_list = Quotation_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            Quotation_list = Quotation_list.filter(timestamp__lte=timestamp_to)
        # print(Quotation_list[0].status)

        Quotations = [
            {
                "id": ql.id,
                "RFQ_ID": ql.RFQ.RFQ_ID,
                "currency": ql.currency.name,
                "net_value": ql.net_value,
                "status": 'Created' if ql.status == 'c' else 'Approved' if ql.status == 'a' else 'Rejected',
                "user": f'{ql.user.first_name} {ql.user.last_name}',
                "timestamp": date_time_formatter(ql.timestamp),
            }
            for ql in Quotation_list
        ]
        return JsonResponse(data=Quotations, safe=False)


def PresalesQuotationToDoDetailsApi(request):
    if request.GET:
        Quote_ID = request.GET.get('Quote_ID', None)
        Quotation_details = Quotation.objects.select_related('RFQ', 'RFQ__type', 'currency', 'user')\
            .get(id=Quote_ID)

        fhs = QuotationFileHandler.objects.filter(quotation=Quotation_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
            
        Quotation_obj = {
            'RFQ_ID': Quotation_details.RFQ.RFQ_ID,
            'submission_deadline': date_time_formatter(Quotation_details.RFQ.submission_deadline),
            'qmbvu': Quotation_details.RFQ.Quote_must_be_valid_until,
            'RFQ_Type': Quotation_details.RFQ.type.name,
            'eqc': Quotation_details.currency.name,
            'net_value': Quotation_details.net_value,
            'currency': Quotation_details.currency.name,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=Quotation_obj, safe=False)


@is_user_login
def PresalesQuotationToDoApproveApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        Quote_ID = request.GET.get('Quote_ID', None)
        feedback = request.GET.get('feedback', None)
        print(Quote_ID)
        quote_obj = Quotation.objects.get(id=Quote_ID)
        ApprovedQuotation.objects.create(
            quotation = quote_obj,
            feedback = feedback,
            user = user_obj,
        )
        quote_obj.status = 'a'
        quote_obj.save()
        data = {
            'status': 'done',
        }
        return JsonResponse(data=data, safe=False)


@is_user_login
def PresalesQuotationToDoRejectApi(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.GET:
        Quote_ID = request.GET.get('Quote_ID', None)
        feedback = request.GET.get('feedback', None)
        quote_obj = Quotation.objects.get(id=Quote_ID)
        RejectedQuotation.objects.create(
            quotation = quote_obj,
            feedback = feedback,
            user = user_obj,
        )
        quote_obj.status = 'r'
        quote_obj.save()
        data = {
            'status': 'done',
        }
        return JsonResponse(data=data, safe=False)




@is_user_login
def PresalesQuotationDoneView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    with connection.cursor() as cursor:
        Quotation_ID = cursor.execute(f"""SELECT DISTINCT [id] FROM [Invoices].[dbo].[system_quotation]""")
        Quotation_ID_results = Quotation_ID.fetchall()
        RFQ_ID = cursor.execute(f"""SELECT DISTINCT srfq.[RFQ_ID] FROM [Invoices].[dbo].[system_quotation] AS sq, [Invoices].[dbo].[system_rfq] AS srfq
                                WHERE sq.[RFQ_id] = srfq.[id]""")
        RFQ_ID_results = RFQ_ID.fetchall()
        currency = cursor.execute(f"""SELECT DISTINCT cr.[id], cr.[name] FROM [Invoices].[dbo].[system_quotation] AS sq, [Invoices].[dbo].[system_rfqcurrency] as cr
                                WHERE sq.[currency_id] = cr.[id]""")
        currency_results = currency.fetchall()
        user = cursor.execute(f"""SELECT DISTINCT sq.[user_id], CONCAT(aua.first_name, ' ', aua.last_name) FROM [Invoices].[dbo].[system_quotation] AS sq
                                JOIN [Invoices].[dbo].[account_useraccount] AS aua ON aua.[id] = sq.[user_id]
                                WHERE sq.[status] = 'c'""")
        user_results = user.fetchall()
    context = {
        'user': user_obj,
        'Quotation_ID_results': Quotation_ID_results,
        'RFQ_ID_results': RFQ_ID_results,
        'Status': Quotation_status_choices,
        'currency_results': currency_results,
        'user_results': user_results,
    }
    return render(request, 'PresalesQuotationDone.html', context)


def PresalesQuotationDoneTableApi(request):
    if request.GET:
        quotation = request.GET.get('quotation', None)
        RFQ_ID = request.GET.get('RFQ_ID', None)
        status = request.GET.get('status', None)
        currency = request.GET.get('currency', None)
        user = request.GET.get('user', None)
        timestamp_from = request.GET.get('timestamp_from', None)
        timestamp_to = request.GET.get('timestamp_to', None)

        # print(request.GET)
        Quotation_list = Quotation.objects.select_related('RFQ', 'RFQ__vendor', 'user', 'currency')
                
        if quotation:
            Quotation_list = Quotation_list.filter(id=quotation)
        if RFQ_ID:
            Quotation_list = Quotation_list.filter(RFQ__RFQ_ID=RFQ_ID)
        if status:
            Quotation_list = Quotation_list.filter(status=status)
        if currency:
            Quotation_list = Quotation_list.filter(currency_id=currency)
        if user:
            Quotation_list = Quotation_list.filter(user=user)
        if timestamp_from:
            Quotation_list = Quotation_list.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            Quotation_list = Quotation_list.filter(timestamp__lte=timestamp_to)
        # print(Quotation_list[0].status)

        Quotations = [
            {
                "id": ql.id,
                "RFQ_ID": ql.RFQ.RFQ_ID,
                "currency": ql.currency.name,
                "net_value": ql.net_value,
                "status": 'Created' if ql.status == 'c' else 'Approved' if ql.status == 'a' else 'Rejected',
                "user": f'{ql.user.first_name} {ql.user.last_name}',
                "timestamp": date_time_formatter(ql.timestamp),
            }
            for ql in Quotation_list
        ]
        return JsonResponse(data=Quotations, safe=False)


def PresalesQuotationDoneDetailsApi(request):
    if request.GET:
        Quote_ID = request.GET.get('Quote_ID', None)
        Quotation_details = Quotation.objects.select_related('RFQ', 'RFQ__type', 'currency', 'user')\
            .get(id=Quote_ID)

        fhs = QuotationFileHandler.objects.filter(quotation=Quotation_details)
        attachments = []
        attachments_count = fhs.count()
        for f in fhs:
            file_name = os.path.basename(f.file.name)
            file_url = f.file.url
            file_extension = os.path.splitext(file_name)[1].split('.')[1]
            attachments.append([file_name, file_url, file_extension, f.id])
            
        Quotation_obj = {
            'RFQ_ID': Quotation_details.RFQ.RFQ_ID,
            'submission_deadline': date_time_formatter(Quotation_details.RFQ.submission_deadline),
            'qmbvu': Quotation_details.RFQ.Quote_must_be_valid_until,
            'RFQ_Type': Quotation_details.RFQ.type.name,
            'eqc': Quotation_details.currency.name,
            'net_value': Quotation_details.net_value,
            'currency': Quotation_details.currency.name,
            'attachments': attachments,
            'attachments_count': attachments_count,
        }
        return JsonResponse(data=Quotation_obj, safe=False)




@is_user_login
def PresalesConfigurationView(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if request.POST:
        type = request.POST.get('type', None)
        type_name = request.POST.get('type_name', None)
        if type == 'RFQ_type':
            check_name = RFQType.objects.filter(name=type_name).exists()
            if check_name:
                return HttpResponseRedirect('/system/PresalesConfiguration/?RFQ_Type=exists')
            else:
                RFQType.objects.create(name=type_name)
                return HttpResponseRedirect('/system/PresalesConfiguration/?RFQ_Type=added')
        if type == 'currency':
            check_name = RFQCurrency.objects.filter(name=type_name).exists()
            if check_name:
                return HttpResponseRedirect('/system/PresalesConfiguration/?currency=exists')
            else:
                RFQCurrency.objects.create(name=type_name)
                return HttpResponseRedirect('/system/PresalesConfiguration/?currency=added')
        if type == 'uom':
            check_name = ProductUom.objects.filter(name=type_name).exists()
            if check_name:
                return HttpResponseRedirect('/system/PresalesConfiguration/?uom=exists')
            else:
                ProductUom.objects.create(name=type_name)
                return HttpResponseRedirect('/system/PresalesConfiguration/?uom=added')
        # if type == 'category':
        #     check_name = ProductCategory.objects.filter(name=type_name).exists()
        #     if check_name:
        #         return HttpResponseRedirect('/system/PresalesConfiguration/?category=exists')
        #     else:
        #         ProductCategory.objects.create(name=type_name)
        #         return HttpResponseRedirect('/system/PresalesConfiguration/?category=added')
    RFQ_types = RFQType.objects.all()
    RFQ_currency = RFQCurrency.objects.all()
    product_uom = ProductUom.objects.all()
    # product_category = ProductCategory.objects.all()
    items_list = [
        [['fa-solid fa-file-circle-question me-1', 'RFQ Types'], RFQ_types.count(), RFQ_types],
        [['fa-solid fa-dollar-sign me-1', 'Currencies'], RFQ_currency.count(), RFQ_currency],
        [['fa-solid fa-weight-hanging me-1', 'UOM'], product_uom.count(), product_uom],
        # [['fa-solid fa-layer-group me-1', 'Categories'], product_category.count(), product_category],
    ]
    context = {
        'user': user_obj,
        'items': items_list,
    }
    return render(request, 'PresalesConfig.html', context)



  



@is_user_login
def UserChangePassword(request):
    if request.method == 'POST':
        username = request.POST.get('userid', None)
        password = request.POST.get('new_password', None)
        try:
            user = UserAccount.objects.get(id=username)
            user.password = make_password(password)
            user.save()
            return HttpResponseRedirect('/system/change/password/?change=true')
        except UserAccount.DoesNotExist:
            print('UserAccount not found')
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    context = {
        'user': user_obj,
    }
    return render(request, 'changePassword.html', context)


def send_email(sender, receiver, subject, message):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(receiver)
    msg["Subject"] = subject
    msg.attach(MIMEText(message,"plain"))
    text = msg.as_string()

    server = smtplib.SMTP("mail.globalts-eg.com",587)
    server.starttls()

    server.login(settings.EMAIL_USER,settings.EMAIL_PASSWORD)

    server.sendmail(sender,receiver,text)
        
    server.quit()


def date_time_formatter(date):
    # Format the datetime as "Month Day, Year, Hour:Minute a.m./p.m."
    formatted_date = date.strftime("%m/%d/%Y %H:%M")
    # formatted_date = date.strftime("%b. %d, %Y, %I:%M %p")
    # print(formatted_date)
    return formatted_date


# views the error page
@is_user_login
def error_404_page(request):
    user_token = request.session['user_token']
    user_obj = Token.objects.get(token=user_token).user
    if user_obj.role.id == 1:
        home_url = '/system/Vendor/'
    if user_obj.role.id == 2:
        home_url = '/system/Procurement/'
    if user_obj.role.id == 3:
        home_url = '/system/Manager/'
    if user_obj.role.id == 4:
        home_url = '/system/Presales/'
    # render the error404 page
    return render(request, 'error404.html', {'Error': 'Do Not Mess With The URL...:(', 'home': home_url})



















