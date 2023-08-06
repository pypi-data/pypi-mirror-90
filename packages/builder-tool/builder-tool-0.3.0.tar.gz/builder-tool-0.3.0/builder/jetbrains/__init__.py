"""
This defines the things used by all "languages" of JetBrains IDEs.
"""
from pathlib import Path

_idea_directory = Path('.idea')

compiler_xml_path = _idea_directory / 'compile.xml'
encodings_xml_path = _idea_directory / 'encodings.xml'
misc_xml_path = _idea_directory / 'misc.xml'
modules_xml_path = _idea_directory / 'modules.xml'

# ----------------------------------------------------------------------------
# Below here are all the templates of files we need to play with
# ----------------------------------------------------------------------------
_compiler_xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="CompilerConfiguration">
    <wildcardResourcePatterns>
      <entry name="!?*.java" />
      <entry name="!?*.form" />
      <entry name="!?*.class" />
      <entry name="!?*.groovy" />
      <entry name="!?*.scala" />
      <entry name="!?*.flex" />
      <entry name="!?*.kt" />
      <entry name="!?*.clj" />
    </wildcardResourcePatterns>
  </component>
</project>"""

_encodings_xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="Encoding">
    <file url="PROJECT" charset="UTF-8" />
  </component>
</project>"""

_misc_xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" languageLevel="JDK_{{ java_version }}" default="false" project-jdk-name="{{ java_version }}" project-jdk-type="JavaSDK">
    <output url="file://$PROJECT_DIR$/build/ij" />
  </component>
</project>"""

_modules_xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/{{ project_name }}.iml" filepath="$PROJECT_DIR$/{{ project_name }}.iml" />
    </modules>
  </component>
</project>"""

# ----------------------------------------------------------------------------
# Here are our maps and common codee, etc.
# ----------------------------------------------------------------------------
_names_to_templates = {
    compiler_xml_path:  _compiler_xml_template,
    encodings_xml_path: _encodings_xml_template,
    misc_xml_path:      _misc_xml_template,
    modules_xml_path:   _modules_xml_template
}
