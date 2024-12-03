document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recordForm');
    const tableBody = document.querySelector('#recordsTable tbody');

    // 加载已保存的记录
    loadRecords();

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        addRecord();
    });

    function addRecord() {
        const date = document.getElementById('date').value;
        const weight = document.getElementById('weight').value;

        if (date && weight) {
            const record = { date, weight };
            const records = getSortedRecords([...getRecords(), record]);

            // 清空表格
            tableBody.innerHTML = '';

            // 重新添加记录
            records.forEach(record => {
                const row = createRow(record);
                tableBody.appendChild(row);
            });

            // 保存记录到 Local Storage
            saveRecords(records);

            // 清空输入框
            document.getElementById('date').value = '';
            document.getElementById('weight').value = '';
        }
    }

    function deleteRecord(row) {
        const date = row.querySelector('td').textContent;
        const records = getRecords().filter(record => record.date !== date);

        // 清空表格
        tableBody.innerHTML = '';

        // 重新添加记录
        records.forEach(record => {
            const row = createRow(record);
            tableBody.appendChild(row);
        });

        // 保存记录到 Local Storage
        saveRecords(records);
    }

    function createRow(record) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${record.date}</td>
            <td>${record.weight} kg</td>
            <td><button>删除</button></td>
        `;

        // 绑定删除按钮的点击事件
        const deleteButton = row.querySelector('button');
        deleteButton.addEventListener('click', () => deleteRecord(row));

        return row;
    }

    function saveRecords(records) {
        localStorage.setItem('records', JSON.stringify(records));
    }

    function loadRecords() {
        const records = getSortedRecords(getRecords());
        records.forEach(record => {
            const row = createRow(record);
            tableBody.appendChild(row);
        });
    }

    function getRecords() {
        return JSON.parse(localStorage.getItem('records')) || [];
    }

    function getSortedRecords(records) {
        return records.sort((a, b) => new Date(a.date) - new Date(b.date));
    }
});
