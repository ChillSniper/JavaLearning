import java.lang.String;
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String str = sc.nextLine();
        StringBuilder sb = new StringBuilder();
        sb.append(str);
        sb.reverse();
        String res = sb.toString();
        if(str.equals(res)) {
            System.out.println("YES");
        }
        else {
            System.out.println("NO");
        }
    }
    public static String arrToString(int[] arr) {
        if(arr == null) {
            return "";
        }
        if(arr.length == 0) {
            return "[]";
        }
        String result = "[";
        for (int i = 0; i < arr.length; i++) {
            if(i != 0) {
                result += ", ";
            }
            result += arr[i];
        }
        result += "]";

        return result;
    }



}