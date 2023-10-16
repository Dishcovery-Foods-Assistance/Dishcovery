
// 원을 추가하는 함수

function addCircle() {
    // 원의 요소를 생성합니다.
    const circle = document.createElement("div");
    circle.classList.add("circle");
    document.getElementById("mealList").appendChild(circle); // mealList 엘리먼트 가져오고 mealList에 원을 추가
}

// 버튼 클릭 이벤트에 함수를 연결합니다.
const addButton = document.getElementById("searchButton");
addButton.addEventListener("click", function(event){
    if (document.getElementById("searchInput").value.trim() !== "") {
        // 입력된 텍스트가 있을 때만 4x4 그리드로 원을 추가합니다.
        addCircles();
    }

});

// Enter 키 이벤트 처리
const inputField = document.getElementById("searchInput");
inputField.addEventListener("keyup", function (event) {
    if (event.key === "Enter" && inputField.value.trim() !== "") {
        // 입력된 텍스트가 있고 Enter 키를 누를 경우 4x4 그리드로 원을 추가합니다.
        addCircles();
    }
});

// 원을 한 번에 4x4로 생성하는 함수
function addCircles() {
    const mealList = document.getElementById("mealList");
    mealList.innerHTML = ""; // mealList 내용 초기화

    for (let i = 0; i < 4; i++) {
        const row = document.createElement("div");
        row.classList.add("row");

        for (let j = 0; j < 4; j++) {
            const circle = document.createElement("div");
            circle.classList.add("circle");
            row.appendChild(circle);
        }

        mealList.appendChild(row);
    }
}