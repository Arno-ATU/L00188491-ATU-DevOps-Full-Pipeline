import random


class QuoteManager:
    """Manages the quote database and retrieval"""
    
    def __init__(self):
        self.quotes = [
            # Motivational Quotes
            {"id": 1, "text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "motivational"},
            {"id": 2, "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "category": "motivational"},
            {"id": 3, "text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "category": "motivational"},
            {"id": 4, "text": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "category": "motivational"},
            {"id": 5, "text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "motivational"},
            {"id": 6, "text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "category": "motivational"},
            {"id": 7, "text": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair", "category": "motivational"},
            
            # Wisdom Quotes
            {"id": 8, "text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates", "category": "wisdom"},
            {"id": 9, "text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "category": "wisdom"},
            {"id": 10, "text": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "wisdom"},
            {"id": 11, "text": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu", "category": "wisdom"},
            {"id": 12, "text": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde", "category": "wisdom"},
            {"id": 13, "text": "Yesterday is history, tomorrow is a mystery, but today is a gift.", "author": "Eleanor Roosevelt", "category": "wisdom"},
            {"id": 14, "text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb", "category": "wisdom"},
            
            # Humor Quotes
            {"id": 15, "text": "I'm not superstitious, but I am a little stitious.", "author": "Michael Scott", "category": "humor"},
            {"id": 16, "text": "I told my wife she was drawing her eyebrows too high. She looked surprised.", "author": "Anonymous", "category": "humor"},
            {"id": 17, "text": "The problem with troubleshooting is that trouble shoots back.", "author": "Anonymous", "category": "humor"},
            {"id": 18, "text": "I'm not arguing, I'm just explaining why I'm right.", "author": "Anonymous", "category": "humor"},
            {"id": 19, "text": "I used to think I was indecisive, but now I'm not so sure.", "author": "Anonymous", "category": "humor"},
            {"id": 20, "text": "Why do programmers prefer dark mode? Because light attracts bugs!", "author": "Anonymous", "category": "humor"},
        ]
    
    def get_random_quote(self):
        """Get a random quote from all categories"""
        return random.choice(self.quotes)
    
    def get_quote_by_category(self, category):
        """Get a random quote from a specific category"""
        category_quotes = [q for q in self.quotes if q['category'].lower() == category.lower()]
        if category_quotes:
            return random.choice(category_quotes)
        return None
    
    def get_quote_by_id(self, quote_id):
        """Get a specific quote by ID"""
        for quote in self.quotes:
            if quote['id'] == quote_id:
                return quote
        return None
    
    def get_categories(self):
        """Get all unique categories"""
        categories = list(set(q['category'] for q in self.quotes))
        return sorted(categories)
    
    def get_quotes_by_author(self, author):
        """Get all quotes by a specific author"""
        return [q for q in self.quotes if author.lower() in q['author'].lower()]