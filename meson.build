project('themechanger', 'c',
          version: '0.12.1',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
)

subdir('data')
subdir('src')

meson.add_install_script('postinstall.py')
