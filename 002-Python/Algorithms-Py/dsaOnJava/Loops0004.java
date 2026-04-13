import java.util.*;
public class Loops0004 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the number of items for which you want to build the pattern: ");
        int n = sc.nextInt();
        sc.close();
        System.out.println("Building butterfly pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.print("*".repeat(i));
            System.out.print(" ".repeat(n-i));
            System.out.print(" ".repeat(n-i));
            System.out.print("*".repeat(i));
            System.out.println();
        }
        for(int i=n-1; i>=1; i--){
            System.out.print("*".repeat(i));
            System.out.print(" ".repeat(n-i));
            System.out.print(" ".repeat(n-i));
            System.out.print("*".repeat(i));
            System.out.println();
        }
        System.out.println("Butterfly pattern built successfully.");
        System.out.println("Building a solid rhombus pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.print(" ".repeat(n-i));
            System.out.print("*".repeat(n));
            System.out.println();
        }
        System.out.println("Solid rhombus pattern built successfully.");
        System.out.println("Building a diamond pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.print(" ".repeat(n-i));
            System.out.print("*".repeat(2*i-1));
            System.out.println();
        }
        for (int i = n-1; i >= 1; i--) {
            System.out.print(" ".repeat(n-i));
            System.out.print("*".repeat(2*i-1));
            System.out.println();
        }
    }
}
