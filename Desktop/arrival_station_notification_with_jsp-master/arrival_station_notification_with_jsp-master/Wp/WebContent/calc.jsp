<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>지도 보여주기</title>
</head>
<body>
	<div id="map" style="width: 500px; height: 400px;"></div>
	<script type="text/javascript"
		src="//dapi.kakao.com/v2/maps/sdk.js?appkey=86205c1f18bae5c2a1044967acfbb9e7"></script>
	<script type="text/javascript">
		function getUrlParams() { //url 파라미터 얻어오기
			var params = {};
			window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(
					str, key, value) {
				params[key] = value;
			});
			return params;
		}
		window.onload = function() {
			params = getUrlParams();
			var des_x = params.x; //데이터로 넘어온 위도
			var des_y = params.y; //데이터로 넘어온 경도
			var name = params.name;
			var container = document.getElementById('map');
			var options = {
				center : new daum.maps.LatLng(des_x, des_y), //목적지 위치 설정
				level : 5
			};
			var map = new daum.maps.Map(container, options);
			var markerPosition = new daum.maps.LatLng(des_x, des_y); //목적지 위치 설정
			message = '<div style="padding:5px;">목적지</div>';
			displayMarker(markerPosition, message); //목적지 위치 마커표시

			if (navigator.geolocation) {
				// GeoLocation을 이용해서 접속 위치를 얻어옵니다
				navigator.geolocation.getCurrentPosition(function(position) {
					var lat = position.coords.latitude; // 현재 위치의 위도
					var lon = position.coords.longitude; // 현재 위치의 경도          

					var locPosition = new daum.maps.LatLng(lat, lon), // 현재 위치 설정
					message = '<div style="padding:5px;">현재위치</div>'; // 인포윈도우에 표시될 내용
					displayMarker(locPosition, message); // 현재 위치 마커표시

					var circle = new daum.maps.Circle({
						center : new daum.maps.LatLng(lat, lon), //현재 위치를 원의 중심으로 설정
						map : map, // 원을 표시할 지도 객체
						radius : 500, // 원의 반지름 (단위 : m)
						fillColor : 'blue', // 채움 색
						fillOpacity : 0.1, // 채움 불투명도
						strokeWeight : 3, // 선의 두께
						strokeColor : 'blue', // 선 색
						strokeOpacity : 0.0, // 선 투명도 
						strokeStyle : 'solid' // 선 스타일
					});
					circle.setMap(map); //현재 위치에 원 그리기
					var result = computeDistance(lat, lon, des_x, des_y); //거리값
					//alert(result);
					if (result <= 0.5) {
						 setTimeout(function(){alert("다음 역에서 하차하십시오.");},1000);	
						clearTimeout(timer);
					}
				});
			} else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
				var locPosition = new daum.maps.LatLng(33.450701, 126.570667), message = '현재위치를 알 수 없습니다.'
				displayMarker(locPosition, message);
			}
			function computeDistance(lat1, lon1, lat2, lon2) {
				var startLatRads = degreesToRadians(lat1);
				var startLongRads = degreesToRadians(lon1);
				var destLatRads = degreesToRadians(lat2);
				var destLongRads = degreesToRadians(lon2);

				var Radius = 6371; //지구의 반경(km)
				var distance = Math.acos(Math.sin(startLatRads)
						* Math.sin(destLatRads) + Math.cos(startLatRads)
						* Math.cos(destLatRads)
						* Math.cos(startLongRads - destLongRads))
						* Radius;

				return distance;
			}

			function degreesToRadians(degrees) {
				radians = (degrees * Math.PI) / 180;
				return radians;
			}
			function displayMarker(locPosition, message) { //마커 생성함수
				var marker = new daum.maps.Marker({
					map : map,
					position : locPosition
				});
				var iwContent = message, // 인포윈도우에 표시할 내용
				iwRemoveable = true
				var infowindow = new daum.maps.InfoWindow({ //인포윈도우 생성
					content : iwContent,
					removable : iwRemoveable
				});
				infowindow.open(map, marker); // 인포윈도우를 마커위에 표시합니다	 				
				map.setCenter(locPosition); // 지도 중심좌표를 접속위치로 변경합니다
			}
		}
		var timer = setTimeout("location.reload()", 10000);
	</script>
</body>
</html>
