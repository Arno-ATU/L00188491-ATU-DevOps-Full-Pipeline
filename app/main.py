import os
import logging
from flask import Flask, jsonify, request, send_from_directory
from .models import QuoteManager
from .stats import StatsTracker

# Application Insights monitoring
try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler
    from opencensus.ext.azure.trace_exporter import AzureExporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False

# Determine static folder path based on environment
if os.path.exists('/app/static'):
    static_folder = '/app/static'
    static_url_path = '/static'
else:
    static_folder = '../static'
    static_url_path = '/static'

app = Flask(__name__, 
            static_folder=static_folder,
            static_url_path=static_url_path)

quote_manager = QuoteManager()
stats_tracker = StatsTracker()

# Configure Application Insights monitoring
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
if connection_string and MONITORING_AVAILABLE:
    # Add Flask middleware for automatic request tracking
    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter(connection_string=connection_string)
    )
    
    # Configure logging to Azure
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(connection_string=connection_string))
    logger.setLevel(logging.INFO)
    
    def log_event(name, properties=None):
        """Log custom events to Application Insights"""
        logger.info(name, extra={'custom_dimensions': properties or {}})
    
    print("Application Insights monitoring enabled")
else:
    # Fallback logging for local development
    def log_event(name, properties=None):
        """Fallback logging when Application Insights not available"""
        print(f"LOG: {name} - {properties}")
    
    if not connection_string:
        print("Application Insights not configured (no connection string)")


@app.route('/')
def index():
    """Serve the main HTML page"""
    return app.send_static_file('index.html')


@app.route('/api/quote', methods=['GET'])
def get_random_quote():
    """Get a random quote from any category"""
    try:
        quote = quote_manager.get_random_quote()
        stats_tracker.record_quote_fetch(quote['category'])
        
        # Log quote fetch event
        log_event('quote_fetched', {
            'category': quote['category'],
            'quote_id': quote['id'],
            'author': quote['author']
        })
        
        return jsonify(quote)
    except Exception as e:
        log_event('quote_fetch_error', {'error': str(e)})
        return jsonify({'error': 'Failed to fetch quote'}), 500


@app.route('/api/quote/category/<category>', methods=['GET'])
def get_quote_by_category(category):
    """Get a random quote from a specific category"""
    try:
        quote = quote_manager.get_quote_by_category(category)
        if quote:
            stats_tracker.record_quote_fetch(category)
            
            # Log category-specific quote fetch
            log_event('quote_fetched_by_category', {
                'category': category,
                'quote_id': quote['id']
            })
            
            return jsonify(quote)
        else:
            log_event('quote_category_not_found', {'category': category})
            return jsonify({'error': f'No quotes found for category: {category}'}), 404
    except Exception as e:
        log_event('quote_fetch_error', {'error': str(e), 'category': category})
        return jsonify({'error': 'Failed to fetch quote'}), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available quote categories"""
    try:
        categories = quote_manager.get_categories()
        log_event('categories_requested', {'count': len(categories)})
        return jsonify({'categories': categories})
    except Exception as e:
        log_event('categories_error', {'error': str(e)})
        return jsonify({'error': 'Failed to fetch categories'}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get usage statistics"""
    try:
        stats = stats_tracker.get_stats()
        log_event('stats_requested', {
            'total_fetches': stats['total_quotes_fetched'],
            'total_favorites': stats['total_favorites']
        })
        return jsonify(stats)
    except Exception as e:
        log_event('stats_error', {'error': str(e)})
        return jsonify({'error': 'Failed to fetch stats'}), 500


@app.route('/api/favorite', methods=['POST'])
def add_favorite():
    """Mark a quote as favorite"""
    data = request.get_json()
    
    if not data or 'quote_id' not in data:
        return jsonify({'error': 'quote_id is required'}), 400
    
    quote_id = data['quote_id']
    success = stats_tracker.add_favorite(quote_id)
    
    if success:
        log_event('favorite_added', {'quote_id': quote_id})
        return jsonify({'message': 'Quote added to favorites', 'quote_id': quote_id})
    else:
        log_event('favorite_add_failed', {'quote_id': quote_id})
        return jsonify({'error': 'Invalid quote_id'}), 400


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Get all favorite quote IDs"""
    try:
        favorites = stats_tracker.get_favorites()
        log_event('favorites_requested', {'count': len(favorites)})
        return jsonify({'favorites': favorites, 'count': len(favorites)})
    except Exception as e:
        log_event('favorites_error', {'error': str(e)})
        return jsonify({'error': 'Failed to fetch favorites'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        log_event('health_check', {
            'status': 'healthy',
            'monitoring_enabled': connection_string is not None
        })
        return jsonify({
            'status': 'healthy', 
            'service': 'quote-generator',
            'monitoring': 'enabled' if connection_string else 'disabled'
        })
    except Exception as e:
        log_event('health_check_failed', {'error': str(e)})
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500



if __name__ == '__main__':
    # Only for local development
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)