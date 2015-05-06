from lxml import etree
import os.path
import shutil

class ExportAddonFile:
    def __init__(self, interface, wTree, rootDir):
        self.i = interface
        self.wTree = wTree
        self.identityUri = 'urn:umlfri.org:metamodel:'	
        self.friendlyName = ''	
        self.friendlyNameVersion = ''
        self.authorName = ''
        self.authorHomepageUrl = ''
        self.authorCommonLicenseName = 'GPL-3'
        self.iconPath = 'icons/'
        self.description = ''
        self.metamodelPath = 'metamodel'
        self.metamodelTemplatePath = 'templates/empty.fritx'
        self.metamodelTemplateName = ''
        self.rootDir = rootDir
        
    def loadFormular(self):
        self.friendlyName = self.wTree.get_widget('entryName').get_text()
        tag = self.wTree.get_widget('entryUriTag').get_text()
        self.identityUri += tag
        self.friendlyNameVersion = self.wTree.get_widget('entryVersion').get_text()
        self.authorName = self.wTree.get_widget('entryAuthor').get_text()
        self.authorHomepageUrl = self.wTree.get_widget('entryHomepage').get_text()
        startIter = self.wTree.get_widget('textviewDescription').get_buffer().get_start_iter()
        endIter = self.wTree.get_widget('textviewDescription').get_buffer().get_end_iter()
        self.description = self.wTree.get_widget('textviewDescription').get_buffer().get_text(startIter,endIter)
        icon = self.wTree.get_widget('entryIcon').get_text()
        self.iconPath += os.path.basename(icon)            
        shutil.copy(icon, os.path.join(self.rootDir,'icons'))
        return (True,)
            
    
    def export(self):
        result = self.loadFormular()
        if not result[0]:
            return result
        root = etree.Element("AddOn")
        root.attrib['xmlns']='http://umlfri.org/xmlschema/addon.xsd'
        
        identity = etree.Element('Identity')
        identity.attrib['uri'] = self.identityUri
        root.append(identity)
        
        friendlyName = etree.Element('FriendlyName')
        friendlyName.attrib['name'] = self.friendlyName
        friendlyName.attrib['version'] = self.friendlyNameVersion
        root.append(friendlyName)
        
        author = etree.Element('Author')
        name = etree.Element('Name')
        name.attrib['name'] = self.authorName
        author.append(name)
        homepage = etree.Element('Homepage')
        homepage.attrib['url'] = self.authorHomepageUrl
        author.append(homepage)
        commonLicense = etree.Element('CommonLicense')
        commonLicense.attrib['name'] = self.authorCommonLicenseName
        author.append(commonLicense)
        root.append(author)
        
        icon = etree.Element('Icon')
        icon.attrib['path'] = self.iconPath
        root.append(icon)
        
        description = etree.Element('Description')
        description.text = unicode('\n'+self.description+'\n    ')
        root.append(description)

        metamodel = etree.Element('Metamodel')
        path = etree.Element('Path')
        path.attrib['path'] = self.metamodelPath
        metamodel.append(path)
        template = etree.Element('Template')
        template.attrib['path'] = self.metamodelTemplatePath
        template.attrib['name'] = self.friendlyName
        metamodel.append(template)
        root.append(metamodel)
        
        addonxml = open(os.path.join(self.rootDir,'addon.xml'), 'w')
        addonxml.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        addonxml.close()
        return (True, '', self.identityUri, self.friendlyNameVersion)
        
