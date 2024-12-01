// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const adminAddForm = document.getElementById('adminAddForm');
    const employeeSubmitForm = document.getElementById('employeeSubmitForm');
    const employeeTable = document.getElementById('employeeTable').getElementsByTagName('tbody')[0];
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const positionFilter = document.getElementById('positionFilter');
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');

    // 用于存储员工数据的数组
    let employees = [];

    // 管理员添加新员工
    adminAddForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('adminName').value;
        const phone = document.getElementById('adminPhone').value;
        const position = document.getElementById('adminPosition').value;
        const joinDate = document.getElementById('adminJoinDate').value;
        const resumeFile = document.getElementById('adminResume').files[0];

        if (resumeFile) {
            const reader = new FileReader();
            reader.onloadend = () => {
                const newEmployee = { name, phone, position, joinDate, resume: reader.result };
                employees.push(newEmployee);
                renderEmployees();
                adminAddForm.reset();
            };
            reader.readAsDataURL(resumeFile);
        } else {
            alert('请选择一个简历文件');
        }
    });

    // 员工提交信息
    employeeSubmitForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('employeeName').value;
        const phone = document.getElementById('employeePhone').value;
        const position = document.getElementById('employeePosition').value;
        const joinDate = document.getElementById('employeeJoinDate').value;
        const resumeFile = document.getElementById('employeeResume').files[0];

        if (resumeFile) {
            const reader = new FileReader();
            reader.onloadend = () => {
                const newEmployee = { name, phone, position, joinDate, resume: reader.result };
                employees.push(newEmployee);
                renderEmployees();
                employeeSubmitForm.reset();
            };
            reader.readAsDataURL(resumeFile);
        } else {
            alert('请选择一个简历文件');
        }
    });

    // 渲染员工信息到表格
    function renderEmployees(filteredEmployees = employees) {
        employeeTable.innerHTML = '';
        filteredEmployees.forEach((employee, index) => {
            const row = employeeTable.insertRow();
            row.insertCell(0).textContent = employee.name;
            row.insertCell(1).textContent = employee.phone;
            row.insertCell(2).textContent = employee.position;
            row.insertCell(3).textContent = employee.joinDate;

            const resumeCell = row.insertCell(4);
            const resumeLink = document.createElement('a');
            resumeLink.href = employee.resume;
            resumeLink.target = '_blank';
            resumeLink.textContent = '查看简历';
            resumeCell.appendChild(resumeLink);

            const actionCell = row.insertCell(5);
            const editButton = document.createElement('button');
            editButton.textContent = '编辑';
            editButton.onclick = () => editEmployee(index);
            actionCell.appendChild(editButton);

            const deleteButton = document.createElement('button');
            deleteButton.textContent = '删除';
            deleteButton.onclick = () => deleteEmployee(index);
            actionCell.appendChild(deleteButton);
        });
    }

    // 编辑员工信息
    function editEmployee(index) {
        const employee = employees[index];
        const newName = prompt('请输入新的姓名', employee.name);
        const newPhone = prompt('请输入新的手机号码', employee.phone);
        const newPosition = prompt('请输入新的职位', employee.position);
        const newJoinDate = prompt('请输入新的入职日期', employee.joinDate);

        if (newName && newPhone && newPosition && newJoinDate) {
            employee.name = newName;
            employee.phone = newPhone;
            employee.position = newPosition;
            employee.joinDate = newJoinDate;
            renderEmployees();
        }
    }

    // 删除员工信息
    function deleteEmployee(index) {
        if (confirm('确定要删除此员工吗？')) {
            employees.splice(index, 1);
            renderEmployees();
        }
    }

    // 搜索员工
    function filterEmployees() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedPosition = positionFilter.value.toLowerCase();
        const start = startDate.value ? new Date(startDate.value) : null;
        const end = endDate.value ? new Date(endDate.value) : null;

        const filteredEmployees = employees.filter(employee => {
            const nameMatch = employee.name.toLowerCase().includes(searchTerm);
            const phoneMatch = employee.phone.toLowerCase().includes(searchTerm);
            const positionMatch = selectedPosition === '' || employee.position.toLowerCase() === selectedPosition;
            const dateMatch = !start || !end || (new Date(employee.joinDate) >= start && new Date(employee.joinDate) <= end);

            return (nameMatch || phoneMatch) && positionMatch && dateMatch;
        });

        renderEmployees(filteredEmployees);
    }

    // 搜索按钮点击事件
    searchButton.addEventListener('click', () => {
        filterEmployees();
    });

    // 搜索框输入时自动搜索
    searchInput.addEventListener('input', () => {
        filterEmployees();
    });

    // 职位筛选变化时自动搜索
    positionFilter.addEventListener('change', () => {
        filterEmployees();
    });

    // 入职日期筛选变化时自动搜索
    startDate.addEventListener('change', () => {
        filterEmployees();
    });

    endDate.addEventListener('change', () => {
        filterEmployees();
    });
});
