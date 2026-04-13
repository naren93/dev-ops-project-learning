import java.util.*;
public class SwitchCase {
    public static void main(String[] args) {
        Scanner sc = new java.util.Scanner(System.in);
        System.out.print("Enter a day number (1-7): ");
        int day = sc.nextInt();
        sc.close();

        switch (day) {
            case 1:
                System.out.println("Monday");
                break;
            case 2:
                System.out.println("Tuesday");
                break;
            case 3:
                System.out.println("Wednesday");
                break;
            case 4:
                System.out.println("Thursday");
                break;
            case 5:
                System.out.println("Friday");
                break;
            case 6:
                System.out.println("Saturday");
                break;
            case 7:
                System.out.println("Sunday");
                break;
            default:
                System.out.println("Invalid day number. Please enter a number between 1 and 7.");
        }
    }
}
