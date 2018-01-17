require "test_helper"

class ActiveJobsTest < Minitest::Test
  def setup
    @initializers = [
      ONDEMAND.join("apps", "activejobs", "initializers"),
      AWESIM.join("apps", "activejobs", "initializers")
    ]
  end

  def test_that_initializers_are_same_across_portals
    init_files = @initializers.map do |p|
      Dir.glob(p.join("**", "*")).map{|f| Pathname.new(f)}.select(&:file?).sort
    end

    # Check for missing files
    rel_files = @initializers.zip(init_files).map do |dir, files|
      files.map {|f| f.relative_path_from(dir)}
    end
    missing = (rel_files.reduce(:+) - rel_files.reduce(:&)).uniq.map do |p|
      @initializers.map { |dir| dir.join(p) }.reject(&:file?)
    end.flatten
    assert missing.empty?, "Missing initializer files:\n  #{missing.join("\n  ")}"

    # Compare files
    init_files.combination(2) do |a_files, b_files|
      a_files.zip(b_files) do |a, b|
        assert FileUtils.cmp(a, b), "Initializer files differ:\n  #{a}\n  #{b}"
      end
    end
  end
end
