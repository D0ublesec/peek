import argparse
import os
import re
import concurrent.futures
from termcolor import colored
from tqdm import tqdm  # For the loading bar
import threading
import time

def load_wordlist(wordlist_file=None, word_string=None):
    """Load words from a wordlist file into a set, or use a direct string."""
    if word_string:
        return {word_string}  # Treat the string as a single word
    elif wordlist_file:
        with open(wordlist_file, 'r') as f:
            return {line.strip() for line in f if line.strip()}
    return set()  # Return empty set if neither is provided

def get_snippet(file_content, word, case_sensitive=False, context_size=30):
    """Get a snippet of text around the word and highlight the matched word."""
    if not case_sensitive:
        file_content = file_content.lower()
        word = word.lower()

    # Search for the word and get a snippet around it
    match = re.search(r'.{0,' + str(context_size) + r'}' + re.escape(word) + r'.{0,' + str(context_size) + r'}', file_content)
    
    if match:
        snippet = match.group(0)
        
        # Find the position of the matched word in the snippet
        match_start = snippet.lower().find(word.lower())
        match_end = match_start + len(word)

        # Split the snippet into three parts:
        before_match = snippet[:match_start]  # Text before the match
        match_text = snippet[match_start:match_end]  # Matched word
        after_match = snippet[match_end:]  # Text after the match

        # Color the different parts
        before_match_colored = colored(before_match, 'cyan')
        match_text_colored = colored(match_text, 'magenta', attrs=['bold'])
        after_match_colored = colored(after_match, 'cyan')

        # Combine the parts into one final colored snippet
        final_snippet = before_match_colored + match_text_colored + after_match_colored

        return final_snippet
    return ""

def search_file(file_path, wordlist, case_sensitive=False, verbose=False, stop_event=None):
    """Search a file for words from the wordlist."""
    word_counts = {}
    snippets = {}  # Dictionary to store snippets for verbose output
    try:
        with open(file_path, 'rb') as f:  # Open file in binary mode
            file_content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return word_counts, snippets

    file_content_str = file_content.decode('utf-8', errors='ignore')  # Decode binary to string with errors ignored

    if not case_sensitive:
        file_content_str = file_content_str.lower()

    for word in wordlist:
        search_word = word if case_sensitive else word.lower()
        # This regex will match the word even if it is adjacent to other words
        count = len(re.findall(r'(?<!\w)' + re.escape(search_word) + r'(?!\w)', file_content_str))  # Exact match
        if count > 0:
            word_counts[word] = word_counts.get(word, [])
            word_counts[word].append((count, file_path))  # Store the count and the file path
            
            if verbose:
                snippet = get_snippet(file_content_str, word, case_sensitive)
                if snippet:
                    snippets[word] = snippets.get(word, [])
                    snippets[word].append((file_path, snippet))

        if stop_event and stop_event.is_set():
            break

    return word_counts, snippets

def search_directory(dir_path, wordlist, case_sensitive=False, verbose=False, stop_event=None):
    """Search all files in a directory and its subdirectories."""
    word_counts = {}
    snippets = {}
    files = []
    
    for root, dirs, files_in_dir in os.walk(dir_path):
        for file in files_in_dir:
            files.append(os.path.join(root, file))

    with tqdm(total=len(files), desc="Searching files", unit="file") as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                futures.append(executor.submit(search_file, file_path, wordlist, case_sensitive, verbose, stop_event))
            
            for future in concurrent.futures.as_completed(futures):
                file_word_counts, file_snippets = future.result()
                for word, occurrences in file_word_counts.items():
                    if word not in word_counts:
                        word_counts[word] = []
                    word_counts[word].extend(occurrences)
                
                for word, snippet_data in file_snippets.items():
                    if word not in snippets:
                        snippets[word] = []
                    snippets[word].extend(snippet_data)

                pbar.update(1)

                if stop_event and stop_event.is_set():
                    break

    return word_counts, snippets

def save_results(word_counts, output_file):
    """Save the matched results to a file."""
    with open(output_file, 'w') as f:
        for word, occurrences in word_counts.items():
            f.write(f"String: {word}\n")
            for count, file_path in occurrences:
                f.write(f"    File: {file_path}, Count: {count}\n")

def print_banner():
    """Print the banner when the script runs."""
    banner = """
   _ (`-.    ('-.     ('-.  .-. .-')   
  ( (OO  ) _(  OO)  _(  OO) \  ( OO )  
 _.`     \(,------.(,------.,--. ,--.  
(__...--'' |  .---' |  .---'|  .'   /  
 |  /  | | |  |     |  |    |      /,  
 |  |_.' |(|  '--. (|  '--. |     ' _) 
 |  .___.' |  .--'  |  .--' |  .   \   
 |  |      |  `---. |  `---.|  |\   \  
 `--'      `------' `------'`--' '--'  
"""
    print(colored(banner, 'magenta'))

def print_results_table(word_counts, snippets, verbose=False):
    """Print the results table after search completion with colorized lines and column delimiters."""
    if word_counts:
        # Calculate the maximum length of the file path to adjust column width
        max_file_path_length = max(len(file_path) for occurrences in word_counts.values() for count, file_path in occurrences)
        
        # Add some padding to the file path column
        file_path_column_width = max(max_file_path_length, 50)  # Ensure it's at least 50 characters wide
        
        # Print the top border
        if verbose:
            print("-" * (30 + 12 + file_path_column_width + 60))
            print(f"| {'Searched Word':<30} | {'Occurrences':<12} | {'File Path':<{file_path_column_width}} | {'Snippet':<47} |")
        else:
            print("-" * (30 + 12 + file_path_column_width + 20))
            print(f"| {'Searched Word':<30} | {'Occurrences':<12} | {'File Path':<{file_path_column_width}} |")
        
        # Print the separator line under the header
        print("-" * (30 + 12 + file_path_column_width + (60 if verbose else 20)))
        
        for word, occurrences in word_counts.items():
            for count, file_path in occurrences:
                if verbose and word in snippets:
                    # Get the snippet for the current file path
                    snippet = next((s for f, s in snippets[word] if f == file_path), '')
                    # Remove newline characters from the snippet
                    snippet = snippet.replace('\n', ' ').strip()
                    print(colored(f"| {word:<30} | {count:<12} | {file_path:<{file_path_column_width}} | {snippet:<60} |", 'green'))
                else:
                    print(colored(f"| {word:<30} | {count:<12} | {file_path:<{file_path_column_width}} |", 'green'))

        # Print bottom border
        print("-" * (30 + 12 + file_path_column_width + (60 if verbose else 20)))
    else:
        print("Search completed with no matches.")


def listen_for_input(stop_event):
    """Listen for the Enter key press to stop the search."""
    input("Press Enter to cancel the search and print the current results...\n")
    print(colored("Stopping the search... Please wait a moment.", 'yellow'))
    stop_event.set()

def main():
    parser = argparse.ArgumentParser(description="Search a file or directory for words from a wordlist or a string.")
    
    # Argument group for file or directory
    group_input = parser.add_mutually_exclusive_group(required=True)
    group_input.add_argument('-f', '--file', help="Path to the file to search in")
    group_input.add_argument('-d', '--dir', help="Path to the directory to search in recursively")
    
    # Argument group for wordlist or string
    group_word_or_string = parser.add_mutually_exclusive_group(required=True)
    group_word_or_string.add_argument('-w', '--wordlist', help="Path to the wordlist file")
    group_word_or_string.add_argument('-s', '--string', help="String to search for")
    
    # Other optional arguments
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode, print each check result")
    parser.add_argument('-o', '--output', help="Save matched results to the specified output file")
    parser.add_argument('--case-sensitive', action='store_true', help="Enable case-sensitive search (default is case-insensitive)")
    parser.add_argument('--no-banner', action='store_true', help="Disable banner print")

    args = parser.parse_args()

    # Print banner if not disabled
    if not args.no_banner:
        print_banner()

    # Load wordlist or string
    if args.string:
        wordlist = load_wordlist(word_string=args.string)
    elif args.wordlist:
        wordlist = load_wordlist(wordlist_file=args.wordlist)
    else:
        print("Error: You must specify either a wordlist file or a string to search.")
        return

    word_counts = {}
    snippets = {}

    # Initialize stop_event to signal when user presses Enter
    stop_event = threading.Event()

    # Start input listener thread
    input_thread = threading.Thread(target=listen_for_input, args=(stop_event,))
    input_thread.daemon = True
    input_thread.start()

    # Perform the search, depending on file or directory argument
    if args.file:
        word_counts, snippets = search_file(args.file, wordlist, case_sensitive=args.case_sensitive, verbose=args.verbose, stop_event=stop_event)
    elif args.dir:
        word_counts, snippets = search_directory(args.dir, wordlist, case_sensitive=args.case_sensitive, verbose=args.verbose, stop_event=stop_event)
    else:
        print("Error: You must specify either a file or a directory to search.")
        return

    # Save to output file if specified
    if args.output:
        save_results(word_counts, args.output)
        print(f"Results saved to {args.output}")

    # Print the results table after search completion
    print_results_table(word_counts, snippets, verbose=args.verbose)

if __name__ == "__main__":
    main()