def remove_dead_code(files_dict, dead_code_list, method_line_ranges):
    """
    Remove dead methods from source code files.
    """
    dead_lines_by_file = {fname: set() for fname in files_dict.keys()}
    
    for dead in dead_code_list:
        if dead in method_line_ranges:
            info = method_line_ranges[dead]
            fname = info['file']
            start = info['start']
            end = info['end']
            
            # Record lines to delete
            for i in range(start, end + 1):
                if fname in dead_lines_by_file:
                    dead_lines_by_file[fname].add(i)
                    
    cleaned_files = {}
    total_lines_removed = 0
    for fname, code in files_dict.items():
        lines = code.splitlines()
        clean_lines = []
        for i, line in enumerate(lines):
            line_num = i + 1
            if line_num not in dead_lines_by_file.get(fname, set()):
                clean_lines.append(line)
            else:
                total_lines_removed += 1
                
        cleaned_files[fname] = "\n".join(clean_lines)
        
    return cleaned_files, total_lines_removed
