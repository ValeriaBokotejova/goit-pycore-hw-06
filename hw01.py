# Technical Task Description
# Develop a system for managing an address book.

# Entities:
# 1. Field: Base class for record fields.
# 2. Name: Class for storing contact names. Mandatory field.
# 3. Phone: Class for storing phone numbers. Should validate the format (10 digits).
# 4. Record: Class for storing contact information, including name and a list of phone numbers.
# 5. AddressBook: Class for storing and managing records.

# Functionality:
# AddressBook: 
# 1. Adding records.
# 2. Searching records by name.
# 3. Deleting records by name.
# Record: 
# 1. Adding phones.
# 2. Deleting phones.
# 3. Editing phones.
# 4. Searching for a phone.


from collections import UserDict

class Field: # Define the base class for fields in a record
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): # Class for storing and validating contact names
    def __init__(self, value):
        value = value.lower()  # Convert all letters to lowercase
        if not value.isalpha(): # Check if the name contains only alphabetic characters
            raise ValueError("Name must contain only alphabetic characters.")
        super().__init__(value)
    

class Phone(Field): # Class for storing and validating phone numbers
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10: # Check if the phone number contains 10 digits
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)

class Record: # Class representing a contact record
    def __init__(self, name):
        self.name = Name(name) # Store the contact name
        self.phones = []       # Initialize an empty list for phone numbers

    def add_phone(self, phone): # Add a phone number to the list
        self.phones.append(Phone(phone))

    def remove_phone(self, phone): # Remove a phone number from the list
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone): # Edit a phone number in the list
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone=None): # Find a phone number in the list
        if phone is None:
            return [p.value for p in self.phones]
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise ValueError("Phone number not found")
    
    def __str__(self): # String representation of the record
    # Determine the number of phones
        num_phones = len(self.phones)
        phone_word = "phone" if num_phones == 1 else "phones"
    
    # Construct the string representation
        return f"Contact name: {self.name.value}, {phone_word}: {', '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict): # Class for managing the address book

    def add_record(self, record):  # Add a record to the address book
        self.data[record.name.value] = record

    def find(self, name):  # Find a record in the address book by name
        return self.data.get(name)

    def delete(self, name): # Delete a record from the address book by name
        del self.data[name]

def input_error(func): # Decorator for handling input errors
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter name."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command."
        except:
            return "Invalid command."
    return inner

def parse_input(user_input): # Parse user input into command and arguments
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


# Functions for handling different commands

@input_error
def add_contact(args, address_book): # Add a contact to the address book
    if len(args) < 2:
        raise ValueError("Give me name and at least one phone number, separated by spaces.")
    name = args[0]
    phones = args[1:]
    record = address_book.find(name)
    if record:
        for phone in phones:
            record.add_phone(phone)
        return f"Phone number(s) added to contact '{name}'."
    else:
        record = Record(name)
        for phone in phones:
            record.add_phone(phone)
        address_book.add_record(record)
        return "Contact added."

@input_error
def change_contact(args, address_book): # Change a contact's phone number
    if len(args) < 2:
        raise ValueError("Please provide both name and new phone number.")
    if len(args) > 2:
        raise ValueError("Please provide the contact name and the new phone number only.")
    name, new_phone = args[0], args[1]
    record = address_book.find(name)
    
    # Create a dictionary of available phone numbers for the contact
    available_phones = {str(i): phone for i, phone in enumerate(record.phones)}
    print(f"Available phone numbers for contact {name}:")
    for i, phone in available_phones.items():
        print(f"{i}: {phone}")

    try:
        # Prompt user to select the phone number to change
        chosen_phone = input("Enter the number of the phone you want to change: ")
        old_phone = available_phones[chosen_phone].value
        record.remove_phone(old_phone)  # Removing the old number
        record.add_phone(new_phone)  # Adding the new number
        return "Contact updated."
    except KeyError:
        return "Invalid phone number. Please enter a valid number."

@input_error
def show_phone(args, address_book): # Show phone numbers for a contact
    if len(args) == 0: # Check if the user entered an empty command
        return "Please provide the name of the contact or type 'phone <contact_name>'."
    name = args[0]
    record = address_book.find(name)
    if record: # If the contact is found
        phones = record.find_phone()  # Get the phone numbers for the contact
        if len(phones) == 1:
            return f"The phone number for contact '{name}' is: {', '.join(phones)}."
        else:
            return f"The phone numbers for contact '{name}' are: {', '.join(phones)}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_all_contacts(address_book): # Show all contacts in the address book
    if address_book:
        return "\n".join([str(record) for record in address_book.values()])
    else:
        return "No contacts found."

@input_error
def process_input(command, args, address_book):  # Process the user input command
    if command == "hello":
        return "How can I help you?"
    elif command == "add":
        return add_contact(args, address_book)
    elif command == "change":
        return change_contact(args, address_book)
    elif command == "phone":
        return show_phone(args, address_book)
    elif command == "all":
        return show_all_contacts(address_book)
    else:
        return "Invalid command."

@input_error
def main():  # Main function to run the program and interact with the user
    address_book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            print(process_input(command, args, address_book))

if __name__ == "__main__":
    main()
