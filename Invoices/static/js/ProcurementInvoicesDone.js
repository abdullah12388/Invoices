$(function () {
    filters = {
        'vendor': '',
        'number': '',
        'date': '',
        'po': '',
        'due': '',
        'bill_to': '',
        'project_name': '',
        'type': '',
        'milestone': '',
        'item': '',
        'vat': '',
        'currency': '',
        'user': '',
        'status': '',
        'timestamp_from': '',
        'timestamp_to': '',
    }
    document.getElementById("vendor").addEventListener("change", function () {
        // console.log(this.value);
        filters.vendor = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("number").addEventListener("change", function () {
        // console.log(this.value);
        filters.number = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("date").addEventListener("change", function () {
        // console.log(this.value);
        filters.date = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("po").addEventListener("change", function () {
        // console.log(this.value);
        filters.po = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("due").addEventListener("change", function () {
        // console.log(this.value);
        filters.due = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("bill_to").addEventListener("change", function () {
        // console.log(this.value);
        filters.bill_to = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("project_name").addEventListener("change", function () {
        // console.log(this.value);
        filters.project_name = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("type").addEventListener("change", function () {
        // console.log(this.value);
        filters.type = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("milestone").addEventListener("change", function () {
        // console.log(this.value);
        filters.milestone = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("item").addEventListener("change", function () {
        // console.log(this.value);
        filters.item = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("vat").addEventListener("change", function () {
        // console.log(this.value);
        filters.vat = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("currency").addEventListener("change", function () {
        // console.log(this.value);
        filters.currency = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("user").addEventListener("change", function () {
        // console.log(this.value);
        filters.user = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("status").addEventListener("change", function () {
        // console.log(this.value);
        filters.status = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("timestamp_from").addEventListener("change", function () {
        // console.log(this.value);
        filters.timestamp_from = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("timestamp_to").addEventListener("change", function () {
        // console.log(this.value);
        filters.timestamp_to = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("sbmtBTN").addEventListener("click", function () {
        document.getElementById('miniloader').classList.remove('d-none');
        document.getElementById('collapse_done_filters').classList.remove('show');
        $.ajax({
            url: "/system/Invoices/ProcurementDone/table/api/",
            method: "GET",
            dataType: "json",
            data: {
                'vendor': filters.vendor,
                'number': filters.number,
                'date': filters.date,
                'po': filters.po,
                'due': filters.due,
                'bill_to': filters.bill_to,
                'project_name': filters.project_name,
                'type': filters.type,
                'milestone': filters.milestone,
                'item': filters.item,
                'vat': filters.vat,
                'currency': filters.currency,
                'user': filters.user,
                'status': filters.status,
                'timestamp_from': filters.timestamp_from,
                'timestamp_to': filters.timestamp_to,
            },
            success: function (t) {
                console.log(t);
                t.forEach((element) => {
                    // console.log(element);
                    element['actions'] = `<button class="btn btn-secondary text-white" style="margin:5px auto;width:100%;" type="button" onclick="ViewInvoiceModal('${element.id}')"><i class="fa-solid fa-eye"></i> Details</button>`;
                });
                updateTableData(t);
            },
        });
    });
    document.getElementById("vendorBTN").addEventListener("click", function () {
        filters.vendor = '';
        $('#vendor').selectpicker('val', "");
    });
    document.getElementById("numberBTN").addEventListener("click", function () {
        filters.number = '';
        $('#number').selectpicker('val', "");
    });
    document.getElementById("dateBTN").addEventListener("click", function () {
        filters.date = '';
        document.getElementById('date').value = '';
    });
    document.getElementById("poBTN").addEventListener("click", function () {
        filters.po = '';
        $('#po').selectpicker('val', "");
    });
    document.getElementById("dueBTN").addEventListener("click", function () {
        filters.due = '';
        $('#due').selectpicker('val', "");
    });
    document.getElementById("billToBTN").addEventListener("click", function () {
        filters.bill_to = '';
        $('#bill_to').selectpicker('val', "");
    });
    document.getElementById("projectNameBTN").addEventListener("click", function () {
        filters.project_name = '';
        $('#project_name').selectpicker('val', "");
    });
    document.getElementById("typeBTN").addEventListener("click", function () {
        filters.type = '';
        $('#type').selectpicker('val', "");
    });
    document.getElementById("milestoneBTN").addEventListener("click", function () {
        filters.milestone = '';
        $('#milestone').selectpicker('val', "");
    });
    document.getElementById("itemBTN").addEventListener("click", function () {
        filters.item = '';
        $('#item').selectpicker('val', "");
    });
    document.getElementById("vatBTN").addEventListener("click", function () {
        filters.vat = '';
        $('#vat').selectpicker('val', "");
    });
    document.getElementById("currencyBTN").addEventListener("click", function () {
        filters.currency = '';
        $('#currency').selectpicker('val', "");
    });
    document.getElementById("userBTN").addEventListener("click", function () {
        filters.user = '';
        $('#user').selectpicker('val', "");
    });
    document.getElementById("statusBTN").addEventListener("click", function () {
        filters.status = '';
        $('#status').selectpicker('val', "");
    });
    document.getElementById("timestampBTN").addEventListener("click", function () {
        filters.timestamp_from = '';
        filters.timestamp_to = '';
        document.getElementById("timestamp_from").value = "";
        document.getElementById("timestamp_to").value = "";
    });
    document.getElementById("rstBTN").addEventListener("click", function () {
        filters = {
            'vendor': '',
            'number': '',
            'date': '',
            'po': '',
            'due': '',
            'bill_to': '',
            'project_name': '',
            'type': '',
            'milestone': '',
            'item': '',
            'vat': '',
            'currency': '',
            'user': '',
            'status': '',
            'timestamp_from': '',
            'timestamp_to': '',
        }
        document.getElementById('sbmtBTN').setAttribute('disabled', 'disabled');
        $('.selectpicker').selectpicker('val', "");
        document.getElementById("date").value = "";
        document.getElementById("timestamp_from").value = "";
        document.getElementById("timestamp_to").value = "";

        var e = $("#doneInvoicesTbl");
        e.bootstrapTable("showLoading");
        e.bootstrapTable("load", []);
        e.bootstrapTable("refresh");
        e.bootstrapTable("hideLoading");
        document.getElementById('card-table').classList.add('d-none');
        document.getElementById('collapse_done_filters').classList.add('show');
    });
});

function updateTableData(filteredData) {
    var e = $("#doneInvoicesTbl");
    e.bootstrapTable("showLoading");
    e.bootstrapTable("load", []);
    e.bootstrapTable("load", filteredData);
    e.bootstrapTable("refresh");
    e.bootstrapTable("hideLoading");
    document.getElementById('miniloader').classList.add('d-none');
    document.getElementById('card-table').classList.remove('d-none');
    // console.log(e.bootstrapTable('getRowByUniqueId', 3645));
}


function ViewInvoiceModal(rowid) {
    var e = $("#doneInvoicesTbl");
    e.bootstrapTable("showLoading");
    // rowData = e.bootstrapTable('getRowByUniqueId', rowid);
    $.ajax({
        url: "/system/Invoices/ProcurementDone/details/api/",
        method: "GET",
        dataType: "json",
        data: {
            'id': rowid,
        },
        success: function (t) {
            // console.log(t);
            document.getElementById('view_invoice_id').innerHTML=t.invoice_id;
            document.getElementById('view_vendor').innerHTML=t.vendor;
            document.getElementById('view_number').innerHTML=t.number;
            document.getElementById('view_date').innerHTML=t.date;
            document.getElementById('view_bill_to').innerHTML=t.bill_to;
            document.getElementById('view_po').innerHTML=t.po;
            document.getElementById('view_due').innerHTML=t.payment_due;
            document.getElementById('view_project_name').innerHTML=t.project_name;
            document.getElementById('view_type').innerHTML=t.type;
            document.getElementById('view_milestone').innerHTML=t.milestone;
            document.getElementById('view_milestone_description').innerHTML=t.milestone_description;
            document.getElementById('total_items').innerHTML=t.items_count;
            document.getElementById('total_amount').innerHTML=t.items_total_amount;
            var iit = $("#InvoiceItemsTbl");
            iit.bootstrapTable("showLoading");
            iit.bootstrapTable("load", []);
            iit.bootstrapTable("load", t.items);
            iit.bootstrapTable("refresh");
            iit.bootstrapTable("hideLoading");
            document.getElementById('ta_view_invoice_currency').innerHTML=t.currency;
            document.getElementById('vat_view_invoice_currency').innerHTML=t.currency;
            document.getElementById('t_view_invoice_currency').innerHTML=t.currency;
            document.getElementById('view_total_amount').innerHTML=t.items_total_amount;
            document.getElementById('view_invoice_vat').innerHTML=t.vat;
            document.getElementById('view_vat_amount').innerHTML=t.vat_amount;
            document.getElementById('view_invoice_total').innerHTML=t.invoice_total;
            document.getElementById('total_files').innerHTML=t.invoice_attachments_count;
            var files_list = ``;
            t.invoice_attachments.forEach((element)=>{
                files_list +=`
                <div class="row mb-2" style="border-left: 1px solid #6c757d;">
                    <div class="col-1 d-flex justify-content-start align-items-center">
                        <h5 class="mb-0">${element[3]}</h5>
                    </div>
                    <div class="col-7 d-flex justify-content-start align-items-center">
                        <h5 class="mb-0">${element[0]}</h5>
                    </div>
                    <div class="col-2 text-center">
                        <a href="${element[1]}" target="_blank" class="btn btn-secondary text-white" style="text-decoration: none;scale: 0.8;">
                            <i class="fa-solid fa-eye"></i> View
                        </a>
                    </div>
                    <div class="col-2 text-center">
                        <a href="${element[1]}" download="${element[0]}" class="btn btn-success text-white" style="text-decoration: none;scale: 0.8;">
                            <i class="fa-solid fa-download"></i> Download
                        </a>
                    </div>
                </div>
                `;
            })
            document.getElementById('files_parent').innerHTML = files_list;
            document.getElementById('view_submitted_by').innerHTML=(t.user).toUpperCase();
            document.getElementById('view_submitted_timestamp').innerHTML=t.submitted_timestamp;

            if(t.status == 'p'){
                document.getElementById('action_border').classList.add('d-none');
                document.getElementById('action_by').classList.add('d-none');
                document.getElementById('action_at').classList.add('d-none');
                document.getElementById('action_feedback').classList.add('d-none');
            }
            if(t.status == 'a'){
                document.getElementById('action_border').classList.remove('d-none');
                document.getElementById('action_by').classList.remove('d-none');
                document.getElementById('action_at').classList.remove('d-none');
                document.getElementById('action_feedback').classList.remove('d-none');
                document.getElementById('action_type_by').innerHTML='Approved By';
                document.getElementById('view_action_by').innerHTML=(t.approved_user).toUpperCase();
                document.getElementById('action_type_at').innerHTML='Approved At';
                document.getElementById('view_action_timestamp').innerHTML=t.approved_timeStamp;
                document.getElementById('view_action_feedback').innerHTML=t.approved_feedback;
            }
            if(t.status == 'r'){
                document.getElementById('action_border').classList.remove('d-none');
                document.getElementById('action_by').classList.remove('d-none');
                document.getElementById('action_at').classList.remove('d-none');
                document.getElementById('action_feedback').classList.remove('d-none');
                document.getElementById('action_type_by').innerHTML='Rejected By';
                document.getElementById('view_action_by').innerHTML=(t.rejected_user).toUpperCase();
                document.getElementById('action_type_at').innerHTML='Rejected At';
                document.getElementById('view_action_timestamp').innerHTML=t.rejected_timeStamp;
                document.getElementById('view_action_feedback').innerHTML=t.rejected_feedback;
            }

            document.getElementById('print_status').value = t.status;

            $('#view_action_modal').modal({
                backdrop: true,
                keyboard: true,
                focus: true,
                show: true,
            });
            e.bootstrapTable("hideLoading");
        },
    });
}


var o = $("#doneInvoicesTbl");
$("#toolbar")
    .find("select")
    .change(function () {
        var filename = document.getElementById('exportFileName').value;
        var currentDate = new Date();
        var temp_table = o.bootstrapTable().bootstrapTable('getData');
        o.bootstrapTable("destroy").bootstrapTable({
            exportDataType: $(this).val(),
            exportOptions: {
                fileName: (filename ? filename + '_' : 'GTS_') + currentDate.toLocaleString(),
            },
            exportTypes: ["json", "xml", "csv", "txt", "sql", "excel", "pdf"],
            columns: [
                { field: "state", checkbox: !0, visible: "selected" === $(this).val() },
                { field: "id", title: "ID" },
                { field: "vendor", title: "Vendor" },
                { field: "date", title: "Invoice Date" },
                { field: "po", title: "P.O. No." },
                { field: "bill_to", title: "Bill To" },
                { field: "user", title: "Submitted By" },
                { field: "timestamp", title: "Timestamp" },
                { field: "status", title: "Status" },
                { field: "actions", title: "Actions" },
                // { field: "area_manager_status", title: "Status" },
            ],
        });
        o.bootstrapTable("showLoading");
        o.bootstrapTable("load", temp_table);
        o.bootstrapTable("refresh");
        o.bootstrapTable("hideLoading");
    })

document.getElementById("print_selected").addEventListener("click", function () {
    var selectedRows = [];
    selectedRows = $("#doneInvoicesTbl").bootstrapTable("getSelections");
    // console.log(selectedRows);
    var printWindow = window.open("", "_blank");
    var currentDate = new Date();
    printWindow.document.open();
    printWindow.document.write(
        "<html><head><title>Done Invoices Table</title>" +
        "<style>" +
        "table { border-collapse: collapse;width: 100%; }" +
        "th, td { border: 1px solid black;text-align: center; }" +
        "</style>" +
        "</head><body>"
    );
    //        printWindow.document.write("<html><head><title>Alarms Table</title></head><body>");
    printWindow.document.write("<h2>Printed on: " + currentDate.toString() + "</h2>");
    printWindow.document.write("<table>");
    // Get the column names from the table header
    var columnNames = [];
    $("#doneInvoicesTbl thead th").each(function () {
        columnNames.push($(this).data("field"));
    });

    // Print the table header with column names
    printWindow.document.write("<tr>");
    for (var j = 1; j < columnNames.length - 1; j++) {
        printWindow.document.write("<th>" + columnNames[j] + "</th>");
    }
    printWindow.document.write("</tr>");

    // Iterate over selected rows
    for (var i = 0; i < selectedRows.length; i++) {
        var row = selectedRows[i];
        printWindow.document.write("<tr>");
        for (var j = 1; j < columnNames.length - 1; j++) {
            var columnName = columnNames[j];
            printWindow.document.write("<td>" + row[columnName] + "</td>");
        }
        printWindow.document.write("</tr>");
    }
    printWindow.document.write("</table></body></html>");
    printWindow.document.close();
    printWindow.print();
})


var x = $("#InvoiceItemsTbl");
$("#items_toolbar")
    .find("select")
    .change(function () {
        var filename = document.getElementById('items_exportFileName').value;
        var currentDate = new Date();
        var temp_table = x.bootstrapTable().bootstrapTable('getData');
        x.bootstrapTable("destroy").bootstrapTable({
            exportDataType: $(this).val(),
            exportOptions: {
                fileName: (filename ? filename + '_' : 'GTS_') + currentDate.toLocaleString(),
            },
            exportTypes: ["json", "xml", "csv", "txt", "sql", "excel", "pdf"],
            columns: [
                { field: "state", checkbox: !0, visible: "selected" === $(this).val() },
                { field: "number", title: "Number" },
                { field: "description", title: "Description" },
                { field: "quantity", title: "Quantity" },
                { field: "uom", title: "UOM" },
                { field: "unit_price", title: "Unit Price" },
                { field: "amount", title: "Amount" },
                // { field: "area_manager_status", title: "Status" },
            ],
        });
        x.bootstrapTable("showLoading");
        x.bootstrapTable("load", temp_table);
        x.bootstrapTable("refresh");
        x.bootstrapTable("hideLoading");
    })

document.getElementById("items_print_selected").addEventListener("click", function () {
    var selectedRows = [];
    selectedRows = $("#InvoiceItemsTbl").bootstrapTable("getSelections");
    // console.log(selectedRows);
    var printWindow = window.open("", "_blank");
    var currentDate = new Date();
    printWindow.document.open();
    printWindow.document.write(
        "<html><head><title>Invoice Items Table</title>" +
        "<style>" +
        "table { border-collapse: collapse;width: 100%; }" +
        "th, td { border: 1px solid black;text-align: center; }" +
        "</style>" +
        "</head><body>"
    );
    //        printWindow.document.write("<html><head><title>Alarms Table</title></head><body>");
    printWindow.document.write("<h2>Printed on: " + currentDate.toString() + "</h2>");
    printWindow.document.write("<table>");
    // Get the column names from the table header
    var columnNames = [];
    $("#InvoiceItemsTbl thead th").each(function () {
        columnNames.push($(this).data("field"));
    });

    // Print the table header with column names
    printWindow.document.write("<tr>");
    for (var j = 1; j < columnNames.length; j++) {
        printWindow.document.write("<th>" + columnNames[j] + "</th>");
    }
    printWindow.document.write("</tr>");

    // Iterate over selected rows
    for (var i = 0; i < selectedRows.length; i++) {
        var row = selectedRows[i];
        printWindow.document.write("<tr>");
        for (var j = 1; j < columnNames.length; j++) {
            var columnName = columnNames[j];
            printWindow.document.write("<td>" + row[columnName] + "</td>");
        }
        printWindow.document.write("</tr>");
    }
    printWindow.document.write("</table></body></html>");
    printWindow.document.close();
    printWindow.print();
})


function printInvoice() {
    var view_invoice_id = document.getElementById('view_invoice_id').innerHTML;
    var view_vendor = document.getElementById('view_vendor').innerHTML;
    var view_number = document.getElementById('view_number').innerHTML;
    var view_date = document.getElementById('view_date').innerHTML;
    var view_bill_to = document.getElementById('view_bill_to').innerHTML;
    var view_po = document.getElementById('view_po').innerHTML;
    var view_due = document.getElementById('view_due').innerHTML;
    var view_project_name = document.getElementById('view_project_name').innerHTML;
    var view_type = document.getElementById('view_type').innerHTML;
    var view_milestone = document.getElementById('view_milestone').innerHTML;
    var view_milestone_description = document.getElementById('view_milestone_description').innerHTML;
    var total_items = document.getElementById('total_items').innerHTML;
    var total_amount = document.getElementById('total_amount').innerHTML;

    var iit = $("#InvoiceItemsTbl");
    var temp_table = iit.bootstrapTable().bootstrapTable('getData');
    items_table_data = ``;
    temp_table.forEach((row)=>{
        items_table_data += `
        <tr>
            <td>${row.number}</td>
            <td>${row.description}</td>
            <td>${row.quantity}</td>
            <td>${row.uom}</td>
            <td>${row.unit_price}</td>
            <td>${row.amount}</td>
        </tr>
        `;
    });
    var ta_view_invoice_currency = document.getElementById('ta_view_invoice_currency').innerHTML;
    var vat_view_invoice_currency = document.getElementById('vat_view_invoice_currency').innerHTML;
    var t_view_invoice_currency = document.getElementById('t_view_invoice_currency').innerHTML;
    var view_total_amount = document.getElementById('view_total_amount').innerHTML;
    var view_invoice_vat = document.getElementById('view_invoice_vat').innerHTML;
    var view_vat_amount = document.getElementById('view_vat_amount').innerHTML;
    var view_invoice_total = document.getElementById('view_invoice_total').innerHTML;
    var total_files = document.getElementById('total_files').innerHTML;
    var files_list = document.getElementById('files_parent').children;
    var files_data = ``;
    for(var i=0;i<files_list.length;i++){
        files_data += `
        <div class="row mb-2" style="border-left: 1px solid #6c757d;">
            <div class="col-2 d-flex justify-content-start align-items-center">
                <h5 class="mb-0">${files_list[i].children[0].children[0].innerHTML}</h5>
            </div>
            <div class="col-10 d-flex justify-content-center align-items-center">
                <h5 class="mb-0">${files_list[i].children[1].children[0].innerHTML}</h5>
            </div>
        </div>
        `;
    }
    var view_submitted_by = document.getElementById('view_submitted_by').innerHTML;
    var view_submitted_timestamp = document.getElementById('view_submitted_timestamp').innerHTML;

    var status = document.getElementById('print_status').value;
    var action_data = ``;
    if (status == 'p') {
        action_data += `
        <hr class="d-none" id="action_border" />
        <div class="row mb-4 d-none" id="action_by">
            <div class="col-5">
                <h5 class="mb-0" id="action_type_by"></h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0" id="view_action_by"></h5>
            </div>
        </div>
        <div class="row mb-4 d-none" id="action_at">
            <div class="col-5">
                <h5 class="mb-0" id="action_type_at"></h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0" id="view_action_timestamp"></h5>
            </div>
        </div>
        <div class="row mb-4 d-none" id="action_feedback">
            <div class="col-5">
                <h5 class="mb-0">Feedback</h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0" id="view_action_feedback"></h5>
            </div>
        </div>
        `;
    }
    if (status == 'a') {
        var action_type_by = document.getElementById('action_type_by').innerHTML;
        var view_action_by = document.getElementById('view_action_by').innerHTML;
        var action_type_at = document.getElementById('action_type_at').innerHTML;
        var view_action_timestamp = document.getElementById('view_action_timestamp').innerHTML;
        var view_action_feedback = document.getElementById('view_action_feedback').innerHTML;
        action_data += `
        <hr />
        <div class="row mb-4">
            <div class="col-5">
                <h5 class="mb-0">${action_type_by}</h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0">${view_action_by}</h5>
            </div>
        </div>
        <div class="row mb-4">
            <div class="col-5">
                <h5 class="mb-0">${action_type_at}</h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0">${view_action_timestamp}</h5>
            </div>
        </div>
        <div class="row mb-4">
            <div class="col-5">
                <h5 class="mb-0">Feedback</h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0">${view_action_feedback}</h5>
            </div>
        </div>
        `;
    }
    if (status == 'r') {
        var action_type_by = document.getElementById('action_type_by').innerHTML;
        var view_action_by = document.getElementById('view_action_by').innerHTML;
        var action_type_at = document.getElementById('action_type_at').innerHTML;
        var view_action_timestamp = document.getElementById('view_action_timestamp').innerHTML;
        var view_action_feedback = document.getElementById('view_action_feedback').innerHTML;
        action_data += `
        <hr />
        <div class="row mb-4">
            <div class="col-5">
                <h5 class="mb-0">${action_type_by}</h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0">${view_action_by}</h5>
            </div>
        </div>
        <div class="row mb-4">
            <div class="col-5">
                <h5 class="mb-0">${action_type_at}</h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0">${view_action_timestamp}</h5>
            </div>
        </div>
        <div class="row mb-4">
            <div class="col-5">
                <h5 class="mb-0">Feedback</h5>
            </div>
            <div class="col-7">
                <h5 class="mb-0">${view_action_feedback}</h5>
            </div>
        </div>
        `;
    }

    var printWindow = window.open("", "_blank");
    printWindow.document.write(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="gts" />
        <meta name="author" content="Abdullah kamal" />
        <title>Dashboard | Invoices</title>
        <link rel="icon" type="image/ico" href="/static/img/favicon.ico" />
        <link href="/static/css/bootstrap/bootstrap.min.css" rel="stylesheet" />
        <link href="/static/css/bootstrap/bootstrap-select.min.css" rel="stylesheet" />
        <link href="/static/css/bootstrap-table/bootstrap-table.min.css" rel="stylesheet" />
        <link href="/static/css/styles.css" rel="stylesheet" />
        <link href="/static/css/loader.css" rel="stylesheet" />
        <link href="/static/css/responsive.css" rel="stylesheet" />
        <link href="/static/fontawesomefree/css/all.min.css" rel="stylesheet" type="text/css">
    </head>
    <body class="sb-nav-fixed">
        <div class="container">
            <div class="row mt-2 mb-4">
                <div class="col-6">
                    <img src="/static/img/gts-logo.png" width="200" alt="Footer Logo">
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <div class="row">
                        <div class="col-4 text-center">
                            <h5 class="modal-title" style="border-radius: 5px;">ID
                                <span>${view_invoice_id}</span>
                            </h5>
                        </div>
                        <div class="col-8 text-center">
                            <h5 class="modal-title">Invoice Details</h5>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-5">
                            <div class="row">
                                <div class="col-5">
                                    <h5>Vendor</h5>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12 text-center">
                                    <h1>${view_vendor}</h1>
                                </div>
                            </div>
                        </div>
                        <div class="col-7">
                            <div class="row">
                                <div class="col-6">
                                    <h5 style="border-right: 2px solid #212529;">Invoice Number</h5>
                                </div>
                                <div class="col-6">
                                    <h5>${view_number}</h5>
                                </div>
                            </div>
                            <div class="row mt-2">
                                <div class="col-6">
                                    <h5 style="border-right: 2px solid #212529;">Invoice Date</h5>
                                </div>
                                <div class="col-6">
                                    <h5>${view_date}</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-4">
                        <div class="col-5">
                            <div class="row">
                                <div class="col-5">
                                    <h5>Bill To</h5>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12 text-center">
                                    <h5>${view_bill_to}</h5>
                                </div>
                            </div>
                        </div>
                        <div class="col-7">
                            <div class="row">
                                <div class="col-6">
                                    <h5 style="border-right: 2px solid #212529;">P.O. No.</h5>
                                </div>
                                <div class="col-6">
                                    <h5>${view_po}</h5>
                                </div>
                            </div>
                            <div class="row mt-2">
                                <div class="col-6">
                                    <h5 style="border-right: 2px solid #212529;">Payment Due</h5>
                                </div>
                                <div class="col-6">
                                    <h5><span>${view_due}</span> Days</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-4">
                        <div class="col-5">
                            <div class="row">
                                <div class="col-5">
                                    <h5>Project</h5>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12 text-center">
                                    <h5>${view_project_name}</h5>
                                </div>
                            </div>
                        </div>
                        <div class="col-7">
                            <div class="row">
                                <div class="col-6">
                                    <h5 style="border-right: 2px solid #212529;">Invoice Type</h5>
                                </div>
                                <div class="col-6">
                                    <h5>${view_type}</h5>
                                </div>
                            </div>
                            <div class="row mt-2">
                                <div class="col-6">
                                    <h5 style="border-right: 2px solid #212529;">Milestone</h5>
                                </div>
                                <div class="col-6">
                                    <h5><span>${view_milestone}</span> %</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-4">
                        <div class="col-5 d-flex justify-content-start align-items-center">
                            <h5 style="border-right: 2px solid #212529;width: 100%;">Milestone Description</h5>
                        </div>
                        <div class="col-7">
                            <h5>${view_milestone_description}</h5>
                        </div>
                    </div>
                    <div class="row mb-4">
                        <div class="col-12">
                            <div class="panel panel-default">
                                <div class="panel-heading text-left"
                                    style="padding: 10px 15px;border-radius: 5px;"
                                    role="tab" id="items_table">
                                    <h4 class="panel-title m-0">
                                        <div class="row">
                                            <div class="col-7">
                                                <a role="button" data-toggle="collapse"
                                                    style="text-decoration: none;color: #000;"
                                                    href="#collapse_items_table" aria-expanded="false"
                                                    aria-controls="collapse_items_table">
                                                    <i class="fa-solid fa-table me-1"></i>
                                                    Invoice Items Table
                                                </a>
                                            </div>
                                            <div class="col-5 text-right">
                                                <div class="row">
                                                    <div
                                                        class="col-4 d-flex justify-content-center align-items-center">
                                                        <h5 class="mb-0 mr-2 pr-2"
                                                            style="border-right: 2px solid #000;">Items</h5>
                                                        <h5 class="mb-0">${total_items}</h5>
                                                    </div>
                                                    <div
                                                        class="col-8 d-flex justify-content-center align-items-center">
                                                        <h5 class="mb-0 mr-2 pr-2"
                                                            style="border-right: 2px solid #000;">Total</h5>
                                                        <h5 class="mb-0">${total_amount}</h5>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </h4>
                                </div>
                                <div id="collapse_items_table" class="panel-collapse collapse in show"
                                    role="tabpanel" aria-labelledby="items_table">
                                    <div class="panel-body">
                                        <div class="card">
                                            <div class="card-body table-striped table-sm">
                                                <table class="table">
                                                    <thead>
                                                        <tr>
                                                            <th>Number</th>
                                                            <th>Description</th>
                                                            <th>Quantity</th>
                                                            <th>UOM</th>
                                                            <th>Unit Price</th>
                                                            <th>Amount</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                    ${items_table_data}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-4 d-flex justify-content-end align-items-center">
                        <div class="col-7">
                            <div class="card-body"
                                style="padding: 20px;border-radius: 5px;">
                                <div class="row">
                                    <div class="col-5">
                                        <h5>Total Amount</h5>
                                    </div>
                                    <div class="col-3 text-center">
                                        <h5>( <span>${ta_view_invoice_currency}</span> )</h5>
                                    </div>
                                    <div class="col-4 text-right">
                                        <h5>${view_total_amount}</h5>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-5">
                                        <h5>VAT ( <span>${view_invoice_vat}</span> % )</h5>
                                    </div>
                                    <div class="col-3 text-center">
                                        <h5>( <span>${vat_view_invoice_currency}</span> )</h5>
                                    </div>
                                    <div class="col-4 text-right">
                                        <h5>${view_vat_amount}</h5>
                                    </div>
                                </div>
                                <hr />
                                <div class="row">
                                    <div class="col-5">
                                        <h5>Total</h5>
                                    </div>
                                    <div class="col-3 text-center">
                                        <h5>( <span>${t_view_invoice_currency}</span> )</h5>
                                    </div>
                                    <div class="col-4 text-right">
                                        <h5>${view_invoice_total}</h5>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-4">
                        <div class="col-12">
                            <div class="panel panel-default">
                                <div class="panel-heading text-left"
                                    style="padding: 10px 15px;border-radius: 5px;"
                                    role="tab" id="invoice_files">
                                    <h4 class="panel-title m-0">
                                        <div class="row">
                                            <div class="col-9">
                                                <a role="button" data-toggle="collapse"
                                                    style="text-decoration: none;color: #000;"
                                                    href="#collapse_invoice_files" aria-expanded="false"
                                                    aria-controls="collapse_invoice_files">
                                                    <i class="fa-solid fa-file-pdf me-1"></i>
                                                    Invoice Attachments
                                                </a>
                                            </div>
                                            <div class="col-3 text-right">
                                                <div class="row">
                                                    <div
                                                        class="col-12 d-flex justify-content-center align-items-center">
                                                        <h5 class="mb-0 mr-2 pr-2"
                                                            style="border-right: 2px solid #000;">Files</h5>
                                                        <h5 class="mb-0">${total_files}</h5>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </h4>
                                </div>
                                <div id="collapse_invoice_files" class="panel-collapse collapse in show"
                                    role="tabpanel" aria-labelledby="invoice_files">
                                    <div class="panel-body">
                                        <div class="card">
                                            <div class="card-body">
                                            ${files_data}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-4">
                        <div class="col-5">
                            <h5 class="mb-0">Submitted By</h5>
                        </div>
                        <div class="col-7">
                            <h5 class="mb-0">${view_submitted_by}</h5>
                        </div>
                    </div>
                    <div class="row mb-4">
                        <div class="col-5">
                            <h5 class="mb-0">Submitted At</h5>
                        </div>
                        <div class="col-7">
                            <h5 class="mb-0">${view_submitted_timestamp}</h5>
                        </div>
                    </div>
                    ${action_data}
                </div>
            </div>
        </div>
        <script type="text/javascript" src="/static/js/jquery.min.js"></script>
        <script type="text/javascript" src="/static/js/bootstrap/bootstrap.bundle.min.js"></script>
        <script type="text/javascript" src="/static/js/VendorInvoicesDone.js"></script>
    </body>
    </html>
    `);
    setTimeout(function(){
        printWindow.document.close();
        printWindow.print();
    }, 100);
}