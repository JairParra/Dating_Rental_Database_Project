
import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Properties;

public class DemoDB {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
				
		
		// *** TESTS *** 
		String[] colnames0 = {"sid", 
		                      "sname", 
		                      "rating", 
		                      "age"};
		
		String[] coltypes0 = {"BIGSERIAL PRIMARY KEY NOT NULL", 
				"VARCHAR(20)",  
				"INTEGER", 
				"INTEGER"};
		
		ArrayList<String> colnames = new ArrayList<String>(Arrays.asList(colnames0)); 		
		ArrayList<String> coltypes = new ArrayList<String>(Arrays.asList(coltypes0)) ; 
		String ex_table = create_table("extable", colnames, coltypes,  true, true, true) ;  
		// *** TESTS *** 
		
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
			
			stmt.close(); 
			
			System.out.println("Query has finished");		
			
			// ************************************************************
			
			System.out.println(ex_table);
			
			
			// Executing updates
			Statement stmt2 = con.createStatement();   // ??? 
			ResultSet Rs2 = stmt2.executeQuery(ex_table); // execute the query 			
			ResultSetMetaData rsmd = Rs2.getMetaData(); // obtain table metadata 
			int columnsNumber = rsmd.getColumnCount();  // obtain number of columns
			
			// iterate through and print results
			while(Rs2.next()) { 
				for(int i =0; i < columnsNumber; i++ ) { 
					System.out.print(Rs2.getString(i) + " "); //Print one element of a row
				}
			}
			
			
			// update and display table 
			// NOTE: Table is empty, will not result anything. 
			
			System.out.println("Query has finished");	
			
			
		}catch(Exception ex){ 
			// Shit went wrong
			System.out.println(ex.getMessage());
		}
		
		

	
		
	}
	
	/**
	 * Creates a table
	 * @param table_name
	 * @param colnames
	 * @param coltypes
	 * @param auto_increment
	 * @param drop_table
	 * @return SQL statment
	 */
	public static String create_table(
			String table_name, 
			ArrayList<String> colnames, 
			ArrayList<String> coltypes, 
			boolean auto_increment, 
			boolean drop_table, 
			boolean show) {
		
		
		// Verify that input lengths match
		if(colnames.size() != coltypes.size()) {
			throw new IllegalArgumentException("column names and column types arrays must have same length"); 
		}
		
		// Proceed to store statement
		String stmt = "" ;  // to store the string result 
		
		
		if(drop_table == true) { 
			stmt += "DROP TABLE IF EXISTS " + table_name + ";\n" ; 
		}
		
		stmt += "CREATE TABLE " + table_name + "(\n"; 
		
		// Update the statement by each column 
		for(int i =0 ; i < colnames.size(); i++) { 
			if(i == colnames.size()-1 ) { 
				stmt += "\t" + colnames.get(colnames.size()-1) + " " + coltypes.get(colnames.size()-1); 
			}
			else { 
				stmt += "\t" + colnames.get(i) + " " +  coltypes.get(i) + ",\n"; 
			}
		}

		// close the statement
		stmt += ")\n; " ; 
		
		// show the table? 
		if(show == true) { 
			stmt += "\nSELECT * FROM " + table_name + "; "; 
		}
		
		System.out.println("Table name: " + table_name);
				
		return stmt; 
	}

}
