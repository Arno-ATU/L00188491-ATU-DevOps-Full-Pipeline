import os
from flask import Flask, jsonify, request
from .models import QuoteManager
from .stats import StatsTracker

# Create Flask app with explicit static configuration
# In production (Docker), files are at /app/static
# In development, files are at ../static relative to app folder
if os.path.exists('/app/static'):
    app = Flask(__name__, 
                static_folder='/app/static',
                static_url_path='/static')
else:
    app = Flask(__name__, 
                static_folder='../static',
                static_url_path='/static')

quote_manager = QuoteManager()
stats_tracker = StatsTracker()


@app.route('/')
def index():
    """Serve the main HTML page"""
    return app.send_static_file('index.html')


@app.route('/api/quote', methods=['GET'])
def get_random_quote():
    """Get a random quote from any category"""
    quote = quote_manager.get_random_quote()
    stats_tracker.record_quote_fetch(quote['category'])
    return jsonify(quote)


@app.route('/api/quote/category/<category>', methods=['GET'])
def get_quote_by_category(category):
    """Get a random quote from a specific category"""
    quote = quote_manager.get_quote_by_category(category)
    if quote:
        stats_tracker.record_quote_fetch(category)
        return jsonify(quote)
    else:
        return jsonify({'error': f'No quotes found for category: {category}'}), 404


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available quote categories"""
    categories = quote_manager.get_categories()
    return jsonify({'categories': categories})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get usage statistics"""
    stats = stats_tracker.get_stats()
    return jsonify(stats)


@app.route('/api/favorite', methods=['POST'])
def add_favorite():
    """Mark a quote as favorite"""
    data = request.get_json()
    
    if not data or 'quote_id' not in data:
        return jsonify({'error': 'quote_id is required'}), 400
    
    quote_id = data['quote_id']
    success = stats_tracker.add_favorite(quote_id)
    
    if success:
        return jsonify({'message': 'Quote added to favorites', 'quote_id': quote_id})
    else:
        return jsonify({'error': 'Invalid quote_id'}), 400


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Get all favorite quote IDs"""
    favorites = stats_tracker.get_favorites()
    return jsonify({'favorites': favorites, 'count': len(favorites)})


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy', 
        'service': 'quote-generator',
        'static_folder': app.static_folder  # For debugging
    })


if __name__ == '__main__':
    # Only for local development - Azure uses different startup
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)