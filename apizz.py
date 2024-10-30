import aiohttp
import asyncio
import argparse
from colorama import Fore, Style, init
import time
import sys

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Enhanced wordlist covering common API paths and versions
COMMON_PATHS = [
    "api", "api/v1", "api/v2", "api/v3", "v1", "v2", "v3", "rest", "json", "graphql", 
    "internal", "secure", "services", "auth", "login", "register", "user", "admin", 
    "products", "orders", "items", "data", "search", "docs", "api-docs", "swagger", 
    "api/users", "api/admin", "api/products", "api/auth", "api/v1/auth", "api/v1/users",
    "v1/accounts", "v2/accounts", "api/v1/profile", "profile", "api/v1/orders", 
    "status", "health", "metrics", "v1/status", "v1/metrics", "api/metrics"
]

async def fetch_url(session, base_url, path, filter_codes, output_file):
    """
    Send a GET request to a specific path and check if it exists.
    """
    url = f"{base_url.rstrip('/')}/{path}"
    try:
        start_time = time.time()
        async with session.get(url) as response:
            response_time = time.time() - start_time

            # Check if response status matches the filter codes
            if response.status in filter_codes:
                status_message = f"[{response.status}] {url} - {response_time:.2f}s"
                if response.status == 200:
                    print(Fore.GREEN + "[FOUND] " + status_message)
                elif response.status == 403:
                    print(Fore.YELLOW + "[FORBIDDEN] " + status_message)
                elif response.status == 401:
                    print(Fore.YELLOW + "[UNAUTHORIZED] " + status_message)
                else:
                    print(Fore.CYAN + "[OTHER] " + status_message)
                
                # Save to output file if specified
                if output_file:
                    with open(output_file, "a") as f:
                        f.write(f"{url} - Status: {response.status} - Time: {response_time:.2f}s\n")
            else:
                print(Fore.RED + f"[NOT FOUND] {url} - Status: {response.status}")
    except Exception as e:
        print(Fore.RED + f"[-] Error accessing {url}: {str(e)}")

async def main(base_url, paths, filter_codes, rate_limit, output_file):
    """
    Main function to initiate requests to each path.
    """
    timeout = aiohttp.ClientTimeout(total=10)
    connector = aiohttp.TCPConnector(limit_per_host=rate_limit)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [fetch_url(session, base_url, path, filter_codes, output_file) for path in paths]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced API and Endpoint Finder")
    parser.add_argument("url", help="Base URL of the target website (e.g., https://example.com)")
    parser.add_argument("--wordlist", help="Path to custom wordlist file", default=None)
    parser.add_argument("--filter-codes", nargs="+", type=int, default=[200, 403, 401],
                        help="HTTP status codes to show (default: 200, 403, 401)")
    parser.add_argument("--rate-limit", type=int, default=10,
                        help="Max requests per second (default: 10)")
    parser.add_argument("--output-file", help="File to save found endpoints", default=None)
    args = parser.parse_args()

    # Load wordlist from file or use the default COMMON_PATHS
    if args.wordlist:
        try:
            with open(args.wordlist, "r") as f:
                paths = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + f"[-] Wordlist file not found: {args.wordlist}")
            sys.exit(1)
    else:
        paths = COMMON_PATHS

    # Start the asyncio event loop
    print(Fore.CYAN + f"[*] Starting scan for APIs and endpoints on {args.url}")
    print(Fore.CYAN + f"[*] Rate limit: {args.rate_limit} requests/second")
    asyncio.run(main(args.url, paths, args.filter_codes, args.rate_limit, args.output_file))
