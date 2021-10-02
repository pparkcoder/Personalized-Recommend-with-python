<%@ page import="login.UserDAO"%>
<%@ page import="java.sql.*"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>로그인 체크</title>
</head>
<body>
	<%
		request.setCharacterEncoding("UTF-8");
		String idData = request.getParameter("id"); //로그인 페이지에서 입력한 id
		String psData = request.getParameter("ps"); //로그인 페이지에서 입력한 ps
		int result = UserDAO.loginCheck(idData, psData);

		if (result == 1) { //로그인 성공
			out.println("<script>");
			out.println("alert('로그인 되었습니다.')");
			out.println("location.href='select.jsp'");
			out.println("</script>");
		} else if (result == 0) { //비밀번호 불일치			
			out.println("<script>");
			out.println("alert('비밀번호가 틀렸습니다.')");
			out.println("location.href='loginFront.jsp'");
			out.println("</script>");
		} else { //아이디 존재X
			out.println("<script>");
			out.println("alert('" + idData + "는 존재하지 않는 아이디 입니다.')");
			out.println("location.href='loginFront.jsp'");
			out.println("</script>");
		}
	%>
</body>
</html>