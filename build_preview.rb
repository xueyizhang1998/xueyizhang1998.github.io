require 'yaml'
require 'liquid'
require 'kramdown'
require 'fileutils'

ROOT = __dir__
class JekyllInclude < Liquid::Tag
  def initialize(name, markup, tokens)
    super
    @filename = markup.split.first
    @params = markup.scan(/(\w+)=("[^"]*"|'[^']*'|[^\s]+)/)
  end
  def render(context)
    args = @params.to_h.transform_values { |value| context.evaluate(Liquid::Expression.parse(value)) }
    context.stack do
      context['include'] = args
      Liquid::Template.parse(File.read(File.join(ROOT, '_includes', @filename)), error_mode: :strict).render!(context)
    end
  end
end
module JekyllFilters
  def relative_url(value)
    value.to_s.sub(%r{^/}, '')
  end
  def markdownify(value)
    Kramdown::Document.new(value.to_s).to_html
  end
end
Liquid::Template.register_tag('include', JekyllInclude)
Liquid::Template.register_filter(JekyllFilters)
site = YAML.load_file(File.join(ROOT, '_config.yml'))
site['data'] = Dir[File.join(ROOT, '_data', '*.yml')].to_h { |path| [File.basename(path, '.yml'), YAML.load_file(path)] }
index = File.read(File.join(ROOT, 'index.html')).sub(/\A---\n.*?\n---\n/m, '')
content = Liquid::Template.parse(index, error_mode: :strict).render!({'site' => site})
html = Liquid::Template.parse(File.read(File.join(ROOT, '_layouts', 'default.html')), error_mode: :strict).render!({'site' => site, 'content' => content, 'page' => {}})
File.write(File.join(ROOT, 'preview.html'), html)
puts "Rendered #{ROOT}/preview.html"
