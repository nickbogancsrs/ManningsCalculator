import streamlit as st
from mannings_calculator import ManningsCalculator

def main():
    # Create and run the Manning's Flow Calculator app
    calculator = ManningsCalculator()
    calculator.create_manning_app()

if __name__ == "__main__":
    main()
