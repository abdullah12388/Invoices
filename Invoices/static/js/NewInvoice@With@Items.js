let pond;
let data_list;

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
        allowMultiple: true,
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


// view milestones data
document.getElementById('po').addEventListener('change', function () {
    $.ajax({
        url: "/system/Invoices/New/PO/Details/api/",
        method: "GET",
        dataType: "json",
        data: {
            'PO_ID': this.value,
        },
        success: function (t) {
            console.log(t);
            data_list = t;
            document.getElementById('PO_total').innerHTML = t.total;
            document.getElementById('PO_payed').innerHTML = t.payed;
            document.getElementById('PO_remaining').innerHTML = t.remaining;
            t.milestones.forEach((element)=>{
                var option = document.createElement('option');
                option.value = element[0];
                option.text = element[1] + ' %';
                document.getElementById('milestone').appendChild(option);
            });
            document.getElementById('milestone').removeAttribute('disabled');
            $('#milestone').selectpicker('refresh');
        },
    });
});
// view items table
document.getElementById('milestone').addEventListener('change', function () {
    // console.log(this.value, data_list.milestones);
    // console.log(data_list.milestones.filter((obj)=> obj[0]==this.value)[0][2]);
    var MPO_details = data_list.milestones.filter((obj)=> obj[0]==this.value);
    document.getElementById('MPO_payed').innerHTML = MPO_details[0][3];
    document.getElementById('MPO_remaining').innerHTML = MPO_details[0][4];
    document.getElementById('MPO_total').innerHTML = MPO_details[0][5];
    document.getElementById('milestone_description').value = MPO_details[0][2];
    document.getElementById('milestone_desc_row').classList.remove('d-none');
    document.getElementById('milestone_desc_row').style = 'transition: all 1s;';
    if (MPO_details[0][4] > 0){
        document.getElementById('project_id').value = data_list.projects[0];
        document.getElementById('project_name').value = data_list.projects[1];
        document.getElementById('number').removeAttribute('disabled');
        document.getElementById('date').removeAttribute('disabled');
        document.getElementById('due').removeAttribute('disabled');
        document.getElementById('bill_to').removeAttribute('disabled');
        document.getElementById('type').removeAttribute('disabled');
        document.getElementById('currency').removeAttribute('disabled');
        document.getElementById('vat').removeAttribute('disabled');
        document.getElementById('item_number').removeAttribute('disabled');
        document.getElementById('quantity').removeAttribute('disabled');
        document.getElementById('uom').removeAttribute('disabled');
        document.getElementById('unit_price').removeAttribute('disabled');
        document.getElementById('description').removeAttribute('disabled');
        document.getElementById('viewItemsBTN').removeAttribute('disabled');
        document.getElementById('addItemBTN').removeAttribute('disabled');
    }else{
        document.getElementById('project_id').value = data_list.projects[0];
        document.getElementById('project_name').value = data_list.projects[1];
        document.getElementById('number').setAttribute('disabled', 'true');
        document.getElementById('date').setAttribute('disabled', 'true');
        document.getElementById('due').setAttribute('disabled', 'true');
        document.getElementById('bill_to').setAttribute('disabled', 'true');
        document.getElementById('type').setAttribute('disabled', 'true');
        document.getElementById('currency').setAttribute('disabled', 'true');
        document.getElementById('vat').setAttribute('disabled', 'true');
        document.getElementById('item_number').setAttribute('disabled', 'true');
        document.getElementById('quantity').setAttribute('disabled', 'true');
        document.getElementById('uom').setAttribute('disabled', 'true');
        document.getElementById('unit_price').setAttribute('disabled', 'true');
        document.getElementById('description').setAttribute('disabled', 'true');
        document.getElementById('viewItemsBTN').setAttribute('disabled', 'true');
        document.getElementById('addItemBTN').setAttribute('disabled', 'true');
    }
});

// view items table
document.getElementById('quantity').addEventListener('change', function () {
    document.getElementById('amount').value = '';
    var unit_price = document.getElementById('unit_price');
    if (unit_price.value) {
        document.getElementById('amount').value = (unit_price.value) * (this.value);
    }
});

document.getElementById('unit_price').addEventListener('change', function () {
    document.getElementById('amount').value = '';
    var quantity = document.getElementById('quantity');
    if (quantity.value) {
        document.getElementById('amount').value = (quantity.value) * (this.value);
    }
});

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

function AddItemIntoTable() {
    var item_number = document.getElementById('item_number');
    var quantity = document.getElementById('quantity');
    var uom = document.getElementById('uom');
    var unit_price = document.getElementById('unit_price');
    var amount = document.getElementById('amount');
    var description = document.getElementById('description');

    item_number.classList.remove('bg-danger');
    quantity.classList.remove('bg-danger');
    uom.classList.remove('bg-danger');
    unit_price.classList.remove('bg-danger');
    description.classList.remove('bg-danger');

    if (!(item_number.value)) {
        // console.log('number');
        item_number.classList.add('bg-danger');
    } else if (!(quantity.value)) {
        // console.log('quantity');
        quantity.classList.add('bg-danger');
    } else if (!(uom.value)) {
        // console.log('uom');
        uom.classList.add('bg-danger');
    } else if (!(unit_price.value)) {
        // console.log('unit_price');
        unit_price.classList.add('bg-danger');
    } else if (!(description.value)) {
        // console.log('description');
        description.classList.add('bg-danger');
    } else {
        var items_count = document.getElementById('items_count_modal');
        var items_total = document.getElementById('items_total_modal');
        items_count.innerHTML = parseInt(items_count.innerHTML) + 1;
        items_total.innerHTML = parseFloat(items_total.innerHTML) + parseFloat(amount.value);

        var selectedOption = uom.options[uom.selectedIndex];
        var action_button = `<button class="btn btn-danger m-auto" style="width:100%" onclick="DeleteItem('${item_number.value}')"><i class="fa-solid fa-trash"></i></button>`;

        var o = $("#ItemsTbl");
        o.bootstrapTable('append', {
            'number': item_number.value,
            'description': description.value,
            'quantity': quantity.value,
            'uom': selectedOption.id,
            'unit_price': unit_price.value,
            'amount': amount.value,
            'timestamp': formatDateTime(new Date()),
            'actions': action_button,
        });
        ResetItemForm();
    }
}

function ResetItemForm() {
    document.getElementById('item_number').value = '';
    document.getElementById('quantity').value = '';
    document.getElementById('uom').value = '';
    document.getElementById('unit_price').value = '';
    document.getElementById('amount').value = 0;
    document.getElementById('description').value = '';
}

function DeleteItem(rowid) {
    var e = $("#ItemsTbl");
    rowData = e.bootstrapTable('getRowByUniqueId', rowid);
    var items_count = document.getElementById('items_count_modal');
    var items_total = document.getElementById('items_total_modal');
    items_count.innerHTML = parseInt(items_count.innerHTML) - 1;
    items_total.innerHTML = parseFloat(items_total.innerHTML) - parseFloat(rowData.amount);
    console.log(rowData);
    e.bootstrapTable('removeByUniqueId', rowid)
}


// verify invoice button
function getFileExtension(fileName) {
    return fileName.slice((fileName.lastIndexOf(".") - 1 >>> 0) + 2);
}

function VerifyInvoice() {
    fields = {
        'PO_Number': 0,
        'Milestone': 0,
        'Vendor_Name': 0,
        'Project_Name': 0,
        'Invoice_Number': 0,
        'Invoice_Date': 0,
        'Payment_Due': 0,
        'Bill_To': 0,
        'Invoice_Type': 0,
        'Currency ': 0,
        'VAT': 0,
        'Items': 0,
        'Upload': 0,
    }
    ResetVerifyFields();
    $('#verify_modal').modal({
        backdrop: true,
        keyboard: true,
        focus: true,
        show: true,
    });
    var po = document.getElementById('po');
    var milestone = document.getElementById('milestone');
    var vendor = document.getElementById('vendor');
    var project_name = document.getElementById('project_name');
    var number = document.getElementById('number');
    var date = document.getElementById('date');
    var due = document.getElementById('due');
    var bill_to = document.getElementById('bill_to');
    var type = document.getElementById('type');
    var currency = document.getElementById('currency');
    var vat = document.getElementById('vat');
    var items_count = document.getElementById('items_count_modal');
    const files = pond.getFiles();
    var flag = false;
    
    if (po.value == '') {
        // console.log("no po");
        fields.PO_Number = 1;
        flag = true;
    }
    if (milestone.value == '') {
        // console.log("no milestone");
        fields.Milestone = 1;
        flag = true;
    }
    if (vendor.value == '') {
        // console.log("no vendor");
        fields.Vendor_Name = 1;
        flag = true;
    }
    if (project_name.value == '') {
        // console.log("no vendor");
        fields.Project_Name = 1;
        flag = true;
    }
    if (number.value == '') {
        // console.log("no number");
        fields.Invoice_Number = 1;
        flag = true;
    }
    if (date.value == '') {
        // console.log("no date");
        fields.Invoice_Date = 1;
        flag = true;
    }
    if (due.value == '') {
        // console.log("no due");
        fields.Payment_Due = 1;
        flag = true;
    }
    if (bill_to.value == '') {
        // console.log("no bill_to");
        fields.Bill_To = 1;
        flag = true;
    }
    if (type.value == '') {
        // console.log("no currency");
        fields.Invoice_Type = 1;
        flag = true;
    }
    if (currency.value == '') {
        // console.log("no currency");
        fields.Currency = 1;
        flag = true;
    }
    if (vat.value == '') {
        // console.log("no vat");
        fields.VAT = 1;
        flag = true;
    }
    if (items_count.innerHTML == '0') {
        // console.log("no items");
        fields.Items = 1;
        flag = true;
    }
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
        document.getElementById('calcBtn').removeAttribute('disabled');
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


// Calculate Invoice

function CalculateInvoice() {
    var items_total = parseFloat(document.getElementById('items_total_modal').innerHTML);
    var vatSelect = document.getElementById('vat');
    var vat = parseInt((vatSelect.options[vatSelect.selectedIndex]).id);
    document.getElementById('calcAmount').innerHTML = items_total;
    document.getElementById('calcVat').innerHTML = (items_total * vat) / 100;
    document.getElementById('calcTotal').innerHTML = items_total + ((items_total * vat) / 100);
    // document.getElementById('cah').classList.add('bg-dark', 'text-white');
    // document.getElementById('cah').style = 'transition: all 1s ease;';
    // document.getElementById('cvh').classList.add('bg-dark', 'text-white');
    // document.getElementById('cvh').style = 'transition: all 1s ease;';
    // document.getElementById('cth').classList.add('bg-dark', 'text-white');
    // document.getElementById('cth').style = 'transition: all 1s ease;';
    document.getElementById('reviewBtn').removeAttribute('disabled');
    document.getElementById('submitBtn').removeAttribute('disabled');
    document.getElementById('calcAmount').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Review Invoice

function ReviewInvoice() {
    var po = document.getElementById('po');
    var milestone = document.getElementById('milestone');
    var milestone_description = document.getElementById('milestone_description');
    var vendor = document.getElementById('vendor');
    var project_name = document.getElementById('project_name');
    var number = document.getElementById('number');
    var date = document.getElementById('date');
    var due = document.getElementById('due');
    var bill_to = document.getElementById('bill_to');
    var type = document.getElementById('type');
    var currency = document.getElementById('currency');
    var vat = document.getElementById('vat');
    var items_count = document.getElementById('items_count_modal');
    var items_total = document.getElementById('items_total_modal');

    var poSelectedOption = po.options[po.selectedIndex];
    var milestoneSelectedOption = milestone.options[milestone.selectedIndex];
    var vendorSelectedOption = vendor.options[vendor.selectedIndex];
    var typeSelectedOption = type.options[type.selectedIndex];
    var currencySelectedOption = currency.options[currency.selectedIndex];
    var vatSelectedOption = vat.options[vat.selectedIndex];

    var calcAmount = document.getElementById('calcAmount');
    var calcVat = document.getElementById('calcVat');
    var calcTotal = document.getElementById('calcTotal');

    // var it = $("#ItemsTbl");
    // var temp_table = it.bootstrapTable().bootstrapTable('getData');

    var files = pond.getFiles();

    // console.log(
    //     'vendor => ' + vendor.value,
    //     'number => ' + number.value,
    //     'date => ' + date.value,
    //     'po => ' + po.value,
    //     'due => ' + due.value,
    //     'bill_to => ' + bill_to.value,
    //     'type => ' + typeSelectedOption.id,
    //     'milestone => ' + milestone.value,
    //     'project_name => ' + project_name.value,
    //     'currency => ' + currencySelectedOption.id,
    //     'vat => ' + vatSelectedOption.id,
    //     'items_count => ' + items_count.innerHTML,
    //     'items_total => ' + items_total.innerHTML,
    //     'calcAmount => ' + calcAmount.innerHTML,
    //     'calcVat => ' + calcVat.innerHTML,
    //     'calcTotal => ' + calcTotal.innerHTML,
    //     temp_table,
    //     files,
    // );

    document.getElementById('view_po').innerHTML = poSelectedOption.innerHTML;
    document.getElementById('view_milestone').innerHTML = milestoneSelectedOption.innerHTML;
    document.getElementById('view_milestone_description').value = milestone_description.value;
    document.getElementById('view_vendor').innerHTML = vendorSelectedOption.innerHTML;
    document.getElementById('view_project_name').innerHTML = project_name.value;
    document.getElementById('view_number').innerHTML = number.value;
    document.getElementById('view_date').innerHTML = date.value;
    document.getElementById('view_bill_to').innerHTML = bill_to.value;
    document.getElementById('view_due').innerHTML = due.value;
    document.getElementById('view_type').innerHTML = typeSelectedOption.innerHTML;
    document.getElementById('total_items').innerHTML = items_count.innerHTML;
    document.getElementById('total_amount').innerHTML = items_total.innerHTML;
    document.getElementById('ta_view_invoice_currency').innerHTML = currencySelectedOption.innerHTML;
    document.getElementById('view_total_amount').innerHTML = calcAmount.innerHTML;
    document.getElementById('view_invoice_vat').innerHTML = vatSelectedOption.innerHTML;
    document.getElementById('vat_view_invoice_currency').innerHTML = currencySelectedOption.innerHTML;
    document.getElementById('view_vat_amount').innerHTML = calcVat.innerHTML;
    document.getElementById('t_view_invoice_currency').innerHTML = currencySelectedOption.innerHTML;
    document.getElementById('view_invoice_total').innerHTML = calcTotal.innerHTML;
    document.getElementById('total_files').innerHTML = files.length;

    var o = $("#ItemsTbl");
    var temp_items_table = o.bootstrapTable().bootstrapTable('getData');

    var t = $("#InvoiceItemsTbl");
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

    // document.getElementById('submitBtn').removeAttribute('disabled');
}


// Submit Invoice

function SubmitInvoice(){
    if(!VerifyInvoice()){
        setTimeout(function () {
            $('#submit_modal').modal({
                backdrop: true,
                keyboard: true,
                focus: true,
                show: true,
            });
            var po = document.getElementById('po');
            var milestone = document.getElementById('milestone');
            var vendor = document.getElementById('vendor');
            var project_id = document.getElementById('project_id');
            var number = document.getElementById('number');
            var date = document.getElementById('date');
            var due = document.getElementById('due');
            var bill_to = document.getElementById('bill_to');
            var type = document.getElementById('type');
            var currency = document.getElementById('currency');
            var vat = document.getElementById('vat');
            var temp_table = $("#ItemsTbl").bootstrapTable().bootstrapTable('getData');
            var files = pond.getFiles();

            // Create FormData object
            const formData = new FormData();
            // Append values to FormData
            formData.append('po', po.value);
            formData.append('milestone', milestone.value);
            formData.append('vendor', vendor.value);
            formData.append('project', project_id.value);
            formData.append('number', number.value);
            formData.append('date', date.value);
            formData.append('due', due.value);
            formData.append('bill_to', bill_to.value);
            formData.append('type', type.value);
            formData.append('currency', currency.value);
            formData.append('vat', vat.value);
            // Append files to FormData
            files.forEach((file, index) => {
                console.log(file.file);
                formData.append(`filepond`, file.file);
            });
            // Append additional data from the table
            temp_table.forEach((row, index) => {
                console.log(row);
                formData.append(`items`, JSON.stringify({
                    'number': row.number,
                    'description': row.description,
                    'quantity': row.quantity,
                    'uom': row.uom,
                    'unit_price': row.unit_price,
                    'amount': row.amount,
                }));
            });

            $.ajax({
                url: '/system/Invoices/New/Submit/api/',
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
                                    <h5 style="margin: 0;">Invoice Number</h5>
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

var o = $("#ItemsTbl");
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
                { field: "number", title: "Number" },
                { field: "description", title: "Description" },
                { field: "quantity", title: "Quantity" },
                { field: "uom", title: "UOM" },
                { field: "unit_price", title: "Unit Price" },
                { field: "amount", title: "Amount" },
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
    selectedRows = $("#ItemsTbl").bootstrapTable("getSelections");
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
    $("#ItemsTbl thead th").each(function () {
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
var t = $("#InvoiceItemsTbl");
$("#items_toolbar")
    .find("select")
    .change(function () {
        var filename = document.getElementById('items_exportFileName').value;
        var currentDate = new Date();
        var temp_table = t.bootstrapTable().bootstrapTable('getData');
        t.bootstrapTable("destroy").bootstrapTable({
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
                { field: "amount", title: "Amount" }
            ],
        });
        t.bootstrapTable("showLoading");
        t.bootstrapTable("load", temp_table);
        t.bootstrapTable("refresh");
        t.bootstrapTable("hideLoading");
    }).trigger('change')


document.getElementById("items_print_selected").addEventListener("click", function () {
    var selectedRows = [];
    selectedRows = $("#InvoiceItemsTbl").bootstrapTable("getSelections");
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
    $("#InvoiceItemsTbl thead th").each(function () {
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
