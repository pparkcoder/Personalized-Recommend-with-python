package login;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class basic {
	static String jdbcDriver = "com.mysql.jdbc.Driver";
	static String url = "jdbc:mysql://localhost:3306/project?serverTimezone=UTC&useSSL=false";
	static String DBid = "root";
	static String DBpassword = "boot";
	
	public static Connection getMySQLConnection() {
		Connection conn = null;
		try {
			Class.forName(basic.jdbcDriver);
			conn = DriverManager.getConnection(url,DBid,DBpassword);
		}catch(ClassNotFoundException | SQLException e) {
			e.printStackTrace();
		}
		return conn;
	}
}
