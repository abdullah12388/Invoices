from django.urls import path, re_path, include
from .views import *
# from django.views.static import serve
"/system/Vendor/Invoices/Status/column/chart/api/"
"/system/Vendor/Invoices/Status/pie/chart/api/"
urlpatterns = [
    # Vendor
    path('Vendor/', VendorDashboardView, name='VendorDashboardView'),
    path('Vendor/Invoices/Status/column/chart/api/', VendorInvoicesStatusColumnChartApi, name='VendorInvoicesStatusColumnChartApi'),
    path('Vendor/Invoices/Status/pie/chart/api/', VendorInvoicesStatusPieChartApi, name='VendorInvoicesStatusPieChartApi'),
    
    path('VendorRFQToDo/', VendorPendingRFQView, name='VendorPendingRFQView'),
    path('VendorRFQToDo/table/api/', VendorRFQToDoTableApi, name='VendorRFQToDoTableApi'),
    path("VendorRFQToDo/details/api/", VendorRFQToDoDetailsApi, name='VendorRFQToDoDetailsApi'),
    path("VendorRFQToDo/create/quote/api/", VendorRFQToDoCreateQuoteApi, name='VendorRFQToDoCreateQuoteApi'),
    path("VendorRFQToDo/create/quote/submit/api/", VendorRFQToDoCreateQuoteSubmitApi, name='VendorRFQToDoCreateQuoteSubmitApi'),

    path('VendorRFQDone/', VendorDoneRFQView, name='VendorDoneRFQView'),
    path('VendorRFQDone/table/api/', VendorRFQDoneTableApi, name='VendorRFQDoneTableApi'),
    path("VendorRFQDone/details/api/", VendorRFQDoneDetailsApi, name='VendorRFQDoneDetailsApi'),
    path("VendorRFQDone/create/quote/api/", VendorRFQDoneCreateQuoteApi, name='VendorRFQDoneCreateQuoteApi'),
    path("VendorRFQDone/create/quote/submit/api/", VendorRFQDoneCreateQuoteSubmitApi, name='VendorRFQDoneCreateQuoteSubmitApi'),
    
    path('Quotation/', VendorQuotationView, name='VendorQuotationView'),
    path('Quotation/table/api/', VendorQuotationTableApi, name='VendorQuotationTableApi'),
    path("Quotation/details/api/", VendorQuoteDetailsApi, name='VendorQuoteDetailsApi'),
    
    
    path('PurchaseOrder/', VendorPOView, name='VendorPOView'),
    path('PurchaseOrder/table/api/', VendorPOTableApi, name='VendorPOTableApi'),
    path("PurchaseOrder/details/api/", VendorPODetailsApi, name='VendorPODetailsApi'),
    
    
    path('Invoices/VendorDone/', VendorDoneInvoicesView, name='VendorDoneInvoicesView'),
    path("Invoices/VendorDone/table/api/", VendorInvoicesDoneTableApi, name='VendorInvoicesDoneTableApi'),
    path("Invoices/VendorDone/details/api/", VendorInvoicesDoneDetailsApi, name='VendorInvoicesDoneDetailsApi'),
    
    path("Invoices/New/", NewInvoiceView, name='NewInvoiceView'),
    path("Invoices/New/PO/Details/api/", NewInvoicePODetailsApi, name='NewInvoicePODetailsApi'),
    path("Invoices/New/Submit/api/", NewInvoiceSubmitApi, name='NewInvoiceSubmitApi'),

    # Procurement
    path('Procurement/', ProcurementDashboardView, name='ProcurementDashboardView'),
    path('Procurement/Invoices/Status/column/chart/api/', ProcurementInvoicesStatusColumnChartApi, name='ProcurementInvoicesStatusColumnChartApi'),
    path('Procurement/Invoices/Status/pie/chart/api/', ProcurementInvoicesStatusPieChartApi, name='ProcurementInvoicesStatusPieChartApi'),
    
    path('ProcurementRFQ/Created/', ProcurementCreatedRFQView, name='ProcurementCreatedRFQView'),
    path('ProcurementRFQ/Created/table/api/', ProcurementCreatedRFQTableApi, name='ProcurementCreatedRFQTableApi'),
    path("ProcurementRFQ/Created/details/api/", ProcurementCreatedRFQDetailsApi, name='ProcurementCreatedRFQDetailsApi'),
    
    path('ProcurementQuotationDone/', ProcurementQuotationDoneView, name='ProcurementQuotationDoneView'),
    path('ProcurementQuotationDone/table/api/', ProcurementQuotationDoneTableApi, name='ProcurementQuotationDoneTableApi'),
    path("ProcurementQuotationDone/details/api/", ProcurementQuotationDoneDetailsApi, name='ProcurementQuotationDoneDetailsApi'),
    
    
    path('ProcurementPO/New/', ProcurementNewPOView, name='ProcurementNewPOView'),
    path('ProcurementPO/New/Submit/api/', ProcurementNewPOSubmitApi, name='ProcurementNewPOSubmitApi'),
    
    path('ProcurementPO/Created/', ProcurementCreatedPOView, name='ProcurementCreatedPOView'),
    path('ProcurementPO/Created/table/api/', ProcurementCreatedPOTableApi, name='ProcurementCreatedPOTableApi'),
    path("ProcurementPO/Created/details/api/", ProcurementCreatedPODetailsApi, name='ProcurementCreatedPODetailsApi'),
    
    
    path('Invoices/ProcurementToDo/', ProcurementPendingInvoicesView, name='ProcurementPendingInvoicesView'),
    path("Invoices/ProcurementToDo/table/api/", ProcurementInvoicesToDoTableApi, name='ProcurementInvoicesToDoTableApi'),
    path("Invoices/ProcurementToDo/details/api/", ProcurementInvoicesToDoDetailsApi, name='ProcurementInvoicesToDoDetailsApi'),
    path("Invoices/ProcurementToDo/approve/api/", ProcurementInvoicesToDoApproveApi, name='ProcurementInvoicesToDoApproveApi'),
    path("Invoices/ProcurementToDo/reject/api/", ProcurementInvoicesToDoRejectApi, name='ProcurementInvoicesToDoRejectApi'),
    
    
    path('Invoices/ProcurementDone/', ProcurementDoneInvoicesView, name='ProcurementDoneInvoicesView'),
    path("Invoices/ProcurementDone/table/api/", ProcurementInvoicesDoneTableApi, name='ProcurementInvoicesDoneTableApi'),
    path("Invoices/ProcurementDone/details/api/", ProcurementInvoicesDoneDetailsApi, name='ProcurementInvoicesDoneDetailsApi'),
    
    path("Invoices/ProcurementNewVendor/", ProcurementNewVendorView, name='ProcurementNewVendorView'),
    path("Invoices/ProcurementNewVendor/api/", ProcurementNewVendorApi, name='ProcurementNewVendorApi'),
    path("Invoices/ProcurementNewVendor/user/api/", ProcurementNewVendorUserApi, name='ProcurementNewVendorUserApi'),
    
    # path("Invoices/NewVendor/", NewInvoiceVendorView, name='NewInvoiceVendorView'),
    # path("Invoices/New/Submit/api/", NewInvoiceSubmitApi, name='NewInvoiceSubmitApi'),
    
    
    # Manager
    path('Manager/', ManagerDashboardView, name='ManagerDashboardView'),
    path('Manager/Invoices/Status/column/chart/api/', ManagerInvoicesStatusColumnChartApi, name='ManagerInvoicesStatusColumnChartApi'),
    path('Manager/Invoices/Status/pie/chart/api/', ManagerInvoicesStatusPieChartApi, name='ManagerInvoicesStatusPieChartApi'),
    
    path('Invoices/ManagerDone/', ManagerDoneInvoicesView, name='ManagerDoneInvoicesView'),
    path("Invoices/ManagerDone/table/api/", ManagerInvoicesDoneTableApi, name='ManagerInvoicesDoneTableApi'),
    path("Invoices/ManagerDone/details/api/", ManagerInvoicesDoneDetailsApi, name='ManagerInvoicesDoneDetailsApi'),
    
    # PreSales
    path('Presales/', PresalesDashboardView, name='PresalesDashboardView'),
    path('PresalesProject/New/', PresalesNewProjectView, name='PresalesNewProjectView'),
    path('PresalesRFQ/New/', PresalesNewRFQView, name='PresalesNewRFQView'),
    path('PresalesRFQ/New/Submit/api/', PresalesNewRFQSubmitApi, name='PresalesNewRFQSubmitApi'),
    path('PresalesRFQ/Created/', PresalesCreatedRFQView, name='PresalesCreatedRFQView'),
    path('PresalesRFQ/Created/table/api/', PresalesCreatedRFQTableApi, name='PresalesCreatedRFQTableApi'),
    path("PresalesRFQ/Created/details/api/", PresalesCreatedRFQDetailsApi, name='PresalesCreatedRFQDetailsApi'),
    
    path('PresalesQuotationToDo/', PresalesQuotationToDoView, name='PresalesQuotationToDoView'),
    path('PresalesQuotationToDo/table/api/', PresalesQuotationToDoTableApi, name='PresalesQuotationToDoTableApi'),
    path("PresalesQuotationToDo/details/api/", PresalesQuotationToDoDetailsApi, name='PresalesQuotationToDoDetailsApi'),
    path("PresalesQuotationToDo/approve/api/", PresalesQuotationToDoApproveApi, name='PresalesQuotationToDoApproveApi'),
    path("PresalesQuotationToDo/reject/api/", PresalesQuotationToDoRejectApi, name='PresalesQuotationToDoRejectApi'),
    
    path('PresalesQuotationDone/', PresalesQuotationDoneView, name='PresalesQuotationDoneView'),
    path('PresalesQuotationDone/table/api/', PresalesQuotationDoneTableApi, name='PresalesQuotationDoneTableApi'),
    path("PresalesQuotationDone/details/api/", PresalesQuotationDoneDetailsApi, name='PresalesQuotationDoneDetailsApi'),

    
    path('PresalesConfiguration/', PresalesConfigurationView, name='PresalesConfigurationView'),
    
    
    
    # change Password
    path('change/password/', UserChangePassword, name='UserChangePassword'),
]
