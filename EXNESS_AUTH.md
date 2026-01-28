# Exness Okta Authentication Guide

This guide explains how to authenticate your GenX FX Trading Platform with your Exness account using Okta SSO.

## 🔐 **Authentication Overview**

Exness uses Okta for secure, enterprise-grade authentication. By signing in through the Okta portal, you can access your Exness account credentials and manage your trading environment.

## 🚀 **How to Sign In**

1.  **Access the Portal**:
    Navigate to the following URL in your web browser:
    [https://exness.okta.com](https://exness.okta.com)

2.  **Enter Credentials**:
    -   Use your **LDAP username** (not your email address).
    -   Follow the on-screen instructions to complete the sign-in process.

3.  **Retrieve Account Details**:
    Once authenticated, you can find your MT4/MT5 account numbers, server details, and API keys required for the GenX FX platform.

## 🛠️ **CLI Integration**

You can also access the authentication portal directly from the AMP CLI:

```bash
python amp_cli.py exness-okta
```

## 📊 **Configuration**

After signing in and retrieving your account details, update your `.env` file with the following information:

```env
# Exness Account Settings
EXNESS_LOGIN=your_account_number
EXNESS_SERVER=Exness-Real
EXNESS_ACCOUNT_TYPE=real
```

## 🔒 **Security Best Practices**

-   **Never share your Okta credentials.**
-   **Enable Multi-Factor Authentication (MFA)** if available.
-   **Log out** of the Okta portal when finished with your session.

---

**GenX FX Trading Platform - Secure. Automated. Powerful.**
