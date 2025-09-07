import java.util.Scanner;
public class Conditionals {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int number = sc.nextInt();
        // Additional input for demonstration purposes
        System.out.print("Enter a number (a): ");
        int numberA = sc.nextInt();
        System.out.print("Enter a number (b): ");
        int numberB = sc.nextInt();
        sc.close();
        if (number > 0) {
            System.out.println("The number is positive.");
        } else if (number < 0) {
            System.out.println("The number is negative.");
        } else {
            System.out.println("The number is zero.");
        }
        // Additional condition to check if the number is even or odd   
        if (number % 2 == 0) {
            System.out.println("The number is even.");
        } else {
            System.out.println("The number is odd.");
        }
        if (numberA > numberB) {
            System.out.println("a is greater than b.");
        } else if (numberA < numberB) {
            System.out.println("a is less than b.");
        } else {
            System.out.println("a is equal to b.");
        }
    }
}
