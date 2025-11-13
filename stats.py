from collections import defaultdict
from datetime import datetime


class StatsTracker:
    """Tracks usage statistics for the quote generator"""
    
    def __init__(self):
        self.category_counts = defaultdict(int)
        self.total_fetches = 0
        self.favorites = set()
        self.fetch_timestamps = []
    
    def record_quote_fetch(self, category):
        """Record that a quote was fetched from a category"""
        self.category_counts[category] += 1
        self.total_fetches += 1
        self.fetch_timestamps.append(datetime.now())
    
    def add_favorite(self, quote_id):
        """Add a quote to favorites"""
        if not isinstance(quote_id, int) or quote_id < 1:
            return False
        
        self.favorites.add(quote_id)
        return True
    
    def get_favorites(self):
        """Get all favorite quote IDs"""
        return sorted(list(self.favorites))
    
    def get_stats(self):
        """Get comprehensive statistics"""
        most_popular = self._get_most_popular_category()
        
        return {
            'total_quotes_fetched': self.total_fetches,
            'categories_accessed': dict(self.category_counts),
            'most_popular_category': most_popular,
            'total_favorites': len(self.favorites),
            'unique_categories_used': len(self.category_counts)
        }
    
    def _get_most_popular_category(self):
        """Get the category with the most fetches"""
        if not self.category_counts:
            return None
        
        return max(self.category_counts.items(), key=lambda x: x[1])[0]
    
    def reset_stats(self):
        """Reset all statistics"""
        self.category_counts = defaultdict(int)
        self.total_fetches = 0
        self.favorites = set()
        self.fetch_timestamps = []