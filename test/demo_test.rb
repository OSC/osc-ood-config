require "test_helper"

class DemoTest < Minitest::Test
  def setup
    @apps = DEMO.join("apps")
  end

  %w[dashboard shell bc_desktop].each do |app|
    define_method "test_that_it_configures_#{app}" do
      assert @apps.join(app).directory?
    end
  end
end
