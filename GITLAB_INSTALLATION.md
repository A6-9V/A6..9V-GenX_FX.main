# Self-Managed GitLab Installation

A self-managed GitLab Community Edition (CE) instance has been installed on this machine.

## Access Information

- **URL:** http://localhost:8989
- **Admin Username:** root
- **Initial Password:** BJ7gO+rVcqI3YUYBYvXlEdkb3ZJCZOGgoLfgaeUi40s=

## Maintenance

- **Configuration File:** /etc/gitlab/gitlab.rb
- **Manage Service:** sudo gitlab-ctl {start|stop|restart|status}
- **Logs:** sudo gitlab-ctl tail

## Optimization Notes

The installation has been optimized for low memory usage (approx 3GB RAM):
- Puma workers reduced to 2
- Sidekiq concurrency reduced to 5
- Monitoring services (Prometheus, Grafana, etc.) disabled
- PostgreSQL shared buffers reduced to 256MB

## Docker Note
Standard Docker containers cannot be run in this environment due to overlayfs mount restrictions. GitLab was installed natively using the Omnibus package.
