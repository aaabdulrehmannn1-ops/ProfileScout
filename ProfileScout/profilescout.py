#!/usr/bin/env python3
"""
================================================================================
  ProfileScout - OSINT Username & Alias Reconnaissance Tool
================================================================================

DEPENDENCIES:
  Install required packages using:
    pip install requests colorama

USAGE:
  python3 profilescout.py

This is a complete, production-ready OSINT tool for security analysts.
No placeholders. No external configuration needed. Ready to execute.
================================================================================
"""

import requests
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style
from urllib.parse import quote
import warnings

# Suppress SSL warnings for stability across different platform configurations
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class ProfileScout:
    """
    Professional OSINT reconnaissance tool for username verification across
    multiple social networks and public platforms.
    """

    # Comprehensive platform database with URL structure templates
    PLATFORMS = {
        "GitHub": "https://github.com/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Twitter/X": "https://twitter.com/{}",
        "LinkedIn": "https://www.linkedin.com/in/{}",
        "Instagram": "https://www.instagram.com/{}",
        "Facebook": "https://www.facebook.com/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}/",
        "Twitch": "https://www.twitch.tv/{}",
        "YouTube": "https://www.youtube.com/@{}",
        "Medium": "https://medium.com/@{}",
        "Dev.to": "https://dev.to/{}",
        "Mastodon": "https://mastodon.social/@{}",
        "Bluesky": "https://bsky.app/profile/{}",
        "Threads": "https://www.threads.net/@{}",
        "Letterboxd": "https://letterboxd.com/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Behance": "https://www.behance.net/{}",
        "GitLab": "https://gitlab.com/{}",
        "Linktree": "https://linktr.ee/{}",
        "Substack": "https://{}.substack.com",
        "Patreon": "https://www.patreon.com/{}",
        "Discord": "https://discordapp.com/users/{}",
    }

    def __init__(self, timeout=8, max_workers=10):
        """
        Initialize ProfileScout reconnaissance engine.

        Args:
            timeout: HTTP request timeout in seconds
            max_workers: Maximum concurrent threads for platform scanning
        """
        self.timeout = timeout
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def display_banner(self):
        """Display beautiful ASCII art banner."""
        banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    {Fore.GREEN}P R O F I L E S C O U T{Fore.CYAN}                              ║
║                {Fore.MAGENTA}OSINT Username & Alias Reconnaissance Tool{Fore.CYAN}                ║
║                    {Fore.YELLOW}Security Analysis Platform{Fore.CYAN}                            ║
║                                                                              ║
║               For professional security analysts & researchers              ║
║                     Passive Footprinting across 25+ Platforms                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)

    def check_profile(self, platform, username):
        """
        Check if a profile exists on a specific platform.

        Args:
            platform: Platform name (key from PLATFORMS dict)
            username: Username/alias to search for

        Returns:
            dict: Contains status, platform, username, and response details
        """
        url_template = self.PLATFORMS[platform]
        encoded_username = quote(username, safe='')
        url = url_template.format(encoded_username)

        result = {
            'platform': platform,
            'username': username,
            'status': 'unknown',
            'url': url,
            'http_code': None,
            'error': None
        }

        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True, verify=False)
            result['http_code'] = response.status_code

            # Profile found
            if response.status_code == 200:
                result['status'] = 'found'
            # Profile not found or unavailable
            elif response.status_code == 404:
                result['status'] = 'not_found'
            # Rate limiting / Too Many Requests
            elif response.status_code == 429:
                result['status'] = 'rate_limited'
                result['error'] = 'Rate limit exceeded'
            # Forbidden access
            elif response.status_code == 403:
                result['status'] = 'forbidden'
                result['error'] = 'Access forbidden'
            # Redirect but not 200 (may indicate profile exists or doesn't)
            elif response.status_code in [301, 302, 307, 308]:
                result['status'] = 'redirect'
            else:
                result['status'] = 'unknown'
                result['error'] = f'HTTP {response.status_code}'

        except requests.exceptions.Timeout:
            result['status'] = 'error'
            result['error'] = 'Connection timeout'
        except requests.exceptions.ConnectionError:
            result['status'] = 'error'
            result['error'] = 'Connection failed'
        except requests.exceptions.RequestException as e:
            result['status'] = 'error'
            result['error'] = 'Request error'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(type(e).__name__)

        return result

    def scan_username(self, username):
        """
        Scan a username across all platforms concurrently.

        Args:
            username: The username/alias to search for

        Returns:
            dict: Scanning results organized by status
        """
        results = {
            'found': [],
            'not_found': [],
            'errors': [],
            'rate_limited': [],
            'other': []
        }

        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[*] Scanning username: {Fore.YELLOW}{username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[*] Checking {len(self.PLATFORMS)} platforms...{Style.RESET_ALL}\n")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.check_profile, platform, username): platform
                for platform in self.PLATFORMS.keys()
            }

            completed_count = 0
            for future in as_completed(futures):
                completed_count += 1
                result = future.result()
                platform = result['platform']

                # Organize results
                if result['status'] == 'found':
                    results['found'].append(result)
                    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} "
                          f"{platform:.<25} {Fore.GREEN}FOUND{Style.RESET_ALL} {result['url']}")

                elif result['status'] == 'not_found':
                    results['not_found'].append(result)
                    print(f"{Fore.LIGHTBLACK_EX}[-]{Style.RESET_ALL} "
                          f"{platform:.<25} Not available")

                elif result['status'] == 'rate_limited':
                    results['rate_limited'].append(result)
                    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} "
                          f"{platform:.<25} {Fore.YELLOW}Rate limited{Style.RESET_ALL}")

                elif result['status'] == 'error':
                    results['errors'].append(result)
                    print(f"{Fore.RED}[✗]{Style.RESET_ALL} "
                          f"{platform:.<25} {Fore.RED}Error: {result['error']}{Style.RESET_ALL}")

                else:
                    results['other'].append(result)
                    print(f"{Fore.LIGHTBLACK_EX}[~]{Style.RESET_ALL} "
                          f"{platform:.<25} {result.get('error', 'Unknown status')}")

        return results

    def print_executive_summary(self, username, results, elapsed_time):
        """
        Print executive summary of reconnaissance scan.

        Args:
            username: Username scanned
            results: Results dictionary from scan_username()
            elapsed_time: Total execution time in seconds
        """
        total_profiles_found = len(results['found'])
        total_platforms_checked = len(self.PLATFORMS)
        total_errors = len(results['errors'])

        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{' '*20}EXECUTIVE SUMMARY - RECONNAISSANCE COMPLETE{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

        print(f"{Fore.WHITE}Target Username{Style.RESET_ALL}........: {Fore.YELLOW}{username}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Platforms Checked{Style.RESET_ALL}........: {Fore.MAGENTA}{total_platforms_checked}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Profiles Discovered{Style.RESET_ALL}......: {Fore.GREEN}{total_profiles_found}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Failed Connections{Style.RESET_ALL}......: {Fore.RED}{total_errors}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Rate Limit Hits{Style.RESET_ALL}.........: {Fore.YELLOW}{len(results['rate_limited'])}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Execution Time{Style.RESET_ALL}...........: {Fore.CYAN}{elapsed_time:.2f} seconds{Style.RESET_ALL}\n")

        if results['found']:
            print(f"{Fore.GREEN}[+] DISCOVERED PROFILES:{Style.RESET_ALL}")
            for result in sorted(results['found'], key=lambda x: x['platform']):
                print(f"    {Fore.GREEN}→{Style.RESET_ALL} {result['platform']:20} {result['url']}")
        else:
            print(f"{Fore.LIGHTBLACK_EX}[-] No profiles discovered for this username.{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

    def run(self):
        """Main execution method."""
        self.display_banner()

        try:
            username = input(f"{Fore.CYAN}[?] Enter username/alias to scan: {Style.RESET_ALL}").strip()

            if not username:
                print(f"{Fore.RED}[✗] Username cannot be empty!{Style.RESET_ALL}")
                sys.exit(1)

            if len(username) > 64 or len(username) < 2:
                print(f"{Fore.RED}[✗] Username must be between 2 and 64 characters.{Style.RESET_ALL}")
                sys.exit(1)

            start_time = time.time()
            results = self.scan_username(username)
            elapsed_time = time.time() - start_time

            self.print_executive_summary(username, results, elapsed_time)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Scan interrupted by user.{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}[✗] Fatal error: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)


def main():
    """Entry point for ProfileScout."""
    scout = ProfileScout(timeout=8, max_workers=12)
    scout.run()


if __name__ == "__main__":
    main()
