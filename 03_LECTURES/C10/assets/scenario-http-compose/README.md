### Scenario: HTTP via a reverse proxy (Docker Compose)

Aim:
- Explain what a reverse proxy does: routing, rewriting, redirects and headers
- Observe where redirects are generated and how base paths affect applications
- Diagnose common issues: incorrect scheme in redirects, incorrect Host header and missing forwarded headers

Components:
- nginx (reverse proxy)
- web (simple HTML server)
- api (Flask JSON service)

Exercises:
1) Start the Compose stack and open http://localhost:8080/
   - Observe the redirect to /app/
2) Verify that /app/ is served by the web container via an nginx rewrite
3) Call /api/users and confirm that it is routed to the api service
4) Inspect response headers (Location, X-Debug-*, X-Forwarded-*)
5) Modify `nginx.conf`:
   - remove the rewrite and observe broken relative paths
   - change the redirect status code from 302 to 301 and discuss caching implications

Run:
- docker compose up --build
- Open a browser: http://localhost:8080/
- Test:
  - curl -i http://localhost:8080/
  - curl -i http://localhost:8080/app/
  - curl -i http://localhost:8080/api/users
