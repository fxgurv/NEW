# coding: utf-8

# Dictionary to map key information to the number of lines to look ahead for related time information.
tm_map = {
    "Examination Time": 4, 
    "Online Payment": 2, 
    "Print Admission Ticket": 2, 
    "Submit Application": 2
}

def set_tm(patterns, v):
    """
    Sets the time map for a list of patterns based on a given value. 
    
    Args:
        patterns (list): A list of string patterns.
        v (str): The key in the tm_map to use for setting the time map.
    """
    for k in patterns:
        tm_map[k] = tm_map[v]

# Patterns related to registration/application 
baoming_pattern = [
    "Registration Method/Time",
    "Registration Time Is",
    "Submit Registration Application",
    "Submit Application",
    "Submit Application",
    "Registration Time",
    "Online Registration"
]
set_tm(baoming_pattern, "Submit Application")

# Example: Extract patterns from URL and process them within the last 3 lines.
# Example usage:
# - Find "Check Eligibility Review Results", "Eligibility Preliminary Review", or "Check Preliminary Examination Results"
# - Get time information from the subsequent few lines.

# Patterns related to examination time 
kaoshi_time_pattern1 = [
    "Public Subject Exam Time", 
    "Exam Content and Time",
    "Written Examination and Interview", 
    "Written Examination Plan", 
    "Written Examination Time", 
    "Exam Subjects", 
    "Written Examination"
]
set_tm(kaoshi_time_pattern1, "Examination Time")

kaoshi_time_pattern2 = [
    "Specialized Subject Exam Time", 
    "Public Subject Exam Time", 
    "Public Subject Written Examination Time"
]
set_tm(kaoshi_time_pattern2, "Examination Time")

# Patterns related to payment/fees
fee_time_pattern = [
    "Registration Confirmation and Online Payment",
    "Registration and Online Payment", 
    "Online Payment", 
    "Payment Confirmation",
    "Online Payment",
    "Print Admission Ticket" # Using Regular Expression
]
set_tm(fee_time_pattern, "Online Payment")

# Patterns related to accessing admission tickets
access_time_pattern = [
    "Print Admission Ticket", 
    "Print",
    "Admission Ticket Printing" 
]
set_tm(access_time_pattern, "Print Admission Ticket")


# Compiled list of patterns
ex_pattern = [
    baoming_pattern, 
    kaoshi_time_pattern1, 
    kaoshi_time_pattern2, 
    fee_time_pattern, 
    access_time_pattern
]

# Handle "Attachment" related information
fj = "Attachment"  # Starts with and traverses downwards 6 lines, also with href attribute.
tm_map[fj] = 6


# Possible source:  consider optional.
# Example Usage:
# "Released on ..."

# Key pattern dictionary, used for mapping information retrieval.
key_pat = {
    "Registration": baoming_pattern,
    "Examination": kaoshi_time_pattern1,
    "Payment": fee_time_pattern, 
    "Admission Ticket": access_time_pattern,
    "all": access_time_pattern
}

# Exam Type list used for classifying jobs/exams
zwlx_list = [
    "Civil Servant",
    "National Civil Servant",
    "Provincial Civil Servant",
    "Selected Students",
    "Targeted Recruitment", 
    "Public Security Recruitment", 
    "Military Civilian", 
    "Military-to-Civil",
    "Retired Military Personnel",
    "Career Establishment",
    "Talent Introduction",
    "Teacher Certification",
    "Special Post Teachers",
    "Hospital Recruitment",
    "Standard Training",
    "Open Selection",
    "Open Selection",
    "Open Selection",
    "Central Enterprises",
    "State-owned Enterprises",
    "Bank",
    "People's Bank of China",
    "Rural Credit Cooperatives",
    "University Village Officials",
    "Three Supports and One Help",
    "Grassroots Workers", 
    "Community Workers", 
    "Public Welfare Positions",
    "Auxiliary Police"
]
