#!/usr/bin/env python3
"""
Quick Start Examples for ProfileScout
Demonstrates common usage patterns and configurations
"""

from profilescout import ProfileScout
import time


def example_1_basic_scan():
    """Example 1: Basic username scan with default settings"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Username Scan")
    print("=" * 80)

    scout = ProfileScout()
    scout.display_banner()

    # Interactive scan
    username = "github"
    start_time = time.time()
    results = scout.scan_username(username)
    elapsed_time = time.time() - start_time

    scout.print_executive_summary(username, results, elapsed_time)


def example_2_custom_timeout():
    """Example 2: Scan with custom timeout (useful for slow connections)"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Custom Timeout Configuration")
    print("=" * 80)

    # Increase timeout from default 8 to 15 seconds for slower connections
    scout = ProfileScout(timeout=15, max_workers=10)
    scout.display_banner()

    username = "microsoft"
    start_time = time.time()
    results = scout.scan_username(username)
    elapsed_time = time.time() - start_time

    scout.print_executive_summary(username, results, elapsed_time)


def example_3_programmatic_usage():
    """Example 3: Programmatic usage for batch processing"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Batch Processing Multiple Usernames")
    print("=" * 80)

    scout = ProfileScout()

    usernames = ["torvalds", "gvanrossum", "khansalah"]

    for username in usernames:
        print(f"\n[*] Processing: {username}")
        start_time = time.time()
        results = scout.scan_username(username)
        elapsed_time = time.time() - start_time

        print(f"\n    Results: {len(results['found'])} profiles found in {elapsed_time:.2f}s")
        for profile in results['found']:
            print(f"    → {profile['platform']}: {profile['url']}")


def example_4_single_platform_check():
    """Example 4: Check availability on a single platform"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Single Platform Verification")
    print("=" * 80)

    scout = ProfileScout()

    # Check if username exists on GitHub only
    result = scout.check_profile("GitHub", "django")
    print(f"Platform: {result['platform']}")
    print(f"Status: {result['status']}")
    print(f"HTTP Code: {result['http_code']}")
    print(f"URL: {result['url']}")


def example_5_performance_tuning():
    """Example 5: Performance tuning for different scenarios"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Performance Tuning")
    print("=" * 80)

    # Scenario A: Fast scan with high concurrency (may trigger rate limits)
    print("\n[Scenario A] Fast Scan - High Concurrency")
    scout_fast = ProfileScout(timeout=5, max_workers=20)
    start_time = time.time()
    results = scout_fast.scan_username("alice")
    elapsed_time = time.time() - start_time
    print(f"  Time: {elapsed_time:.2f}s | Found: {len(results['found'])} profiles")

    # Scenario B: Balanced scan
    print("\n[Scenario B] Balanced Scan - Medium Concurrency")
    scout_balanced = ProfileScout(timeout=8, max_workers=12)
    start_time = time.time()
    results = scout_balanced.scan_username("bob")
    elapsed_time = time.time() - start_time
    print(f"  Time: {elapsed_time:.2f}s | Found: {len(results['found'])} profiles")

    # Scenario C: Slow/Reliable scan with low concurrency
    print("\n[Scenario C] Careful Scan - Low Concurrency")
    scout_careful = ProfileScout(timeout=12, max_workers=5)
    start_time = time.time()
    results = scout_careful.scan_username("charlie")
    elapsed_time = time.time() - start_time
    print(f"  Time: {elapsed_time:.2f}s | Found: {len(results['found'])} profiles")


def example_6_result_analysis():
    """Example 6: Detailed result analysis"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Result Analysis")
    print("=" * 80)

    scout = ProfileScout()

    results = scout.scan_username("developer")

    print(f"\n[+] FOUND PROFILES ({len(results['found'])}):")
    for result in results['found']:
        print(f"    {result['platform']:20} -> {result['url']}")

    print(f"\n[-] NOT FOUND ({len(results['not_found'])}):")
    for result in results['not_found'][:5]:  # Show first 5
        print(f"    {result['platform']:20} (Available)")

    print(f"\n[!] RATE LIMITED ({len(results['rate_limited'])}):")
    for result in results['rate_limited']:
        print(f"    {result['platform']:20} (Try again later)")

    print(f"\n[✗] ERRORS ({len(results['errors'])}):")
    for result in results['errors']:
        print(f"    {result['platform']:20} ({result['error']})")


if __name__ == "__main__":
    from colorama import init, Fore, Style
    init(autoreset=True)
    
    print()
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}                    {Fore.BRIGHT}{Fore.CYAN}P R O F I L E S C O U T{Style.RESET_ALL}                 {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}          {Fore.BRIGHT}{Fore.MAGENTA}OSINT Username & Alias Reconnaissance Tool{Style.RESET_ALL}        {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}                  {Fore.BRIGHT}{Fore.YELLOW}Security Analysis Platform{Style.RESET_ALL}                {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}               {Fore.BRIGHT}{Fore.GREEN}Developed by: Abdul Rehman Akram{Style.RESET_ALL}             {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print("\nChoose an example to run:")
    print("  1. Basic scan")
    print("  2. Custom timeout settings")
    print("  3. Batch processing")
    print("  4. Single platform check")
    print("  5. Performance tuning comparison")
    print("  6. Result analysis")
    print("  0. Exit")

    choice = input("\nEnter your choice (0-6): ").strip()

    examples = {
        '1': example_1_basic_scan,
        '2': example_2_custom_timeout,
        '3': example_3_programmatic_usage,
        '4': example_4_single_platform_check,
        '5': example_5_performance_tuning,
        '6': example_6_result_analysis,
    }

    if choice in examples:
        examples[choice]()
    elif choice != '0':
        print("Invalid choice!")
