// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const resumeForm = document.getElementById('resumeForm');

    resumeForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const phone = document.getElementById('phone').value;
        const position = document.getElementById('position').value;
        const joinDate = document.getElementById('joinDate').value;

        const formData = new FormData();
        formData.append('name', name);
        formData.append('phone', phone);
        formData.append('position', position);
        formData.append('joinDate', joinDate);

        try {
            const response = await fetch('https://hhm-hub.github.io/end/jianli2/src/index.html', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                alert('简历提交成功！');
                resumeForm.reset();
            } else {
                alert('简历提交失败，请稍后再试。');
            }
        } catch (error) {
            console.error('网络错误:', error);
            alert('网络错误，请检查您的网络连接。');
        }
    });
});

