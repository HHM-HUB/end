let currentBalance = 0;
let recordList = [];

// 从 localStorage 加载数据
function loadFromLocalStorage() {
    const savedData = localStorage.getItem('savingsAppData');
    if (savedData) {
        const { balance, records } = JSON.parse(savedData);
        currentBalance = balance;
        recordList = records;
        document.getElementById('currentBalance').textContent = currentBalance.toFixed(2);
        updateRecordList();
    }
}

// 保存数据到 localStorage
function saveToLocalStorage() {
    const data = {
        balance: currentBalance,
        records: recordList
    };
    localStorage.setItem('savingsAppData', JSON.stringify(data));
}

function deposit() {
    const amountInput = document.getElementById('amount');
    const amount = parseFloat(amountInput.value);

    if (!isNaN(amount) && amount > 0) {
        currentBalance += amount;
        document.getElementById('currentBalance').textContent = currentBalance.toFixed(2);

        // 添加存款记录
        const date = new Date().toLocaleString();
        recordList.push({ amount, date });
        console.log('存款记录:', recordList); // 调试信息
        updateRecordList();
        saveToLocalStorage(); // 保存数据

        amountInput.value = '';
    } else {
        alert('请输入有效的正数金额');
    }
}

function updateRecordList() {
    const recordListElement = document.getElementById('recordList');
    recordListElement.innerHTML = '';

    recordList.forEach(record => {
        const li = document.createElement('li');
        li.textContent = `存入 ${record.amount.toFixed(2)} 元 - ${record.date}`;
        recordListElement.appendChild(li);
    });
}

function toggleRecords() {
    const recordListElement = document.getElementById('recordList');
    if (recordListElement.style.display === 'none') {
        recordListElement.style.display = 'block';
    } else {
        recordListElement.style.display = 'none';
    }
}

function exportRecords() {
    console.log('导出记录:', recordList); // 调试信息

    const data = [
        ['金额', '时间'],
        ...recordList.map(record => [record.amount, record.date])
    ];

    const ws = XLSX.utils.aoa_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, '存款记录');

    XLSX.writeFile(wb, '存款记录.xlsx');
}

// 页面加载时加载数据
window.onload = loadFromLocalStorage;
