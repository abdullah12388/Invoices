let pond;
var precent = 0;
var due = false;

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


    // const formElement = document.getElementById('req-form');
    // let filesToUpload = [];

    // formElement.addEventListener('submit', event => {
    //     event.preventDefault();

    //     // Get the FilePond files
    //     filesToUpload = pond.getFiles();

    //     // Create a FormData object to store form data and files
    //     const formData = new FormData(formElement);

    //     // Append the selected files to the FormData
        // filesToUpload.forEach((file, index) => {
        //     formData.append(`filepond`, file.file);
        // });

    //     // Send the form data with files to the server
        // fetch('./', {
        //     method: 'POST',
        //     body: formData,
        // })
        //     .then(response => {
        //         // Handle the server response
        //         console.log('Form submitted successfully');
        //         // Reset the form after successful submission
        //         // formElement.reset();
        //         // pond.removeFiles();
        //         $('#success').css('display', 'flex');
        //         setTimeout(()=>{
        //             location.reload();
        //         },3000);
        //     })
        //     .catch(error => {
        //         // Handle any errors
        //         console.error('Error submitting form:', error);
        //     });
    // });


    // Fetch the CSRF token from the cookie
    // function getCSRFToken() {
    //     const name = 'csrftoken';
    //     const cookieValue = document.cookie
    //         .split('; ')
    //         .find((cookie) => cookie.startsWith(name + '='))
    //         .split('=')[1];
    //     return cookieValue;
    // }
});


// view items table
function formatDateTime(date) {
    if (!(date instanceof Date)) {
        date = new Date(date);
    }
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
    var year = date.getFullYear();
    var hours = String(date.getHours()).padStart(2, '0');
    var minutes = String(date.getMinutes()).padStart(2, '0');
    var formattedDateTime = `${month}/${day}/${year} ${hours}:${minutes}`;
    return formattedDateTime;
}

document.getElementById('total_value').addEventListener('change', function(){
    if(this.value){
        document.getElementById('milestone_addBtn').removeAttribute('disabled');
    }else{
        document.getElementById('milestone_addBtn').setAttribute('disabled', 'true');
    }
})

document.getElementById('milestone_precentage').addEventListener('change', function(){
    var milestone_amount = document.getElementById('milestone_amount');
    var total_value = document.getElementById('total_value');
    milestone_amount.value = (parseFloat(total_value.value) * parseFloat(this.value))/100;
})


document.getElementById('enableBTN').addEventListener('click', function(){
    document.getElementById('enableDiv').classList.add('d-none');
    document.getElementById('pd_input').classList.remove('d-none');
    document.getElementById('pd_label').classList.remove('d-none');
    document.getElementById('pd_req').classList.remove('d-none');
    due = true;
});

function AddItemIntoTable() {
    var milestone_id = document.getElementById('milestone_id');
    var milestone_precentage = document.getElementById('milestone_precentage');
    var milestone_due = document.getElementById('milestone_due');
    var milestone_amount = document.getElementById('milestone_amount');
    var milestone_description = document.getElementById('milestone_description');
    var pattern = /^(?!\d+$)(?!\s+$).*$/;
    
    milestone_precentage.classList.remove('bg-danger');
    milestone_due.classList.remove('bg-danger');
    milestone_description.classList.remove('bg-danger');

    if ((!(milestone_precentage.value)) || (milestone_precentage.value < 0) || (milestone_precentage.value == 0)) {
        // console.log('number');
        milestone_precentage.classList.add('bg-danger');
    } 
    else if ((due && (!(milestone_due.value))) || ((milestone_due.value) % 1 !== 0)) {
        // console.log(milestone_due);
        milestone_due.classList.add('bg-danger');
    }
    else if (!pattern.test(milestone_description.value)) {
        // console.log('unit_price');
        milestone_description.classList.add('bg-danger');
    } else {
        check_precent = parseInt(precent) + parseInt(milestone_precentage.value);
        if(check_precent <= 100){
            milestone_precentage.classList.remove('bg-danger', 'text-white');
            precent = parseInt(precent) + parseInt(milestone_precentage.value);
            var milestones_count = document.getElementById('milestones_count_modal');
            var milestones_total = document.getElementById('milestones_total_modal');
            milestones_count.innerHTML = parseInt(milestones_count.innerHTML) + 1;
            milestones_total.innerHTML = parseFloat(milestones_total.innerHTML) + parseFloat(milestone_amount.value);
    
            var action_button = `<button class="btn btn-danger m-auto" style="width:100%" onclick="DeleteItem('${milestone_id.value}')"><i class="fa-solid fa-trash"></i></button>`;
    
            var o = $("#milestonesTbl");
            o.bootstrapTable('append', {
                'id': milestone_id.value,
                'precentage': milestone_precentage.value,
                'due': milestone_due.value,
                'amount': milestone_amount.value,
                'description': milestone_description.value,
                'timestamp': formatDateTime(new Date()),
                'actions': action_button,
            });
            milestone_id.value = parseInt(milestone_id.value) + 1;
            ResetItemForm();
        }else{
            milestone_precentage.classList.add('bg-danger', 'text-white');
        }
    }
}

function ResetItemForm() {
    document.getElementById('milestone_precentage').classList.remove('bg-danger', 'text-white');
    document.getElementById('milestone_precentage').value = '';
    document.getElementById('milestone_due').value = '';
    document.getElementById('milestone_amount').value = '';
    document.getElementById('milestone_description').value = '';
    
    document.getElementById('enableDiv').classList.remove('d-none');
    document.getElementById('pd_input').classList.add('d-none');
    document.getElementById('pd_label').classList.add('d-none');
    document.getElementById('pd_req').classList.add('d-none');
    due = false;
}

function DeleteItem(rowid) {
    var e = $("#milestonesTbl");
    rowData = e.bootstrapTable('getRowByUniqueId', rowid);
    var milestones_count = document.getElementById('milestones_count_modal');
    var milestones_total = document.getElementById('milestones_total_modal');
    milestones_count.innerHTML = parseInt(milestones_count.innerHTML) - 1;
    milestones_total.innerHTML = parseFloat(milestones_total.innerHTML) - parseFloat(rowData.amount);
    console.log(rowData);
    e.bootstrapTable('removeByUniqueId', rowid);
    document.getElementById('milestone_id').value = parseInt(document.getElementById('milestone_id').value) - 1;
    precent = parseInt(precent) - parseInt(rowData.precentage);
}


// verify invoice button
function getFileExtension(fileName) {
    return fileName.slice((fileName.lastIndexOf(".") - 1 >>> 0) + 2);
}

function VerifyPO() {
    fields = {
        'quotation': 0,
        'po': 0,
        'contact_person': 0,
        'total_value': 0,
        'currency': 0,
        'shipping_terms': 0,
        'milestones': 0,
        'Upload': 0,
    }
    ResetVerifyFields();
    $('#verify_modal').modal({
        backdrop: true,
        keyboard: true,
        focus: true,
        show: true,
    });
    var quotation = document.getElementById('quotation');
    var po = document.getElementById('po');
    var contact_person = document.getElementById('contact_person');
    var total_value = document.getElementById('total_value');
    var currency = document.getElementById('currency');
    var shipping_terms = document.getElementById('shipping_terms');
    var milestones_count = document.getElementById('milestones_count_modal');
    const files = pond.getFiles();
    var flag = false;
    var pattern = /^(?!\d+$)(?!\s+$).*$/;

    if (files.length == 0) {
        // console.log("FilePond does not have any files");
        fields.Upload = 1;
        flag = true;
    } else {
        for(var file=0;file<files.length;file++){
            var firstFile = files[file].file;
            // Get the file extension
            var fileExtension = getFileExtension(firstFile.name);
            // Check if the file has a pdf extension
            if (fileExtension.toLowerCase() === 'pdf') {
                console.log('The file has a PDF extension.');
            } else {
                console.log('The file does not have a PDF extension.');
                fields.Upload = 2;
                flag = true;
            }
        }
    }
    if (quotation.value == '') {
        // console.log("no items");
        fields.quotation = 1;
        flag = true;
    }
    if (!pattern.test(po.value)) {
        // console.log("no po");
        fields.po = 1;
        flag = true;
    }
    if (contact_person.value == '') {
        // console.log("no vat");
        fields.contact_person = 1;
        flag = true;
    }
    if ((total_value.value == '') || (total_value.value < 0) || (total_value.value == 0)) {
        // console.log("no currency");
        fields.total_value = 1;
        flag = true;
    }
    if (currency.value == '') {
        // console.log("no milestone");
        fields.currency = 1;
        flag = true;
    }
    if (!pattern.test(shipping_terms.value)) {
        // console.log("no bill_to");
        fields.shipping_terms = 1;
        flag = true;
    }
    if (milestones_count.innerHTML == '0') {
        // console.log("no due");
        fields.milestones = 1;
        flag = true;
    }

    if (flag) {
        setTimeout(function () {
            CreateErrorFields(fields);
        }, 2000);
    } else {
        setTimeout(function () {
            CreateValidFields();
        }, 2000);
    }
    return flag;
}


function CreateErrorFields(fields) {
    // console.log(fields);
    document.getElementById('error_div').innerHTML = '';
    document.getElementById('verify_img').classList.add('d-none');
    document.getElementById('error_img').classList.remove('d-none');
    document.getElementById('verify_message').classList.add('d-none');
    document.getElementById('error_message').classList.remove('d-none');

    document.getElementById('error_div').style = "transition: all 1s ease;";
    document.getElementById('verify_img').style = "transition: all 1s ease;";
    document.getElementById('error_img').style = "transition: all 1s ease;";
    document.getElementById('verify_message').style = "transition: all 1s ease;";
    document.getElementById('error_message').style = "transition: all 1s ease;";

    var errors_div = document.getElementById('error_div');
    var temp = ``;
    for (var field in fields) {
        if (fields[field] == 1 || fields[field] == 2) {
            // console.log(field);
            if (field == 'Upload' && fields[field] == 2) {
                temp += `
                <div class="row mt-2" >
                    <div class="col-5 d-flex justify-content-start align-items-center" style="border-right: 2px solid #212529;">
                        <h5 style="margin: 0;">${field}</h5>
                    </div>
                    <div class="col-7 d-flex justify-content-center align-items-center">
                        <h5 class="text-danger" style="margin: 0;">Not A PDF File!.</h5>
                    </div>
                </div>
                `;
            } else {
                temp += `
                <div class="row mt-2" >
                    <div class="col-5 d-flex justify-content-start align-items-center" style="border-right: 2px solid #212529;">
                        <h5 style="margin: 0;">${field}</h5>
                    </div>
                    <div class="col-7 d-flex justify-content-center align-items-center">
                        <h5 class="text-danger" style="margin: 0;">Required Field!.</h5>
                    </div>
                </div>
                `;
            }
        }
    }
    errors_div.innerHTML += temp;
    errors_div.style = "transition: all 1s ease;";
}

function CreateValidFields() {
    document.getElementById('error_div').innerHTML = '';
    document.getElementById('verify_img').classList.add('d-none');
    document.getElementById('error_img').classList.add('d-none');
    document.getElementById('valid_img').classList.remove('d-none');
    document.getElementById('verify_message').classList.add('d-none');
    document.getElementById('error_message').classList.add('d-none');
    document.getElementById('valid_message').classList.remove('d-none');
    setTimeout(function () {
        $('#verify_modal').modal('hide');
        document.getElementById('reviewBtn').removeAttribute('disabled');
        document.getElementById('submitBtn').removeAttribute('disabled');
    }, 1000);
}

function ResetVerifyFields() {
    document.getElementById('error_div').innerHTML = '';
    document.getElementById('verify_img').classList.remove('d-none');
    document.getElementById('error_img').classList.add('d-none');
    document.getElementById('valid_img').classList.add('d-none');
    document.getElementById('verify_message').classList.remove('d-none');
    document.getElementById('error_message').classList.add('d-none');
    document.getElementById('valid_message').classList.add('d-none');
}



// Review Invoice

function ReviewPO() {
    var quotation = document.getElementById('quotation');
    var po = document.getElementById('po');
    var contact_person = document.getElementById('contact_person');
    var total_value = document.getElementById('total_value');
    var currency = document.getElementById('currency');
    var shipping_terms = document.getElementById('shipping_terms');
    var milestones_count = document.getElementById('milestones_count_modal');
    var milestone_total = document.getElementById('milestones_total_modal');


    var quotationSelectedOption = quotation.options[quotation.selectedIndex];
    var currencySelectedOption = currency.options[currency.selectedIndex];

    var files = pond.getFiles();


    document.getElementById('view_quotation').innerHTML = quotationSelectedOption.value;
    document.getElementById('view_RFQ').innerHTML = quotationSelectedOption.id;
    document.getElementById('view_PO').innerHTML = po.value;
    document.getElementById('view_total_value').innerHTML = `${total_value.value} ${currencySelectedOption.id}`;
    document.getElementById('view_contact_person').innerHTML = contact_person.value;
    document.getElementById('view_shipping_terms').innerHTML = shipping_terms.value;
    document.getElementById('total_milestones').innerHTML = milestones_count.innerHTML;
    document.getElementById('total_amount').innerHTML = milestone_total.innerHTML;
    document.getElementById('total_files').innerHTML = files.length;

    var o = $("#milestonesTbl");
    var temp_items_table = o.bootstrapTable('getData');

    var t = $("#POMilestonesTbl");
    t.bootstrapTable("showLoading");
    t.bootstrapTable("load", []);
    t.bootstrapTable("load", temp_items_table);
    t.bootstrapTable("refresh");
    t.bootstrapTable("hideLoading");

    var files_list = ``;
    files.forEach((element)=>{
        files_list +=`
        <div class="row mb-2" style="border-left: 1px solid #6c757d;">
            <div class="col-1 d-flex justify-content-start align-items-center">
                <h5 class="mb-0">#</h5>
            </div>
            <div class="col-11 d-flex justify-content-start align-items-center">
                <h5 class="mb-0">${element.filename}</h5>
            </div>
        </div>
        `;
    })
    document.getElementById('files_parent').innerHTML = files_list;

    $('#review_modal').modal({
        backdrop: true,
        keyboard: true,
        focus: true,
        show: true,
    });

    document.getElementById('submitBtn').removeAttribute('disabled');
}


// Submit Invoice

function SubmitPO(){
    if(!VerifyPO()){
        setTimeout(function () {
            $('#submit_modal').modal({
                backdrop: true,
                keyboard: true,
                focus: true,
                show: true,
            });

            var quotation = document.getElementById('quotation');
            var po = document.getElementById('po');
            var contact_person = document.getElementById('contact_person');
            var total_value = document.getElementById('total_value');
            var currency = document.getElementById('currency');
            var shipping_terms = document.getElementById('shipping_terms');

            var temp_table = $("#milestonesTbl").bootstrapTable('getData');
            var files = pond.getFiles();
            
            // Create FormData object
            const formData = new FormData();
            // Append values to FormData
            formData.append('quotation', quotation.value);
            formData.append('po', po.value);
            formData.append('contact_person', contact_person.value);
            formData.append('total_value', total_value.value);
            formData.append('currency', currency.value);
            formData.append('shipping_terms', shipping_terms.value);
            // Append files to FormData
            files.forEach((file, index) => {
                console.log(file.file);
                formData.append(`filepond`, file.file);
            });
            // Append additional data from the table
            temp_table.forEach((row, index) => {
                console.log(row);
                formData.append(`milestones`, JSON.stringify({
                    'precentage': row.precentage,
                    'due': row.due,
                    'amount': row.amount,
                    'description': row.description,
                }));
            });
            $.ajax({
                url: '/system/ProcurementPO/New/Submit/api/',
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
                    console.log(response);
                    if(response.status == 'added'){
                        document.getElementById('submit_img').classList.add('d-none');
                        document.getElementById('submit_valid_img').classList.remove('d-none');
                        document.getElementById('submit_message').classList.add('d-none');
                        document.getElementById('submit_valid_message').classList.remove('d-none');
                        document.getElementById('submit_error_img').classList.add('d-none');
                        document.getElementById('submit_error_message').classList.add('d-none');
                        document.getElementById('submit_error_div').innerHTML = '';

                        document.getElementById('submit_img').style = "transition: all 1s ease;";
                        document.getElementById('submit_valid_img').style = "transition: all 1s ease;";
                        document.getElementById('submit_message').style = "transition: all 1s ease;";
                        document.getElementById('submit_valid_message').style = "transition: all 1s ease;";
                        document.getElementById('submit_error_img').style = "transition: all 1s ease;";
                        document.getElementById('submit_error_message').style = "transition: all 1s ease;";
                        document.getElementById('submit_error_div').style = "transition: all 1s ease;";
                        setTimeout(function () {
                            window.location.reload();
                        }, 1000);
                    }else{
                        setTimeout(function () {
                            document.getElementById('submit_img').classList.add('d-none');
                            document.getElementById('submit_valid_img').classList.add('d-none');
                            document.getElementById('submit_message').classList.add('d-none');
                            document.getElementById('submit_valid_message').classList.add('d-none');
                            document.getElementById('submit_error_img').classList.remove('d-none');
                            document.getElementById('submit_error_message').classList.remove('d-none');
                            document.getElementById('submit_error_div').innerHTML = `
                            <div class="row mt-2" >
                                <div class="col-5 d-flex justify-content-start align-items-center" style="border-right: 2px solid #212529;">
                                    <h5 style="margin: 0;">P.O. Number</h5>
                                </div>
                                <div class="col-7 d-flex justify-content-center align-items-center">
                                    <h5 class="text-danger" style="margin: 0;">Already Exists...!</h5>
                                </div>
                            </div>
                            `;
                            document.getElementById('submit_img').style = "transition: all 1s ease;";
                            document.getElementById('submit_valid_img').style = "transition: all 1s ease;";
                            document.getElementById('submit_message').style = "transition: all 1s ease;";
                            document.getElementById('submit_valid_message').style = "transition: all 1s ease;";
                            document.getElementById('submit_error_img').style = "transition: all 1s ease;";
                            document.getElementById('submit_error_message').style = "transition: all 1s ease;";
                            document.getElementById('submit_error_div').style = "transition: all 1s ease;";
                        }, 2000);
                    }
                }
            });
        }, 3000);
    }
}


// temp items table

var o = $("#milestonesTbl");
$("#toolbar")
    .find("select")
    .change(function () {
        var filename = document.getElementById('exportFileName').value;
        var currentDate = new Date();
        var temp_table = o.bootstrapTable('getData');
        o.bootstrapTable("destroy").bootstrapTable({
            exportDataType: $(this).val(),
            exportOptions: {
                fileName: (filename ? filename + '_' : 'GTS_') + currentDate.toLocaleString(),
            },
            exportTypes: ["json", "xml", "csv", "txt", "sql", "excel", "pdf"],
            columns: [
                { field: "state", checkbox: !0, visible: "selected" === $(this).val() },
                { field: "id", title: "ID" },
                { field: "precentage", title: "Precentage" },
                { field: "due", title: "Payment Due" },
                { field: "amount", title: "Amount" },
                { field: "description", title: "Description" },
                { field: "timestamp", title: "Timestamp" },
                { field: "actions", title: "Actions" },
            ],
        });
        o.bootstrapTable("showLoading");
        o.bootstrapTable("load", temp_table);
        o.bootstrapTable("refresh");
        o.bootstrapTable("hideLoading");
    }).trigger('change')


document.getElementById("print_selected").addEventListener("click", function () {
    var selectedRows = [];
    selectedRows = $("#milestonesTbl").bootstrapTable("getSelections");
    console.log(selectedRows);
    var printWindow = window.open("", "_blank");
    var currentDate = new Date();
    printWindow.document.open();
    printWindow.document.write(
        "<html><head><title>Milestones Table</title>" +
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
    $("#milestonesTbl thead th").each(function () {
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


// review items table
var t = $("#POMilestonesTbl");
$("#milestone_toolbar")
    .find("select")
    .change(function () {
        var filename = document.getElementById('milestones_exportFileName').value;
        var currentDate = new Date();
        var temp_table = t.bootstrapTable('getData');
        t.bootstrapTable("destroy").bootstrapTable({
            exportDataType: $(this).val(),
            exportOptions: {
                fileName: (filename ? filename + '_' : 'GTS_') + currentDate.toLocaleString(),
            },
            exportTypes: ["json", "xml", "csv", "txt", "sql", "excel", "pdf"],
            columns: [
                { field: "state", checkbox: !0, visible: "selected" === $(this).val() },
                { field: "id", title: "ID" },
                { field: "precentage", title: "Precentage" },
                { field: "due", title: "Payment Due" },
                { field: "amount", title: "Amount" },
                { field: "description", title: "Description" },
                { field: "timestamp", title: "Timestamp" },
            ],
        });
        t.bootstrapTable("showLoading");
        t.bootstrapTable("load", temp_table);
        t.bootstrapTable("refresh");
        t.bootstrapTable("hideLoading");
    }).trigger('change')


document.getElementById("milestones_print_selected").addEventListener("click", function () {
    var selectedRows = [];
    selectedRows = $("#POMilestonesTbl").bootstrapTable("getSelections");
    console.log(selectedRows);
    var printWindow = window.open("", "_blank");
    var currentDate = new Date();
    printWindow.document.open();
    printWindow.document.write(
        "<html><head><title>Items Table</title>" +
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
    $("#POMilestonesTbl thead th").each(function () {
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
