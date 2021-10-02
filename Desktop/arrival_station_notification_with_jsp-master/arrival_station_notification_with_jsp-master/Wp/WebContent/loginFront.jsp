<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>로그인</title>
</head>
<body>
<h1>내려내려 로그인 페이지 입니다.</h1><br/><br/>
<form action="check.jsp" method="post">
	아이디 : <input type = "text" name ="id" maxlength="20"/><br/><br/>
	비밀번호  : <input type = "password" name = "ps" maxlength = "20"/><br/><br/><br/>
	<input type = "submit" value = "로그인"/> &nbsp;&nbsp;
	<input type = "button" value = "회원가입" onclick="location.href='join.jsp'"/>	
</form>
</body>
</html>