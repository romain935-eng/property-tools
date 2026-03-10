# API route handlers.
#
# REST resources: /api/units/, /api/jobs/, /api/demands/, etc.
# Error shape:  {"error": "message", "code": "SNAKE_CASE_CODE"}
# Pagination:   limit / offset query params, default limit=50.
# Leaseholder-facing routes use UUIDs, never internal DB ids.
