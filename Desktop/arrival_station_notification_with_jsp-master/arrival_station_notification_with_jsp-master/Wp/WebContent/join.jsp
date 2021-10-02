<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>회원가입</title>
</head>
<body>
<h1>내려내려 회원가입 페이지 입니다.</h1><br/><br/>
<form action="joincheck.jsp" method="post">
	아이디 : <input type = "text" name ="id" maxlength="20"/><br/><br/>
	비밀번호  : <input type = "password" name = "ps" maxlength = "20"/><br/><br/><br/>
	<input type = "submit" value = "회원가입"/> 	
</form>
</body>
</html>