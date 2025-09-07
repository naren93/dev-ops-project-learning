import java.util.*;

public class Loops0003 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the number of items for which you want to build the pattern: ");
        int n = sc.nextInt();
        sc.close();
        System.out.println("Building a RECTANGLE pattern with " + n + " items:");
        for (int i = 1; i < n; i++) {
            System.out.print("* ".repeat(n));
            System.out.println();
        }
        System.out.println("Building a single COLUMN pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.println("*");
        }
        System.out.println();
    } 
}
