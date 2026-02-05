# Performance & CI/CD Learnings

- **CI/CD Optimization**: Committing virtual environments (like `forexconnect_env_37`) to the repository can cause linting tools (`black`, `isort`, `flake8`) to explode in scope and fail the CI. Always configure these tools to exclude such directories using a `pyproject.toml` or tool-specific config files.
- **Docker Multi-Stage Builds**: When using multi-stage builds with Python, ensure the site-packages path matches the Python version in both the builder and production stages. A mismatch (e.g., copying from 3.11 to 3.13) will result in missing dependencies.
- **Unified Pipeline**: Consolidating multiple specialized workflows (`ci-cd.yml`, `deploy-static.yml`, `manual-deploy.yml`) into a single robust pipeline improves maintainability and reduces redundant runs.
- **Vite Build Paths**: In Vite projects where the root is set to a subdirectory (e.g., `client`), the build output (`dist`) is typically inside that subdirectory. Deployment scripts must use the correct relative path (`client/dist`).
