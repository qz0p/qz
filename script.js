// 봉투가 한번 열리면 닫히지 않도록 클래스 추가
document.querySelector('.envelope-wrapper').addEventListener('click', function() {
    if (!this.classList.contains('opened')) {
        this.classList.add('opened');  // 봉투 열기
        setTimeout(() => {
            const card = document.querySelector('.card');
            card.classList.add('show');  // 카드 보이게 하는 클래스 추가
            card.style.opacity = 1; // 카드가 보이게 설정
            card.style.transform = 'translateY(-200%)'; // 카드가 위로 올라옴
        }, 1200);  // 봉투가 열리는 시간과 맞추기 위해 1.2초 후에 카드 애니메이션 시작
    }
});

// 눈 내리는 효과 생성
document.addEventListener('DOMContentLoaded', function() {
    // 눈투 클릭 이벤트
    document.querySelector('.envelope-wrapper').addEventListener('click', function() {
        if (!this.classList.contains('opened')) {
            this.classList.add('opened');  // 봉투 열기
            const card = document.querySelector('.card');
            card.classList.add('show');  // 카드 보이게 하는 클래스 추가
            card.style.opacity = 1; // 카드가 보이게 설정
            // 카드가 봉투에서 위로 나오는 애니메이션
            card.style.transform = 'translateY(-100%)'; // 카드가 위로 올라옴
        }
    });

    // 카드 클릭 이벤트
    document.querySelector('.card').addEventListener('click', function(e) {
        e.stopPropagation(); // 카드 클릭 시 이벤트 전파 방지
        if (!this.classList.contains('expanded')) {
            this.classList.add('expanded'); // 카드 확장
            this.style.transform = 'translateY(-40%) scale(1.3)'; // 카드가 위로 올라가면서 크기 3배로 확대
            this.style.transition = 'transform 0.5s ease'; // 크기 확대 애니메이션

            // 카드가 펼쳐진 후에 내용이 보이도록 지연
            setTimeout(() => {
                const cardInside = this.querySelector('.card-inside');
                cardInside.style.opacity = 1; // 카드가 펼쳐질 때 내용 보이게
            }, 500); // 카드가 펼쳐진 후에 내용이 보이도록 지연

            // 드래그 기능 추가
            let isDragging = false;
            let startY;

            this.addEventListener('mousedown', (e) => {
                isDragging = true;
                startY = e.clientY - this.getBoundingClientRect().top; // 시작 위치 저장
                this.style.transition = 'none'; // 드래그 중에는 전환 효과 제거
            });

            const mouseMoveHandler = (e) => {
                if (isDragging) {
                    this.style.position = 'absolute'; // 카드의 위치를 절대 위치로 설정
                    this.style.top = e.clientY - startY + 'px'; // 카드 위치 업데이트
                }
            };

            document.addEventListener('mousemove', mouseMoveHandler);

            document.addEventListener('mouseup', () => {
                isDragging = false; // 드래그 종료
                this.style.transition = 'transform 0.5s ease'; // 전환 효과 복원
                document.removeEventListener('mousemove', mouseMoveHandler); // 이벤트 리스너 제거
            });
        }
    });

    // 배경 클릭 이벤트 (카드가 펼쳐진 상태에서 아무 동작도 하지 않음)
    document.querySelector('.overlay').addEventListener('click', function() {
        // 아무 동작도 하지 않음
    });

    // 눈송이를 생성하는 함수
    function createSnowflake() {
        const snowflakeContainer = document.querySelector('.snow'); // 눈송이를 추가할 요소
        if (!snowflakeContainer) {
            console.error('눈송���를 추가할 요소가 없습니다.');
            return; // 요소가 없으면 함수 종료
        }

        const snowflake = document.createElement('div');
        snowflake.classList.add('snowflake');

        // 랜덤한 크기 설정 (1px에서 5px 사이)
        const size = Math.random() * 7 + 1; // 1px에서 5px 사이의 크기
        snowflake.style.width = size + 'px';
        snowflake.style.height = size + 'px';

        snowflake.style.left = Math.random() * window.innerWidth + 'px'; // 랜덤한 위치
        snowflake.style.animationDuration = Math.random() * 3 + 2 + 's'; // 랜덤한 애니메이션 시간
        snowflakeContainer.appendChild(snowflake); // 눈송이 추가
    }

    // 눈송이 생성 주기 설정
    setInterval(createSnowflake, 200); // 0.5초마다 눈송이 생성
});

// 화 크기가 변경될 때도 속 작동하도록
window.addEventListener('resize', () => {
    const snowflakes = document.querySelectorAll('.snowflake');
    snowflakes.forEach(snowflake => {
        snowflake.style.left = Math.random() * window.innerWidth + 'px';
    });
});

// 반짝이는 별 효과 추가
function createStars() {
    for(let i = 0; i < 50; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = `${Math.random() * 100}vw`;
        star.style.top = `${Math.random() * 100}vh`;
        star.style.animationDelay = `${Math.random() * 3}s`;
        document.body.appendChild(star);
    }
}

createStars();

