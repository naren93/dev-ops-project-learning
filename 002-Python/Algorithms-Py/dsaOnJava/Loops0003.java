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
        System.out.println("Building a square pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.print("* ".repeat(n));
            System.out.println();
        }
        System.out.println("Building a single COLUMN pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.println("*");
        }
        System.out.println();
        System.out.println("Building a single ROW pattern with " + n + " items:");
        System.out.print("* ".repeat(n));
        System.out.println();
        System.out.println("Building a hollow square pattern with " + n + " items:");
        for (int i = 0; i < n; i++) {
            if (i==0 || i==n-1) {
                System.out.print("* ".repeat(n));
            } else {
                System.out.print("* ");
                System.out.print("  ".repeat(n-2));
                System.out.print("*");
            }
            System.out.println();
        }
        System.out.println("Building a hollow rectangle pattern with " + n + " items:");
        for (int i = 0; i < n-1; i++) {
            if (i==0 || i==n-2) {
                System.out.print("* ".repeat(n));
            } else {
                System.out.print("* ");
                System.out.print("  ".repeat(n-2));
                System.out.print("*");
            }
            System.out.println();
        }
        System.out.println("Building a right-angled triangle pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.print("* ".repeat(i));
            System.out.println();
        }
        System.out.println("Building a reverse right-angled triangle pattern with " + n + " items:");
        for (int i = n; i >= 1; i--) {
            System.out.print("* ".repeat(i));
            System.out.println();
        }
        System.out.println("Building a pyramid pattern with " + n + " items:");
        for (int i = 1; i <= n; i++) {
            System.out.print(" ".repeat(n-i));
            System.out.print("* ".repeat(i));
            System.out.println();
        }
        System.out.println("Building a reverse pyramid pattern with " + n + " items:");
        for (int i = n; i >= 1; i--) {
            System.out.print(" ".repeat(n-i));
            System.out.print("* ".repeat(i));
            System.out.println();
        }
        System.out.println("Building a floyd's triangle pattern with " + n + " items:");
        int count = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(count + " ");
                count++;
            }
            System.out.println();
        }
        System.out.println("Building a 0-1 right triangle pattern with " + n + " items:");
        int flag = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(flag + " ");
                flag = 1 - flag;
            }
            System.out.println();
        }
    }
}
