import pytest


async def test_create_short_url(client):
   payload = {
      "url": "https://google.com"
   }

   response = await client.post("/url", json=payload)

   assert response.status_code == 201

   data = response.json()
   assert data["url"] == payload["url"]
   assert "shorted_url" in data
   assert data["shorted_url"].startswith("http://127.0.0.1:8000/r/")


async def test_create_short_url_invalid_url(client):
   payload = {
      "url": "google.com"
   }

   response = await client.post("/url", json=payload)

   assert response.status_code == 422


async def test_get_original_url(client):
   create_response = await client.post(
      "/url",
      json={"url": "https://example.com"}
   )

   shorted_url = create_response.json()["shorted_url"]
   code = shorted_url.split("/")[-1]

   response = await client.get(f"/url/{code}")

   assert response.status_code == 200
   assert response.json()["url"] == "https://example.com"


async def test_get_url_stats(client):
   create_response = await client.post(
      "/url",
      json={"url": "https://fastapi.tiangolo.com"}
   )

   code = create_response.json()["shorted_url"].split("/")[-1]

   stats_response = await client.get(f"/url/{code}/stats")

   assert stats_response.status_code == 200

   data = stats_response.json()
   assert data["url"] == "https://fastapi.tiangolo.com"
   assert "created_at" in data
   assert "clicks" in data


async def test_get_url_not_found(client):
   response = await client.get("/url/ABCDEFGH")

   assert response.status_code == 404
