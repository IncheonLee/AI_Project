// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function() {
    // 툴팁 초기화 (Bootstrap)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 팝오버 초기화 (Bootstrap)
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 메시지 자동 스크롤
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // 날짜 필터 초기화
    initDateFilters();
});

// 날짜 필터 초기화 함수
function initDateFilters() {
    const dateFilters = document.querySelectorAll('.date-filter');
    
    dateFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 활성 필터 클래스 제거
            dateFilters.forEach(f => f.classList.remove('active'));
            
            // 현재 필터에 활성 클래스 추가
            this.classList.add('active');
            
            // 필터링 로직 구현
            const filterType = this.getAttribute('data-filter');
            filterItems(filterType);
        });
    });
}

// 항목 필터링 함수
function filterItems(filterType) {
    const items = document.querySelectorAll('.filterable-item');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    const lastWeek = new Date(today);
    lastWeek.setDate(lastWeek.getDate() - 7);
    
    items.forEach(item => {
        const dateStr = item.getAttribute('data-date');
        if (!dateStr) return;
        
        const itemDate = new Date(dateStr);
        itemDate.setHours(0, 0, 0, 0);
        
        switch(filterType) {
            case 'today':
                item.style.display = itemDate.getTime() === today.getTime() ? '' : 'none';
                break;
            case 'yesterday':
                item.style.display = itemDate.getTime() === yesterday.getTime() ? '' : 'none';
                break;
            case 'week':
                item.style.display = itemDate >= lastWeek ? '' : 'none';
                break;
            default:
                item.style.display = '';
        }
    });
}

// 타임스탬프를 날짜 형식으로 변환하는 함수
function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString();
}

// 할 일 완료 상태 토글 함수
function toggleTaskStatus(taskId, element) {
    const checkbox = element.querySelector('input[type="checkbox"]');
    const taskText = element.querySelector('.task-text');
    
    // 체크박스 상태 변경
    checkbox.checked = !checkbox.checked;
    
    // 텍스트 스타일 변경
    if (checkbox.checked) {
        taskText.classList.add('text-decoration-line-through', 'text-muted');
    } else {
        taskText.classList.remove('text-decoration-line-through', 'text-muted');
    }
    
    // AJAX 요청으로 서버에 상태 변경 전송
    fetch(`/toggle_task/${taskId}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            console.error('상태 변경 실패');
            // 실패 시 체크박스 상태 원복
            checkbox.checked = !checkbox.checked;
            if (checkbox.checked) {
                taskText.classList.add('text-decoration-line-through', 'text-muted');
            } else {
                taskText.classList.remove('text-decoration-line-through', 'text-muted');
            }
        }
    })
    .catch(error => {
        console.error('에러:', error);
    });
} 