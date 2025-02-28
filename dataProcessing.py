import os

def Segment():
    """Splits 'Original.txt' into 5 segments and stores them in the 'Segments' folder."""
    if not os.path.exists('Original.txt'):
        print("❌ Error: 'Original.txt' not found! Make sure to upload the file first.")
        return  

    with open('Original.txt', 'r') as f:
        content = f.read()

    if not content:
        print("❌ Error: 'Original.txt' is empty!")
        return  

    os.makedirs("Segments", exist_ok=True)  # Ensure Segments directory exists
    segment_size = len(content) // 5  # Divide into 5 equal parts
    k = 0

    for i in range(5):
        segment_path = os.path.join("Segments", f"{i}.txt")
        with open(segment_path, 'w') as f:
            ctr = 0
            for j in range(k, len(content)):
                k += 1
                f.write(content[j])
                ctr += 1
                if ctr == segment_size and i != 4:
                    break  

    print("✅ File successfully segmented into the 'Segments' folder.")

def gatherInfo():
    """Creates a log file in 'Infos' containing the size of each segment."""
    if not os.path.exists("Segments"):
        print("❌ Error: 'Segments' folder not found! Run Segment() first.")
        return

    os.makedirs("Infos", exist_ok=True)  # Ensure Infos directory exists
    log_path = os.path.join("Infos", "Log.txt")

    with open(log_path, 'w') as mainFile:
        for filename in sorted(os.listdir("Segments")):
            segment_path = os.path.join("Segments", filename)
            with open(segment_path, 'r') as f:
                content_length = len(f.read())
                mainFile.write(f"{content_length}::::")

    print("✅ Segment info successfully recorded in 'Infos/Log.txt'.")

def trim():
    """Ensures each segment contains only the valid data by trimming unnecessary parts."""
    log_path = os.path.join("Infos", "Log.txt")

    if not os.path.exists(log_path):
        print("❌ Error: 'Log.txt' not found! Run gatherInfo() first.")
        return

    with open(log_path, 'r') as mainFile:
        content = mainFile.read().split('::::')

    segments_path = "Segments"
    file_list = sorted(os.listdir(segments_path))

    for i, filename in enumerate(file_list):
        segment_path = os.path.join(segments_path, filename)

        with open(segment_path, 'r') as f:
            data = f.read()

        if i < len(content) - 1:  # Avoid index error
            valid_length = int(content[i])
            trimmed_data = data[:valid_length]  # Keep only valid data

            with open(segment_path, 'w') as f:
                f.write(trimmed_data)

    print("✅ Segments successfully trimmed.")

def Merge():
    """Combines all segments back into 'Output.txt'."""
    if not os.path.exists("Segments"):
        print("❌ Error: 'Segments' folder not found! Cannot merge.")
        return

    with open("Output.txt", "w") as mainFile:
        for i in range(5):
            segment_path = os.path.join("Segments", f"{i}.txt")

            if not os.path.exists(segment_path):
                print(f"❌ Error: Missing segment {i}.txt. Merge failed.")
                return

            with open(segment_path, "r") as f:
                content = f.read()
                print(f'📂 Merging Segment {i} -> {content}')
                mainFile.write(content)

            os.remove(segment_path)  # Delete the segment after merging

    print("✅ Segments successfully merged into 'Output.txt'.")
