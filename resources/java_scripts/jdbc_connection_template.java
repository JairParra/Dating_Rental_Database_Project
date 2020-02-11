
import java.sql.*;
import java.util.Properties;

public class DemoDB {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
				
		
		try {
			
			// Setting up connection parameters 
			String url = "jdbc:postgresql://comp421.cs.mcgill.ca:5432/cs421";
			Properties props = new Properties();
			props.setProperty("user","hparra");
			props.setProperty("password","Y*jcO)8*"); // wtf? 
			props.setProperty("ssl","false");
			
			// Create the actual connection 
			Class.forName("org.postgresql.Driver"); // Driver call 
			Connection con = DriverManager.getConnection(url, props);  // set up connection 
			
			// SQL Statements
			PreparedStatement stmt = con.prepareStatement("SELECT * FROM competition;");   
			ResultSet Rs = stmt.executeQuery(); // execute the query 
			while(Rs.next()) { 
				System.out.println(Rs.getInt(1) + " " + Rs.getString(2)) ; // Obtain first and second columns 
			}
			
		}catch(Exception ex){ 
			// Shit got wrong
			System.out.println(ex.getMessage());
		}
	}

}
