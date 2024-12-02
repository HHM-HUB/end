document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('entryForm');
    const entryList = document.getElementById('entryList');
    const totalBalance = document.getElementById('totalBalance');

    // 从 localStorage 中加载数据
    let entries = JSON.parse(localStorage.getItem('entries')) || [];

    // 计算总余额
    function calculateTotalBalance() {
        let balance = 0;
        entries.forEach(entry => {
            if (entry.type === 'income') {
                balance += entry.amount;
            } else {
                balance -= entry.amount;
            }
        });
        totalBalance.textContent = balance.toFixed(2);
    }

    // 按月分组条目
    function groupEntriesByMonth(entries) {
        const groupedEntries = {};
        entries.forEach(entry => {
            const date = new Date(entry.date);
            const month = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
            if (!groupedEntries[month]) {
                groupedEntries[month] = [];
            }
            groupedEntries[month].push(entry);
        });
        return groupedEntries;
    }

    // 渲染条目列表
    function renderEntries() {
        entryList.innerHTML = '';
        const groupedEntries = groupEntriesByMonth(entries);

        for (const [month, entries] of Object.entries(groupedEntries)) {
            const monthDiv = document.createElement('div');
            monthDiv.className = 'month';

            const monthHeader = document.createElement('div');
            monthHeader.className = 'month-header collapsed';
            monthHeader.innerHTML = `
                <span>${month}</span>
                <span class="arrow">▶</span>
            `;
            monthHeader.addEventListener('click', () => {
                monthDiv.classList.toggle('collapsed');
            });

            const entriesDiv = document.createElement('div');
            entriesDiv.className = 'entries';

            entries.forEach((entry, index) => {
                const entryDiv = document.createElement('div');
                entryDiv.className = 'entry-item';
                entryDiv.innerHTML = `
                    <span>¥${entry.amount.toFixed(2)} - ${entry.description} (${entry.type})</span>
                    <span style="color: ${entry.type === 'expense' ? 'red' : 'green'};">
                        ${entry.type === 'expense' ? '-¥' : '+¥'}${entry.amount.toFixed(2)}
                    </span>
                    <button class="delete-button" data-index="${index}">删除</button>
                `;
                entriesDiv.appendChild(entryDiv);
            });

            monthDiv.appendChild(monthHeader);
            monthDiv.appendChild(entriesDiv);
            entryList.appendChild(monthDiv);
        }

        calculateTotalBalance();

        // 添加删除按钮的点击事件
        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const index = parseInt(e.target.getAttribute('data-index'));
                entries.splice(index, 1);
                localStorage.setItem('entries', JSON.stringify(entries));
                renderEntries();
            });
        });
    }

    // 初始化页面
    renderEntries();

    // 处理表单提交
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const amount = parseFloat(document.getElementById('amount').value);
        const description = document.getElementById('description').value;
        const type = document.getElementById('type').value;
        const date = document.getElementById('date').value;

        if (isNaN(amount) || amount <= 0) {
            alert('请输入有效的金额');
            return;
        }

        const newEntry = { amount, description, type, date };
        entries.push(newEntry);
        localStorage.setItem('entries', JSON.stringify(entries));

        renderEntries();

        // 清空表单
        document.getElementById('amount').value = '';
        document.getElementById('description').value = '';
        document.getElementById('date').value = '';
    });
});
