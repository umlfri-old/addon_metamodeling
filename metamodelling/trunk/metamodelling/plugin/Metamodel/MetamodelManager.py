'''
Created on 21.3.2010

@author: Michal Kovacik
'''
import os
from __init__ import * 
from ObjectVisualGenerator import ObjectVisualGenerator
from RelationshipVisualGenerator import RelationshipVisualGenerator
from ComplementaryGenerator import ComplementaryGenerator

VISUAL_IDENTITY = "visual_identity"
OBJECT_IDENTITY = "object_name"
RELATIONSHIP_IDENTITY = "relationship_name"
REF_OBJECT_NAME = "ref_object_name"
REF_RELATIONSHIP_NAME = "ref_relationship_name"

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
 
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
 
        return cls.instance

class MetamodelManager(object):
    '''
    Class, which controls all the logic of a visual representation of both objects and relationships
    '''
    __metaclass__ = Singleton
    def __init__(self):
        self.metamodels = dict()
        self.metamodelsRel = dict()
        
    def ShowEditWindow(self,selected,project): 
        '''
        from this method is EditWindow showed.
        '''   
        if (self.metamodels.has_key(selected.GetObject().GetValue(VISUAL_IDENTITY))or
        self.metamodelsRel.has_key(selected.GetObject().GetValue(VISUAL_IDENTITY))):
            if selected.GetObject().GetType()=='Object':
                EditWindow(self,selected,project,'Object',treestore = self.metamodels.get(selected.GetObject().GetValue(VISUAL_IDENTITY)))
            elif selected.GetObject().GetType()=='Relationship':
                EditWindow(self,selected,project,'Relationship',treestore = self.metamodelsRel.get(selected.GetObject().GetValue(VISUAL_IDENTITY))) 
            elif selected.GetObject().GetType()=='ObjectStakeholder':
                EditWindow(self,self.__GetRelatedElement(project, selected),project,'Object',treestore = self.metamodels.get(selected.GetObject().GetValue(VISUAL_IDENTITY)),visual_identity = selected.GetObject().GetValue(VISUAL_IDENTITY)) 
            elif selected.GetObject().GetType()=='RelationshipStakeholder':
                EditWindow(self,self.__GetRelatedElement(project, selected),project,'Relationship',treestore = self.metamodelsRel.get(selected.GetObject().GetValue(VISUAL_IDENTITY)),visual_identity = selected.GetObject().GetValue(VISUAL_IDENTITY))       
          
        else: 
            if selected.GetObject().GetType()=='Object':
                EditWindow(self,selected,project,'Object')
            elif selected.GetObject().GetType()=='Relationship':
                EditWindow(self,selected,project,'Relationship')
            elif selected.GetObject().GetType()=='ObjectStakeholder':
                EditWindow(self,self.__GetRelatedElement(project, selected),project,'Object',visual_identity = selected.GetObject().GetValue(VISUAL_IDENTITY))    
            elif selected.GetObject().GetType()=='RelationshipStakeholder':
                EditWindow(self,self.__GetRelatedElement(project, selected),project,'Relationship',visual_identity = selected.GetObject().GetValue(VISUAL_IDENTITY))        
    
    def GenerateMetamodels(self,project,projectname,zipfile=None):
        '''
        method used to generate metamodels and complementary stuff
        '''
        ComplementaryGenerator.CopyDummyProjectIcon(projectname,zipfile)
        elementDomainMap = self.__GetUniqueElements(project)
        for el in self.metamodels.keys():
            domainname = elementDomainMap.get(el).GetValue(OBJECT_IDENTITY)
            relationships = self.__GetRelationshipsForElement(project, el)
            print el
            print relationships
            ObjectVisualGenerator.GenerateObject(projectname,el,self.metamodels.get(el),domainname,relationships,zipfile)
            ComplementaryGenerator.CopyDummyObjectIcon(projectname,el,zipfile)
        relationshipDomainMap = self.__GetUniqueRelationships(project)
        for conn in self.metamodelsRel.keys():
            domainname = relationshipDomainMap.get(conn).GetValue(RELATIONSHIP_IDENTITY)
            RelationshipVisualGenerator.GenerateRelationship(projectname,conn,self.metamodelsRel.get(conn),domainname,zipfile)
            ComplementaryGenerator.CopyDummyRelationshipIcon(projectname,conn,zipfile)
        #in this phase we will also generate the rest...
        graphs=list()
        for gr in project.GetRoot().GetDiagrams():
            graphs.append(gr.GetName())
        ComplementaryGenerator.CopyDummyGraphIcon(projectname,graphs,zipfile)    
        ComplementaryGenerator.GenerateMetamodelFile(projectname,graphs,zipfile)
        ComplementaryGenerator.CopyPaths(projectname,zipfile)
        ComplementaryGenerator.CopySampleDomain(projectname,zipfile)
        ComplementaryGenerator.GenerateTemplate(projectname,zipfile)
        ComplementaryGenerator.GenerateAddon(projectname,zipfile)
        ComplementaryGenerator.CopyPackageItems(projectname,zipfile)
        
    def __GetDomainForElement(self,project,visual_id):
        '''
        for Object or ObjectRelationship returns domain(data) on which the visual_id points
        '''
        if (project is not None):
            for diag in project.GetRoot().GetDiagrams():
                diagelements = diag.GetElements()
                for i in range(0,len(diagelements)):
                    elobj = diagelements[i].GetObject()
                    if ((elobj.GetType()=='Object') and (elobj.GetValue(VISUAL_IDENTITY)==visual_id)):
                        return elobj.GetValue(OBJECT_IDENTITY)
           
    def __GetRelationshipsForElement(self,project,visual_id):
        '''
        returns set of relationship connected with element
        '''
        relationships = dict()
        if (project is not None):
            for diag in project.GetRoot().GetDiagrams():
                diagconnections = diag.GetConnections()
                for i in range(0,len(diagconnections)):
                    conn = diagconnections[i]
                    if (((conn.GetObject().GetType()=='Relationship')or
                         (conn.GetObject().GetType()=='RelationshipStakeholder'))and
                        (
                        (((conn.GetSourceObject().GetType()=='Object')or
                         (conn.GetSourceObject().GetType()=='ObjectStakeholder')) and
                        (conn.GetSourceObject().GetValue(VISUAL_IDENTITY)==visual_id))
                        or
                        (((conn.GetDestinationObject().GetType()=='Object')or
                         (conn.GetDestinationObject().GetType()=='ObjectStakeholder')) and
                        (conn.GetDestinationObject().GetValue(VISUAL_IDENTITY)==visual_id))
                        )
                        ):
                        relationships[conn.GetObject().GetValue(VISUAL_IDENTITY)]=''         
        
        return relationships.keys()
    
    def __GetRelatedElement(self,project,selected):
        '''
        for stakeholder types gets the element with a data on which stakeholder points
        '''
        if selected.GetObject().GetType()=='ObjectStakeholder':
            if (project is not None):
                for diag in project.GetRoot().GetDiagrams():
                    diagelements = diag.GetElements()
                    for i in range(0,len(diagelements)):
                        el=diagelements[i]
                        if ((el.GetObject().GetType()=='Object')and(el.GetObject().GetValue(OBJECT_IDENTITY)==selected.GetObject().GetValue(REF_OBJECT_NAME))):
                            return el
                        
                    
        elif selected.GetObject().GetType()=='RelationshipStakeholder':
            if (project is not None):
                for diag in project.GetRoot().GetDiagrams():
                    diagconnections = diag.GetConnections()
                    for i in range(0,len(diagconnections)):
                        conn=diagconnections[i]
                        if ((conn.GetObject().GetType()=='Relationship')and(conn.GetObject().GetValue(RELATIONSHIP_IDENTITY)==selected.GetObject().GetValue(REF_RELATIONSHIP_NAME))):
                            print 'match'
                            return conn
        print 'non match'
        return None
    
    def __GetUniqueElements(self,project):
        '''
        returns dict of visual_identity:domain_object
        '''
        elements = dict()
        if (project is not None):
            for diag in project.GetRoot().GetDiagrams():
                diagelements = diag.GetElements()
                for i in range(0,len(diagelements)):
                    el=diagelements[i]
                    if ((el.GetObject().GetType()=='Object') and (not elements.has_key(el.GetObject().GetValue(VISUAL_IDENTITY)))):
                        elements[el.GetObject().GetValue(VISUAL_IDENTITY)]=el.GetObject()
                    elif ((el.GetObject().GetType()=='ObjectStakeholder')):
                        el1 = self.__GetRelatedElement(project, el)
                        if (not elements.has_key(el.GetObject().GetValue(VISUAL_IDENTITY))):
                            elements[el.GetObject().GetValue(VISUAL_IDENTITY)]=el1.GetObject()
        return elements
    
    def __GetUniqueRelationships(self,project):
        '''
        returns dict of visual_identity:domain_object
        '''
        relationships = dict()
        if (project is not None):
            for diag in project.GetRoot().GetDiagrams():
                diagrelationships = diag.GetConnections()
                for i in range(0,len(diagrelationships)):
                    diag=diagrelationships[i]
                    if ((diag.GetObject().GetType()=='Relationship') and (not relationships.has_key(diag.GetObject().GetValue(VISUAL_IDENTITY)))):
                        relationships[diag.GetObject().GetValue(VISUAL_IDENTITY)]=diag.GetObject()
                    elif ((diag.GetObject().GetType()=='RelationshipStakeholder')):
                        diag1 = self.__GetRelatedElement(project, diag)
                        if (not relationships.has_key(diag.GetObject().GetValue(VISUAL_IDENTITY))):
                            relationships[diag.GetObject().GetValue(VISUAL_IDENTITY)]=diag1.GetObject()
        return relationships
        
if __name__ == '__main__':
    a=MetamodelManager()