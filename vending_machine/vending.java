import java.util.Scanner;
import java.util.ArrayList;
import java.lang.Math;

class vending {

	static ArrayList<Double> make_prices(int num, int lower_price_limit, int upper_price_limit) {

		ArrayList<Double> prices = new ArrayList<Double>();
		for(int i=0; i<num; i++){
			prices.add(Math.floor(Math.random() * 10) * 0.25);
		}

		return prices;
	}



	static ArrayList<String> make_items(ArrayList<Double> prices_list) {

		ArrayList<String> items_list = new ArrayList<String>();
		char[] letters = new char[]{'A', 'B', 'C', 'D', 'E'};

		for(int n = 0; n < prices_list.size(); n++) {
			int l_count = (int)Math.floor(n / 5);
			String item = letters[l_count] + String.valueOf(n%5 + 1);
			items_list.add(item);
		}

		return items_list;

	}


	static String make_whitespace(int len_diff) {

		String whitespace = new String("");
		for(int i=0; i<len_diff; i++){
			whitespace += " ";
		}
		
		return whitespace;
	}



	static void print_vending_machine(int num, ArrayList<Double> prices_list, ArrayList<String> items_list) {
	
		int len_diff;

		for(int i=1; i<num; i++){

			if(( (i+1)%5 ) == 0){

				String[] price_line = new String[5];
				String[] item_line = new String[5];
				for(int j = i-4; j<i+1; j++){
					item_line[j%5] = items_list.get(j);
					price_line[j%5] = "$" + String.valueOf(prices_list.get(j));
					if(items_list.get(j) != "SOLD OUT"){
						len_diff = price_line[j%5].length() - item_line[j%5].length();
						item_line[j%5] += make_whitespace(len_diff);
					}
					else {
						len_diff = 8 - price_line[j%5].length();
						price_line[j%5] += make_whitespace(len_diff);
					}
				}

			for(int i_count = 0; i_count<5; i_count++){
				System.out.print(item_line[i_count] + " || ");
			}

			System.out.println();

			for(int p_count=0; p_count<5; p_count++){
				System.out.print(price_line[p_count] + " || ");
			}

			System.out.println("");
			System.out.println("");

			}
		}
	}



	public static void main(String[] args) {
	
		System.out.println("How many entries would you like in your vending machine?" + "\n" +
	    "Please keep the number of entries <= 25.");

		Scanner scan = new Scanner(System.in);
		Scanner scan_str = new Scanner(System.in);
		int num = scan.nextInt();

		if(num > 25){
			System.out.println("You can't have more than 25 items in the machine.");
			throw new RuntimeException("num_error");
		}

		ArrayList<Double> prices_list = make_prices(num, 1, 8);
		ArrayList<String> items_list = make_items(prices_list);

		System.out.println("How much money do you have?");
		int money_in = scan.nextInt();

		ArrayList<String> sold_out_list = new ArrayList<String>();
		String remaining_money = new String();
		String choice = new String();

		// cast money var to double
		float money = (float)money_in;


		while(money > 0) {

			if(sold_out_list.size() == items_list.size()){
				System.out.println("This machine is empty!");
				remaining_money = "$" + String.valueOf(money);
				System.out.println("You have " + remaining_money + " money.");
				return;
			}

			remaining_money = "$" + String.valueOf(money);
			System.out.println("You have " + remaining_money + " money.");

			print_vending_machine(num, prices_list, items_list);

			System.out.println("What's your choice?");
			choice = scan_str.nextLine();

			if(sold_out_list.contains(choice)){
				System.out.println("This item is sold out! Please choose another item.");
				continue;
			}

			if(money < prices_list.get( items_list.indexOf(choice) )){
				System.out.println("You can't afford that! Please choose another item.");
				continue;
			}

			money -= prices_list.get(items_list.indexOf(choice));

			sold_out_list.add(choice);

			items_list.set(items_list.indexOf(choice), "SOLD OUT");


			}



	}
}