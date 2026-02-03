import java.util.Scanner;

class samples {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        do{
            System.out.println("\nCALCULATOR MENU\n");
            System.out.println("1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Exit");
            System.out.print("Choose an option: ");
            int choice = sc.nextInt();
            switch(choice){
                case 1:{
                    System.out.print("Enter two numbers: ");
                    int a = sc.nextInt();
                    int b = sc.nextInt();
                    System.out.println("Result: " + (a + b));
                    break;
                }
                case 2:{
                    System.out.print("Enter two numbers: ");
                    int a = sc.nextInt();
                    int b = sc.nextInt();
                    System.out.println("Result: " + (a - b));
                    break;
                }
                case 3:{
                    System.out.print("Enter two numbers: ");
                    int a = sc.nextInt();
                    int b = sc.nextInt();
                    System.out.println("Result: " + (a * b));
                    break;
                }
                case 4:{
                    System.out.print("Enter two numbers: ");
                    int a = sc.nextInt();
                    int b = sc.nextInt();
                    if(b != 0){
                        System.out.println("Result: " + (a / b));
                    } 
                    else{
                        System.out.println("Error: Division by zero");
                    }
                    break;
                }
                case 5:
                    System.out.println("Exiting...");
                    sc.close();
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        } while (true);
    }
}