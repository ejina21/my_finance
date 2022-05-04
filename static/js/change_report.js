const selectAllReports = Array.from(document.querySelectorAll('span.reports'));

function addListenersToSelectAllReports() {
    selectAllReports.forEach((item) => {
        item.addEventListener('click', (evt => openPopup(item)));
    })
}

function openPopup(report) {
    const old_report = document.querySelector('span.active');
    const table = document.getElementById('table-operations');
    document.getElementById('income').textContent = report.getAttribute('income') + ' р';
    document.getElementById('expenses').textContent = report.getAttribute('expenses') + ' р';
    document.getElementById('total').textContent = report.getAttribute('total') + ' р';
    const operations = JSON.parse(document.getElementById('jsonData').getAttribute('data-json'));
    let HTML = '<span class="sub-heading mt-2">Совершенные операции</span><table>';
    operations.forEach((item) => {
        if (parseInt(report.getAttribute('start_date').replace(/-/g,""),10)
            <= parseInt(item.date.replace(/-/g,""),10) && parseInt(item.date.replace(/-/g,""),10)
            <= parseInt(report.getAttribute('end_date').replace(/-/g,""),10)
        ) {
            HTML += '<tr><td class="chart-label">' + item.amount + '</td><td class="chart-label pl-4">' + item.article__name + '</td></tr>';
        }
    })
    HTML += '</table>';
    table.innerHTML = HTML;
    if (old_report) {
        old_report.classList.remove('active');
    }
    report.classList.add('active');
}

addListenersToSelectAllReports();