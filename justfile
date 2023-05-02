local:
  (cd src || exit 1; python -m uvicorn project.main:app --reload)
