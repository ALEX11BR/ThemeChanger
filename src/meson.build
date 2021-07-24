pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'themechanger')
gnome = import('gnome')

gnome.compile_resources('themechanger',
  'themechanger.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('gtkversion', '3.0')

configure_file(
  input: 'themechanger.in',
  output: 'themechanger',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

themechanger_sources = [
  '__init__.py',
  'archivefilefilter.py',
  'getavailablethemes.py',
  'installthemes.py',
  'main.py',
  'searchablethemelist.py',
  'window.py',
]

install_data(themechanger_sources, install_dir: moduledir)
