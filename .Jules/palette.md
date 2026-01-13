## 2025-02-18 - The False Error Pattern
**Learning:** Users perceive "Server not responding" on initial load as a broken application, even if it's just a sub-second latency. A missing loading state is functionally identical to an error state in the user's mind.
**Action:** Always initialize with a dedicated `loading` state (`isLoading = true`) and distinct UI (spinner/skeleton) before resolving to success or error. Never let `null` data default to an error UI during the initial fetch.
