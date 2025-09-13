import sys
import os
import re
import json
import shutil
# from string import Template # No longer needed

def to_snake_case(name):
    """Converts a string to snake_case."""
    return name.lower().replace(" ", "_")

def parse_qa_file(file_path):
    """Parses a text file with Q/A pairs and returns a list of dicts."""
    flashcards = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {file_path}")
        sys.exit(1)

    # Regex to find all question/answer blocks, ignoring case and final punctuation
    # It handles prefixes like Q/A, D/R, etc.
    pattern = re.compile(
        r"^(?:Q|D|Domanda|Question)[\.:]?\s*(.*?)\s*^(?:A|R|Risposta|Answer)[\.:]?\s*(.*?)\s*$",
        re.MULTILINE | re.IGNORECASE
    )

    matches = pattern.findall(content)
    
    for q, a in matches:
        flashcards.append({"question": q.strip(), "answer": a.strip()})

    if not flashcards:
        print("Warning: No question/answer pairs were found in the input file.")

    return flashcards

def generate_html(project_title, flashcards_data, template_path, output_dir):
    """Generates the final HTML file from a template and data."""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: HTML template not found at {template_path}")
        sys.exit(1)

    # template = Template(template_content) # Deactivated
    
    # Convert flashcards data to a JSON string for embedding in the script
    json_data_string = json.dumps(flashcards_data, indent=4, ensure_ascii=False)
    
    # Substitute placeholders in the template using simple replace
    final_html = template_content.replace('${project_title}', project_title)
    final_html = final_html.replace("'${flashcards_data}'", json_data_string) # Be specific to avoid errors

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    project_snake_case = to_snake_case(project_title)
    output_file_path = os.path.join(output_dir, f"{project_snake_case}.html")
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Successfully generated HTML file at: {output_file_path}")
    except IOError as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)

def archive_source_file(source_path, output_dir):
    """Copies the source text file into the project's output directory."""
    try:
        destination_path = os.path.join(output_dir, os.path.basename(source_path))
        # Prevent copying file onto itself
        if not os.path.abspath(source_path) == os.path.abspath(destination_path):
            shutil.copy(source_path, destination_path)
            print(f"Successfully archived source file to: {destination_path}")
        else:
            print("Source file is already in the output directory. Skipping archive.")
    except (IOError, shutil.Error) as e:
        print(f"Error archiving source file: {e}")
        sys.exit(1)

def main():
    """Main function to run the flashcard generator."""
    if len(sys.argv) != 3:
        print("Usage: python src/main.py <path_to_input_file> \"<Project Name>\"")
        sys.exit(1)
        
    input_file = sys.argv[1]
    project_name = sys.argv[2]
    
    print(f"Starting flashcard generation for project: '{project_name}'")
    
    # Define paths based on script location
    script_dir = os.path.dirname(__file__)
    base_dir = os.path.dirname(script_dir)
    template_path = os.path.join(script_dir, 'templates', 'flashcard_template.html')
    
    project_name_snake_case = to_snake_case(project_name)
    output_dir = os.path.join(base_dir, 'outputs', project_name_snake_case)

    # 1. Parse the data
    flashcards = parse_qa_file(input_file)
    
    # 2. Generate the HTML
    if flashcards:
        generate_html(project_name, flashcards, template_path, output_dir)
        # 3. Archive the source file
        archive_source_file(input_file, output_dir)
    else:
        print("Stopping process as no data was parsed.")

if __name__ == "__main__":
    main()
