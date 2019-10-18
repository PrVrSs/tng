async def test_index(client):
    response = await client.get('/')
    assert response.status == 200
