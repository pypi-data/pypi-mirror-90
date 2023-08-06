# StartR
Python package for bootstrapping TFW tutorials

### Usage

```
from tfwstartr import Startr

# Get available templates
available_starter_templates = Startr.get_starters()

# Get supported packages for a package manager
package_manager = 'pip' # Currently available: pip, npm
supported_packages = Startr.get_supported_packages(package_manager)

# Get required packages for a specific starter template
# The parameters can be found in _available_starter_templates_
required_packages = Startr.get_starter_requirements(
    language_name,
    framework_name,
    starter_name,
)

# Bootstrap a starter project
# It will generate a ZIP file that you can either
#    return or save
extra_packages = {
    'package_name_1': 'version_1',
    'package_name_2': 'version_2', 
}
with Startr() as startr:
    data = startr.generate_starter(
        language_name,
        framework_name,
        starter_name,
        extra_packages,
    )
    # Return the generated template
    # return data

    # Save the generated template, e.g. extract it to a folder
    import zipfile
    with zipfile.ZipFile(data) as f:
        f.extractall('/tmp/tfwstartr')
```
