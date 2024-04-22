# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from system.views import *


# class TestUrls(SimpleTestCase):
    
#     def test_VendorDashboardView_url_resolved(self):
#         url = reverse('VendorDashboardView')
#         self.assertEquals(resolve(url).func, VendorDashboardView)
        
#     def test_VendorStatusColumnChartApi_url_resolved(self):
#         url = reverse('VendorStatusColumnChartApi')
#         self.assertEquals(resolve(url).func, VendorStatusColumnChartApi)

#     def test_VendorStatusPieChartApi_url_resolved(self):
#         url = reverse('VendorStatusPieChartApi')
#         self.assertEquals(resolve(url).func, VendorStatusPieChartApi)
        
#     def test_VendorStatusPieChartApi_url_resolved(self):
#         url = reverse('VendorStatusPieChartApi')
#         self.assertEquals(resolve(url).func, VendorStatusPieChartApi)
        
#     def test_VendorPendingRFQView_url_resolved(self):
#         url = reverse('VendorPendingRFQView')
#         self.assertEquals(resolve(url).func, VendorPendingRFQView)
        
#     def test_VendorRFQToDoTableApi_url_resolved(self):
#         url = reverse('VendorRFQToDoTableApi')
#         self.assertEquals(resolve(url).func, VendorRFQToDoTableApi)
        
#     def test_VendorRFQToDoDetailsApi_url_resolved(self):
#         url = reverse('VendorRFQToDoDetailsApi')
#         self.assertEquals(resolve(url).func, VendorRFQToDoDetailsApi)
        
#     def test_VendorRFQToDoCreateQuoteApi_url_resolved(self):
#         url = reverse('VendorRFQToDoCreateQuoteApi')
#         self.assertEquals(resolve(url).func, VendorRFQToDoCreateQuoteApi)
        
#     def test_VendorRFQToDoCreateQuoteSubmitApi_url_resolved(self):
#         url = reverse('VendorRFQToDoCreateQuoteSubmitApi')
#         self.assertEquals(resolve(url).func, VendorRFQToDoCreateQuoteSubmitApi)
        
#     def test_VendorDoneRFQView_url_resolved(self):
#         url = reverse('VendorDoneRFQView')
#         self.assertEquals(resolve(url).func, VendorDoneRFQView)
        
#     def test_VendorRFQDoneTableApi_url_resolved(self):
#         url = reverse('VendorRFQDoneTableApi')
#         self.assertEquals(resolve(url).func, VendorRFQDoneTableApi)
        
#     def test_VendorRFQDoneDetailsApi_url_resolved(self):
#         url = reverse('VendorRFQDoneDetailsApi')
#         self.assertEquals(resolve(url).func, VendorRFQDoneDetailsApi)
        
#     def test_VendorRFQDoneCreateQuoteApi_url_resolved(self):
#         url = reverse('VendorRFQDoneCreateQuoteApi')
#         self.assertEquals(resolve(url).func, VendorRFQDoneCreateQuoteApi)
        
#     def test_VendorRFQDoneCreateQuoteSubmitApi_url_resolved(self):
#         url = reverse('VendorRFQDoneCreateQuoteSubmitApi')
#         self.assertEquals(resolve(url).func, VendorRFQDoneCreateQuoteSubmitApi)
        
#     def test_VendorQuotationView_url_resolved(self):
#         url = reverse('VendorQuotationView')
#         self.assertEquals(resolve(url).func, VendorQuotationView)
        
#     def test_VendorQuotationTableApi_url_resolved(self):
#         url = reverse('VendorQuotationTableApi')
#         self.assertEquals(resolve(url).func, VendorQuotationTableApi)
        
#     def test_VendorQuoteDetailsApi_url_resolved(self):
#         url = reverse('VendorQuoteDetailsApi')
#         self.assertEquals(resolve(url).func, VendorQuoteDetailsApi)
        
#     def test_VendorPOView_url_resolved(self):
#         url = reverse('VendorPOView')
#         self.assertEquals(resolve(url).func, VendorPOView)
        
#     def test_VendorPOTableApi_url_resolved(self):
#         url = reverse('VendorPOTableApi')
#         self.assertEquals(resolve(url).func, VendorPOTableApi)
        
#     def test_VendorPODetailsApi_url_resolved(self):
#         url = reverse('VendorPODetailsApi')
#         self.assertEquals(resolve(url).func, VendorPODetailsApi)
        
#     def test_VendorDoneInvoicesView_url_resolved(self):
#         url = reverse('VendorDoneInvoicesView')
#         self.assertEquals(resolve(url).func, VendorDoneInvoicesView)
        
#     def test_VendorInvoicesDoneTableApi_url_resolved(self):
#         url = reverse('VendorInvoicesDoneTableApi')
#         self.assertEquals(resolve(url).func, VendorInvoicesDoneTableApi)
        
#     def test_VendorInvoicesDoneDetailsApi_url_resolved(self):
#         url = reverse('VendorInvoicesDoneDetailsApi')
#         self.assertEquals(resolve(url).func, VendorInvoicesDoneDetailsApi)
        
#     def test_NewInvoiceView_url_resolved(self):
#         url = reverse('NewInvoiceView')
#         self.assertEquals(resolve(url).func, NewInvoiceView)
        
#     def test_NewInvoicePODetailsApi_url_resolved(self):
#         url = reverse('NewInvoicePODetailsApi')
#         self.assertEquals(resolve(url).func, NewInvoicePODetailsApi)
        
#     def test_NewInvoiceSubmitApi_url_resolved(self):
#         url = reverse('NewInvoiceSubmitApi')
#         self.assertEquals(resolve(url).func, NewInvoiceSubmitApi)
        
#     def test_ProcurementDashboardView_url_resolved(self):
#         url = reverse('ProcurementDashboardView')
#         self.assertEquals(resolve(url).func, ProcurementDashboardView)
        
#     def test_ProcurementStatusColumnChartApi_url_resolved(self):
#         url = reverse('ProcurementStatusColumnChartApi')
#         self.assertEquals(resolve(url).func, ProcurementStatusColumnChartApi)
        
#     def test_ProcurementStatusPieChartApi_url_resolved(self):
#         url = reverse('ProcurementStatusPieChartApi')
#         self.assertEquals(resolve(url).func, ProcurementStatusPieChartApi)
        
#     def test_ProcurementCreatedRFQView_url_resolved(self):
#         url = reverse('ProcurementCreatedRFQView')
#         self.assertEquals(resolve(url).func, ProcurementCreatedRFQView)
        
#     def test_ProcurementCreatedRFQTableApi_url_resolved(self):
#         url = reverse('ProcurementCreatedRFQTableApi')
#         self.assertEquals(resolve(url).func, ProcurementCreatedRFQTableApi)
        
#     def test_ProcurementCreatedRFQDetailsApi_url_resolved(self):
#         url = reverse('ProcurementCreatedRFQDetailsApi')
#         self.assertEquals(resolve(url).func, ProcurementCreatedRFQDetailsApi)
        
#     def test_ProcurementQuotationDoneView_url_resolved(self):
#         url = reverse('ProcurementQuotationDoneView')
#         self.assertEquals(resolve(url).func, ProcurementQuotationDoneView)
        
#     def test_ProcurementQuotationDoneTableApi_url_resolved(self):
#         url = reverse('ProcurementQuotationDoneTableApi')
#         self.assertEquals(resolve(url).func, ProcurementQuotationDoneTableApi)
        
#     def test_ProcurementQuotationDoneDetailsApi_url_resolved(self):
#         url = reverse('ProcurementQuotationDoneDetailsApi')
#         self.assertEquals(resolve(url).func, ProcurementQuotationDoneDetailsApi)
        
#     def test_ProcurementNewPOView_url_resolved(self):
#         url = reverse('ProcurementNewPOView')
#         self.assertEquals(resolve(url).func, ProcurementNewPOView)
        
#     def test_ProcurementNewPOSubmitApi_url_resolved(self):
#         url = reverse('ProcurementNewPOSubmitApi')
#         self.assertEquals(resolve(url).func, ProcurementNewPOSubmitApi)
        
#     def test_ProcurementCreatedPOView_url_resolved(self):
#         url = reverse('ProcurementCreatedPOView')
#         self.assertEquals(resolve(url).func, ProcurementCreatedPOView)
        
#     def test_ProcurementCreatedPOTableApi_url_resolved(self):
#         url = reverse('ProcurementCreatedPOTableApi')
#         self.assertEquals(resolve(url).func, ProcurementCreatedPOTableApi)
        
#     def test_ProcurementCreatedPODetailsApi_url_resolved(self):
#         url = reverse('ProcurementCreatedPODetailsApi')
#         self.assertEquals(resolve(url).func, ProcurementCreatedPODetailsApi)
        
#     def test_ProcurementPendingInvoicesView_url_resolved(self):
#         url = reverse('ProcurementPendingInvoicesView')
#         self.assertEquals(resolve(url).func, ProcurementPendingInvoicesView)
#     def test_ProcurementInvoicesToDoTableApi_url_resolved(self):
#         url = reverse('ProcurementInvoicesToDoTableApi')
#         self.assertEquals(resolve(url).func, ProcurementInvoicesToDoTableApi)
        
#     def test_ProcurementInvoicesToDoDetailsApi_url_resolved(self):
#         url = reverse('ProcurementInvoicesToDoDetailsApi')
#         self.assertEquals(resolve(url).func, ProcurementInvoicesToDoDetailsApi)
        
#     def test_ProcurementInvoicesToDoApproveApi_url_resolved(self):
#         url = reverse('ProcurementInvoicesToDoApproveApi')
#         self.assertEquals(resolve(url).func, ProcurementInvoicesToDoApproveApi)
        
#     def test_ProcurementInvoicesToDoRejectApi_url_resolved(self):
#         url = reverse('ProcurementInvoicesToDoRejectApi')
#         self.assertEquals(resolve(url).func, ProcurementInvoicesToDoRejectApi)
        
#     def test_ProcurementDoneInvoicesView_url_resolved(self):
#         url = reverse('ProcurementDoneInvoicesView')
#         self.assertEquals(resolve(url).func, ProcurementDoneInvoicesView)
        
#     def test_ProcurementInvoicesDoneTableApi_url_resolved(self):
#         url = reverse('ProcurementInvoicesDoneTableApi')
#         self.assertEquals(resolve(url).func, ProcurementInvoicesDoneTableApi)
        
#     def test_ProcurementInvoicesDoneDetailsApi_url_resolved(self):
#         url = reverse('ProcurementInvoicesDoneDetailsApi')
#         self.assertEquals(resolve(url).func, ProcurementInvoicesDoneDetailsApi)
        
#     def test_ProcurementNewVendorView_url_resolved(self):
#         url = reverse('ProcurementNewVendorView')
#         self.assertEquals(resolve(url).func, ProcurementNewVendorView)
        
#     def test_ProcurementNewVendorApi_url_resolved(self):
#         url = reverse('ProcurementNewVendorApi')
#         self.assertEquals(resolve(url).func, ProcurementNewVendorApi)
        
#     def test_ProcurementNewVendorUserApi_url_resolved(self):
#         url = reverse('ProcurementNewVendorUserApi')
#         self.assertEquals(resolve(url).func, ProcurementNewVendorUserApi)
        
#     def test_ManagerDashboardView_url_resolved(self):
#         url = reverse('ManagerDashboardView')
#         self.assertEquals(resolve(url).func, ManagerDashboardView)
        
#     def test_ManagerStatusColumnChartApi_url_resolved(self):
#         url = reverse('ManagerStatusColumnChartApi')
#         self.assertEquals(resolve(url).func, ManagerStatusColumnChartApi)
        
#     def test_ManagerStatusPieChartApi_url_resolved(self):
#         url = reverse('ManagerStatusPieChartApi')
#         self.assertEquals(resolve(url).func, ManagerStatusPieChartApi)
        
#     def test_ManagerProjectView_url_resolved(self):
#         url = reverse('ManagerProjectView')
#         self.assertEquals(resolve(url).func, ManagerProjectView)
        
#     def test_ManagerRFQView_url_resolved(self):
#         url = reverse('ManagerRFQView')
#         self.assertEquals(resolve(url).func, ManagerRFQView)
        
#     def test_ManagerRFQTableApi_url_resolved(self):
#         url = reverse('ManagerRFQTableApi')
#         self.assertEquals(resolve(url).func, ManagerRFQTableApi)
        
#     def test_ManagerRFQDetailsApi_url_resolved(self):
#         url = reverse('ManagerRFQDetailsApi')
#         self.assertEquals(resolve(url).func, ManagerRFQDetailsApi)
        
#     def test_ManagerQuotationView_url_resolved(self):
#         url = reverse('ManagerQuotationView')
#         self.assertEquals(resolve(url).func, ManagerQuotationView)
        
#     def test_ManagerQuotationTableApi_url_resolved(self):
#         url = reverse('ManagerQuotationTableApi')
#         self.assertEquals(resolve(url).func, ManagerQuotationTableApi)
        
#     def test_ManagerQuotationDetailsApi_url_resolved(self):
#         url = reverse('ManagerQuotationDetailsApi')
#         self.assertEquals(resolve(url).func, ManagerQuotationDetailsApi)
        
#     def test_ManagerPOView_url_resolved(self):
#         url = reverse('ManagerPOView')
#         self.assertEquals(resolve(url).func, ManagerPOView)
        
#     def test_ManagerPOTableApi_url_resolved(self):
#         url = reverse('ManagerPOTableApi')
#         self.assertEquals(resolve(url).func, ManagerPOTableApi)
        
#     def test_ManagerPODetailsApi_url_resolved(self):
#         url = reverse('ManagerPODetailsApi')
#         self.assertEquals(resolve(url).func, ManagerPODetailsApi)
        
#     def test_ManagerInvoicesView_url_resolved(self):
#         url = reverse('ManagerInvoicesView')
#         self.assertEquals(resolve(url).func, ManagerInvoicesView)
        
#     def test_ManagerInvoicesTableApi_url_resolved(self):
#         url = reverse('ManagerInvoicesTableApi')
#         self.assertEquals(resolve(url).func, ManagerInvoicesTableApi)
        
#     def test_ManagerInvoicesDetailsApi_url_resolved(self):
#         url = reverse('ManagerInvoicesDetailsApi')
#         self.assertEquals(resolve(url).func, ManagerInvoicesDetailsApi)
        
#     def test_ManagerVendorView_url_resolved(self):
#         url = reverse('ManagerVendorView')
#         self.assertEquals(resolve(url).func, ManagerVendorView)
        
#     def test_ManagerConfigurationView_url_resolved(self):
#         url = reverse('ManagerConfigurationView')
#         self.assertEquals(resolve(url).func, ManagerConfigurationView)
        
#     def test_PresalesDashboardView_url_resolved(self):
#         url = reverse('PresalesDashboardView')
#         self.assertEquals(resolve(url).func, PresalesDashboardView)
        
#     def test_PresalesStatusColumnChartApi_url_resolved(self):
#         url = reverse('PresalesStatusColumnChartApi')
#         self.assertEquals(resolve(url).func, PresalesStatusColumnChartApi)
        
#     def test_PresalesStatusPieChartApi_url_resolved(self):
#         url = reverse('PresalesStatusPieChartApi')
#         self.assertEquals(resolve(url).func, PresalesStatusPieChartApi)
        
#     def test_PresalesNewProjectView_url_resolved(self):
#         url = reverse('PresalesNewProjectView')
#         self.assertEquals(resolve(url).func, PresalesNewProjectView)
        
#     def test_PresalesNewRFQView_url_resolved(self):
#         url = reverse('PresalesNewRFQView')
#         self.assertEquals(resolve(url).func, PresalesNewRFQView)
        
#     def test_PresalesNewRFQSubmitApi_url_resolved(self):
#         url = reverse('PresalesNewRFQSubmitApi')
#         self.assertEquals(resolve(url).func, PresalesNewRFQSubmitApi)
        
#     def test_PresalesCreatedRFQView_url_resolved(self):
#         url = reverse('PresalesCreatedRFQView')
#         self.assertEquals(resolve(url).func, PresalesCreatedRFQView)
        
#     def test_PresalesCreatedRFQTableApi_url_resolved(self):
#         url = reverse('PresalesCreatedRFQTableApi')
#         self.assertEquals(resolve(url).func, PresalesCreatedRFQTableApi)
        
#     def test_PresalesCreatedRFQDetailsApi_url_resolved(self):
#         url = reverse('PresalesCreatedRFQDetailsApi')
#         self.assertEquals(resolve(url).func, PresalesCreatedRFQDetailsApi)
        
#     def test_PresalesQuotationToDoView_url_resolved(self):
#         url = reverse('PresalesQuotationToDoView')
#         self.assertEquals(resolve(url).func, PresalesQuotationToDoView)
        
#     def test_PresalesQuotationToDoTableApi_url_resolved(self):
#         url = reverse('PresalesQuotationToDoTableApi')
#         self.assertEquals(resolve(url).func, PresalesQuotationToDoTableApi)
        
#     def test_PresalesQuotationToDoDetailsApi_url_resolved(self):
#         url = reverse('PresalesQuotationToDoDetailsApi')
#         self.assertEquals(resolve(url).func, PresalesQuotationToDoDetailsApi)
        
#     def test_PresalesQuotationToDoApproveApi_url_resolved(self):
#         url = reverse('PresalesQuotationToDoApproveApi')
#         self.assertEquals(resolve(url).func, PresalesQuotationToDoApproveApi)
        
#     def test_PresalesQuotationToDoRejectApi_url_resolved(self):
#         url = reverse('PresalesQuotationToDoRejectApi')
#         self.assertEquals(resolve(url).func, PresalesQuotationToDoRejectApi)
        
#     def test_PresalesQuotationDoneView_url_resolved(self):
#         url = reverse('PresalesQuotationDoneView')
#         self.assertEquals(resolve(url).func, PresalesQuotationDoneView)
        
#     def test_PresalesQuotationDoneTableApi_url_resolved(self):
#         url = reverse('PresalesQuotationDoneTableApi')
#         self.assertEquals(resolve(url).func, PresalesQuotationDoneTableApi)
        
#     def test_PresalesQuotationDoneDetailsApi_url_resolved(self):
#         url = reverse('PresalesQuotationDoneDetailsApi')
#         self.assertEquals(resolve(url).func, PresalesQuotationDoneDetailsApi)
        
#     def test_PresalesConfigurationView_url_resolved(self):
#         url = reverse('PresalesConfigurationView')
#         self.assertEquals(resolve(url).func, PresalesConfigurationView)
        
#     def test_UserChangePassword_url_resolved(self):
#         url = reverse('UserChangePassword')
#         self.assertEquals(resolve(url).func, UserChangePassword)
        