from locust import task, run_single_user, FastHttpUser
from insert_product import login


class AddToCartUser(FastHttpUser):
    host = "http://localhost:5000"

    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        self.token = self.get_auth_token()

    def get_auth_token(self):
        """Retrieve the authentication token."""
        cookies = login(self.username, self.password)
        return cookies.get("token")

    @task
    def fetch_cart(self):
        """Simulates a GET request to the /cart route."""
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Cookie": f"token={self.token}",  # Fixed syntax for Cookie header
            "Referer": f"{self.host}/product/1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        }
        with self.client.get("/cart", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to fetch cart: {response.status_code}")


if __name__ == "__main__":
    run_single_user(AddToCartUser)
