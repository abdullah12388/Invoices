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
    // Get the current date and time
    // const currentDate = new Date();
    // const year = currentDate.getFullYear();
    // const month = String(currentDate.getMonth() + 1).padStart(2, '0');  // Months are 0-indexed
    // const day = String(currentDate.getDate()).padStart(2, '0');
    // const hours = String(currentDate.getHours()).padStart(2, '0');
    // const minutes = String(currentDate.getMinutes()).padStart(2, '0');

    // Format the date and time for datetime-local input
    // const formattedDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
    
    // Set the value of the input field
    // document.getElementById('submission_deadline').value = formattedDateTime;
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

function formatDate(date) {
    if (!(date instanceof Date)) {
        date = new Date(date);
    }
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
    var year = date.getFullYear();
    var formattedDateTime = `${month}/${day}/${year}`;
    return formattedDateTime;
}


function AddItemIntoTable() {
    var item_number = document.getElementById('item_number');
    var product_id = document.getElementById('product_id');
    var quantity = document.getElementById('quantity');
    var uom = document.getElementById('uom');
    var category = document.getElementById('category');
    var dd_sp = document.getElementById('dd_sp');
    var description = document.getElementById('description');
    var items_count = document.getElementById('items_count_modal');

    product_id.classList.remove('bg-danger');
    quantity.classList.remove('bg-danger');
    uom.classList.remove('bg-danger');
    category.classList.remove('bg-danger');
    dd_sp.classList.remove('bg-danger');
    description.classList.remove('bg-danger');

    if (!(product_id.value)) {
        // console.log('number');
        product_id.classList.add('bg-danger');
    } else if (!(quantity.value)) {
        // console.log('quantity');
        quantity.classList.add('bg-danger');
    } else if (!(uom.value)) {
        // console.log('uom');
        uom.classList.add('bg-danger');
    } else if (!(category.value)) {
        // console.log('category');
        category.classList.add('bg-danger');
    } else if(!(dd_sp.value)){
        // console.log('dd_sp');
        dd_sp.classList.add('bg-danger');
    } else if (!(description.value)) {
        // console.log('description');
        description.classList.add('bg-danger');
    } else {
        var o = $("#ItemsTbl");
        var tableData = o.bootstrapTable('getData');
        if(tableData.length > 0){
            tableData.forEach((row)=>{
                if(row['product_id'] == product_id.value){
                    product_id.classList.add('bg-danger');
                }else{
                    items_count.innerHTML = parseInt(items_count.innerHTML) + 1;
                    var selectedOption = uom.options[uom.selectedIndex];
                    var action_button = `<button class="btn btn-danger m-auto" style="width:100%" onclick="DeleteItem('${item_number.value}')"><i class="fa-solid fa-trash"></i></button>`;
                    product_id.classList.remove('bg-danger');
                    o.bootstrapTable('append', {
                        'item_number': item_number.value,
                        'product_id': product_id.value,
                        'description': description.value,
                        'category': category.id,
                        'dd_sp': dd_sp.value,
                        'quantity': quantity.value,
                        'uom': selectedOption.id,
                        'actions': action_button,
                    });
                    item_number.value = parseInt(item_number.value) + 1;
                    ResetItemForm();
                }
            })
        }else{
            items_count.innerHTML = parseInt(items_count.innerHTML) + 1;
            var selectedOption = uom.options[uom.selectedIndex];
            var action_button = `<button class="btn btn-danger m-auto" style="width:100%" onclick="DeleteItem('${item_number.value}')"><i class="fa-solid fa-trash"></i></button>`;
            o.bootstrapTable('append', {
                'item_number': item_number.value,
                'product_id': product_id.value,
                'description': description.value,
                'category': category.id,
                'dd_sp': dd_sp.value,
                'quantity': quantity.value,
                'uom': selectedOption.id,
                'actions': action_button,
            });
            item_number.value = parseInt(item_number.value) + 1;
            ResetItemForm();
        }
    }
}

function ResetItemForm() {
    // document.getElementById('item_number').value = '';
    document.getElementById('product_id').value = '';
    document.getElementById('quantity').value = '';
    document.getElementById('uom').value = '';
    document.getElementById('category').value = '';
    document.getElementById('dd_sp').value = '';
    document.getElementById('description').value = '';
}

function DeleteItem(rowid) {
    var e = $("#ItemsTbl");
    rowData = e.bootstrapTable('getRowByUniqueId', rowid);
    var items_count = document.getElementById('items_count_modal');
    items_count.innerHTML = parseInt(items_count.innerHTML) - 1;
    var item_number = document.getElementById('item_number');
    item_number.value = parseInt(item_number.value) - 1;
    // console.log(rowData);
    e.bootstrapTable('removeByUniqueId', rowid)
}


// verify invoice button
function getFileExtension(fileName) {
    return fileName.slice((fileName.lastIndexOf(".") - 1 >>> 0) + 2);
}


function fillFields(){
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');  // Months are 0-indexed
    const day = String(currentDate.getDate()).padStart(2, '0');

    // Format the date and time for datetime-local input
    const formattedDateTime = `${year}-${month}-${day}`;
    
    // Set the value of the input field

    document.getElementById('RFQ_ID').value = 571;
    $('#project').selectpicker('val', '1');
    $('#project').selectpicker('refresh');
    $('#vendor').selectpicker('val', '1');
    $('#vendor').selectpicker('refresh');
    document.getElementById('ship_to_address').value = 'Abdullah';
    document.getElementById('Bidder_ID').value = 12;
    document.getElementById('qmbvu').value = formattedDateTime;
    $('#RFQ_type').selectpicker('val', '1');
    $('#RFQ_type').selectpicker('refresh');
    $('#eqc').selectpicker('val', '1');
    $('#eqc').selectpicker('refresh');
    $('#qrfai').selectpicker('val', 'y');
    $('#qrfai').selectpicker('refresh');
    $('#bccsq').selectpicker('val', 'y');
    $('#bccsq').selectpicker('refresh');
    $('#bcai').selectpicker('val', 'y');
    $('#bcai').selectpicker('refresh');
    $('#bccq').selectpicker('val', 'y');
    $('#bccq').selectpicker('refresh');
    document.getElementById('items_count_modal').innerHTML = 1;

    var t = $("#ItemsTbl");
    t.bootstrapTable("showLoading");
    t.bootstrapTable("load", [{
        'item_number': 1,
        'product_id': 120,
        'description': 'abdullah',
        'category': 'test',
        'dd_sp': '01/03/2024',
        'quantity': 10,
        'uom': 'ea',
        'actions': 'test',
    }]);
    t.bootstrapTable("refresh");
    t.bootstrapTable("hideLoading");
}


function VerifyRFQ() {
    fields = {
        'RFQ_ID': 0,
        'Project': 0,
        'Vendor': 0,
        'Ship_to_address': 0,
        'Bidder_ID': 0,
        'Submission_Deadline': 0,
        'Quote_must_be_valid_until': 0,
        'RFQ_type ': 0,
        'Expected_quote_currency': 0,
        'Quotes_required_for_all_items': 0,
        'Bidder_can_change_submitted_quote': 0,
        'Bidder_can_add_items': 0,
        'Bidder_can_change_quantity': 0,
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
    var RFQ_ID = document.getElementById('RFQ_ID');
    var project = document.getElementById('project');
    var vendor = document.getElementById('vendor');
    var ship_to_address = document.getElementById('ship_to_address');
    var Bidder_ID = document.getElementById('Bidder_ID');
    var submission_deadline = document.getElementById('submission_deadline');
    var qmbvu = document.getElementById('qmbvu');
    var RFQ_type = document.getElementById('RFQ_type');
    var eqc = document.getElementById('eqc');
    var qrfai = document.getElementById('qrfai');
    var bccsq = document.getElementById('bccsq');
    var bcai = document.getElementById('bcai');
    var bccq = document.getElementById('bccq');

    var items_count = document.getElementById('items_count_modal');
    const files = pond.getFiles();
    var flag = false;

    if (RFQ_ID.value == '') {
        // console.log("no items");
        fields.RFQ_ID = 1;
        flag = true;
    }
    if (project.value == '') {
        // console.log("no items");
        fields.Project = 1;
        flag = true;
    }
    if (vendor.value == '') {
        // console.log("no items");
        fields.Vendor = 1;
        flag = true;
    }
    if (ship_to_address.value == '') {
        // console.log("no items");
        fields.Ship_to_address = 1;
        flag = true;
    }
    if (Bidder_ID.value == '') {
        // console.log("no vat");
        fields.Bidder_ID = 1;
        flag = true;
    }
    if (submission_deadline.value == '') {
        // console.log("no milestone");
        fields.Submission_Deadline = 1;
        flag = true;
    }
    if (qmbvu.value == '') {
        // console.log("no milestone");
        fields.Quote_must_be_valid_until = 1;
        flag = true;
    }
    if (RFQ_type.value == '') {
        // console.log("no bill_to");
        fields.RFQ_type = 1;
        flag = true;
    }
    if (eqc.value == '') {
        // console.log("no due");
        fields.Expected_quote_currency = 1;
        flag = true;
    }
    if (qrfai.value == '') {
        // console.log("no po");
        fields.Quotes_required_for_all_items = 1;
        flag = true;
    }
    if (bccsq.value == '') {
        // console.log("no date");
        fields.Bidder_can_change_submitted_quote = 1;
        flag = true;
    }
    if (bcai.value == '') {
        // console.log("no number");
        fields.Bidder_can_add_items = 1;
        flag = true;
    }
    if (bccq.value == '') {
        // console.log("no vendor");
        fields.Bidder_can_change_quantity = 1;
        flag = true;
    }
    if (items_count.innerHTML == '0') {
        // console.log("no vendor");
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
                    <div class="col-6 d-flex justify-content-start align-items-center" style="border-right: 2px solid #212529;">
                        <h5 style="margin: 0;">${field.replace(/_/g, ' ')}</h5>
                    </div>
                    <div class="col-6 d-flex justify-content-center align-items-center">
                        <h5 class="text-danger" style="margin: 0;">Not A PDF File!.</h5>
                    </div>
                </div>
                `;
            } else {
                temp += `
                <div class="row mt-2" >
                    <div class="col-6 d-flex justify-content-start align-items-center" style="border-right: 2px solid #212529;">
                        <h5 style="margin: 0;">${field.replace(/_/g, ' ')}</h5>
                    </div>
                    <div class="col-6 d-flex justify-content-center align-items-center">
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

function ReviewRFQ() {
    var RFQ_ID = document.getElementById('RFQ_ID');
    var vendor = document.getElementById('vendor');
    var project = document.getElementById('project');
    var ship_to_address = document.getElementById('ship_to_address');
    var Bidder_ID = document.getElementById('Bidder_ID');
    var submission_deadline = document.getElementById('submission_deadline');
    var qmbvu = document.getElementById('qmbvu');
    var RFQ_type = document.getElementById('RFQ_type');
    var eqc = document.getElementById('eqc');
    var qrfai = document.getElementById('qrfai');
    var bccsq = document.getElementById('bccsq');
    var bcai = document.getElementById('bcai');
    var bccq = document.getElementById('bccq');
    var items_count = document.getElementById('items_count_modal');

    var vendorSelectedOption = vendor.options[vendor.selectedIndex];
    var projectSelectedOption = project.options[project.selectedIndex];
    var RFQ_typeSelectedOption = RFQ_type.options[RFQ_type.selectedIndex];
    var eqcSelectedOption = eqc.options[eqc.selectedIndex];
    var qrfaiSelectedOption = qrfai.options[qrfai.selectedIndex];
    var bccsqSelectedOption = bccsq.options[bccsq.selectedIndex];
    var bcaiSelectedOption = bcai.options[bcai.selectedIndex];
    var bccqSelectedOption = bccq.options[bccq.selectedIndex];

    var files = pond.getFiles();

    document.getElementById('view_vendor').innerHTML = vendorSelectedOption.id;
    document.getElementById('view_RFQ_ID').innerHTML = RFQ_ID.value;
    document.getElementById('view_project_name').innerHTML = projectSelectedOption.id;
    document.getElementById('view_ship_to_address').innerHTML = ship_to_address.value;
    document.getElementById('view_bidder_id').innerHTML = Bidder_ID.value;
    document.getElementById('view_submission_deadline').innerHTML = formatDateTime(submission_deadline.value);
    document.getElementById('view_qmbvu').innerHTML = formatDate(qmbvu.value);
    document.getElementById('view_RFQ_Type').innerHTML = RFQ_typeSelectedOption.id;
    document.getElementById('view_eqc').innerHTML = eqcSelectedOption.id;
    document.getElementById('view_qrfai').innerHTML = qrfaiSelectedOption.id;
    document.getElementById('view_bccsq').innerHTML = bccsqSelectedOption.id;
    document.getElementById('view_bcai').innerHTML = bcaiSelectedOption.id;
    document.getElementById('view_bccq').innerHTML = bccqSelectedOption.id;
    document.getElementById('total_items').innerHTML = items_count.innerHTML;
    document.getElementById('total_files').innerHTML = files.length;

    var o = $("#ItemsTbl");
    var temp_items_table = o.bootstrapTable().bootstrapTable('getData');

    var t = $("#RFQItemsTbl");
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

function SubmitRFQ(){
    if(!VerifyRFQ()){
        setTimeout(function () {
            $('#submit_modal').modal({
                backdrop: true,
                keyboard: true,
                focus: true,
                show: true,
            });
            var RFQ_ID = document.getElementById('RFQ_ID');
            var vendor = document.getElementById('vendor');
            var project = document.getElementById('project');
            var ship_to_address = document.getElementById('ship_to_address');
            var Bidder_ID = document.getElementById('Bidder_ID');
            var submission_deadline = document.getElementById('submission_deadline');
            var qmbvu = document.getElementById('qmbvu');
            var RFQ_type = document.getElementById('RFQ_type');
            var eqc = document.getElementById('eqc');
            var qrfai = document.getElementById('qrfai');
            var bccsq = document.getElementById('bccsq');
            var bcai = document.getElementById('bcai');
            var bccq = document.getElementById('bccq');

            var temp_table = $("#ItemsTbl").bootstrapTable().bootstrapTable('getData');
            var files = pond.getFiles();

            // Create FormData object
            const formData = new FormData();
            // Append values to FormData
            formData.append('RFQ_ID', RFQ_ID.value);
            formData.append('vendor', vendor.value);
            formData.append('project', project.value);
            formData.append('ship_to_address', ship_to_address.value);
            formData.append('Bidder_ID', Bidder_ID.value);
            formData.append('submission_deadline', submission_deadline.value);
            formData.append('qmbvu', qmbvu.value);
            formData.append('RFQ_type', RFQ_type.value);
            formData.append('eqc', eqc.value);
            formData.append('qrfai', qrfai.value);
            formData.append('bccsq', bccsq.value);
            formData.append('bcai', bcai.value);
            formData.append('bccq', bccq.value);
            // Append files to FormData
            files.forEach((file, index) => {
                console.log(file.file);
                formData.append(`filepond`, file.file);
            });
            // Append additional data from the table
            temp_table.forEach((row, index) => {
                console.log(row);
                formData.append(`products`, JSON.stringify({
                    'item_number': row.item_number,
                    'product_id': row.product_id,
                    'description': row.description,
                    'category': row.category,
                    'dd_sp': row.dd_sp,
                    'quantity': row.quantity,
                    'uom': row.uom,
                }));
            });
            $.ajax({
                url: '/system/PresalesRFQ/New/Submit/api/',
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
                                    <h5 style="margin: 0;">RFQ ID</h5>
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
                { field: "item_number", title: "Item" },
                { field: "product_id", title: "Product ID" },
                { field: "description", title: "Product Description" },
                { field: "category", title: "Product Category" },
                { field: "dd_sp", title: "Delivery Date/Service Period" },
                { field: "quantity", title: "Quantity" },
                { field: "uom", title: "UOM" },
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
var t = $("#RFQItemsTbl");
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
                { field: "item_number", title: "Item" },
                { field: "product_id", title: "Product ID" },
                { field: "description", title: "Product Description" },
                { field: "category", title: "Product Category" },
                { field: "dd_sp", title: "Delivery Date/Service Period" },
                { field: "quantity", title: "Quantity" },
                { field: "uom", title: "UOM" },
            ],
        });
        t.bootstrapTable("showLoading");
        t.bootstrapTable("load", temp_table);
        t.bootstrapTable("refresh");
        t.bootstrapTable("hideLoading");
    }).trigger('change')


document.getElementById("items_print_selected").addEventListener("click", function () {
    var selectedRows = [];
    selectedRows = $("#RFQItemsTbl").bootstrapTable("getSelections");
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
    $("#RFQItemsTbl thead th").each(function () {
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
