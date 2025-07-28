from typing import Union, Optional

class NumberFormatter:
    """
    Utility class for formatting numbers in the budget application.
    Handles currency formatting with dollar signs and comma separators for large numbers.
    """
    
    @staticmethod
    def format_currency(value: Union[int, float, str, None], 
                       show_cents: bool = True, 
                       show_positive_sign: bool = False) -> str:
        """
        Format a number as currency with dollar sign and comma separators.
        
        Args:
            value: The number to format (int, float, str, or None)
            show_cents: Whether to show cents (.00) (default: True)
            show_positive_sign: Whether to show + for positive numbers (default: False)
            
        Returns:
            Formatted currency string (e.g., "$1,234.56", "$-1,234.56")
        """
        if value is None:
            return "$0.00" if show_cents else "$0"
            
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return "$0.00" if show_cents else "$0"
        
        # Handle the sign
        is_negative = num_value < 0
        abs_value = abs(num_value)
        
        # Format with commas
        if show_cents:
            formatted = f"{abs_value:,.2f}"
        else:
            formatted = f"{abs_value:,.0f}"
        
        # Add currency symbol and sign
        if is_negative:
            return f"-${formatted}"
        elif show_positive_sign and num_value > 0:
            return f"+${formatted}"
        else:
            return f"${formatted}"
    
    @staticmethod
    def format_number(value: Union[int, float, str, None],
                     decimal_places: int = 2,
                     show_positive_sign: bool = False) -> str:
        """
        Format a number with comma separators (no currency symbol).
        
        Args:
            value: The number to format
            decimal_places: Number of decimal places to show (default: 2)
            show_positive_sign: Whether to show + for positive numbers (default: False)
            
        Returns:
            Formatted number string (e.g., "1,234.56", "-1,234.56")
        """
        if value is None:
            return "0.00" if decimal_places > 0 else "0"
            
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return "0.00" if decimal_places > 0 else "0"
        
        # Handle the sign
        is_negative = num_value < 0
        abs_value = abs(num_value)
        
        # Format with commas and specified decimal places
        if decimal_places > 0:
            formatted = f"{abs_value:,.{decimal_places}f}"
        else:
            formatted = f"{abs_value:,.0f}"
        
        # Add sign
        if is_negative:
            return f"-{formatted}"
        elif show_positive_sign and num_value > 0:
            return f"+{formatted}"
        else:
            return formatted
    
    @staticmethod
    def format_percentage(value: Union[int, float, str, None],
                         decimal_places: int = 1) -> str:
        """
        Format a number as a percentage.
        
        Args:
            value: The number to format (should be between 0-1 for 0-100%)
            decimal_places: Number of decimal places to show (default: 1)
            
        Returns:
            Formatted percentage string (e.g., "25.5%")
        """
        if value is None:
            return "0.0%" if decimal_places > 0 else "0%"
            
        try:
            num_value = float(value) * 100
        except (ValueError, TypeError):
            return "0.0%" if decimal_places > 0 else "0%"
        
        if decimal_places > 0:
            return f"{num_value:.{decimal_places}f}%"
        else:
            return f"{num_value:.0f}%"
    
    @staticmethod
    def safe_format_table_amount(value: Union[int, float, str, None]) -> str:
        """
        Safe formatting for table display - handles various input types gracefully.
        Used specifically for table cells that might contain unexpected data types.
        
        Args:
            value: The value to format
            
        Returns:
            Formatted currency string, defaults to $0.00 on any error
        """
        if value is None or value == "":
            return "$0.00"
            
        # Handle already formatted strings
        if isinstance(value, str):
            # If it already looks like currency, return as-is
            if value.startswith('$') or value.startswith('-$') or value.startswith('+$'):
                return value
            # Try to extract number from string
            clean_value = value.replace('$', '').replace(',', '').strip()
            try:
                return NumberFormatter.format_currency(float(clean_value))
            except (ValueError, TypeError):
                return "$0.00"
        
        return NumberFormatter.format_currency(value)