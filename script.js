let schedules = [];

function addSchedule() {
    const scheduleInput = document.getElementById('scheduleInput');
    const dateInput = document.getElementById('dateInput');
    const schedule = scheduleInput.value.trim();
    const date = dateInput.value;

    if (schedule && date) {
        schedules.push({ schedule, date });
        updateScheduleList();
        scheduleInput.value = '';
        dateInput.value = '';
    } else {
        alert('일정과 날짜를 모두 입력해주세요.');
    }
}

function updateScheduleList() {
    const list = document.getElementById('scheduleList');
    list.innerHTML = '';
    schedules.sort((a, b) => new Date(a.date) - new Date(b.date));
    schedules.forEach((item, index) => {
        list.innerHTML += `<li>${item.date}: ${item.schedule}</li>`;
    });
}