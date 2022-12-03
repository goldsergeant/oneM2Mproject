const $drop = document.querySelector(".dropBox");
const $title = document.querySelector(".dropBox h1");
var file;
const url=window.location.href+"progress";

function getProgress(){
    	
    $.ajax({
        type : "GET", //전송방식을 지정한다 (POST,GET)
        url : url,//호출 URL을 설정한다. GET방식일경우 뒤에 파라티터를 붙여서 사용해도된다.
        dataType : "text",//호출한 페이지의 형식이다. xml,json,html,text등의 여러 방식을 사용할 수 있다.
        error : function(){
            if(url.indexOf('process')>-1){
                window.location.href=url.split('/')[0];
            }
            },
        success : function(Parse_data){
            $("#Parse_Area").html(Parse_data); //div에 받아온 값을 넣는다.
            document.getElementById('progress').value=Parse_data;
            if(Parse_data>=100){
                clearInterval(interval);
            }
        }
         
    });
}
let interval;

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
    interval=setInterval(getProgress,1000);

    let files=document.getElementById('file').files;
    let flag=0;
    for(const f of files){
        if(f.name.endsWith('docx')==false)
            flag=1;
    }
    if(flag==0){
        document.getElementById('progressBox').style.visibility="visible";
    }
})