# ProfileScout - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install requests colorama
```

### Step 2: Run ProfileScout
```bash
python3 profilescout.py
```

### Step 3: Enter a Username
```
╔════════════════════════════════════════════════════════════╗
║                    P R O F I L E S C O U T                 ║
║          OSINT Username & Alias Reconnaissance Tool        ║
║                  Security Analysis Platform                ║
║               Developed by: Abdul Rehman Akram             ║
╚════════════════════════════════════════════════════════════╝

[?] Enter username/alias to scan: john_developer
```

That's it! ProfileScout will scan 25+ platforms and show you all discovered profiles.

---

## 📋 What You'll See

**Live Scanning:**
```
[+] GitHub..................... FOUND https://github.com/john_developer
[-] Reddit..................... Not available
[+] Dev.to..................... FOUND https://dev.to/john_developer
[!] Twitch..................... Rate limited
[✗] Pinterest.................. Error: Connection timeout
```

**Executive Summary:**
```
Target Username.........: john_developer
Platforms Checked.......: 25
Profiles Discovered.....: 3
Failed Connections.....: 0
Execution Time...........: 2.45 seconds

[+] DISCOVERED PROFILES:
    → GitHub             https://github.com/john_developer
    → Dev.to            https://dev.to/john_developer
    → Medium            https://medium.com/@john_developer
```

---

## 🎯 Common Scenarios

### Scan a Public Figure
```bash
$ python3 profilescout.py
[?] Enter username/alias to scan: torvalds
```

### Check Multiple Usernames (Programmatically)
Create a file named `batch_scan.py`:
```python
from profilescout import ProfileScout

scout = ProfileScout()

for username in ["alice", "bob", "charlie"]:
    results = scout.scan_username(username)
    print(f"{username}: {len(results['found'])} profiles found")
```

Run it:
```bash
python3 batch_scan.py
```

### Use Different Timeout Settings
```python
from profilescout import ProfileScout

# For slower internet connections
scout = ProfileScout(timeout=15, max_workers=8)
results = scout.scan_username("username")
```

---

## 🛠️ Troubleshooting

### Installation Issues

**Error:** `ModuleNotFoundError: No module named 'requests'`

**Fix:**
```bash
pip install --upgrade pip
pip install requests colorama
```

### Connection Issues

**Error:** `[✗] Connection timeout` on many platforms

**Fix:** Increase timeout
```python
scout = ProfileScout(timeout=15)  # Instead of default 8
```

### Rate Limiting

**Error:** Many `[!] Rate limited` messages

**Fix:** Reduce concurrent workers
```python
scout = ProfileScout(max_workers=5)  # Instead of default 12
```

---

## 📊 Platforms Checked

ProfileScout checks these 25+ platforms:

- **Code**: GitHub, GitLab, Dev.to
- **Social**: Reddit, Twitter/X, Instagram, Facebook, LinkedIn, TikTok, Mastodon, Bluesky, Threads
- **Video**: YouTube, Twitch, Letterboxd
- **Music**: Spotify, SoundCloud
- **Creative**: Behance, Medium, Patreon, Substack
- **Gaming**: Steam, Discord
- **Other**: Pinterest, Linktree

---

## 💡 Tips & Tricks

### 1. Check Username Availability
Run ProfileScout on a username you're interested in registering. If nothing is found, it might be available on most platforms!

### 2. Verify Related Accounts
Found one profile? ProfileScout helps verify if someone uses the same username elsewhere.

### 3. Security Research
Analysts use ProfileScout for passive reconnaissance before engagements.

### 4. Batch Processing
Process multiple usernames in a loop (see "Scan Multiple Usernames" above).

---

## 🔒 Privacy & Security

- ✅ Completely passive - no interaction with profiles
- ✅ No data stored or transmitted
- ✅ No authentication required
- ✅ Local execution only
- ✅ Rate-aware to respect platform limits

---

## 📞 Need Help?

Check the main [README.md](README.md) for:
- Detailed installation instructions
- Advanced configuration
- Platform-specific notes
- Error documentation
- Architecture overview

---

**Ready to scan? Run: `python3 profilescout.py`**

