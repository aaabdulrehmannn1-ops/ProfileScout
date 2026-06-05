# ProfileScout - Developer Documentation

## Table of Contents
1. [Architecture](#architecture)
2. [Core Classes](#core-classes)
3. [API Reference](#api-reference)
4. [Extending ProfileScout](#extending-profilescout)
5. [Performance Tuning](#performance-tuning)
6. [Testing & Validation](#testing--validation)

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        ProfileScout                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐          ┌──────────────────┐              │
│  │  CLI Interface│          │ Platform Database│              │
│  │  - Banner     │          │ - 25+ Platform   │              │
│  │  - Input      │          │   URL Templates  │              │
│  │  - Color Out  │          │ - HTTP Settings  │              │
│  └───────┬───────┘          └────────┬─────────┘              │
│          │                           │                         │
│          └───────────────┬───────────┘                         │
│                          │                                     │
│          ┌───────────────▼────────────────┐                   │
│          │    ProfileScout Engine         │                   │
│          │  - check_profile()             │                   │
│          │  - scan_username()             │                   │
│          │  - Error handling              │                   │
│          └───────────────┬────────────────┘                   │
│                          │                                     │
│          ┌───────────────▼────────────────┐                   │
│          │ Concurrent Request Layer       │                   │
│          │ - ThreadPoolExecutor           │                   │
│          │ - HTTP requests                │                   │
│          │ - Status code handling         │                   │
│          └───────────────┬────────────────┘                   │
│                          │                                     │
│          ┌───────────────▼────────────────┐                   │
│          │    Result Aggregator           │                   │
│          │ - Categorize results           │                   │
│          │ - Generate summary             │                   │
│          └────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input (username)
    ↓
Input Validation
    ↓
Platform Initialization
    ↓
ThreadPoolExecutor (12 threads max)
    ├─→ Platform 1: URL + HTTP Request → Status Code Analysis → Result
    ├─→ Platform 2: URL + HTTP Request → Status Code Analysis → Result
    ├─→ Platform N: URL + HTTP Request → Status Code Analysis → Result
    ↓
Result Aggregation (by status: found/not_found/error/rate_limited)
    ↓
Human-Readable Summary + Executive Report
    ↓
Display to User
```

---

## Core Classes

### ProfileScout Main Class

```python
class ProfileScout:
    """Main OSINT reconnaissance engine"""
    
    PLATFORMS = {str: str}  # Platform name -> URL template
    
    def __init__(self, timeout=8, max_workers=10):
        """Initialize the reconnaissance engine"""
        
    def check_profile(self, platform, username) -> dict:
        """Check single platform for profile existence"""
        
    def scan_username(self, username) -> dict:
        """Concurrent scan of all platforms"""
        
    def display_banner():
        """Display ASCII art banner"""
        
    def print_executive_summary(username, results, elapsed_time):
        """Print comprehensive summary report"""
```

### Platform Verification Result Structure

```python
result = {
    'platform': str,           # Platform name
    'username': str,           # Username scanned
    'status': str,             # 'found', 'not_found', 'error', 'rate_limited', etc.
    'url': str,                # Complete profile URL
    'http_code': int,          # HTTP status code (200, 404, 429, etc.)
    'error': Optional[str]     # Error message if applicable
}
```

### Scan Results Structure

```python
results = {
    'found': [result, ...],           # Discovered profiles
    'not_found': [result, ...],       # Usernames not claimed
    'errors': [result, ...],          # Connection/verification errors
    'rate_limited': [result, ...],    # Rate limit responses
    'other': [result, ...]            # Other statuses
}
```

---

## API Reference

### ProfileScout.__init__(timeout=8, max_workers=10)

Initialize ProfileScout reconnaissance engine.

**Parameters:**
- `timeout` (int): HTTP request timeout in seconds. Default: 8
- `max_workers` (int): Maximum concurrent threads. Default: 10

**Example:**
```python
scout = ProfileScout(timeout=15, max_workers=20)
```

### ProfileScout.check_profile(platform, username)

Verify profile existence on a single platform.

**Parameters:**
- `platform` (str): Platform name (key from PLATFORMS dict)
- `username` (str): Username/alias to verify

**Returns:** Dict with keys: platform, username, status, url, http_code, error

**Example:**
```python
result = scout.check_profile("GitHub", "torvalds")
print(result['status'])  # Output: 'found'
print(result['url'])     # Output: https://github.com/torvalds
```

### ProfileScout.scan_username(username)

Scan username across all platforms concurrently.

**Parameters:**
- `username` (str): Username to scan

**Returns:** Dict with categorized results (found, not_found, errors, etc.)

**Example:**
```python
results = scout.scan_username("alice")
print(f"Found {len(results['found'])} profiles")
for profile in results['found']:
    print(f"  {profile['platform']}: {profile['url']}")
```

### ProfileScout.display_banner()

Display ASCII art banner (called automatically during run()).

**Example:**
```python
scout.display_banner()
```

### ProfileScout.print_executive_summary(username, results, elapsed_time)

Print comprehensive reconnaissance summary.

**Parameters:**
- `username` (str): Scanned username
- `results` (dict): Results from scan_username()
- `elapsed_time` (float): Execution time in seconds

**Example:**
```python
elapsed = time.time() - start_time
scout.print_executive_summary("bob", results, elapsed)
```

---

## Extending ProfileScout

### Adding New Platforms

**Method 1: Direct Modification**

Edit `profilescout.py` and add to `PLATFORMS` dictionary:

```python
PLATFORMS = {
    # ... existing platforms ...
    "NewPlatform": "https://newplatform.com/{}",
    "AnotherOne": "https://another.platform.com/profile/{}",
}
```

**Method 2: Dynamic Addition**

```python
scout = ProfileScout()
scout.PLATFORMS["CustomPlatform"] = "https://custom.com/{}"
results = scout.scan_username("username")
```

### Custom Request Headers

Modify headers for specific platforms:

```python
class CustomProfileScout(ProfileScout):
    def check_profile(self, platform, username):
        result = super().check_profile(platform, username)
        
        if platform == "LinkedIn":
            self.session.headers.update({
                'Authorization': 'Bearer token_here'
            })
        
        return result
```

### Custom Status Code Handling

Override status code logic:

```python
class CustomProfileScout(ProfileScout):
    def check_profile(self, platform, username):
        result = super().check_profile(platform, username)
        
        # Custom logic for specific platforms
        if platform == "Twitter/X" and result['http_code'] == 404:
            # Twitter returns 404 even for protected accounts
            result['status'] = 'possibly_found'
        
        return result
```

### Custom Result Processing

Process results differently:

```python
scout = ProfileScout()
results = scout.scan_username("username")

# Save to JSON
import json
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Filter results
github_results = [r for r in results['found'] if r['platform'] == 'GitHub']
```

---

## Performance Tuning

### Timeout Optimization

```python
# For fast corporate networks
scout_fast = ProfileScout(timeout=3, max_workers=20)

# For standard connections
scout_standard = ProfileScout(timeout=8, max_workers=12)

# For slow/unreliable connections
scout_slow = ProfileScout(timeout=15, max_workers=6)
```

### Concurrency Tuning

```python
# Benchmark different worker counts
import time

for workers in [4, 8, 12, 16, 20]:
    scout = ProfileScout(max_workers=workers)
    start = time.time()
    results = scout.scan_username("test")
    elapsed = time.time() - start
    print(f"Workers: {workers}, Time: {elapsed:.2f}s")
```

### Batch Processing Optimization

```python
from concurrent.futures import ThreadPoolExecutor

def scan_batch(usernames):
    scout = ProfileScout()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(scout.scan_username, username): username
            for username in usernames
        }
        
        for future in futures:
            username = futures[future]
            results = future.result()
            print(f"{username}: {len(results['found'])} profiles")

scan_batch(["alice", "bob", "charlie"])
```

---

## Testing & Validation

### Basic Functionality Test

```python
import sys
from profilescout import ProfileScout

def test_basic():
    """Test basic ProfileScout functionality"""
    
    scout = ProfileScout()
    
    # Test 1: Check single platform
    result = scout.check_profile("GitHub", "torvalds")
    assert result['platform'] == "GitHub"
    assert result['status'] in ['found', 'not_found', 'error']
    print("[PASS] Single platform check")
    
    # Test 2: Scan username
    results = scout.scan_username("github")
    assert 'found' in results
    assert 'errors' in results
    print("[PASS] Full username scan")
    
    # Test 3: Profile found status
    assert any(r['status'] == 'found' for r in results['found']), \
        "Should find some profiles for 'github'"
    print("[PASS] Profile discovery")
    
    return True

if __name__ == "__main__":
    try:
        test_basic()
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
```

### Performance Benchmarking

```python
import time
from profilescout import ProfileScout

def benchmark():
    """Benchmark ProfileScout performance"""
    
    scout = ProfileScout()
    
    # Single platform performance
    start = time.time()
    result = scout.check_profile("GitHub", "test")
    single_time = time.time() - start
    print(f"Single platform check: {single_time*1000:.1f}ms")
    
    # Full scan performance
    start = time.time()
    results = scout.scan_username("benchmark")
    full_time = time.time() - start
    print(f"Full scan (25 platforms): {full_time:.2f}s")
    print(f"Average per platform: {full_time/25*1000:.1f}ms")
    
    # Accuracy
    found = len(results['found'])
    not_found = len(results['not_found'])
    errors = len(results['errors'])
    print(f"\nResults: {found} found, {not_found} available, {errors} errors")

if __name__ == "__main__":
    benchmark()
```

### Integration Testing

```python
import sys
from profilescout import ProfileScout

def integration_test():
    """Test ProfileScout with known usernames"""
    
    test_cases = [
        ("torvalds", {"GitHub"}),           # Should find GitHub
        ("notarealusername12345", set()),   # Should find nothing
        ("github", {"GitHub"}),             # Should find GitHub
    ]
    
    scout = ProfileScout()
    
    for username, expected_platforms in test_cases:
        results = scout.scan_username(username)
        found_platforms = {r['platform'] for r in results['found']}
        
        # Check if expected platforms are found
        for platform in expected_platforms:
            if platform not in found_platforms:
                return False, f"Expected {platform} for {username}"
    
    return True, "All integration tests passed"

if __name__ == "__main__":
    success, message = integration_test()
    print(message)
    sys.exit(0 if success else 1)
```

---

## Advanced Usage Examples

### Custom Filtering

```python
from profilescout import ProfileScout

scout = ProfileScout()
results = scout.scan_username("developer")

# Filter only code-related platforms
code_platforms = {"GitHub", "GitLab", "Dev.to"}
code_profiles = [
    r for r in results['found']
    if r['platform'] in code_platforms
]

print(f"Code profiles: {code_profiles}")
```

### Batch CSV Export

```python
import csv
from profilescout import ProfileScout

def export_batch_to_csv(usernames, output_file):
    scout = ProfileScout()
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Username', 'Platform', 'URL', 'Status'])
        
        for username in usernames:
            results = scout.scan_username(username)
            for profile in results['found']:
                writer.writerow([
                    username,
                    profile['platform'],
                    profile['url'],
                    profile['status']
                ])

export_batch_to_csv(["alice", "bob"], "results.csv")
```

---

## Error Handling Guide

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: requests` | Missing dependency | `pip install requests` |
| `Connection timeout` | Network issue | Increase timeout: `timeout=15` |
| `[!] Rate limited` | Too many requests | Reduce workers: `max_workers=5` |
| `SSLError` | Certificate issue | Already handled (verify=False) |
| `No profiles found` | User doesn't exist | Username may not be popular |

---

## Contributing Guidelines

To contribute improvements:

1. Fork/clone the repository
2. Create a new branch
3. Add new platforms to `PLATFORMS` dict
4. Test thoroughly with multiple usernames
5. Submit pull request with description

---

## Support & Resources

- **Main Documentation**: See README.md
- **Quick Start**: See QUICKSTART.md
- **Examples**: See examples.py
- **Configuration**: See config.py

