import java.sql.*;
import java.util.Scanner;


public class app {

    private static final String DB_URL = "jdbc:mysql://localhost:3306/flight_ticket_database";
    private static final String USER = "root";
    private static final String PASSWORD = "1111";
    
}
public class FlightTicketBookingSystem {

    private static final String DB_URL = "jdbc:mysql://localhost:3306/flight_ticket_database";
    private static final String USER = "root";
    private static final String PASSWORD = "1111";


    public static void main(String[] args) {
        try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASSWORD);
             Scanner scanner = new Scanner(System.in)) {

            // Creating a Statement
            Statement stmt = conn.createStatement();

            // Input user information
            System.out.println("Please enter information about the user:");
            System.out.print("Name: ");
            String name = scanner.nextLine();
            System.out.print("Email: ");
            String email = scanner.nextLine();

            // Insert user data
            String insertUserSQL = "INSERT INTO users (name, email) VALUES (?, ?)";
            try (PreparedStatement pstmt = conn.prepareStatement(insertUserSQL)) {
                pstmt.setString(1, name);
                pstmt.setString(2, email);
                pstmt.executeUpdate();
            }

            // Input flight information
            System.out.println("Please enter information about the flight you would like to book:");
            System.out.print("Origin: ");
            String origin = scanner.nextLine();
            System.out.print("Destination: ");
            String destination = scanner.nextLine();
            System.out.print("Price: ");
            String price = scanner.nextLine();

            // Update flight information
            String updateFlightSQL = "UPDATE users SET flight_origin = ?, flight_destination = ?, flight_price = ? WHERE email = ?";
            try (PreparedStatement pstmt = conn.prepareStatement(updateFlightSQL)) {
                pstmt.setString(1, origin);
                pstmt.setString(2, destination);
                pstmt.setString(3, price);
                pstmt.setString(4, email);
                pstmt.executeUpdate();
            }

            // Cancel flight
            System.out.print("Would you like to cancel your flight? (y/n): ");
            String cancelFlight = scanner.nextLine();
            if (cancelFlight.equalsIgnoreCase("y")) {
                String deleteUserSQL = "DELETE FROM users WHERE email = ?";
                try (PreparedStatement pstmt = conn.prepareStatement(deleteUserSQL)) {
                    pstmt.setString(1, email);
                    pstmt.executeUpdate();
                }
                System.out.println("Flight cancelled.");
            } else {
                System.out.println("Flight booked.");
            }

            // Display data
            System.out.print("Would you like to display your ticket? (y/n): ");
            String displayData = scanner.nextLine();
            if (displayData.equalsIgnoreCase("y")) {
                String selectSQL = "SELECT * FROM users";
                try (ResultSet rs = stmt.executeQuery(selectSQL)) {
                    ResultSetMetaData rsmd = rs.getMetaData();
                    int columnCount = rsmd.getColumnCount();

                    // Print column headers
                    for (int i = 1; i <= columnCount; i++) {
                        System.out.print(rsmd.getColumnName(i) + "\t");
                    }
                    System.out.println();

                    // Print row data
                    while (rs.next()) {
                        for (int i = 1; i <= columnCount; i++) {
                            System.out.print(rs.getString(i) + "\t");
                        }
                        System.out.println();
                    }
                }
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
