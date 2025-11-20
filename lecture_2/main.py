CURRENT_YEAR = 2025


def generate_profile(age:int) -> str:
    """
    Determines a person's life stage based on their age.

    Uses predefined ranges to classify the age as
    "Child", "Teenager", or "Adult".

    Args:
        age (int): The current age of the person.

    Returns:
        str: The name of the life stage ('Child', 'Teenager', 'Adult').
    """
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <=19:
        return "Teenager"
    elif 20 <= age <= 100:
        return "Adult"
    raise ValueError("Invalid age value")


print("Welcome, Dear student!")


#Get user inputs
user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")


#Age calculation
birth_year = int(birth_year_str)
current_age = CURRENT_YEAR-birth_year


#Ask users hobbies
hobbies = []
while True:
    user_input = input("Enter a favorite hobby or type 'stop' to finish:")

    # Condition for exiting the loop
    if user_input.lower() == "stop":
        break
    hobbies.append(user_input)

life_stage = generate_profile(current_age)

#Create profile dictionary
user_profile = {"name": user_name,
                "age": current_age,
                "stage": life_stage,
                "hobbies": hobbies}

#Formatted profile summary output
print(f"\n---\n"
      f"Profile Summary:\n"
      f"Name: {user_profile["name"]}\n"
      f"Age: {user_profile["age"]}\n"
      f"Life Stage: {user_profile["stage"]}")

# Conditional hobby output: if the list is not empty, print the list, otherwise a message
if user_profile["hobbies"]:
    print(f"Favorite Hobbies ({len(user_profile["hobbies"])}):")
    for hobby in user_profile["hobbies"]:
        print(f"- {hobby}")
else:
    print("You didn`t mention any hobbies")
print("---")



