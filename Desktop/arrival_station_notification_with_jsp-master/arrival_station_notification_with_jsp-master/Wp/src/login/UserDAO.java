package login;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

public class UserDAO { // 로그인체크,회원가입
	private String userID;
	private String userPassword;

	public String getUserID() {
		return userID;
	}

	public void setUserID(String userID) {
		this.userID = userID;
	}

	public String getUserPassword() {
		return userPassword;
	}

	public void setUserPassword(String userPassword) {
		this.userPassword = userPassword;
	}

	// 데이터베이스 연결은 basic.getMySQLConnection()
	public static int loginCheck(String idData, String psData) {
		try {
			Connection conn = basic.getMySQLConnection();
			Statement st = conn.createStatement();
			ResultSet rs = st.executeQuery("Select * from user WHERE id='" + idData + "'");

			if (rs.next()) { // 아이디(idData)가 DB와 일치하고
				if (rs.getString("password").equals(psData)) {
					return 1; // 비밀번호(psData)가 DB와 일치할 경우
				} else {
					return 0;// 비밀번호(psData)가 DB와 일치하지 않을 경우
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return -1; // 아이디가 존재하지 않는 경우
	}

	public static int insert(String idData, String psData) {
		try {
			int num = loginCheck(idData, psData);
			if (num == -1) {// 회원가입이 가능한 경우
				Connection conn = basic.getMySQLConnection();
				Statement st = conn.createStatement();
				return st.executeUpdate("Insert into user(id,password) values('" + idData + "','" + psData + "')");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return -1; // 아이디가 존재하여 가입이 불가능한 경우
	}
}
