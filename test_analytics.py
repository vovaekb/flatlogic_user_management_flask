from app import app

def test_analytics():
    print('testing /analytics GET')
    with app.test_client() as c:
        rv = c.get('/analytics', json={})
        print(rv.data)
        print('status: ', rv.status_code)


if __name__ == '__main__':
    test_analytics()