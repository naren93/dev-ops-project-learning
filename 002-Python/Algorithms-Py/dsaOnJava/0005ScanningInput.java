import java.util.*;
class ScanningInput {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter first name: ");
        String firstName = sc.next();
        System.out.print("Enter last name: ");
        String lastName = sc.next();
        System.out.println("Your name is "+ firstName + " " + lastName);
        sc.close();
        // Note: Always close the scanner to avoid resource leaks.
        // If you want to read a full line including spaces, use sc.nextLine() instead
        // of sc.next() for the first name or last name.
        // Example:
        // System.out.print("Enter full name: ");
        // String fullName = sc.nextLine();
        // System.out.println("Your full name is " + fullName);
        // This will read the entire line until the newline character.
        // If you want to read multiple inputs in a single line, you can use sc.next() multiple times.
        // Example:
        // System.out.print("Enter your age and city: ");
        // int age = sc.nextInt();
        // String city = sc.next();
        // System.out.println("You are " + age + " years old and live in "+ city + ".");
        // This will read an integer followed by a string in the same line.
        // Remember to handle exceptions for invalid inputs, such as using try-catch blocks.
        // Example:
        // try {
        //     int age = sc.nextInt();
        //     System.out.println("Your age is " + age);
        // } catch (InputMismatchException e) {
        //     System.out.println("Please enter a valid integer for age.");
        // } finally {
        //     sc.close();
        // }
        // This will catch any input mismatch exceptions and prompt the user accordingly.
        // Always ensure to close the scanner in a finally block or use try-with-resources to
        // automatically close it when done.
        // Example of try-with-resources:
        // try (Scanner sc = new Scanner(System.in)) {
        //     System.out.print("Enter your favorite color: ");
        //     String color = sc.nextLine();
        //     System.out.println("Your favorite color is " + color);
        // } // The scanner will be closed automatically here.
        // This is a cleaner way to handle resources in Java.
        // You can also use sc.hasNext() to check if there is another token available before
        // reading it, which helps avoid exceptions when reading input.
        // Example:
        // if (sc.hasNext()) {
        //     String input = sc.next();
        //     System.out.println("You entered: " + input);
        // } else {
        //     System.out.println("No input provided.");
        // }
        // This will check if there is any input available before attempting to read it.
        // Additionally, you can use sc.nextLine() to read the entire line of input,
        // which is useful when you want to capture a full sentence or multiple words.
        // Example:
        // System.out.print("Enter a sentence: ");
        // String sentence = sc.nextLine();
        // System.out.println("You entered: " + sentence);
        // This will read the entire line until the newline character, allowing for spaces and
        // multiple words in the input.
        // Remember to handle edge cases, such as empty inputs or unexpected characters,
        // to ensure your program runs smoothly and provides a good user experience.
        // Always validate user input where necessary, such as checking if a string is empty
        // or if an integer is within a certain range.
        // Example of input validation:
        // System.out.print("Enter your age (0-120): ");
        // int age = sc.nextInt();
        // if (age < 0 || age > 120) {
        //     System.out.println("Please enter a valid age between 0 and 120.");
        // } else {
        //     System.out.println("Your age is " + age);
        // }
        // This will ensure that the user inputs a valid age within the specified range.
        // Always provide clear instructions to the user on what input is expected,
        // and handle any exceptions gracefully to improve the user experience.
        // For example, if you expect a number but the user enters a string,
        // you can catch the exception and prompt them to try again.
    }
}
