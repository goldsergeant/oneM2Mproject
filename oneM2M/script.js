const $drop = document.querySelector(".dropBox");
const $title = document.querySelector(".dropBox h1");

// 드래그한 파일 객체가 해당 영역에 놓였을 때
$drop.ondrop = (e) => {
    e.preventDefault();
    $drop.className = "dropBox";

    // 파일 리스트
    const files = [...e.dataTransfer?.files];

    $title.innerHTML = files.map(v => v.name).join("<br>");
}

// ondragover 이벤트가 없으면 onDrop 이벤트가 실핻되지 않습니다.
$drop.ondragover = (e) => {
    e.preventDefault();
}

// 드래그한 파일이 최초로 진입했을 때
$drop.ondragenter = (e) => {
    e.preventDefault();

    $drop.classList.add("active");
}

// 드래그한 파일이 영역을 벗어났을 때
$drop.ondragleave = (e) => {
    e.preventDefault();

    $drop.classList.remove("active");
}

$drop.addEventListener('drop', function (e) {
    e.preventDefault();
    console.log('drop');
    console.dir(e.dataTransfer);

    var data = e.dataTransfer.files[0];
    console.dir(data);
    $drop.innerHTML = "<p>" + e.dataTransfer.files[0].name + "</p>";
    this.style.textAlign = "center";

})

document.getElementById('btn-upload').addEventListener('click',(e)=>{
    e.preventDefault();
    console.log('버튼 클릭');
    document.getElementById('file').click();
});
function changeValue(obj) {
    var file=obj.files[0].name;
    $drop.innerHTML = "<p>" + file + "</p>";
    $drop.style.textAlign = "center";
    $drop.style.textAlign="center";
}