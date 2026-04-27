import java.util.Scanner;
class calculator {
    private int add(int a, int b){
        return a + b;
    }

    private int subtract(int a, int b){
        return a - b;
    }

    private int multiply(int a, int b){
        return a * b;
    }

    private int divide(int a, int b){
        if(b != 0){
            return a / b;
        } 
        else{
            System.out.println("Error: Division by zero");
            return 0;
        }
    }
    public static void main(String[] args){
        example obj = new example();
        System.out.println(obj.add(5, 3));
        System.out.println(obj.subtract(5, 3));
        System.out.println(obj.multiply(5, 3));
        System.out.println(obj.divide(5, 3));
    }
}