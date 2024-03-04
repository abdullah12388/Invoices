var currentyear =  new Date().getFullYear()
document.getElementById('per_year_from').value = currentyear;
document.getElementById('per_year_to').value = currentyear;

function searchColumnChart(){
    filter_type = document.getElementById('filter_type').value;
    $.ajax({
        url: "/system/Manager/Invoices/Status/column/chart/api/",
        method: "GET",
        dataType: "json",
        data: {
            'filter': filter_type,
            'from': document.getElementById(filter_type+'_from').value,
            'to': document.getElementById(filter_type+'_to').value,
        },
        success: function (t) {
            console.log(t);
            var e = new google.visualization.DataTable();
            e.addColumn("string", "Status"),
            e.addColumn("number", "Count"),
            e.addColumn({ type: "number", role: "annotation" }),
            e.addColumn({ role: 'style' }),
            t.forEach((t) => {
                e.addRow(t);
            });
            var a = new google.visualization.ColumnChart(document.getElementById("InvoiceStatusColumnChart"));
            google.visualization.events.addListener(a, "select", function () {
                const t = a.getSelection();
                if (t && t.length > 0) {
                    const a = t[0].row,
                        o = e.getValue(a, 0);
                    // window.location.href = "/tank/sites/" + o.split(" ")[1] + "/";
                    // console.log(o.split(" ")[1]);
                }
            }),
            a.draw(e, {
                title: "Invoice Count per Status",
                // hAxis: { title: "Tasks", titleTextStyle: { fontSize: 18, color: "#053061", bold: !0, italic: !1 } },
                vAxis: { title: "Count", titleTextStyle: { fontSize: 18, color: "#035061", bold: !0, italic: !1 } },
                legend: { position: "none" },
            });
        },
    });
}


function resetColumnChart(){
    var dateInputs = document.querySelectorAll('.date-inputs');
    dateInputs.forEach(function(child) {
        child.classList.add('d-none');
    });
    document.getElementById('date_filter').value = '';
    document.getElementById('per_time_from').value = '';
    document.getElementById('per_time_to').value = '';
    document.getElementById('per_day_from').value = '';
    document.getElementById('per_day_to').value = '';
    document.getElementById('per_month_from').value = '';
    document.getElementById('per_month_to').value = '';
    document.getElementById('per_year_from').value = currentyear;
    document.getElementById('per_year_to').value = currentyear;
    // all data api
    InvoiceStatusColumnChart();
}


document.getElementById('date_filter').addEventListener('change', function(){
    // Hide all elements with class 'date-inputs'
    var dateInputs = document.querySelectorAll('.date-inputs');
    dateInputs.forEach(function(child) {
        child.classList.add('d-none');
    });

    // Show the selected element based on the value of the dropdown
    if(this.value == 'h'){
        document.getElementById('row_per_time').classList.remove('d-none');
        document.getElementById('filter_type').value = 'per_time';
    }
    if(this.value == 'd'){
        document.getElementById('row_per_day').classList.remove('d-none');
        document.getElementById('filter_type').value = 'per_day';
    }
    if(this.value == 'm'){
        document.getElementById('row_per_month').classList.remove('d-none');
        document.getElementById('filter_type').value = 'per_month';
    }
    if(this.value == 'y'){
        document.getElementById('row_per_year').classList.remove('d-none');
        document.getElementById('filter_type').value = 'per_year';
    }
})


function InvoiceStatusColumnChart() {
    $.ajax({
        url: "/system/Manager/Invoices/Status/column/chart/api/",
        method: "GET",
        dataType: "json",
        success: function (t) {
            console.log(t);
            var e = new google.visualization.DataTable();
            e.addColumn("string", "Status"),
            e.addColumn("number", "Count"),
            e.addColumn({ type: "number", role: "annotation" }),
            e.addColumn({ role: 'style' }),
            t.forEach((t) => {
                e.addRow(t);
            });
            var a = new google.visualization.ColumnChart(document.getElementById("InvoiceStatusColumnChart"));
            google.visualization.events.addListener(a, "select", function () {
                const t = a.getSelection();
                if (t && t.length > 0) {
                    const a = t[0].row,
                        o = e.getValue(a, 0);
                    // window.location.href = "/tank/sites/" + o.split(" ")[1] + "/";
                    // console.log(o.split(" ")[1]);
                }
            }),
            a.draw(e, {
                title: "Invoice Count per Status",
                // hAxis: { title: "Tasks", titleTextStyle: { fontSize: 18, color: "#053061", bold: !0, italic: !1 } },
                vAxis: { title: "Count", titleTextStyle: { fontSize: 18, color: "#035061", bold: !0, italic: !1 } },
                legend: { position: "none" },
            });
        },
    });
}

function InvoiceStatusPieChart() {
    $.ajax({
        url: "/system/Manager/Invoices/Status/pie/chart/api/",
        method: "GET",
        dataType: "json",
        success: function (t) {
            console.log(t);
            var e = new google.visualization.DataTable();
            e.addColumn("string", "Status"),
            e.addColumn("number", "Count"),
            t.forEach((t) => {
                e.addRow(t);
            });
            var a = new google.visualization.PieChart(document.getElementById("InvoiceStatusPieChart"));
            google.visualization.events.addListener(a, "select", function () {
                const t = a.getSelection();
                if (t && t.length > 0) {
                    const a = t[0].row;
                    // companyTablePie(e.getValue(a, 0).split(" ")[0]);
                    // console.log(e.getValue(a, 0).split(" ")[0]);
                    // window.location.href = "/tank/sites/" + e.getValue(a, 0).split(" ")[0] + "/";
                }
            }),
            a.draw(e, { title: "Invoice Count per Status", pieHole: 0.3, colors: ['#343a40', '#28a745', '#dc3545'] });
        },
    });
}


$(function () {
    google.charts.load("current", { packages: ["corechart", "bar"] });
    google.charts.setOnLoadCallback(InvoiceStatusColumnChart);
    google.charts.setOnLoadCallback(InvoiceStatusPieChart);
});


function downloadCharts(chart_id, select_id) {
    var chartElement = document.getElementById(chart_id);
    var selectElement = document.getElementById(select_id);
    if (selectElement.value === 'png') {
        html2canvas(chartElement).then(function (canvas) {
            var chartImage = canvas.toDataURL('image/png');
            var downloadLink = document.createElement('a');
            downloadLink.href = chartImage;
            downloadLink.download = 'GTS_chart_' + (new Date).toLocaleString() + '.png';
            downloadLink.click();
            selectElement.value = "";
        });
    }
    if (selectElement.value === 'pdf') {
        html2canvas(chartElement, { logging: true, allowTaint: true }).then(function (canvas) {
            var chartImage = canvas.toDataURL('image/png');
            var pdf = new jsPDF('landscape', 'mm', 'a4');
            var imgAspectRatio = canvas.width / canvas.height;
            var imgWidth, imgHeight;
            if (imgAspectRatio > 1) {
                imgWidth = pdf.internal.pageSize.getWidth();
                imgHeight = imgWidth / imgAspectRatio;
            } else {
                imgHeight = pdf.internal.pageSize.getHeight();
                imgWidth = imgHeight * imgAspectRatio;
            }
            var xPos = (pdf.internal.pageSize.getWidth() - imgWidth) / 2;
            var yPos = (pdf.internal.pageSize.getHeight() - imgHeight) / 2;
            pdf.addImage(chartImage, 'PNG', xPos, yPos, imgWidth, imgHeight);
            pdf.save('GTS_chart_' + (new Date()).toLocaleString() + '.pdf');
            selectElement.value = "";
        });
    }
}