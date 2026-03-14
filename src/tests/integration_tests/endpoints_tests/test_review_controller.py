#pylint: disable=unused-argument
def test_create_review(client, fake_user, fake_product, fake_category):
    response = client.post("/api/v1/reviews/", json={
        "user_id": fake_user.id,
        "product_id": fake_product.id,
        "rating": 5,
        "comment": "Excellent!"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == fake_user.id
    assert data["product_id"] == fake_product.id
    assert data["rating"] == 5


def test_create_review_user_not_found(client, fake_product, fake_category):
    response = client.post("/api/v1/reviews/", json={
        "user_id": 9999,
        "product_id": fake_product.id,
        "rating": 4,
        "comment": "Good"
    })
    assert response.status_code == 404


def test_create_review_product_not_found(client, fake_user):
    response = client.post("/api/v1/reviews/", json={
        "user_id": fake_user.id,
        "product_id": 9999,
        "rating": 3,
        "comment": "Average"
    })
    assert response.status_code == 404


def test_get_review_by_id(client, fake_review):
    response = client.get(f"/api/v1/reviews/{fake_review.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_review.id


def test_get_review_not_found(client):
    response = client.get("/api/v1/reviews/9999")
    assert response.status_code == 404


def test_list_reviews_no_filters(client, fake_review):
    response = client.get("/api/v1/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_list_reviews_filter_by_product(client, fake_review):
    response = client.get("/api/v1/reviews/", params={"product_id": fake_review.product_id})
    assert response.status_code == 200
    data = response.json()
    assert all(r["product_id"] == fake_review.product_id for r in data)


def test_list_reviews_filter_by_user(client, fake_review):
    response = client.get("/api/v1/reviews/", params={"user_id": fake_review.user_id})
    assert response.status_code == 200
    data = response.json()
    assert all(r["user_id"] == fake_review.user_id for r in data)


def test_list_reviews_filter_by_rating(client, fake_review):
    response = client.get("/api/v1/reviews/", params={"min_rating": 1, "max_rating": 5})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_review(client, fake_review):
    delete_response = client.delete(f"/api/v1/reviews/{fake_review.id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/reviews/{fake_review.id}")
    assert get_response.status_code == 404
