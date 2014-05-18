import os
import re
import sys
import platform
import inspect
import nuke
import string


DEBUG = False

def camel(value, delimiter=' '):
  def camelCase():
    yield str.lower
    while True:
      yield str.capitalize
  c = camelCase()
  return "".join(c.next()(x) if x else delimiter for x in value.split(delimiter))


def unCamel(value, delimiter='_', lowercase=True, capitals=False):
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1%s\2'%delimiter, value)
  s2 = re.sub('([a-z0-9])([A-Z])', r'\1%s\2'%delimiter, s1)
  if lowercase is True:
    s2=s2.lower()
  elif capitals is True:
    s2=string.capwords(s2)
  return s2


class GizmoPathManager(object):

  def __init__(self, exclude=r'^(\.|icons|.*\.bak|readme\.txt)', searchPaths=None):
    '''Used to add folders within the gizmo folder(s) to the gizmo path
    exclude: a regular expression for folders / gizmos which should NOT be
    added; by default, excludes files / folders that begin with a "."
    searchPaths: a list of paths to recursively search; if not given, it
    will use the NUKE_GIZMO_PATH environment variable; if that is
    not defined, it will use the directory in which this file resides;
    and if it cannot detect that, it will use the pluginPath
    '''
    #if isinstance(exclude, basestring):
    exclude = re.compile(exclude)
    self.exclude = exclude
    if searchPaths is None:
      searchPaths = os.environ.get('NUKE_GIZMO_PATH', '').split(os.pathsep)
      if not searchPaths:
        import inspect
        this_file = inspect.getsourcefile(lambda: None)
        if this_file:
          searchPaths = [os.path.dirname(os.path.abspath(this_file))]
        else:
          searchPaths = list(nuke.pluginPath())
    self.searchPaths = searchPaths
    self.reset()

  @classmethod
  def canonicalPath(cls, path):
    # fixes path names and resolution
    return os.path.normcase(os.path.normpath((os.path.abspath(path))))
    # return os.path.normcase(os.path.normpath(os.path.realpath(os.path.abspath(path))))

  def reset(self):
    # reset the _crawlData dict
    self._crawlData = {}

  def addGizmoPaths(self):
    '''
    Recursively search searchPaths for folders to add to the nuke
    pluginPath.
    '''
    self.reset()
    self._visited = set()
    for gizmoPath in self.searchPaths:
      self._recursiveAddGizmoPaths(gizmoPath, self._crawlData, foldersOnly=False)

  def _recursiveAddGizmoPaths(self, folder, crawlData, foldersOnly=False):
    # If we're in GUI mode, also store away data in _crawlData to to be used
    # later by addGizmoMenuItems
    if not os.path.isdir(folder):
      return

    if nuke.GUI:
      if 'files' not in crawlData:
        crawlData['gizmos'] = {}
      if 'dirs' not in crawlData:
        crawlData['dirs'] = {}

    # avoid an infinite loop due to symlinks...
    canonicalPath = self.canonicalPath(folder)
    if canonicalPath in self._visited:
      return
    self._visited.add(canonicalPath)

    for subItem in sorted(os.listdir(canonicalPath)):
      if self.exclude and self.exclude.search(subItem):
        continue
      subPath = os.path.join(canonicalPath, subItem)
      if os.path.isdir(subPath):
        nuke.pluginAppendPath(subPath)
        nuke.pluginAppendPath(os.path.join(subPath,'icons'))
        if DEBUG:
          nuke.tprint('GIZMO PATH: %s' % subPath)
        subData = {}
        if nuke.GUI:
          crawlData['dirs'][subItem] = subData
        self._recursiveAddGizmoPaths(subPath, subData)
      elif nuke.GUI and (not foldersOnly) and os.path.isfile(subPath):
        name, ext = os.path.splitext(subItem)
        if ext == '.gizmo':
          if re.match('[0-9]{3}', name[-3:]):
            gizmoName = name[:-4]
            version = name[-3:]
          else:
            gizmoName = name
            version = '000'
          crawlData['gizmos'][gizmoName]=[]
          crawlData['gizmos'][gizmoName].append(int(version))
          if DEBUG:
            nuke.tprint('GIZMO NAME: %s' % name)
            nuke.tprint('GIZMO VERS: %s' % version )


  def addGizmoMenuItems(self, toolbar=None, default_top_menu=None):
    '''
    Recursively create menu items for gizmos found on the searchPaths.
    Only call this if youre in nuke GUI mode! (ie, from inside menu.py)
    toolbar - the toolbar to which to add the menus; defaults to "Nodes"
    default_top_menu - if you do not wish to create new "top level" menu items,
    then top-level directories for which there is not already a top-level
    menu will be added to this menu instead (which must already exist)
    '''
    if not self._crawlData:
      self.addGizmoPaths()
    if toolbar is None:
      toolbar = nuke.menu("Nodes")
    elif isinstance(toolbar, basestring):
      toolbar = nuke.menu(toolbar)
    #toolbar.addCommand("-", "", "")
    self._recursiveAddGizmoMenuItems(toolbar, self._crawlData, defaultSubMenu=default_top_menu, topLevel=True)


  def _recursiveAddGizmoMenuItems(self, toolbar, crawlData, defaultSubMenu=None, topLevel=False):
    for name, versions in crawlData['gizmos'].items():
      niceName = name
      filename = "%s_%03d" % (name, max(versions))
      niceName = name.replace('_',' ')
      niceName = unCamel(niceName,' ',False,True)
      if DEBUG:
        nuke.tprint('GIZMO NAME: %s' % name)
        nuke.tprint('GIZMO VERS: %s' % ('%03d' % max(versions)) )
        nuke.tprint('GIZMO NICENAME: %s' % niceName)
      toolbar.addCommand(niceName,"nuke.createNode('%s')" % filename, '%s.png' % name )

    for folder, data in crawlData.get('dirs', {}).iteritems():
      import sys
      subMenu = toolbar.findItem(folder)
      if subMenu is None:
        if defaultSubMenu:
          subMenu = toolbar.findItem(defaultSubMenu)
          subMenu.addCommand("-", "", "")
        else:
          subMenu = toolbar.addMenu(folder, "%s.png" % folder)
      subMenu.addCommand("-", "", "")
      self._recursiveAddGizmoMenuItems(subMenu, data)



