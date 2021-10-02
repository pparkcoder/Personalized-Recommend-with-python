package login;

import java.io.IOException;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/StationSearchServlet")
public class StationSearchServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	
	//서블릿을 구현한 이유 : 기본 CGI보다 빠르고, AJAX의 요청에 따른 응답을 JSON형태로 만들어주기 위함
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		request.setCharacterEncoding("UTF-8");		//파라미터를 UTF-8로 인코딩
		response.setContentType("text/html;charset=UTF-8");
		String stationName = request.getParameter("stationName");	//파라미터값 가져오기
		response.getWriter().write(getJSON(stationName));	//역에관한 정보를 JSON형태로 저장해주기 ->전체적인 서블릿의 역할
															//getWriter - 응답에 문자 데이터를 전송하기 위한 출력 스트림을 리턴
	}

	public String getJSON(String stationName) {	//요청한 페이지(select.jsp)에서 JSON의 형태로 받기위해서  JSON형태(name:value 꼴)을 만들어준다
		if (stationName == null)
			stationName = "";  
		StringBuffer result = new StringBuffer("");
		result.append("{\"result\":[");	//JSON에서 key값을 result로 설정
		StationDAO stationDAO = new StationDAO();
		ArrayList<Station> stationList = stationDAO.search(stationName);	//넘어온 역이름을 데이터 베이스에서 검색
		for (int i = 0; i < stationList.size(); i++) {
			result.append("[{\"value\": \"" + stationList.get(i).getStation_line() + "\"},");	//,를 통해 value를 구분
			result.append("{\"value\": \"" + stationList.get(i).getStation_name() + "\"},");
			result.append("{\"value\": \"" + stationList.get(i).getStation_x() + "\"},");
			result.append("{\"value\": \"" + stationList.get(i).getStation_y() + "\"}],");
		}	//하나의 역 정보를 배열의 원소정보로 묶음
		result.append("]}");
		return result.toString();
	}
}
