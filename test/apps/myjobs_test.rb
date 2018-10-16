require "test_helper"

class MyJobsTest < Minitest::Test
  def setup
    @templates = [
      ONDEMAND.join("apps", "myjobs", "templates"),
      AWESIM.join("apps", "myjobs", "templates"),
      DEMO_TEST.join("apps", "myjobs", "templates")
    ]
  end

  def test_that_templates_are_same_across_portals
    tpl_files = @templates.map do |p|
      Dir.glob(p.join("**", "*")).map{|f| Pathname.new(f)}.select(&:file?).sort
    end

    # Check for missing files
    rel_files = @templates.zip(tpl_files).map do |dir, files|
      files.map {|f| f.relative_path_from(dir)}
    end
    missing = (rel_files.reduce(:+) - rel_files.reduce(:&)).uniq.map do |p|
      @templates.map { |dir| dir.join(p) }.reject(&:file?)
    end.flatten
    assert missing.empty?, "Missing template files:\n  #{missing.join("\n  ")}"

    # Compare files
    tpl_files.combination(2) do |a_files, b_files|
      a_files.zip(b_files) do |a, b|
        assert FileUtils.cmp(a, b), "Template files differ:\n  #{a}\n  #{b}"
      end
    end
  end
end
