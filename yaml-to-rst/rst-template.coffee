module.exports = (name, url, content) -> 

  line = ('-' for i in [0..(name.length)]).join('')

  header = "#{line}\n#{name}_\n#{line}"

  # interpolate in the following string
  """
  .. index::
    single: #{name}

  .. _mdoc_#{name}:

  #{header}

  #{content}

  .. _#{name}: #{url}
  """
