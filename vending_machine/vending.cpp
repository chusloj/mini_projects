#include <iostream>
#include <string>
#include <math.h>

using namespace::std;

void fill_price_array(int num, float price_array[]){
	for(int i = 0; i < num; i++){
		float price = (rand() % 10) * 0.25;
		if(price == 0){
			price = 0.5;
		}

		price_array[i] = roundf(price * 100) / 100;
	}
}





void fill_item_array(int num, string item_array[]){
	int l_count;
	char letters[5] = {'A', 'B', 'C', 'D', 'E'};
	string item;
	for(int i=0; i<num; i++){
		l_count = floor(i/5);
		item = letters[l_count] + to_string( (i%5) + 1 );
		item_array[i] = item;
	}
}


string make_whitespace(int len_diff){
	string whitespace = "";
	for(int i=0; i<len_diff; i++){
		whitespace += " ";
	}
	return whitespace;
}


void print_vending_machine(int num, float price_array[], string item_array[]){
	int len_diff;

	for(int i=1; i<num; i++){
		if( ((i+1)%5) == 0){
			string price_line[5];
			string item_line[5];
			for(int j = i-4; j<i+1; j++){
				item_line[j%5] = item_array[j];
				price_line[j%5] = "$" + to_string(price_array[j]);
				if(item_array[j] != "SOLD OUT"){
					len_diff = price_line[j%5].length() - item_line[j%5].length();
					item_line[j%5] += make_whitespace(len_diff);
				}
				else{
					len_diff = 8 - price_line[j%5].length();
					price_line[j%5] += make_whitespace(len_diff);
				}
			}

		for(int i_count = 0; i_count<5; i_count++){
			cout << item_line[i_count] + " || ";
		}
		cout << endl;
		for(int p_count=0; p_count<5; p_count++){
			cout << price_line[p_count] + " || ";
		}
		cout << endl;
		cout << endl;
		}
	}
}


bool is_sold_out(int num, bool sold_out_list[]){
	for(int i=0; i<num; i++){
		if(sold_out_list[i] != true){
			return false;
		}
	}

	return true;
}



int get_index_of_items(int num, string choice, string item_array[]){
	for(int i = 0; i<num; i++){
		if(item_array[i] == choice){
			return i;
		}
	}
	return 404; // code that something's wrong
}



int main(){

	int num;

	cout << "How large would you like the machine to be?";
	cout << " ";
	cout << "Please keep the size of the machine <= 25." << endl;
	cin >> num;

	// num error
	if(num > 25){
		cout << "You can't have more than 25 items in the machine." << endl;
		throw "num_error";
	}


	float price_array[num];
	string item_array[num];



	fill_price_array(num, price_array);
	fill_item_array(num, item_array);

	float money;
	cout << "How much money do you have?" << endl;
	cin >> money;

	bool sold_out_list[num];
	string remaining_money;
	string choice;
	// string item_array_titles = item_array;

	while(money > 0){

		if(is_sold_out(num, sold_out_list) == true){
			cout << "This machine is empty!" << endl;
			remaining_money = "$" + to_string(money);
			cout << "You have " + remaining_money + " money" << endl;
			return 0;
		}

		remaining_money = "$" + to_string(money);
		cout << "You have " + remaining_money + " remaining." << endl;

		print_vending_machine(num, price_array, item_array);

		cout << endl << "What's your choice?" << endl;
		cin >> choice;

		if(get_index_of_items(num, choice, item_array) == 404){
			cout << "This item is sold out! Please choose another item." << endl;
			continue;
		}

		// if(item_array[get_index_of_items(num, choice, item_array)] == "SOLD_OUT"){
			// cout << "Please choose a valid selection." << endl;
			// continue;
		// }

		if(money < price_array[get_index_of_items(num, choice, item_array)]){
			cout << "You can't afford that! Please choose another item." << endl;
			continue;
		}

		money -= price_array[get_index_of_items(num, choice, item_array)];

		sold_out_list[get_index_of_items(num, choice, item_array)] = true;

		item_array[get_index_of_items(num, choice, item_array)] = "SOLD OUT";



		// TODO: make function to find index of a given choice, change it to
		// 'SOLD OUT' and add 'true'

	}




	return 0;
}