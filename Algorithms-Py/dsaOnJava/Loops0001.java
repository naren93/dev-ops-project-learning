public class Loops0001 {
    public static void main(String[] args) {
        System.out.println("For Loop:");
        for (int i = 1; i <= 5; i++) {
            System.out.println("Hello, World! " + i);
        }
        int i = 1;
        System.out.println("While Loop:");
        while (i<=5) {
            System.out.println("Hello, World! " + i);
            i++;
        }
        i = 1;
        System.out.println("Do-While Loop:");
        do {
            System.out.println("Hello, World! " + i);
            i++;
        } while (i <= 5);
    }
}
