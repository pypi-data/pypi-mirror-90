# Fabric Authenticator for Jupyterhub

The authenticator for Fabric Testbed Jupyterhub
Based on CILogon authentication, in addition it checks if user belongs to Fabric JUPYTERHUB COU group

## Usage
### If using dockerspawner:

In jupyter_config.py:
If using Fabric CI Logon Authenticator

```
   import fabricauthenticator
   c.JupyterHub.authenticator_class = 'fabricauthenticator.FabricAuthenticator'
   c.Authenticator.enable_auth_state = True

   # set the OIDC client info in following CILogon configuration
   c.CILogonOAuthenticator.client_id = ""
   c.CILogonOAuthenticator.client_secret = ""
   c.CILogonOAuthenticator.oauth_callback_url = "<host>/hub/oauth_callback"
```
If using Fabric Vouch Proxy Authenticator
```
c.JupyterHub.authenticator_class = 'fabricauthenticator.vouch_proxy_authenticator.VouchProxyAuthenticator'
```

### if using KubeSpawner

in config.yaml:
If using Fabric CI Logon Authenticator
```
hub:
  extraConfig:
    authconfig: |
      c.Authenticator.enable_auth_state = True
      c.CILogonOAuthenticator.client_id = ""
      c.CILogonOAuthenticator.client_secret = ""
      c.CILogonOAuthenticator.oauth_callback_url = "<host>/hub/oauth_callback"
auth:
  type: custom
  custom:
      className: fabricauthenticator.FabricAuthenticator
```
If using Fabric Vouch Proxy Authenticator
```
hub:
  extraConfig:
    authconfig: |
      c.Authenticator.enable_auth_state = True
auth:
  type: custom
  custom:
      className: fabricauthenticator.vouch_proxy_authenticator.VouchProxyAuthenticator
```