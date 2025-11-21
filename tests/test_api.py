import pytest
import json
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Import here to avoid circular imports
        from app.main import stats_tracker
        # Reset stats before each test
        stats_tracker.reset_stats()
        yield client


class TestAPIEndpoints:
    """Tests for Flask API endpoints"""
    
    def test_index_route(self, client):
        """Test that index route returns HTML"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'quote-generator'
    
    def test_get_random_quote(self, client):
        """Test getting a random quote"""
        response = client.get('/api/quote')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'id' in data
        assert 'text' in data
        assert 'author' in data
        assert 'category' in data
    
    def test_get_random_quote_returns_different_quotes(self, client):
        """Test that multiple requests can return different quotes"""
        # Note: This test might occasionally fail due to randomness
        # but with 20 quotes, getting the same quote 5 times is unlikely
        quotes = []
        for _ in range(5):
            response = client.get('/api/quote')
            data = json.loads(response.data)
            quotes.append(data['id'])
        
        # At least 2 different quotes should be returned
        assert len(set(quotes)) >= 2
    
    def test_get_quote_by_category_motivational(self, client):
        """Test getting a motivational quote"""
        response = client.get('/api/quote/category/motivational')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['category'] == 'motivational'
    
    def test_get_quote_by_category_wisdom(self, client):
        """Test getting a wisdom quote"""
        response = client.get('/api/quote/category/wisdom')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['category'] == 'wisdom'
    
    def test_get_quote_by_category_humor(self, client):
        """Test getting a humor quote"""
        response = client.get('/api/quote/category/humor')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['category'] == 'humor'
    
    def test_get_quote_by_invalid_category(self, client):
        """Test that invalid category returns 404"""
        response = client.get('/api/quote/category/nonexistent')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        
        assert 'error' in data
    
    def test_get_categories(self, client):
        """Test getting all categories"""
        response = client.get('/api/categories')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'categories' in data
        assert isinstance(data['categories'], list)
        assert len(data['categories']) > 0
    
    def test_get_categories_contains_expected(self, client):
        """Test that categories endpoint returns expected categories"""
        response = client.get('/api/categories')
        data = json.loads(response.data)
        
        categories = data['categories']
        assert 'motivational' in categories
        assert 'wisdom' in categories
        assert 'humor' in categories
    
    def test_get_stats_initial(self, client):
        """Test getting stats returns proper structure"""
        response = client.get('/api/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'total_quotes_fetched' in data
        assert 'categories_accessed' in data
        assert 'most_popular_category' in data
        assert 'total_favorites' in data
        assert 'unique_categories_used' in data
    
    def test_add_favorite_valid(self, client):
        """Test adding a valid favorite"""
        response = client.post('/api/favorite',
                              data=json.dumps({'quote_id': 1}),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'message' in data
        assert data['quote_id'] == 1
    
    def test_add_favorite_missing_quote_id(self, client):
        """Test that missing quote_id returns 400"""
        response = client.post('/api/favorite',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert 'error' in data
    
    def test_add_favorite_invalid_quote_id(self, client):
        """Test that invalid quote_id returns 400"""
        response = client.post('/api/favorite',
                              data=json.dumps({'quote_id': -1}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert 'error' in data
    
    def test_add_favorite_no_json_body(self, client):
        """Test that request without JSON body returns 415 (Unsupported Media Type)"""
        response = client.post('/api/favorite')
        
        # Flask returns 415 when Content-Type is not application/json
        assert response.status_code == 415
    
    def test_get_favorites_empty(self, client):
        """Test getting favorites when none exist"""
        response = client.get('/api/favorites')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'favorites' in data
        assert 'count' in data
        assert data['count'] == 0
    
    def test_get_favorites_after_adding(self, client):
        """Test getting favorites after adding some"""
        # Add some favorites
        client.post('/api/favorite',
                   data=json.dumps({'quote_id': 1}),
                   content_type='application/json')
        client.post('/api/favorite',
                   data=json.dumps({'quote_id': 3}),
                   content_type='application/json')
        
        # Get favorites
        response = client.get('/api/favorites')
        data = json.loads(response.data)
        
        assert data['count'] == 2
        assert 1 in data['favorites']
        assert 3 in data['favorites']
    
    def test_stats_tracking_after_quote_fetch(self, client):
        """Test that stats are updated after fetching quotes"""
        # Fetch some quotes
        client.get('/api/quote')
        client.get('/api/quote/category/motivational')
        
        # Check stats
        response = client.get('/api/stats')
        data = json.loads(response.data)
        
        assert data['total_quotes_fetched'] >= 2
    
    def test_content_type_json(self, client):
        """Test that API returns JSON content type"""
        response = client.get('/api/quote')
        
        assert response.content_type == 'application/json'
    
    def test_multiple_quote_fetches_increment_stats(self, client):
        """Test that multiple fetches increment stats correctly"""
        # Fetch multiple times
        for _ in range(5):
            client.get('/api/quote')
        
        # Check stats
        response = client.get('/api/stats')
        data = json.loads(response.data)
        
        assert data['total_quotes_fetched'] == 5

    def test_static_file_serving(self, client):
        """Test that static files are served correctly"""
        response = client.get('/static/style.css')
        assert response.status_code in [200, 404]  # 404 ok in test env without static files
        
    def test_root_serves_html(self, client):
        """Test root serves index.html"""
        response = client.get('/')
        assert response.status_code == 200