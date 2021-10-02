<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.sql.*" %>
<%@ page import="login.UserDAO" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>회원가입 체크</title>
</head>
<body>
<%
	request.setCharacterEncoding("UTF-8");
	String idData = request.getParameter("id");
	String psData = request.getParameter("ps");
	int result = UserDAO.insert(idData, psData);
	
	if (result==-1) { //회원가입이 불가능한 경우
		out.println("<script>");
		out.println("alert('존재하는 아이디 입니다.')");
		out.println("location.href='join.jsp'");
		out.println("</script>");
	}
	else{
		out.println("<script>");
		out.println("alert('" + idData + "님 가입이 완료되었습니다.')");
		out.println("location.href='loginFront.jsp'");
		out.println("</script>");
	}
%>
</body>
</html>