# Configuration file for lab.

c = get_config()  # noqa

# DEPRECATED in 2.0. Use PasswordIdentityProvider.allow_password_change
#  Default: True
c.ServerApp.allow_password_change = False

# The IP address the Jupyter server will listen on.
#  Default: 'localhost'
c.ServerApp.ip = '0.0.0.0'

# Whether to open in a browser after starting.
#                          The specific browser used is platform dependent and
#                          determined by the python standard library `webbrowser`
#                          module, unless it is overridden using the --browser
#                          (ServerApp.browser) configuration option.
#  Default: False
c.ServerApp.open_browser = False

# The port the server will listen on (env: JUPYTER_PORT).
#  Default: 0
# Choose 9999 to match UChicago AF preferences
c.ServerApp.port = 9999

# Supply overrides for terminado. Currently only supports "shell_command".
#  Default: {}
# Set shell to bash as AnalysisBase assumes it
# force login shell to pickup ~/.bash_profile
c.ServerApp.terminado_settings = {"shell_command": ["/bin/bash", "-l"]}
