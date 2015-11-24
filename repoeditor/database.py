import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class Database():
    """Database reflecting your repo, built based on your XML file
    """
    
    # This variable lets user select one component of each category.
    # Based on the selection further operation can be performed.
    selection = {'license': None, 'package': None, 'version': None}
    
    # Indicates category component of which has been selected last.
    last_tag = None
    
    # Contains information parsed from XML file
    tree = None
    
    # Contains path to your XML file
    file_path = None
    
    # False if XML file reflects data in database, True otherwise
    changed = False
    
    # True until database is empty (no XML parsed, no data entered by user)
    empty = True

    # Used as an initial title of Qt window
    app_version = 'RepoEditor 1.0'

    def etitem_to_xml(self, etitem):
        """Converts ElementTree item to text in XML format
        """
        ugly_xml = ET.tostring(etitem).decode()
        reparsed = minidom.parseString(ugly_xml)
        pretty_xml = reparsed.toprettyxml()
        lines = [line for line in pretty_xml.splitlines() if line.strip()]
        xml = '\n'.join(lines[1:]) # skip the first line (header)
        return xml
        
    def get_xml(self, tag, name):
        """Returns item of given name and category indicated by 'tag'.
           Returned value is a text in XML format. 'tag' can be either
           'license' or 'package' or 'version'.
        """
        package = self.selection['package']
        items = self.get_items(tag, name, package)
        return self.etitem_to_xml(items[0])
    
    def reset(self):
        """Restores initial values of the variables, except for current
           selection. See also select method.
        """
        self.file_path = None
        self.changed = True
        self.empty = True
        path = os.path.join('templates', 'root.xml')
        self.tree = ET.parse(path)
         
    def load(self, file_path):
        """Loads content of given XML into self.tree
        """
        try:
            self.tree = ET.parse(file_path)
            self.sort()
        except Exception as ex:
            self.reset()
            raise

        self.file_path = file_path
        self.changed = False
        self.empty = False
        self.select()
        
    def save(self, file_path=None):
        """Saves content of self.tree into XML file
        """
        if file_path:
            self.file_path = file_path
        
        xml = self.etitem_to_xml(self.tree.getroot())
        reparsed = minidom.parseString(xml)
        pretty = reparsed.toprettyxml()
        lines = [line for line in pretty.splitlines() if line.strip()]
        xml = '\n'.join(lines[1:])
        
        path = os.path.join('templates', 'header.xml')
        with open(path, 'r') as f:
            header = f.read()
            
        with open(self.file_path, 'w') as f:
            f.write(header + xml)
            
        self.changed = False

    def get_names(self, tag, package=None):
        """Returns names of all the items in given category indicated by
           'tag'. Tag can be either 'license' or 'package' or 'version'.
           If tag is 'version', name of corresponding package also must
           be specified.
        """
        root = self.tree.getroot()
        if tag == 'version':
            names = [item.attrib['name'] for item in root.iterfind(tag) \
                     if item.attrib['package'] == package]
        else:
            names = [item.attrib['name'] for item in root.iterfind(tag)]
        return names
        
    def get_items(self, tag, name, package):
        """Returns items of given name in given category indicated by
           'tag'. Tag can be either 'license' or 'package' or 'version'.
           If tag is 'version', name of corresponding package also must
           be specified.
        """
        root = self.tree.getroot()
        if tag in ['version']:
            items = [item for item in root.iterfind(tag) \
                     if item.attrib['name'] == name and \
                     item.attrib['package'] == package]
        else:
            items = [item for item in root.iterfind(tag) \
                     if item.attrib['name'] == name]
        return items
        
    def get_vars(self):
        """Returns self.selection, but None values are replaced by empty
           strings.
        """
        vars_ = {tag: self.selection[tag] if self.selection[tag] else '' \
                for tag in self.selection}
        return vars_
        
    def format_title(self):
        """Returns title suitable for Qt window.
        """
        title = self.app_version
        if self.file_path:
            title += ' - ' + self.file_path + ['','*'][self.changed]

        return title

    def mark_changed(self):
        """Updates variables to reflect the fact that data has been
           changed by the user.
        """
        self.changed = True
        self.empty = False

    def select(self, item=None):
        """Updates selection based on the given item. if item is None,
           selection is cleared to initial values.
        """
        if item:
            tag = item.tag
            self.last_tag = tag
            self.selection[tag] = item.attrib['name']
            if tag == 'package':
                self.selection['version'] = None
            elif tag == 'version':
                self.selection['package'] = item.attrib['package']
        else:
            self.selection = {'license': None, 'package': None, 'version': None}
            self.last_tag = None

    def get_selected(self):
        """Returns tag and name of the item that was selected most recently.
        """
        if self.last_tag:
            name = self.selection[self.last_tag]
            if self.last_tag == 'version':
                name += ' of package ' + self.selection['package']
        else:
            name = ''
        return self.last_tag, name

    def overwrite_item(self, item=None):
        """Method can be used to add/remove/update/rename item.
           Items which belong to 'license' category are identified by unique name.
           Items which belong to 'package' category are identified by unique name.
           Items which belong to 'version' category are identified not only by name
           but also by package name. Pair of 'name' and 'package name' must be unique
           per each version.
           Category of the item is determined by it's tag'. Tag can be either
           'license' or 'package' or 'version'.
           
           This method relies on value of selection. See self.selection and self.last_tag
           
           To add item, specify 'item' argument and make sure that selection is empty.
           To remove item, skip 'item' argument and select item to be removed.
           To update item, specify 'item' argument and select item to be updated.
           To rename item, specify 'item' argument and select item to be renamed.
        """
        root = self.tree.getroot()
        
        if item:
            tag = item.tag
            name_new = item.attrib['name']
        else:
            tag = self.last_tag
            name_new = ''
        
        # remove selected
        if tag == self.last_tag:
            name = self.selection[tag]
            if tag == 'version':
                package = self.selection['package']
            else:
                package = None
                
            items_old = self.get_items(tag, name, package)
            for item_old in items_old:
                root.remove(item_old)

             # update referencing items
            if tag == 'license':
                packages = [item for item in root.iterfind('package')]
                for package in packages:
                    for license in package.iterfind('license'):
                        if license.text == self.selection[tag]:
                            license.text = name_new
            elif tag == 'package':
                versions = [item for item in root.iterfind('version') if item.attrib['package'] == name]
                for version in versions:
                    version.attrib['package'] = name_new
        
        if item:
            # remove existing
            if tag == 'version':
                package = item.attrib['package']
            else:
                package = None

            items_old = self.get_items(tag, name_new, package)
            for item_old in items_old:
                root.remove(item_old)

            root.append(item)

        self.changed = True
        
    def sort(self):
        """Sorts items in database. Also removes duplicates. Resulting
           format is:
           License1
           License2
           Package1
           Package2
           Package3
           Version1 of Package1
           Version2 of Package1
           Version1 of Package2
           Version1 of Package3
           Version2 of Package3
           Version3 of Package3
           
           Licenses, packages and versions are additionally sorted
           alphabetically by their names.
        """
        root = self.tree.getroot()
        items = []
        
        licenses = [item for item in root.iterfind('license')]
        licenses_sorted = sorted(licenses, key=lambda i: i.attrib['name'])
        items += licenses_sorted
        
        packages = [item for item in root.iterfind('package')]
        packages_sorted = sorted(packages, key=lambda i: i.attrib['name'])
        items += packages_sorted
        
        for package in packages_sorted:
            versions = [item for item in root.iterfind('version') if item.attrib['package'] == package.attrib['name']]
            max_len = max([max([len(part) for part in i.attrib['name'].split('.')]) for i in versions] + [0]) 
            
            def extend_parts(version_name):
                return '.'.join([(max_len*'0' + part)[-max_len:] for part in version_name.split('.')])
            
            versions_sorted = sorted(versions, key=lambda i: extend_parts(i.attrib['name']))
            items += versions_sorted
        
        root.clear()
        for item in items:
            root.append(item)

        self.changed = True

