"""
Utility functions module
Contains various useful helper functions
"""
import re
from datetime import datetime, timedelta
from typing import Optional, Tuple


def validate_input(prompt: str, validation_func, error_message: str = "Invalid input, please try again") -> str:
    """
    General function for validating user input
    
    Args:
        prompt: Prompt message
        validation_func: Validation function
        error_message: Error message
    
    Returns:
        Validated input
    """
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        print(f"❌ {error_message}")


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse date string to datetime object
    Supports multiple formats:
    - 2024-05-25
    - 2024-05-25 14:30
    - today, tomorrow, day after tomorrow
    - Relative time: +3days, +1week
    """
    if not date_str:
        return None
    
    date_str = date_str.strip().lower()
    now = datetime.now()
    
    # Handle relative dates
    if date_str == "today":
        return now.replace(hour=23, minute=59, second=59)
    elif date_str == "tomorrow":
        return (now + timedelta(days=1)).replace(hour=23, minute=59, second=59)
    elif date_str == "day after tomorrow":
        return (now + timedelta(days=2)).replace(hour=23, minute=59, second=59)
    
    # Handle relative time format: +3days, +1week
    relative_pattern = r'\+(\d+)(days?|weeks?)'
    match = re.match(relative_pattern, date_str)
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        if unit.startswith('day'):
            return now + timedelta(days=num)
        elif unit.startswith('week'):
            return now + timedelta(weeks=num)
    
    # Standard date formats
    date_formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d",
        "%Y/%m/%d %H:%M",
        "%m-%d",  # Month-day of current year
        "%m/%d"   # Month/day of current year
    ]
    
    for fmt in date_formats:
        try:
            if fmt in ["%m-%d", "%m/%d"]:
                # Add year
                parsed_date = datetime.strptime(date_str, fmt).replace(year=now.year)
                # If date has passed, set to next year
                if parsed_date < now:
                    parsed_date = parsed_date.replace(year=now.year + 1)
                return parsed_date
            else:
                return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


def format_duration(seconds: int) -> str:
    """Format time duration"""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minutes"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes == 0:
            return f"{hours} hours"
        return f"{hours} hours {minutes} minutes"


def format_time_ago(dt: datetime) -> str:
    """Format relative time (how long ago)"""
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "just now"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text and add ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def create_progress_bar(current: int, total: int, width: int = 20) -> str:
    """Create simple progress bar"""
    if total == 0:
        return "░" * width
    
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(100 * current / total)
    return f"{bar} {percentage}%"


def parse_priority(priority_str: str) -> int:
    """Parse priority string"""
    priority_str = priority_str.strip().lower()
    priority_map = {
        'low': 1, 'l': 1, '1': 1,
        'medium': 2, 'med': 2, 'm': 2, '2': 2,
        'high': 3, 'h': 3, '3': 3
    }
    return priority_map.get(priority_str, 2)


def colorize_text(text: str, color: str) -> str:
    """Add color to text (ANSI color codes)"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    
    if color.lower() in colors:
        return f"{colors[color.lower()]}{text}{colors['reset']}"
    return text


def get_user_choice(options: list, prompt: str = "Please select") -> int:
    """
    Get user choice
    
    Args:
        options: List of options
        prompt: Prompt message
    
    Returns:
        Selected index (starting from 0)
    """
    while True:
        print(f"\n{prompt}:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("Enter option number: ")) - 1
            if 0 <= choice < len(options):
                return choice
            else:
                print("❌ Invalid choice, please try again")
        except ValueError:
            print("❌ Please enter a valid number")


def confirm_action(message: str = "Confirm this action") -> bool:
    """Confirm action"""
    while True:
        response = input(f"{message} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("❌ Please enter y/n")


def safe_int_input(prompt: str, default: int = 0, min_val: int = None, max_val: int = None) -> int:
    """Safe integer input"""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                return default
            
            num = int(value)
            
            if min_val is not None and num < min_val:
                print(f"❌ Value cannot be less than {min_val}")
                continue
            
            if max_val is not None and num > max_val:
                print(f"❌ Value cannot be greater than {max_val}")
                continue
            
            return num
            
        except ValueError:
            print("❌ Please enter a valid number")


def print_table(headers: list, rows: list, max_width: int = 80):
    """Print table"""
    if not rows:
        print("📝 No data available")
        return
    
    # Calculate column widths
    col_widths = []
    for i in range(len(headers)):
        max_width_col = len(headers[i])
        for row in rows:
            if i < len(row):
                max_width_col = max(max_width_col, len(str(row[i])))
        col_widths.append(min(max_width_col, max_width // len(headers)))
    
    # Print header
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))
    
    # Print data rows
    for row in rows:
        data_row = " | ".join(
            truncate_text(str(row[i]) if i < len(row) else "", col_widths[i]).ljust(col_widths[i])
            for i in range(len(headers))
        )
        print(data_row) 