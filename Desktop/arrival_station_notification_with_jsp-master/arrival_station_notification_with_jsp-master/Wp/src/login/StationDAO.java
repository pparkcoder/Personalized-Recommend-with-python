package login;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;

public class StationDAO {
	public static int num;
	public static int line;
	public static String name;
	public static double x;
	public static double y;
	private Connection conn;
	private PreparedStatement pstmt;
	private ResultSet rs;

	public StationDAO() {
		try {
			String dbURL = "jdbc:mysql://localhost:3306/project?serverTimezone=UTC&useSSL=false";
			String dbID = "root";
			String dbPassword = "boot";
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection(dbURL, dbID, dbPassword);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	public ArrayList<Station> search(String stationName) { // 역의 정보를 검색하여 리스트로 출력
		String SQL = "SELECT * FROM station WHERE station_name LIKE ?";	
		ArrayList<Station> stationList = new ArrayList<Station>();
		try {
			pstmt = conn.prepareStatement(SQL);
			pstmt.setString(1, "%" + stationName + "%"); // 위의 SQL에서 LIKE에 대한 와일드 카드
			rs = pstmt.executeQuery();	//SQL문의 결과
			while (rs.next()) {		//역의 이름이 존재하면
				Station station = new Station();
				station.setStation_line(rs.getInt(2));
				station.setStation_name(rs.getString(3));
				station.setStation_x(rs.getDouble(4));
				station.setStation_y(rs.getDouble(5));
				stationList.add(station);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return stationList;
	}
}
