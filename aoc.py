#!/usr/bin/env python3
"""
A module for transparently using 7zip-compressed Advent of Code input files.

This module provides a convenient workflow for using Advent of Code puzzle
inputs while respecting the author's request not to post them publicly. It
allows you to store your inputs in a local, password-protected .7z archive.

The first time you use it with a plain text file (e.g., "input01.txt"),
it will automatically create a compressed, password-protected
"input01.txt.7z" archive and delete the original plain text file.
On subsequent runs, it reads directly from the .7z archive in memory.

Requirements:
- The `7zz` command-line utility must be installed and in your
  system's PATH.  (This is part of the p7zip package).
- A file named `.password` must exist in the current directory,
  containing the password for the archives.
"""
import os
import re
import subprocess

class AoCInput:
    """
    An object representing a puzzle input file, which may be compressed.
    """

    def __init__(self, input_file: str):
        """
        Initializes the AoCInput object and handles file compression.

        If `input_file` is a plain text file (e.g., "input01.txt"), this
        constructor will create a password-protected .7z archive and delete
        the original.

        Args:
            input_file (str): The path to the input file (e.g., "input01.txt"
                              or "input01.txt.7z").

        Raises:
            FileNotFoundError: If the required `.password` file is not found.
            RuntimeError: If the `7zz` command fails during compression.
        """
        try:
            with open('.password', 'r') as f:
                self._password = f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(
                "Required '.password' file not found in the current directory."
            )

        self.filepath = input_file

        # If given a plain text file like "input01.txt"
        if re.match(r"^input\d+\.txt$", self.filepath):
            archive_path = f"{self.filepath}.7z"

            # If the compressed version doesn't already exist, create it.
            if not os.path.exists(archive_path):
                print(f"Compressing {self.filepath} to {archive_path}...")
                command = [
                    "7zz", "a", f"-p{self._password}", archive_path, self.filepath
                ]
                # Run the command, hiding its output unless there's an error.
                result = subprocess.run(
                    command, capture_output=True, text=True
                )
                if result.returncode != 0:
                    raise RuntimeError(
                        f"Error compressing {self.filepath}: 7zz exited with code {result.returncode}\n"
                        f"Stderr: {result.stderr}"
                    )

            # Point the object to the compressed file and delete the original
            self.filepath = archive_path
            if os.path.exists(input_file):
                os.remove(input_file)

    def slurp(self) -> str:
        """
        Decompresses the input file and returns its entire content as a single string.

        This is useful for puzzles where the input is a single block of text or
        where newline processing is significant.

        Returns:
            str: The entire decompressed file content.

        Raises:
            subprocess.CalledProcessError: If the `7zz` command fails during extraction.
        """
        if not self.filepath.endswith(".7z"):
            # This case should not be reached if using the constructor as intended.
            with open(self.filepath, 'r') as f:
                return f.read()

        command = [
            "7zz", "e", "-so", f"-p{self._password}", self.filepath
        ]
        # Run the command, capture stdout, and raise an exception on failure.
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )
        # Python doesn't have a chomp() function!
        return re.sub( r"\r?\n$", "", result.stdout )

    def lines(self) -> list[str]:
        """
        Decompresses the input file and returns its content as a list of lines.

        This is the most common method for line-based AoC puzzles. Note that
        this method does not strip trailing newlines from each line.

        Returns:
            list[str]: A list of strings, where each string is a line from the file.
        """
        content = self.slurp()
        return content.splitlines()

# --- Example Usage ---
def main():
    """
    Demonstrates how to use the AoCInput class.
    
    To run this example:
    1. Create a file named ".password" with a password in it:
       echo "mysecretpassword" > .password
    2. Create a sample input file named "input01.txt":
       echo -e "1000\n2000\n3000" > input01.txt
    3. Run this script:
       python3 aoc_input.py
    """
    print("--- First Run: Compressing the file ---")
    try:
        # On the first run, this will create 'input01.txt.7z' and delete 'input01.txt'
        input_obj = AoCInput("input01.txt")
        
        # Get the input as a list of lines
        lines = input_obj.lines()
        print(f"Read {len(lines)} lines from {input_obj.filepath}")
        print("First line:", lines[0])
        
        # You can now solve the puzzle
        total = sum(int(line) for line in lines)
        print("Sum of numbers:", total)

    except (FileNotFoundError, RuntimeError) as e:
        print(f"An error occurred: {e}")
        return

    print("\n--- Second Run: Reading from the archive ---")
    if not os.path.exists("input01.txt.7z"):
        print("Archive file not found. Please run the first part of the example again.")
        return
        
    try:
        # On subsequent runs, it reads directly from the .7z file
        input_obj_2 = AoCInput("input01.txt.7z")
        
        # Get the whole file as a single string
        whole_file = input_obj_2.slurp()
        print(f"Read {len(whole_file)} characters from {input_obj_2.filepath} using slurp()")
        print("File content preview:\n---")
        print(whole_file.strip())
        print("---")

    except (FileNotFoundError, RuntimeError) as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
