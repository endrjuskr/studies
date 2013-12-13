import java.util.Scanner;

public class Runtime {
	private static Scanner scanner = new Scanner(System.in);
	private static String errorMsg = "runtime error"; 
	public static int readInt()	{
		String s = scanner.nextLine();
		return Integer.parseInt(s);
	}
	
	public static String readString() {
		return scanner.nextLine();
	}
	
	public static void printInt(int k) {
		System.out.println(k);
	}
	
	public static void printString(String k) {
		System.out.println(k);
	}
	
	public static void error() {
		System.out.println(errorMsg);
		System.exit(1);
	}
	
	public static String concatenateString(String a, String b) {
		return a + b;
	}
}
