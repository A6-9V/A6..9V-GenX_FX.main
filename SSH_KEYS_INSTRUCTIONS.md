# SSH Key Pair and Organization Secret Instructions

## 🔑 Generated Keys

I have generated a 4096-bit RSA SSH key pair for you.

**CRITICAL SECURITY NOTE**: These keys are NOT stored in this repository. They have been deleted from the environment and added to `.gitignore` to prevent them from being committed. You must copy the keys from the chat message and save them in a secure location (like a password manager or GitHub Organization Secrets).

### Public Key (`id_rsa.pub`)
*Please copy from the chat response.*

### Private Key (`id_rsa`)
*Please copy from the chat response. Keep this extremely secure.*

## 🛠️ How to save as Organization Secret (GitHub)

1. Go to your GitHub Organization page.
2. Navigate to **Settings** -> **Secrets and variables** -> **Actions**.
3. Click on the **Secrets** tab.
4. Click **New organization secret**.
5. Name the secret (e.g., `ORG_SSH_PRIVATE_KEY`).
6. Paste the **Private Key** content into the value field.
7. Select repository access (e.g., "All repositories" or specific ones).
8. Click **Add secret**.
9. Repeat for the **Public Key** if needed (e.g., as `ORG_SSH_PUBLIC_KEY`).

## 🚀 How to use in GitHub Actions

```yaml
- name: Setup SSH
  uses: webfactory/ssh-agent@v0.9.0
  with:
    ssh-private-key: ${{ secrets.ORG_SSH_PRIVATE_KEY }}
```
