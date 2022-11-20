const $drop = document.querySelector(".dropBox");
const $title = document.querySelector(".dropBox h1");
var file;

// 드래그한 파일 객체가 해당 영역에 놓였을 때
$drop.ondrop = (e) => {
    e.preventDefault();
    $drop.className = "dropBox";

    // 파일 리스트
    const files = [...e.dataTransfer?.files];
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
//파일을 떨어뜨렸을때
$drop.addEventListener('drop', function (e) {
    e.preventDefault();
    console.log('drop');
    console.dir(e.dataTransfer);

    file = e.dataTransfer.files[0];
    console.dir(file);
    let p=document.createElement('p');
    p.innerHTML=file.name;
    $drop.appendChild(p);
    this.style.textAlign = "center";
    this.removeChild(document.getElementById('btn-choose'));
    document.getElementById('file').files=e.dataTransfer.files;
})

document.getElementById('btn-choose').addEventListener('click',(e)=>{
    e.preventDefault();
    document.getElementById('file').click();
});
function changeValue(obj) {
    file=obj.files[0];
    let p=document.createElement('p');
    p.innerHTML=file.name;
    $drop.appendChild(p);
    $drop.removeChild(document.getElementById('btn-choose'));
    $drop.style.textAlign="center";
}

document.getElementById('upload').addEventListener('click',(e)=>{
    let files=document.getElementById('file').files;
    let flag=0;
    for(const f of files){
        if(f.name.endsWith('docx')==false)
            flag=1;
    }
    if(flag==0){
        let p=document.createElement('p');
        p.setAttribute('class','process');
        p.innerHTML='please wait one minute';
        console.log('실행');
        document.body.insertBefore(p,document.body.firstChild);
    }
})