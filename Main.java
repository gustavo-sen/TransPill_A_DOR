import java.io.*;

public class Main {
    public static void main(String[] args) {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            scanner scan = new scanner(reader);
            parser parser = new parser(scan);

            System.out.println("Enter expressions (end with semicolon ';'):");

            while (true) {
                System.out.print("> ");
                String input = reader.readLine();
                if (input == null || input.equalsIgnoreCase("exit")) break;

                // Feed input to the scanner
                scan.yyreset(new StringReader(input));
                parser.parse();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
