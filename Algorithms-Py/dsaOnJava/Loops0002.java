import java.util.*;
public class Loops0002 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number for printing the series of natural numbers upto that number: ");
        int n = sc.nextInt();
        sc.close();
        System.out.println("Natural numbers from 1 to " + n + ":");
        for (int i = 1; i <= n; i++) {
            System.out.print(i + " ");
        }
        System.out.println("\nPrinting the tables of the number inputted by the user:");
        for (int i = 1; i <= 12; i++) {
            System.out.println(n + " x " + i + " = " + (n * i));
        }
        System.out.println();
    }
}
