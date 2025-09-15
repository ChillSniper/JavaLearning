public class NewDemo {
    public static void main(String[] args) {
        int[] arr = {1,2,3,4,5,6,7,8,9};
        String s = arrToString(arr);
        System.out.println(s);
    }
    public static String arrToString(int[] arr) {
        StringBuffer sb = new StringBuffer();
        sb.append("[");
        for (int i = 0; i < arr.length; i++) {
            if(i != 0) {
                sb.append(",");
            }
            sb.append(arr[i]);
        }
        sb.append("]");
        return sb.toString();
    }
}
