<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="css/bootstrap.css">
<title>역 검색 페이지</title>
<script src="http://code.jquery.com/jquery-3.1.1.min.js"></script>
<script src="js/bootstrap.js"></script>
<script type="text/javascript">
	var request = new XMLHttpRequest(); //웹사이트에 요청을 보내는 객체
	function searchFunction() {
		request.open("Post","./StationSearchServlet?stationName="+ encodeURIComponent(document.getElementById("stationName").value), true); 
		//encodeURIComponent - 보내는값을 utf-8으로 인코딩해서 보냄
		//id가 stationName인 것을 인코딩하여 서블릿의 파라미터로 넘긴다
		//첫번째 파라미터 - http 요구 방식(get,post) , 두번째 파라미터 - 요구하고자 하는 url , 세번째 파라미터 - 비동기시 true 동기시 false
		request.onreadystatechange = searchProcess; //open이 성공적으로 끝나면 searchProcess실행
		//요청에 대한 응답을 받았을 때 실행할 함수를 지정 , 지정이기 때문에 어떠한 변수도 전달하지 않는다
		//요청시에 open과 send를 사용
		request.send(null);
	}
	function searchProcess() {
		var table = document.getElementById("ajaxTable");
		table.innerHTML = ""; //빈공간으로 초기화
		if (request.readyState = 4 && request.status == 200) { 
			//통신이 성공적으로 이루어진 경우 ,서버로 모든 응답을 받았으면 XMLHttpRequest.DONE=4로 정의되어 있음
			//상태값 검사가 끝나면 HTTP 응답상태를 검사 ,기본적으로 200으로 설정되어 있음
			var object = eval('(' + request.responseText + ')'); 
			//request.responseText = json type , 서버의 응답을 텍스트 문자열로 변환
			//eval 함수를 사용하면 String 형태의 js 코드를 동적으로 실행 가능
			var result = object.result; //json에서 key값인 result를 가져온다
			for (var i = 0; i < result.length; i++) {
				var row = table.insertRow(0); //0 - 상단부터 추가 
				var j = 0;
				for (var j = 0; j < result[i].length; j++) {
					var cell = row.insertCell(j); //j - 인덱스
					cell.innerHTML = result[i][j].value;
				}
				var str = "목적지 설정";
				var re = str.link("http://localhost:8080/Wp/calc.jsp?x="+ result[i][2].value + "&y=" + result[i][3].value + "&name=" + result[i][1].value);
				row.insertCell(result[i].length).innerHTML = re; //한 행의 끝에 목적지 설정 버튼 넣어주기
			}
		}
	}
	window.onload = function() { //로딩되면 바로 실행 (초기화면에 바로 역 리스트 보여주기)
		searchFunction();
	}
</script>
</head>
<body>
	<br>
	<div class="container">
		<div class="form-group row pull-right">
			<div class="col-xs-8">
				<input class="form-control" id="stationName"
					onkeyup="searchFunction()" type="text" size=20>
			</div>
			<div class="col-xs-2">
				<button class="btn btn-primary" onclick="searchFunction();"
					type="button">검색</button>
			</div>
		</div>
		<table class="table"
			style="text-align: center; border: 1px solid #dddddd">
			<thead>
				<tr>
					<th style="background-color: #fafafa; text-align: center;">호선</th>
					<th style="background-color: #fafafa; text-align: center;">역
						이름</th>
					<th style="background-color: #fafafa; text-align: center;">위도</th>
					<th style="background-color: #fafafa; text-align: center;">경도</th>
					<th style="background-color: #fafafa; text-align: center;">설정</th>
				</tr>
			</thead>
			<tbody id="ajaxTable">
			</tbody>
		</table>
	</div>
</body>
</html>