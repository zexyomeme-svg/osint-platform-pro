import requests
import json
from datetime import datetime
from typing import Dict, List, Any

class OSINTSearcher:
    """Comprehensive OSINT search engine using free public APIs and services"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Phone number platforms to check
    PHONE_PLATFORMS = {
        'truecaller': 'https://www.truecaller.com/search/',
        'whitepages': 'https://www.whitepages.com/phone/',
        'spokeo': 'https://www.spokeo.com/phone/',
        'reverse_phone': 'https://www.reversephonesite.com/',
        'phonebook': 'https://www.phonebook.com/phone/'
    }
    
    # Person search platforms
    PERSON_PLATFORMS = {
        'whitepages': 'https://www.whitepages.com/',
        'spokeo': 'https://www.spokeo.com/',
        'pipl': 'https://www.pipl.com/',
        'social_bearing': 'https://socialbearing.com/',
        'search_people': 'https://www.searchpeoplefree.com/'
    }
    
    # Social media platforms for username search
    SOCIAL_PLATFORMS = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://instagram.com/{}",
        "Reddit": "https://reddit.com/user/{}",
        "YouTube": "https://youtube.com/@{}",
        "TikTok": "https://tiktok.com/@{}",
        "LinkedIn": "https://linkedin.com/in/{}",
        "Pinterest": "https://pinterest.com/{}",
        "Twitch": "https://twitch.tv/{}",
        "Telegram": "https://t.me/{}",
        "Discord": "https://discord.com/users/{}",
        "Medium": "https://medium.com/@{}",
        "Dev.to": "https://dev.to/{}",
        "Mastodon": "https://mastodon.social/@{}",
        "Bluesky": "https://bsky.app/profile/{}"
    }

    @staticmethod
    def search_name(first_name: str, last_name: str, location: str = None) -> Dict[str, Any]:
        """
        Search for person by name across multiple platforms
        
        Args:
            first_name: Person's first name
            last_name: Person's last name
            location: Optional location/state
            
        Returns:
            Dictionary with search results from multiple platforms
        """
        results = {
            'name': f"{first_name} {last_name}",
            'search_time': datetime.now().isoformat(),
            'platforms': {}
        }
        
        # Search query
        query = f"{first_name}+{last_name}"
        if location:
            query += f"+{location}"
        
        # Platform searches (check availability)
        for platform_name, base_url in OSINTSearcher.PERSON_PLATFORMS.items():
            try:
                if platform_name == 'whitepages':
                    url = f"{base_url}{query.replace('+', '-')}"
                elif platform_name == 'spokeo':
                    url = f"{base_url}{query.replace('+', '-')}"
                else:
                    url = f"{base_url}{query}"
                
                response = requests.head(url, headers=OSINTSearcher.HEADERS, timeout=3)
                results['platforms'][platform_name] = {
                    'available': response.status_code in [200, 302, 404],  # 404 means site is up
                    'url': url,
                    'status_code': response.status_code
                }
            except Exception as e:
                results['platforms'][platform_name] = {
                    'available': False,
                    'error': str(e),
                    'url': f"{base_url}{query}"
                }
        
        return results

    @staticmethod
    def search_phone(phone_number: str) -> Dict[str, Any]:
        """
        Search for phone number across multiple reverse phone lookup platforms
        
        Args:
            phone_number: Phone number to search (format: +1234567890 or 1234567890)
            
        Returns:
            Dictionary with reverse phone lookup results
        """
        # Clean phone number
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        results = {
            'phone_number': clean_phone,
            'formatted': format_phone_number(clean_phone),
            'search_time': datetime.now().isoformat(),
            'platforms': {}
        }
        
        # Try multiple platforms
        platforms_to_check = {
            'truecaller': f"https://www.truecaller.com/search/US/{clean_phone}",
            'whitepages': f"https://www.whitepages.com/phone/{clean_phone}",
            'spokeo': f"https://www.spokeo.com/phone/{clean_phone}",
            'reverse_phone_lookup': f"https://www.reversephonesite.com/{clean_phone}",
            'numverify': f"https://numverify.com/?number=%2B{clean_phone}"
        }
        
        for platform, url in platforms_to_check.items():
            try:
                response = requests.head(url, headers=OSINTSearcher.HEADERS, timeout=3)
                results['platforms'][platform] = {
                    'available': response.status_code in [200, 302, 404],
                    'url': url,
                    'status_code': response.status_code
                }
            except Exception as e:
                results['platforms'][platform] = {
                    'available': False,
                    'error': str(e),
                    'url': url
                }
        
        return results

    @staticmethod
    def search_username(username: str) -> Dict[str, List[Dict[str, str]]]:
        """
        Search for username across all major social platforms
        
        Args:
            username: Username to search
            
        Returns:
            Dictionary with search results from multiple platforms
        """
        results = {
            'username': username,
            'search_time': datetime.now().isoformat(),
            'found': [],
            'not_found': [],
            'error': []
        }
        
        for platform_name, url_template in OSINTSearcher.SOCIAL_PLATFORMS.items():
            url = url_template.format(username)
            
            try:
                response = requests.get(url, headers=OSINTSearcher.HEADERS, timeout=4)
                
                if response.status_code == 200:
                    results['found'].append({
                        'platform': platform_name,
                        'url': url,
                        'status': 'Found',
                        'profile_url': url
                    })
                else:
                    results['not_found'].append({
                        'platform': platform_name,
                        'url': url,
                        'status': 'Not Found',
                        'status_code': response.status_code
                    })
            except requests.Timeout:
                results['error'].append({
                    'platform': platform_name,
                    'url': url,
                    'error': 'Request timeout'
                })
            except Exception as e:
                results['error'].append({
                    'platform': platform_name,
                    'url': url,
                    'error': str(e)
                })
        
        return results

    @staticmethod
    def search_by_image_url(image_url: str) -> Dict[str, Any]:
        """
        Search by image URL using multiple reverse image search engines
        
        Args:
            image_url: URL of the image to search
            
        Returns:
            Dictionary with reverse image search results
        """
        results = {
            'image_url': image_url,
            'search_time': datetime.now().isoformat(),
            'services': {}
        }
        
        # Reverse image search services
        services = {
            'google': f"https://www.google.com/searchbyimage?image_url={image_url}",
            'yandex': f"https://yandex.com/images/search?rpt=imageview&url={image_url}",
            'bing': f"https://www.bing.com/images/search?view=detailv2&iss=sbiupload&FORM=SBIQBR&sbisrc=ImageDropper&q=imgurl:{image_url}",
            'tineye': f"https://tineye.com/search?url={image_url}",
            'saucenao': f"https://saucenao.com/search.php?url={image_url}",
        }
        
        for service_name, search_url in services.items():
            try:
                response = requests.head(search_url, headers=OSINTSearcher.HEADERS, timeout=3)
                results['services'][service_name] = {
                    'available': True,
                    'search_url': search_url,
                    'status_code': response.status_code
                }
            except Exception as e:
                results['services'][service_name] = {
                    'available': False,
                    'search_url': search_url,
                    'error': str(e)
                }
        
        return results

    @staticmethod
    def search_email(email: str) -> Dict[str, Any]:
        """
        Search for email information and associated accounts
        
        Args:
            email: Email address to search
            
        Returns:
            Dictionary with email search results
        """
        results = {
            'email': email,
            'search_time': datetime.now().isoformat(),
            'breaches': [],
            'services': {}
        }
        
        # Extract username from email for social search
        username = email.split('@')[0] if '@' in email else email
        
        # Try to find breaches using haveibeenpwned (check if available)
        try:
            response = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                headers={**OSINTSearcher.HEADERS, 'User-Agent': 'OSINT-Platform-Pro'},
                timeout=5
            )
            if response.status_code == 200:
                results['breaches'] = response.json()
        except Exception as e:
            results['breaches_error'] = str(e)
        
        # Search for email on common platforms
        email_platforms = {
            'gmail': 'https://mail.google.com',
            'outlook': 'https://outlook.com',
            'github': f"https://github.com/search?q={email}",
            'linkedin': f"https://linkedin.com/search/results/all/?keywords={email}",
        }
        
        for platform, url in email_platforms.items():
            try:
                response = requests.head(url, headers=OSINTSearcher.HEADERS, timeout=3)
                results['services'][platform] = {
                    'available': True,
                    'status_code': response.status_code
                }
            except Exception as e:
                results['services'][platform] = {
                    'available': False,
                    'error': str(e)
                }
        
        return results

    @staticmethod
    def search_company(company_name: str) -> Dict[str, Any]:
        """
        Search for company information
        
        Args:
            company_name: Name of the company
            
        Returns:
            Dictionary with company search results
        """
        results = {
            'company_name': company_name,
            'search_time': datetime.now().isoformat(),
            'platforms': {}
        }
        
        company_platforms = {
            'crunchbase': f"https://www.crunchbase.com/organization/{company_name.lower().replace(' ', '-')}",
            'linkedin': f"https://www.linkedin.com/search/results/companies/?keywords={company_name}",
            'github': f"https://github.com/search?q=org:{company_name}",
            'twitter': f"https://twitter.com/search?q={company_name}",
            'google': f"https://www.google.com/search?q={company_name}+company",
        }
        
        for platform, url in company_platforms.items():
            try:
                response = requests.head(url, headers=OSINTSearcher.HEADERS, timeout=3)
                results['platforms'][platform] = {
                    'available': True,
                    'url': url,
                    'status_code': response.status_code
                }
            except Exception as e:
                results['platforms'][platform] = {
                    'available': False,
                    'url': url,
                    'error': str(e)
                }
        
        return results


def format_phone_number(phone: str) -> str:
    """Format phone number to standard format"""
    clean = ''.join(filter(str.isdigit, phone))
    
    if len(clean) == 10:
        return f"({clean[:3]}) {clean[3:6]}-{clean[6:]}"
    elif len(clean) == 11:
        return f"+{clean[0]} ({clean[1:4]}) {clean[4:7]}-{clean[7:]}"
    else:
        return clean


# Initialize searcher
osint_searcher = OSINTSearcher()
