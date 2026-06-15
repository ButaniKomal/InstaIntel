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
import time
import os
import argparse
from datetime import datetime
from colorama import init, Fore, Style
import pyfiglet

init(autoreset=True)

class InstaIntel:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {}
        
    def banner(self):
        banner_text = pyfiglet.figlet_format("INSTA INTEL", font="slant")
        print(Fore.CYAN + banner_text)
        print(Fore.YELLOW + "═" * 60)
        print(Fore.GREEN + "    Private ID Intelligence | Author: Komal Butani")
        print(Fore.YELLOW + "═" * 60 + "\n")
    
    def fetch_info(self, username):
        """Fetch Instagram user information"""
        print(Fore.BLUE + f"[⚡] Targeting: @{username}")
        print(Fore.CYAN + "[🛰️] Connecting to Instagram API...")
        
        # Instagram API endpoints
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {}).get('user', {})
                
                self.results = {
                    'username': user_data.get('username'),
                    'full_name': user_data.get('full_name'),
                    'bio': user_data.get('biography'),
                    'followers': user_data.get('edge_followed_by', {}).get('count'),
                    'following': user_data.get('edge_follow', {}).get('count'),
                    'posts': user_data.get('edge_owner_to_timeline_media', {}).get('count'),
                    'is_private': user_data.get('is_private'),
                    'is_verified': user_data.get('is_verified'),
                    'business_category': user_data.get('business_category_name'),
                    'external_url': user_data.get('external_url'),
                    'profile_pic': user_data.get('profile_pic_url_hd'),
                }
                return True
            else:
                print(Fore.RED + f"[!] Error: {response.status_code}")
                return False
        except Exception as e:
            print(Fore.RED + f"[!] Failed: {str(e)}")
            return False
    
    def display_results(self):
        """Display gathered intelligence"""
        print(Fore.GREEN + "\n📊 INTELLIGENCE REPORT\n" + "─" * 40)
        
        info = [
            ("📱 Username", self.results.get('username')),
            ("👤 Full Name", self.results.get('full_name')),
            ("📝 Bio", self.results.get('bio', 'No bio')),
            ("👥 Followers", f"{self.results.get('followers', 0):,}"),
            ("👣 Following", f"{self.results.get('following', 0):,}"),
            ("📸 Posts", f"{self.results.get('posts', 0):,}"),
            ("🔒 Private Account", "✅ Yes" if self.results.get('is_private') else "❌ No"),
            ("✓ Verified", "✅ Yes" if self.results.get('is_verified') else "❌ No"),
            ("💼 Business", self.results.get('business_category', 'N/A')),
            ("🔗 External URL", self.results.get('external_url', 'N/A')),
        ]
        
        for label, value in info:
            if value:
                print(Fore.WHITE + f"{label}: " + Fore.CYAN + f"{value}")
        
        print(Fore.YELLOW + "\n" + "─" * 40)
    
    def advanced_scan(self, username):
        """Advanced OSINT scanning"""
        print(Fore.MAGENTA + "\n🕵️ Advanced OSINT Scan\n" + "─" * 40)
        
        # Check other platforms
        platforms = {
            'Twitter': f"https://twitter.com/{username}",
            'GitHub': f"https://github.com/{username}",
            'YouTube': f"https://youtube.com/@{username}",
            'TikTok': f"https://tiktok.com/@{username}",
        }
        
        for platform, url in platforms.items():
            try:
                r = requests.head(url, timeout=3)
                if r.status_code == 200:
                    print(Fore.GREEN + f"[✓] {platform}: Found")
                else:
                    print(Fore.RED + f"[✗] {platform}: Not found")
            except:
                print(Fore.RED + f"[✗] {platform}: Unreachable")
        
        print(Fore.MAGENTA + "\n" + "─" * 40)
    
    def save_report(self, username):
        """Save results to file"""
        if not os.path.exists('output'):
            os.makedirs('output')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/{username}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        
        print(Fore.GREEN + f"\n💾 Report saved: {filename}")
    
    def run(self, username):
        """Main execution"""
        self.banner()
        
        if self.fetch_info(username):
            self.display_results()
            self.advanced_scan(username)
            self.save_report(username)
            
            print(Fore.CYAN + "\n✨ Scan Complete! ✨")
        else:
            print(Fore.RED + "\n❌ Failed to fetch data")

def main():
    parser = argparse.ArgumentParser(description='INSTA - Private ID Intelligence Tool')
    parser.add_argument('username', help='Instagram username to investigate')
    parser.add_argument('-o', '--output', help='Save output to file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    tool = InstaIntel()
    tool.run(args.username)

if __name__ == "__main__":
    main()
