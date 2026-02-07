### Scenario: HTTP through reverse proxy (docker compose)

Goal:
- Understand what a reverse proxy does: routing, rewriting, redirects, headers
- Observe "where" a redirect is generated and how base paths affect apps
- Debug common issues: wrong scheme in redirects, wrong Host, missing forwarded headers

Components:
- nginx (reverse proxy)
- web (simple HTML server)
- api (Flask JSON service)

Exercises:
1) Run compose, open http://localhost:8080/
   - Notice it redirects to /app/
2) Confirm /app/ is served by web container, but via nginx rewrite
3) Call /api/users and see it is routed to api service
4) Inspect headers in responses (Location, X-Debug-*, X-Forwarded-*)
5) Modify nginx.conf:
   - remove rewrite and observe broken relative paths
   - change redirect code 302 -> 301 and discuss caching impact

Run:
- docker compose up --build
- open browser: http://localhost:8080/
- test:
  - curl -i http://localhost:8080/
  - curl -i http://localhost:8080/app/
  - curl -i http://localhost:8080/api/users
