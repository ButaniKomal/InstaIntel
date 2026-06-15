#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                    INSTA INTELLIGENCE v2.0                   ║
║                  Private ID Reconnaissance                   ║
║                      Author: Komal Butani                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import requests
import json
import sys
import os
from datetime import datetime

# Colors for beautiful output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def banner():
    """Display cool banner"""
    print(CYAN + """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██╗███╗   ██╗███████╗████████╗ █████╗                  ║
║   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗                 ║
║   ██║██╔██╗ ██║███████╗   ██║   ███████║                 ║
║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║                 ║
║   ██║██║ ╚████║███████║   ██║   ██║  ██║                 ║
║   ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝                 ║
║                                                           ║
║           PRIVATE ID INTELLIGENCE v2.0                    ║
║              Created by: Komal Butani                     ║
╚═══════════════════════════════════════════════════════════╝
    """ + RESET)
    print(YELLOW + "═" * 60 + RESET)
    print(GREEN + "    Instagram OSINT & Reconnaissance Tool" + RESET)
    print(YELLOW + "═" * 60 + RESET + "\n")

def fetch_instagram_data(username):
    """Fetch public Instagram data"""
    print(BLUE + f"[⚡] Targeting: @{username}" + RESET)
    print(CYAN + "[🛰️] Connecting to Instagram API..." + RESET)
    
    # Instagram API endpoint
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('data', {}).get('user', {})
            
            if user:
                return {
                    'username': user.get('username', 'N/A'),
                    'full_name': user.get('full_name', 'N/A'),
                    'bio': user.get('biography', 'No bio'),
                    'followers': user.get('edge_followed_by', {}).get('count', 0),
                    'following': user.get('edge_follow', {}).get('count', 0),
                    'posts': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_private': user.get('is_private', False),
                    'is_verified': user.get('is_verified', False),
                    'business_category': user.get('business_category_name', 'N/A'),
                    'external_url': user.get('external_url', 'N/A'),
                    'profile_pic': user.get('profile_pic_url_hd', 'N/A')
                }
            else:
                print(RED + "[!] User not found!" + RESET)
                return None
        else:
            print(RED + f"[!] Error: {response.status_code}" + RESET)
            return None
            
    except Exception as e:
        print(RED + f"[!] Connection failed: {str(e)}" + RESET)
        return None

def display_results(data):
    """Display formatted results"""
    print(GREEN + "\n📊 INTELLIGENCE REPORT" + RESET)
    print(YELLOW + "─" * 50 + RESET)
    
    info_list = [
        ("📱 Username", data.get('username')),
        ("👤 Full Name", data.get('full_name')),
        ("📝 Bio", data.get('bio')[:100] + "..." if len(data.get('bio', '')) > 100 else data.get('bio')),
        ("👥 Followers", f"{data.get('followers', 0):,}"),
        ("👣 Following", f"{data.get('following', 0):,}"),
        ("📸 Posts", f"{data.get('posts', 0):,}"),
        ("🔒 Private Account", "✅ YES" if data.get('is_private') else "❌ NO"),
        ("✓ Verified", "✅ YES" if data.get('is_verified') else "❌ NO"),
        ("💼 Business", data.get('business_category')),
        ("🔗 External URL", data.get('external_url')),
    ]
    
    for label, value in info_list:
        if value and value != 'N/A':
            print(CYAN + f"{label}: " + RESET + str(value))
    
    print(YELLOW + "─" * 50 + RESET)

def check_other_platforms(username):
    """Find user on other platforms"""
    print(MAGENTA + "\n🌐 MULTI-PLATFORM SCAN" + RESET)
    print(YELLOW + "─" * 50 + RESET)
    
    platforms = {
        'Twitter': f"https://twitter.com/{username}",
        'GitHub': f"https://github.com/{username}",
        'YouTube': f"https://youtube.com/@{username}",
        'TikTok': f"https://tiktok.com/@{username}",
        'Reddit': f"https://reddit.com/user/{username}",
        'Pinterest': f"https://pinterest.com/{username}",
    }
    
    found = False
    for platform, url in platforms.items():
        try:
            response = requests.head(url, timeout=3)
            if response.status_code == 200:
                print(GREEN + f"  ✓ {platform}: Found" + RESET)
                found = True
            else:
                print(RED + f"  ✗ {platform}: Not found" + RESET)
        except:
            print(RED + f"  ✗ {platform}: Unreachable" + RESET)
    
    if not found:
        print(YELLOW + "  No profiles found on other platforms" + RESET)
    
    print(YELLOW + "─" * 50 + RESET)

def save_report(data, username):
    """Save results to JSON file"""
    # Create output folder if not exists
    if not os.path.exists('output'):
        os.makedirs('output')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/{username}_{timestamp}.json"
    
    # Add metadata
    data['scan_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['tool'] = "INSTA Intel v2.0"
    data['author'] = "Komal Butani"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(GREEN + f"\n💾 Report saved: {filename}" + RESET)
    return filename

def main():
    """Main function"""
    # Check if username provided
    if len(sys.argv) < 2:
        banner()
        print(RED + "[!] Usage: python insta.py <username>" + RESET)
        print(CYAN + "\nExample: python insta.py cristiano" + RESET)
        sys.exit(1)
    
    username = sys.argv[1]
    
    # Clear screen for clean look
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Show banner
    banner()
    
    # Fetch data
    data = fetch_instagram_data(username)
    
    if data:
        # Display results
        display_results(data)
        
        # Check other platforms
        check_other_platforms(username)
        
        # Save report
        filename = save_report(data, username)
        
        # Final message
        print(GREEN + "\n✨ Scan Complete! ✨" + RESET)
        print(CYAN + f"📄 Full report saved to: {filename}" + RESET)
    else:
        print(RED + "\n❌ Failed to fetch data!" + RESET)
        print(YELLOW + "\nPossible reasons:" + RESET)
        print("  • Username doesn't exist")
        print("  • Account is private")
        print("  • Rate limited (wait a few minutes)")
        print("  • No internet connection")

if __name__ == "__main__":
    main()
