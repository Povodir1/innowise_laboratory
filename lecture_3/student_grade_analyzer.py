students = []


def avg(grades_list: list) -> float:
    """
    Calculates the average grade from a list of grades.
    Uses try/except to handle division by zero if the list is empty.
    """
    try:
        return sum(grades_list) / len(grades_list)
    except ZeroDivisionError:
        # Return 0.0 if there are no grades (as the average is N/A per spec)
        return 0.0


def add_new_student():
    """
    Adds a new student to the list. 
    Checks if a student with the same name already exists.
    """
    print("--- Add New Student ---")
    name = input("Enter student name: ").strip()

    # Check for duplicate name
    if name in [student["name"] for student in students]:
        print(f"Student '{name}' already exists.")
    else:
        # Create a new dictionary with an empty list of grades
        students.append({"name": name, "grades": []})
        print(f"Student '{name}' successfully added.")


def add_grade_for_student():
    """
    Adds grades for an existing student.
    Grade input continues until 'stop' is entered.
    Includes data validation and error handling.
    """
    if not students:
        print("Student list is empty. Please add a student first.")
        return

    print("--- Add Grades ---")
    name = input("Enter student name to add grades: ").strip()

    current_student_list = [student_data for student_data in students if student_data["name"] == name]
    current_student = current_student_list[0] if current_student_list else None

    if current_student is None:
        print(f"Student '{name}' not found.")
        return

    print(f"Enter grades for {name} (0 to 100). Type 'done' to finish.")
    while True:
        grade = input("Grade (or 'done'): ").strip().lower()

        if grade == "done":
            break

        # 1. Check if the input is a number
        if not grade.isdigit():
            print("Invalid input. Grade must be a number.")
            continue

        try:
            grade_int = int(grade)
            # 2. Validate the range (0 to 100, according to spec)
            if not 0 <= grade_int <= 100:
                print("Invalid input. Grade must be between 0 and 100.")
                continue

            # Add the valid grade
            current_student['grades'].append(grade_int)
            print(f"Grade {grade_int} added.")

        except ValueError:
            print("Invalid input. Grade must be an integer.")


def show_report():
    """
    Generates a full report: individual average grade for each student, 
    maximum, minimum, and overall average grade for the entire group.
    """
    if not students:
        print("Student list is empty.")
        return

    print("\n--- Student Report ---")

    overall_sum_of_grades = 0
    overall_grade_count = 0

    # List to store averages for max/min calculation
    all_student_averages = []

    for student in students:
        if not student["grades"]:
            # N/A case: student exists but has no grades
            print(f"{student['name']}'s average grade is N/A")
            continue

        student_avg_grade = avg(student["grades"])

        # Print the student's average grade (formatted to one decimal place)
        print(f"{student['name']}'s average grade is {student_avg_grade:.1f}")
        all_student_averages.append(student_avg_grade)

        # Update variables for overall average (sum of all grades)
        overall_sum_of_grades += sum(student["grades"])
        overall_grade_count += len(student["grades"])

    print("-" * 30)

    # Print summary (only if at least one student has grades)
    if all_student_averages:
        # Find max/min from the list of averages
        max_average = max(all_student_averages)
        min_average = min(all_student_averages)

        # Overall average grade (sum of all grades / total number of grades)
        overall_average = overall_sum_of_grades / overall_grade_count

        # All summary outputs are formatted to one decimal place for consistency
        print(f"Max average: {max_average:.1f}")
        print(f"Min average: {min_average:.1f}")
        print(f"Overall average: {overall_average:.1f}")
    else:
        print("No grades available to calculate statistics.")

    print("---------------------------\n")


def find_top_performer():
    """
    Finds the student with the highest average grade using a lambda function.
    """
    if not students:
        print("Student list is empty.")
        return

    # Filter students who have grades to avoid errors
    students_with_grades = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("No students have grades recorded.")
        return

    try:
        # Find the student with the maximum average grade, using the avg function as the key
        top_student = max(students_with_grades, key=lambda student: avg(student["grades"]))

        top_avg = avg(top_student["grades"])
        print(f"\n--- Top Performer ---")
        print(f"Name: {top_student['name']}")
        print(f"Average Grade: {top_avg:.1f}")
        print("-----------------------\n")

    except ValueError:
        # This exception is unlikely after filtering, but remains for robustness
        print("Error while finding the top performer.")


def main():
    """
    The main function of the program, implementing the console menu.
    """
    print("--- Student Grade Manager ---")
    while True:
        choice = input(f"\nSelect action:\n"
                       f"1. Add a new student\n"
                       f"2. Add grades for a student\n"
                       f"3. Show report (all students)\n"
                       f"4. Find top performer\n"
                       f"5. Exit\n"
                       f"Your choice: ").strip()

        # Using match/case to handle the selection
        match choice:
            case "1":
                add_new_student()
            case "2":
                add_grade_for_student()
            case "3":
                show_report()
            case "4":
                find_top_performer()
            case "5":
                print("Program terminated.")
                break
            case _:
                print("Invalid choice. Please enter a number from 1 to 5.")


# Program entry point
if __name__ == "__main__":
    main()
