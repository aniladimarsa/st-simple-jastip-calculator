import streamlit as str 
from streamlit_option_menu import option_menu

def input_purchase_price(currency: str) -> float:
    """Input the purchase price"""
    
    # Input the purchase price and return it
    purchase_price = str.number_input(f"Masukkan harga {currency}", value=0.0, step=0.01, format="%.2f")
    return purchase_price
    
def calculate_converted_price(purchase_price: float, multiplier: int) -> float:
    """Calculate the converted price"""
    
    # Do the calculation to convert the price and return it
    converted_price = purchase_price * multiplier 
    return converted_price

def format_price(converted_price: float) -> str:
    """Format the price to be 99,999.99"""
    
    # Convert the converted price to be string
    converted_str = f"{converted_price:,.2f}"
    
    # Parse it into int part and decimal part
    converted_int, converted_dec = converted_str.split(".")
    
    # Combine the int and decimal part using '.' as the separator, then return it
    formatted_price = f"{converted_int}.{converted_dec}"
    return formatted_price

def input_selling_price(converted_price: float, max_adjustable_amout: float, intended_step: float) -> float:
    """Input the selling price"""
    
    # Initialize session state
    if "last_updated" not in str.session_state:
        str.session_state.last_updated = None
    if "last_selling_price" not in str.session_state:
        str.session_state.last_selling_price = converted_price
    if "previous_slider" not in str.session_state:
        str.session_state.previous_slider = converted_price
    if "previous_input" not in str.session_state:
        str.session_state.previous_input = converted_price
    
    # Create widgets for selling price input
    selling_price_slider = str.slider("Mau dijual dengan harga berapa?", converted_price, converted_price + max_adjustable_amout, step=intended_step, key="selling_slider")
    selling_price_input = str.number_input("atau ketik harga jual di sini:", step=0.01, format="%.2f", key="selling_input")  
    
    # If the slider value has changed, update the selling price to the current slider value
    if selling_price_slider != str.session_state.previous_slider:
        str.session_state.input_method = "slider"
        str.session_state.selling_price = selling_price_slider
        str.session_state.previous_slider = selling_price_slider

    # If the input value has changed, update the selling price to the current input value
    elif selling_price_input != str.session_state.previous_input:
        str.session_state.input_method = "input"
        str.session_state.selling_price = selling_price_input
        str.session_state.previous_input = selling_price_input
    
    return str.session_state.selling_price
    
def calculate_estimated_profit(converted_price, selling_price):   
    """Calculate the estimated profit"""
    
    # Substract selling price by the converted price and return it
    estimated_profit = selling_price - converted_price
    return estimated_profit 

def main():
    
    # Create a sidebar menu
    with str.sidebar:
        selected = option_menu('Menu', ['Hitung Modal Jastip Malaysia-Indonesia', 'Convert IDR ke MYR'], default_index=0)
    
    # If the 'Hitung Modal Jastip Malaysia-Indonesia' option is chosen, then calculate the estimated profit obtained from Jastip
    if selected == 'Hitung Modal Jastip Malaysia-Indonesia':    
        str.title("Hitung Modal Jastip Malaysia-Indonesia")
        str.text("Asumsi 1 MYR = 3500 IDR")
        
        # Input the price in MYR and convert it to IDR
        ringgit_price = input_purchase_price("Ringgit")
        rupiah_price = calculate_converted_price(ringgit_price, 3500) # Assume that 1 IDR = RM3,500
        
        # Format the price in IDR to be displayed and display it
        formatted_rupiah_price = format_price(rupiah_price)
        str.markdown(f"Harga dalam Rupiah: **{formatted_rupiah_price}**")
        
        # Input the selling price and calculate the estimated profit
        selling_price = input_selling_price(rupiah_price, 750000.00, 500.00)
        estimated_profit = calculate_estimated_profit(rupiah_price, selling_price)
        
        # Format the estimated profit to be displayed and display it
        formatted_estimated_profit = format_price(estimated_profit)
        str.markdown(f"Perkiraan profit: ***{formatted_estimated_profit}***")
    
    # If the 'Convert IDR ke MYR' option is chosen, then convert the amount of IDR to MYR
    if selected == 'Convert IDR ke MYR':
        str.title("Convert Ringgit ke Rupiah")
        str.text("Asumsi 1 MYR = 3500 IDR")
        
        # Input the IDR amount
        rupiah_price = input_purchase_price("Rupiah")
        ringgit_price = calculate_converted_price(rupiah_price, (1/3500)) # Assume that 1 IDR = RM3,500
        
        # Format the MYR amount to be displayed and display it
        formatted_ringgit_price = format_price(ringgit_price)
        str.markdown(f"Harga dalam Ringgit: **{formatted_ringgit_price}**")
        
if __name__ == "__main__":
    main()
    