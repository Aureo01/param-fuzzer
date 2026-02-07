#!/usr/bin/env python3
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from rich.console import Console
from rich.table import Table

console = Console()

def generate_fuzz_urls(url):
    #Prepare URLs for parameter fuzzing by swapping one parameter at a time with FUZZ
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query, keep_blank_values=True)

    fuzzed_urls = []
    param_names = list(query_params.keys())

    for param in param_names:
        new_params = query_params.copy()
        new_params[param] = ["FUZZ"]
        new_query = urlencode(new_params, doseq=True)
        fuzzed_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        fuzzed_urls.append({
            "original_param": param,
            "url": fuzzed_url
        })

    return fuzzed_urls

def print_table(results):
    # Show fuzzed URLs in a clean table for quick analysis
    table = Table(title="··-URLs with Parameters Replaced by FUZZ-··", show_header=True, header_style="bold cyan")
    table.add_column("Original Parameter", style="green")
    table.add_column("URL with FUZZ", style="magenta")

    for r in results:
        table.add_row(r["original_param"], r["url"])

    console.print(table)

def save_results(results, filename="fuzzed_params.txt"):
    #Save fuzzed URLs to output file
    with open(filename, "w") as f:
        for r in results:
            f.write(f"{r['url']}\n")
    console.print(f"URLs saved to: {filename}")

def load_urls(path):
    # Read URLs from a file and discard empty lines
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="Replace URL parameters with 'FUZZ' placeholder for fuzzing")
    parser.add_argument("-w", "--wordlist", help="Input file with URLs (one per line)")
    parser.add_argument("url", nargs="?", help="Single URL (optional if using -w)")
    parser.add_argument("-o", "--output", default="fuzzed_params.txt", help="Output file for generated URLs")

    args = parser.parse_args()

    if args.wordlist:
        urls = load_urls(args.wordlist)
    elif args.url:
        urls = [args.url]
    else:
        console.print("[red]💬You must specify a URL or a file with -w.[/red]")
        return

    all_results = []
    for url in urls:
        if not url.startswith(("http://", "https://")):
            console.print(f"[red]💬Invalid URL (must start with http:// or https://): {url}[/red]")
            continue

        results = generate_fuzz_urls(url)
        all_results.extend(results)

    if not all_results:
        console.print("[yellow]·💬No parameters found in URLs.[/yellow]")
        return

    print_table(all_results)
    save_results(all_results, args.output)

if __name__ == "__main__":
    main()
