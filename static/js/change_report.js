const selectAllReports = Array.from(document.querySelectorAll('span.reports'));

function addListenersToSelectAllReports() {
    selectAllReports.forEach((item) => {
        item.addEventListener('click', (evt => changeData(item)));
    })
    selectAllReports[0].classList.add('active')
}

function changeData(report) {
    const old_report = document.querySelector('span.active');
    document.getElementById('income').textContent = report.getAttribute('income') + ' р';
    document.getElementById('expenses').textContent = report.getAttribute('expenses') + ' р';
    document.getElementById('total').textContent = report.getAttribute('total') + ' р';
    createTable(report)
    if (old_report) {
        old_report.classList.remove('active');
    }
    report.classList.add('active');
    del()
}

function createTable(report){
    const table = document.getElementById('table-operations');
    const operations = JSON.parse(document.getElementById('jsonData').getAttribute('data-json'));
    let HTML = '<span class="sub-heading mt-2">Совершенные операции</span><table>';
    operations.forEach((item) => {
        if (report.getAttribute('articles').includes(item.article) &&
            parseInt(report.getAttribute('start_date').replace(/-/g,""),10)
            <= parseInt(item.date.replace(/-/g,""),10) && parseInt(item.date.replace(/-/g,""),10)
            <= parseInt(report.getAttribute('end_date').replace(/-/g,""),10)
        ) {
            HTML += item.is_purchase ?
                '<tr><td class="chart-label expenses">' + item.amount + '</td><td class="chart-label pl-4">' + item.article__name + '</td></tr>':
                '<tr><td class="chart-label income">' + item.amount + '</td><td class="chart-label pl-4">' + item.article__name + '</td></tr>';
        }
    })
    HTML += '</table>';
    table.innerHTML = HTML;
}

const ModalBackground = document.querySelector('.container');

ModalBackground.addEventListener('click', (evt) => {
    const button = document.getElementById('del-div')
    if (button.style.display === 'flex') {
        button.style.display = 'none';
    }
})

addListenersToSelectAllReports();