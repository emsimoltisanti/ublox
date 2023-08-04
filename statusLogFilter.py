def get_status(fixType_value, carrSoln_value):
    """
    Get the status based on the fixType and carrSoln values.

    @param fixType_value: The value of "fixType" extracted from the original format.
    @type fixType_value: str

    @param carrSoln_value: The value of "carrSoln" extracted from the original format.
    @type carrSoln_value: str

    @return: The status determined based on the fixType and carrSoln values.
    @rtype: str
    """
    if fixType_value == "0" or carrSoln_value == "0":
        return "NO FIX"
    elif fixType_value == "1":
        return "DR ONLY"
    elif fixType_value in ("2", "3") and carrSoln_value == "1":
        return "GNSS FLOAT"
    elif fixType_value in ("2", "3") and carrSoln_value == "2":
        return "GNSS FIXED"
    elif fixType_value == "4" and carrSoln_value == "1":
        return "GNSS FLOAT + DR"
    elif fixType_value == "4" and carrSoln_value == "2":
        return "GNSS FIXED + DR"
    else:
        return "Unknown"


def filter_and_index_log_file(input_file, output_file):
    """
    Filter and index the log file.

    @param input_file: The input log file name to be filtered and indexed (without the .log extension).
    @type input_file: str

    @param output_file: The output file name for the filtered and indexed log in CSV format.
    @type output_file: str
    """
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        filtered_lines = []
        index = 1  # Initialize the index to 1

        # Add the header line to the file
        header_line = "Index,Status\n"
        filtered_lines.append(header_line)

        for line in lines:
            if "<UBX(NAV-PVT" in line:
                # Extract "fixType" and "carrSoln" values from the original format
                data = line.split(", ")
                fixType_value = None
                carrSoln_value = None

                for value in data:
                    if "fixType=" in value:
                        fixType_value = value.split("=")[1]
                    elif "carrSoln=" in value:
                        carrSoln_value = value.split("=")[1]

                if fixType_value is not None and carrSoln_value is not None:
                    # Get the status based on the conditions
                    status = get_status(fixType_value, carrSoln_value)

                    # Create the new line with the new format, including the "index" and "status" fields
                    new_line = f"{index},{status}\n"
                    filtered_lines.append(new_line)
                    index += 1  # Increment the index on each iteration

        with open(output_file, 'w') as file:
            file.writelines(filtered_lines)

        print(f"Filtered and indexed file saved to {output_file}")
    except FileNotFoundError:
        print("The file could not be found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    input_filename = input("Enter the name of the .log file to filter and index (without the .log extension): ")
    output_filename = "filtered_and_indexed_log.csv"  # Output file name for the filtered and indexed log in CSV format

    print("Starting processing...")
    filter_and_index_log_file(f"{input_filename}.log", output_filename)
