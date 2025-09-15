import java.util.StringJoiner;

public class LearnStringJoiner
{
    public static void main(String[] args) {
//        StringJoiner sj = new StringJoiner("---", "[", "]");
//        sj.add("1").add("2").add("3").add("4").add("5").add("6").add("7");
//        System.out.println(sj.toString());
        StringBuilder sb = new StringBuilder("aaaaaaaaa");
        System.out.println(sb.capacity());
        System.out.println(sb.length());
    }
}
