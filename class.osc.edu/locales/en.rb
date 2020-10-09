# Files in the config/locales directory are used for internationalization
# and are automatically loaded by Rails. If you want to use locales other
# than English, add the necessary files in this directory.
#
# To use the locales, use `I18n.t`:
#
#     I18n.t 'hello'
#
# In views, this is aliased to just `t`:
#
#     <%= t('hello') %>
#
# To use a different locale, set it with `I18n.locale`:
#
#     I18n.locale = :es
#
# This would use the information in config/locales/es.yml.
#
# To learn more, please read the Rails Internationalization guide
# available at http://guides.rubyonrails.org/i18n.html.

def content_tag(*args, &block)
  ActionController::Base.helpers.content_tag(*args, &block)
end

def concat(*args, &block)
  ActionController::Base.helpers.concat(*args, &block)
end


def r_studio_groups
  @r_studio_groups ||= 
  [
    "PAS1758", #STAT 2480
    "PAS1644", #STAT 3202
    "PAS1642", #STAT 5730
    "PAS1723", #ANTHRO 9982
    "PAS1732", #TDAI Workshop
    "PZS0687", #OSC Workshop
    "PZS1010", #OSC RNA-Seq Workshop
    "PAS1754", #PUBHLTH 5015
    "PES0835", #BANA 7025
    "PES0836", #UC Workshop
  ]
end

def jupyter_groups
  @jupyter_groups ||= 
  [
   "PAS1745",   #BIOCHEM 5721
   "PAS1759",   #PHYSICS 6820
   "PWIT0412",  #PHYSICS 280 WIT 
  ]
end

def anthro_9982?
  groups.include?("PAS1723") || staff?
end

def stat_2480?
  groups.include?("PAS1758") || staff?
end

def groups
  @groups ||= OodSupport::Process.groups.map(&:name)
end

def include_rstudio?
  (groups & r_studio_groups).size > 0 || staff?
end

def include_jupyter?
 (groups & jupyter_groups).size > 0 || staff?
end

def staff?
  @staff ||= groups.include?('oscstaff')
end

def rstudio_ref
  "/pun/sys/dashboard/batch_connect/sys/bc_osc_rstudio_server/form/session_contexts/new"
end

def rstudio_img
  "/pun/sys/dashboard/apps/icon/bc_osc_rstudio_server"
end

def jupyter_ref
  "/pun/sys/dashboard/batch_connect/sys/bc_osc_jupyter/form/session_contexts/new"
end

def jupyter_img
  "/pun/sys/dashboard/apps/icon/bc_osc_jupyter"
end

def iqmol_ref
  "/pun/sys/dashboard/batch_connect/sys/bc_osc_iqmol/session_contexts/new"
end

def iqmol_img
  "/pun/sys/dashboard/apps/icon/bc_osc_iqmol"
end

def interactive_ref
  "/pun/sys/dashboard/batch_connect/sessions"
end

def stat2480_links
  [
    ["Course textbook: The Analysis of Biological Data", "https://whitlockschluter3e.zoology.ubc.ca"]
  ]
end

def anthro9982_links
  [
    ["Anthropology 9982 Course Website", "https://osu.instructure.com/courses/85349"]
  ]
end

def icon(ref, text, img_src, img_alt_text)
  content_tag(:div, class: "col-sm-3 col-md-3") do
    concat (
      content_tag(:a, class: "thumbnail app", href: ref) do
        concat (
          content_tag(:div, class: "center-block", style: "text-align: center") do
            unless img_src.nil?
              concat content_tag(:img, class: "app-icon", src: img_src, alt: img_alt_text) {}
            else
              concat content_tag(:i, class: "fa fa-window-restore fa-fw app-icon") {}
            end
            concat content_tag(:p) { text }
          end
        )
      end
    )
 end
end

def links_section(heading, links)
  content_tag(:section) do
    concat content_tag(:h3, heading)
    concat (
      content_tag(:ul) do
        links.each do |text, ref|
          concat ( 
            content_tag(:li) do
              concat content_tag(:a, href: ref, target:"_blank") { text }
            end
          )
        end
      end
    )
  end
end


def welcome_html
  content_tag(:div) do
    concat content_tag(:h1, class: "hidden") { "Classroom Dashboard" }
    concat content_tag(:h2, class: "apps-section-header-blue") { "Useful Links" }
    concat (
      content_tag(:div, class: "card") do
        concat (
          content_tag(:div, class: "card-body") do
            concat links_section("General Links", [["Carmen","https://carmen.osu.edu"]])
            concat links_section("STAT 2480", stat2480_links) if stat_2480?
            concat links_section("ANTHROP 9982", anthro9982_links) if anthro_9982?
          end
        )  
      end
    )

    concat content_tag(:h2, class: "apps-section-header-blue") { "Interactive Apps" }
    concat (
      content_tag(:div, class: "row") do
        concat icon(rstudio_ref, "RStudio Server", rstudio_img, "Bc osc rstudio server") if include_rstudio?
        concat icon(jupyter_ref, "Jupyter", jupyter_img, "Bc osc jupyter") if include_jupyter?
        concat icon(iqmol_ref, "IQmol", iqmol_img, "Bc osc i q mol")
        concat icon(interactive_ref, "My Interactive Sessions", nil, nil)
      end 
    )
  end
end

locale = {
  en: {
    dashboard: {
      welcome_html: welcome_html,
      shared_apps_title: "Shared Apps",
      sharing_catalog_title: "App Catalog",
      sharing_support_msg_html: '',
      sharing_welcome_msg_html: ''
    }   
  }
}
