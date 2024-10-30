# Apizz - Enhanced API Endpoint Finder

Apizz is a fast, asynchronous Python tool for discovering potential API endpoints on a target website. It allows for endpoint discovery, filtering by HTTP status codes, rate limiting, and saving results to a file. Built with `aiohttp` and `asyncio`, Apizz is optimized for scanning common API paths, making it ideal for security testers and bug bounty hunters.

## Features

- Asynchronous requests for faster scans.
- Colored output to easily distinguish between endpoint statuses.
- Customizable HTTP status filters to focus on specific responses (e.g., 200, 403, 401).
- Adjustable rate limiting to avoid overwhelming target servers.
- Save results to a specified file for future reference.
- Enhanced wordlist with common API paths and versions, covering a wide range of standard API structures.

## Requirements

- Python 3.7 or above
- Install dependencies:

```bash
pip install aiohttp colorama
```

## Usage

Run Apizz with the base URL and optional parameters:

```bash
python apizz.py <base_url> [options]
```

### Positional Argument

- `<base_url>`: The target website URL to scan (e.g., `https://example.com`).

### Options

- `--wordlist`: Path to a custom wordlist file (default: uses the built-in list of common API paths).
- `--filter-codes`: Space-separated list of HTTP status codes to show in the output (default: `200`, `403`, `401`).
- `--rate-limit`: Maximum requests per second to avoid rate limiting (default: `10`).
- `--output-file`: Specify a file to save found endpoints and their statuses.

## Example Commands

1. **Basic scan with default settings:**

   ```bash
   python apizz.py https://example.com
   ```

2. **Using a custom wordlist:**

   ```bash
   python apizz.py https://example.com --wordlist custom_wordlist.txt
   ```

3. **Filtering only 200 and 403 status codes:**

   ```bash
   python apizz.py https://example.com --filter-codes 200 403
   ```

4. **Saving results to an output file:**

   ```bash
   python apizz.py https://example.com --output-file results.txt
   ```

5. **Setting a rate limit of 5 requests per second:**

   ```bash
   python apizz.py https://example.com --rate-limit 5
   ```

## Sample Output

The tool provides color-coded output for quick interpretation:

- `[FOUND]` - Endpoint with a 200 OK status.
- `[FORBIDDEN]` - Endpoint with a 403 Forbidden status.
- `[UNAUTHORIZED]` - Endpoint with a 401 Unauthorized status.
- `[NOT FOUND]` - Endpoint that doesn’t exist (404 Not Found).

### Example output:

```
[*] Starting scan for APIs and endpoints on https://example.com
[*] Rate limit: 10 requests/second
[FOUND] https://example.com/api/v1 - 0.23s
[FORBIDDEN] https://example.com/admin - 0.21s
[UNAUTHORIZED] https://example.com/api/v1/auth - 0.19s
[NOT FOUND] https://example.com/nonexistent - 0.25s
```

## License

This project is licensed under the MIT License.

Happy scanning!
