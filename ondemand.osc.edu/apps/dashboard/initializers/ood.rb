NavConfig.categories_whitelist=true

require 'socket'
hostname = Socket.gethostname
case hostname
when /dev/
  idp = 'https://idp-dev.osc.edu'
when /test/
  idp = 'https://idp-test.osc.edu'
else
  idp = 'https://idp.osc.edu'
end
ENV['OOD_DASHBOARD_HELP_CUSTOM_URL'] = "#{idp}/auth/realms/osc/account/identity"
