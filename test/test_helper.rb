$LOAD_PATH.unshift File.expand_path("../../lib", __FILE__)
require "pathname"

ONDEMAND=Pathname.new("ondemand.osc.edu")
AWESIM=Pathname.new("apps.awesim.org")
CLASS=Pathname.new("class.osc.edu")
TOTALSIM=Pathname.new("apps.totalsim.us")

require "minitest/autorun"
