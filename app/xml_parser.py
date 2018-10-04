#from ImageRanking import xml_details
import xml.etree.ElementTree as ET
tree = ET.parse('sample_xml')
root = tree.getroot()

for name in root.iter('name'):
    print(name.text)

for path in root.iter('path'):
    print(path.text)

for imagename in root.iter('filename'):
    print(imagename.text)