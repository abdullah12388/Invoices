let pond;

document.addEventListener('DOMContentLoaded', () => {
    // Get a reference to the file input element
    const inputElement = document.querySelector('.my-pond');
    FilePond.registerPlugin(
        FilePondPluginFileEncode,
        FilePondPluginImagePreview,
        FilePondPluginImageExifOrientation,
        FilePondPluginFileValidateSize,
    );

    // Create a FilePond instance
    pond = FilePond.create(inputElement, {
        acceptedFileTypes: ['application/pdf'],
        // allowMultiple: true,
        imagePreviewHeight: 200,
        instantUpload: false,
        maxFileSize: '5MB', // Set the maximum file size to 5 MB
        onaddfile: (error, file) => {
            if (error) {
                console.log('FilePond error:', error);
            } else {
                console.log('File added:', file.file);
            }
        }
    });
});

// verify invoice button
function getFileExtension(fileName) {
    return fileName.slice((fileName.lastIndexOf(".") - 1 >>> 0) + 2);
}

$(function () {
    filters = {
        'RFQ_ID': '',
        'project': '',
        'Bidder_ID': '',
        'RFQ_Type': '',
        'eqc': '',
        'qrfai': '',
        'bccsq': '',
        'bcai': '',
        'bccq': '',
        'Product_ID': '',
        'sd_from': '',
        'sd_to': '',
        'qmbvu_from': '',
        'qmbvu_to': '',
    }
    document.getElementById("RFQ_ID").addEventListener("change", function () {
        // console.log(this.value);
        filters.RFQ_ID = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("project").addEventListener("change", function () {
        // console.log(this.value);
        filters.project = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("Bidder_ID").addEventListener("change", function () {
        // console.log(this.value);
        filters.Bidder_ID = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("RFQ_Type").addEventListener("change", function () {
        // console.log(this.value);
        filters.RFQ_Type = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("eqc").addEventListener("change", function () {
        // console.log(this.value);
        filters.eqc = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("qrfai").addEventListener("change", function () {
        // console.log(this.value);
        filters.qrfai = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("bccsq").addEventListener("change", function () {
        // console.log(this.value);
        filters.bccsq = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("bcai").addEventListener("change", function () {
        // console.log(this.value);
        filters.bcai = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("bccq").addEventListener("change", function () {
        // console.log(this.value);
        filters.bccq = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("Product_ID").addEventListener("change", function () {
        // console.log(this.value);
        filters.Product_ID = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("sd_from").addEventListener("change", function () {
        // console.log(this.value);
        filters.sd_from = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("sd_to").addEventListener("change", function () {
        // console.log(this.value);
        filters.sd_to = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("qmbvu_from").addEventListener("change", function () {
        // console.log(this.value);
        filters.qmbvu_from = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("qmbvu_to").addEventListener("change", function () {
        // console.log(this.value);
        filters.qmbvu_to = this.value;
        document.getElementById('sbmtBTN').removeAttribute('disabled');
    });
    document.getElementById("sbmtBTN").addEventListener("click", function () {
        document.getElementById('miniloader').classList.remove('d-none');
        document.getElementById('collapse_pending_filters').classList.remove('show');
        $.ajax({
            url: "/system/VendorRFQDone/table/api/",
            method: "GET",
            dataType: "json",
            data: {
                'RFQ_ID': filters.RFQ_ID,
                'project': filters.project,
                'Bidder_ID': filters.Bidder_ID,
                'RFQ_Type': filters.RFQ_Type,
                'eqc': filters.eqc,
                'qrfai': filters.qrfai,
                'bccsq': filters.bccsq,
                'bcai': filters.bcai,
                'bccq': filters.bccq,
                'Product_ID': filters.Product_ID,
                'sd_from': filters.sd_from,
                'sd_to': filters.sd_to,
                'qmbvu_from': filters.qmbvu_from,
                'qmbvu_to': filters.qmbvu_to,
            },
            success: function (t) {
                // console.log(t);
                t.forEach((element) => {
                    // console.log(element);
                    element['actions'] = `<button class="btn btn-secondary text-white" style="margin:5px auto;width:100%;" type="button" onclick="ViewRFQModal('${element.RFQ_ID}')"><i class="fa-solid fa-eye me-2"></i> Details</button>
                    <button class="btn btn-success" style="margin:5px auto;width:100%;" type="button" onclick="ViewCreateQuoteModal('${element.RFQ_ID}')"><i class="fa-solid fa-pen me-2"></i> Quote</button>`;
                });
                updateTableData(t);
            },
        });
    });
    document.getElementById("RFQIDBTN").addEventListener("click", function () {
        filters.RFQ_ID = '';
        $('#RFQ_ID').selectpicker('val', "");
    });
    document.getElementById("projectBTN").addEventListener("click", function () {
        filters.project = '';
        $('#project').selectpicker('val', "");
    });
    document.getElementById("BidderIDBTN").addEventListener("click", function () {
        filters.Bidder_ID = '';
        $('#Bidder_ID').selectpicker('val', "");
    });
    document.getElementById("RFQTypeBTN").addEventListener("click", function () {
        filters.RFQ_Type = '';
        $('#RFQ_Type').selectpicker('val', "");
    });
    document.getElementById("eqcBTN").addEventListener("click", function () {
        filters.eqc = '';
        $('#eqc').selectpicker('val', "");
    });
    document.getElementById("qrfaiBTN").addEventListener("click", function () {
        filters.qrfai = '';
        $('#qrfai').selectpicker('val', "");
    });
    document.getElementById("bccsqBTN").addEventListener("click", function () {
        filters.bccsq = '';
        $('#bccsq').selectpicker('val', "");
    });
    document.getElementById("bcaiBTN").addEventListener("click", function () {
        filters.bcai = '';
        $('#bcai').selectpicker('val', "");
    });
    document.getElementById("bccqBTN").addEventListener("click", function () {
        filters.bccq = '';
        $('#bccq').selectpicker('val', "");
    });
    document.getElementById("ProductIDBTN").addEventListener("click", function () {
        filters.Product_ID = '';
        $('#Product_ID').selectpicker('val', "");
    });
    document.getElementById("SubmissionDeadlineBTN").addEventListener("click", function () {
        filters.sd_from = '';
        filters.sd_to = '';
        document.getElementById("sd_from").value = "";
        document.getElementById("sd_to").value = "";
    });
    document.getElementById("qmbvuBTN").addEventListener("click", function () {
        filters.qmbvu_from = '';
        filters.qmbvu_to = '';
        document.getElementById("qmbvu_from").value = "";
        document.getElementById("qmbvu_to").value = "";
    });
    document.getElementById("rstBTN").addEventListener("click", function () {
        filters = {
            'RFQ_ID': '',
            'project': '',
            'Bidder_ID': '',
            'RFQ_Type': '',
            'eqc': '',
            'qrfai': '',
            'bccsq': '',
            'bcai': '',
            'bccq': '',
            'Product_ID': '',
            'sd_from': '',
            'sd_to': '',
            'qmbvu_from': '',
            'qmbvu_to': '',
        }
        document.getElementById('sbmtBTN').setAttribute('disabled', 'disabled');
        $('.selectpicker').selectpicker('val', "");
        document.getElementById("sd_from").value = "";
        document.getElementById("sd_to").value = "";
        document.getElementById("qmbvu_from").value = "";
        document.getElementById("qmbvu_to").value = "";

        var e = $("#replyedRFQTbl");
        e.bootstrapTable("showLoading");
        e.bootstrapTable("load", []);
        e.bootstrapTable("refresh");
        e.bootstrapTable("hideLoading");
        document.getElementById('card-table').classList.add('d-none');
        document.getElementById('collapse_pending_filters').classList.add('show');
    });
});

function updateTableData(filteredData) {
    var e = $("#replyedRFQTbl");
    e.bootstrapTable("showLoading");
    e.bootstrapTable("load", []);
    e.bootstrapTable("load", filteredData);
    e.bootstrapTable("refresh");
    e.bootstrapTable("hideLoading");
    document.getElementById('miniloader').classList.add('d-none');
    document.getElementById('card-table').classList.remove('d-none');
    // console.log(e.bootstrapTable('getRowByUniqueId', 3645));
}


function ViewRFQModal(rowid) {
    var e = $("#replyedRFQTbl");
    e.bootstrapTable("showLoading");
    // rowData = e.bootstrapTable('getRowByUniqueId', rowid);
    $.ajax({
        url: "/system/VendorRFQDone/details/api/",
        method: "GET",
        dataType: "json",
        data: {
            'RFQ_ID': rowid,
        },
        success: function (t) {
            // console.log(t);
            document.getElementById('RFQ_Sys_ID').innerHTML=t.id;
            document.getElementById('view_vendor').innerHTML=t.vendor;
            document.getElementById('view_RFQ_ID').innerHTML=t.RFQ_ID;
            document.getElementById('view_project_name').innerHTML=t.project_name;
            document.getElementById('view_ship_to_address').innerHTML=t.ship_to_address;
            document.getElementById('view_bidder_id').innerHTML=t.bidder_id;
            document.getElementById('view_submission_deadline').innerHTML=t.submission_deadline;
            document.getElementById('view_qmbvu').innerHTML=t.qmbvu;
            document.getElementById('view_RFQ_Type').innerHTML=t.RFQ_Type;
            document.getElementById('view_eqc').innerHTML=t.eqc;
            document.getElementById('view_qrfai').innerHTML=t.qrfai;
            document.getElementById('view_bccsq').innerHTML=t.bccsq;
            document.getElementById('view_bcai').innerHTML=t.bcai;
            document.getElementById('view_bccq').innerHTML=t.bccq;
            document.getElementById('total_products').innerHTML=t.products_count;
            var rpt = $("#RFQProductsTbl");
            rpt.bootstrapTable("showLoading");
            rpt.bootstrapTable("load", []);
            rpt.bootstrapTable("load", t.products);
            rpt.bootstrapTable("refresh");
            rpt.bootstrapTable("hideLoading");
            document.getElementById('total_files').innerHTML=t.attachments_count;
            var files_list = ``;
            t.attachments.forEach((element)=>{
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



function ViewCreateQuoteModal(rowid, invoice_id) {
    var e = $("#replyedRFQTbl");
    e.bootstrapTable("showLoading");
    $.ajax({
        url: "/system/VendorRFQDone/create/quote/api/",
        method: "GET",
        dataType: "json",
        data: {
            'RFQ_ID': rowid,
        },
        success: function (t) {
            // console.log(t);
            document.getElementById('cq_RFQ_ID').innerHTML=t.RFQ_ID;
            document.getElementById('cq_RFQ_Type').innerHTML=t.RFQ_Type;
            document.getElementById('cq_submission_deadline').innerHTML=t.submission_deadline;
            document.getElementById('cq_qmbvu').innerHTML=t.qmbvu;
            document.getElementById('cq_eqc').innerHTML=t.eqc;

            // reset selectpicker
            document.getElementById('cq_currency').innerHTML = '';
            var default_option_obj = document.createElement('option')
            default_option_obj.value = '';
            default_option_obj.innerHTML = 'Currency...';
            default_option_obj.selected = 'true';
            default_option_obj.disabled = 'true';
            document.getElementById('cq_currency').appendChild(default_option_obj);

            t.currencies.forEach((element)=>{
                var option_obj = document.createElement('option')
                option_obj.value = element[0];
                option_obj.innerHTML = element[1];
                // options_list +=`<option value="${element[0]}">${element[1]}</option>`;
                document.getElementById('cq_currency').appendChild(option_obj);
            })

            $('#create_quote_action_modal').modal({
                backdrop: true,
                keyboard: true,
                focus: true,
                show: true,
            });
            e.bootstrapTable("hideLoading");
        },
    });
}


function CreateQuote() {
    var RFQ_ID = document.getElementById('cq_RFQ_ID');
    var total_net_value = document.getElementById('total_net_value');
    var currency = document.getElementById('cq_currency');
    var files = pond.getFiles();
    var valid_flag = true;

    if(total_net_value.value){
        valid_flag = true;
        document.getElementById('total_net_value').classList.remove('bg-danger', 'text-white');
    }else{
        valid_flag = false;
        document.getElementById('total_net_value').classList.add('bg-danger', 'text-white');
    }
    if(currency.value){
        valid_flag = true;
        document.getElementById('cq_currency').classList.remove('bg-danger', 'text-white');
    }else{
        valid_flag = false;
        document.getElementById('cq_currency').classList.add('bg-danger', 'text-white');
    }
    if(files.length > 0){
        for(var file=0;file<files.length;file++){
            var firstFile = files[file].file;
            // Get the file extension
            var fileExtension = getFileExtension(firstFile.name);
            // Check if the file has a pdf extension
            if (fileExtension.toLowerCase() === 'pdf') {
                console.log('The file has a PDF extension.');
                valid_flag = true;
                document.getElementById('ua_card_header').classList.remove('bg-danger');
                document.getElementById('ua_card_header').classList.add('bg-success');
            } else {
                console.log('The file does not have a PDF extension.');
                valid_flag = false;
                document.getElementById('ua_card_header').classList.add('bg-danger');
            }
        }
    }else{
        valid_flag = false;
        document.getElementById('ua_card_header').classList.add('bg-danger');
    }

    if(valid_flag){
        // Create FormData object
        const formData = new FormData();
        // Append values to FormData
        formData.append('RFQ_ID', RFQ_ID.innerHTML);
        formData.append('total_net_value', total_net_value.value);
        formData.append('currency', currency.value);
        // Append files to FormData
        files.forEach((file, index) => {
            // console.log(file.file);
            formData.append(`filepond`, file.file);
        });
        $.ajax({
            url: '/system/VendorRFQDone/create/quote/submit/api/',
            type: 'POST',
            dataType: 'json', // Set the content type if sending JSON data
            data: formData, // Convert data to JSON string if sending JSON
            processData: false,  // Don't process the data
            contentType: false,  // Don't set content type
            headers: {
                'X-CSRFToken': document.getElementById('csrfToken').value,
            },
            success: function (response) {
                // Handle the successful response
                // console.log(response);
                $('#create_quote_action_modal').modal('hide');

                var o = $("#replyedRFQTbl");
                o.bootstrapTable("showLoading");
                var allData = o.bootstrapTable('getData');
                for (var i = 0; i < allData.length; i++) {
                    if (allData[i].RFQ_ID === RFQ_ID.innerHTML) {
                        allData[i].quotation += 1;
                        break; 
                    }
                }
                o.bootstrapTable('load', allData);
                o.bootstrapTable("hideLoading");
                RFQ_ID.innerHTML = '';
                total_net_value.value = '';
                currency.value = '';
                pond.removeFiles();
                valid_flag = true;
            }
        });
    }
}



var o = $("#replyedRFQTbl");
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
                { field: "RFQ_ID", title: "RFQ ID" },
                { field: "vendor", title: "Vendor" },
                { field: "project", title: "Project" },
                { field: "submission_deadline", title: "Submission Deadline" },
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
    selectedRows = $("#replyedRFQTbl").bootstrapTable("getSelections");
    // console.log(selectedRows);
    var printWindow = window.open("", "_blank");
    var currentDate = new Date();
    printWindow.document.open();
    printWindow.document.write(
        "<html><head><title>Pending RFQ Table</title>" +
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
    $("#replyedRFQTbl thead th").each(function () {
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


var x = $("#RFQProductsTbl");
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
    selectedRows = $("#RFQProductsTbl").bootstrapTable("getSelections");
    // console.log(selectedRows);
    var printWindow = window.open("", "_blank");
    var currentDate = new Date();
    printWindow.document.open();
    printWindow.document.write(
        "<html><head><title>RFQ Products Table</title>" +
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
    $("#RFQProductsTbl thead th").each(function () {
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
    var total_items = document.getElementById('total_items').innerHTML;
    var total_amount = document.getElementById('total_amount').innerHTML;

    var iit = $("#RFQProductsTbl");
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