"""
@Author  : likianta <likianta@foxmail.com>
@Module  : launcher.py
@Created : 2020-08-30
@Updated : 2020-12-03
@Version : 0.2.15
@Desc    :
"""
from os import path
from PySide2.QtCore import QObject
from PySide2.QtQml import QQmlApplicationEngine, QQmlContext
from PySide2.QtWidgets import QApplication


class Application(QApplication):
    """
    Attributes:
        engine (QQmlApplicationEngine)
        root (QQmlContext)
        _entrance (str): see `__init__`
        __holder (dict): __holder 只是为了在整个生命周期中持续持有实例, 以防止
            Python 垃圾回收机制误杀注入到 QML 全局变量的对象, 本身没有其他用处.
    """
    
    def __init__(self, theme_dir='', **kwargs):
        """
        Args:
            theme_dir: 要引入外部自定义 QML 模块, 则填写该模块的父目录路径. 例如:
                    |- my_prj
                        |- main.py
                    |- my_theme
                        |- MyComponentLib
                            |- MyComponentA.qml
                            |- MyComponentB.qml
                            |- MyComponentC.qml
                            |- qmldir  # The folder must include a 'qmldir' file
                我们要在 my_prj 中引入 my_theme 项目下的 MyComponentLib 组件库,
                那么 theme_dir 参数填:
                    theme_dir = '~/my_theme' (`~` 指你的绝对路径的目录)
                
        Keyword Args:
            organization (str): default 'dev.likianta.lk_qtquick_scaffold'. 该键
                是为了避免在 QML 中使用 QtQuick.Dialogs.FileDialog 时, 出现警告
                信息:
                    QML Settings: The following application identifiers have not
                    been set: QVector("organizationName", "organizationDomain")
        """
        super().__init__()

        self.engine = QQmlApplicationEngine()
        self.root = self.engine.rootContext()
        self.__holder = {}

        # Set font to Microsoft Yahei if platform is Windows
        from platform import system
        if system() == 'Windows':
            from PySide2.QtGui import QFont
            self.setFont(QFont('Microsoft YaHei'))
            
        # Set organization name to avoid warning info if we use QtQuick.Dialogs.
        # FileDialog component
        self.setOrganizationName(kwargs.get(
            'organization', 'dev.likianta.lk_qtquick_scaffold'
        ))
        
        # Register custom qml component library (folder's absolute paths)
        # See `self.add_import_path` for detailed info.
        self.curr_dir = path.dirname(__file__)  # -> '~/lk_qtquick_scaffold'
        self.add_import_path(theme_dir or f'{self.curr_dir}/theme')
        #   TODO: test whether '/theme/LightClean' worked as '/theme'
        self.add_import_path(path.abspath(f'{self.curr_dir}/debugger'))
        self.add_import_path(path.abspath(f'{self.curr_dir}/qml_helper'))
        ''' Now you can use the following modules in Qml:
            
            import LKDebugger 1.0  // from '~/lk_qtquick_scaffold/debugger'
            import LKHelper 1.0    // from '~/lk_qtquick_scaffold/qml_helper'
            
            import LightClean 1.0  // from '~/lk_qtquick_scaffold/theme' (if you
                                   // didn't pass `theme_dir` your custom one,
                                   // the built-in themes will be all available)
            // PS: For now (2020-12) there is only one built-in theme provided.
        '''
        
    def add_import_path(self, qmldir: str):
        """
        Args:
            qmldir: The absolute path of directory, this dir should contain at
                least one component library folder (the folder's first letter
                shoule be capitalized), the the library folder should contain a
                'qmldir' file (no suffix).
                For example:
                    qmldir = '~/lk_qtquick_scaffold/theme'
                    # lk_qtquick_scaffold
                    # |- theme (folder)  # <- we import this one's absolute path
                    #    |- LightClean (folder)
                    #       |- qmldir (file)
        """
        self.engine.addImportPath(qmldir)
        
    def register_pyobj(self, obj: QObject, name=''):
        """ 将 Python 中定义好的 (继承自 QObject 的) 对象作为全局变量加载到 QML
            的上下文当中.
            
        Args:
            obj: A Python class instance inherits QObject
            name: Object name, 建议使用大驼峰式命名, 并建议以 "Py" 开头.
                Examples: "PyHandler", "PyHook"
            
        Notes:
            1. 在调用 self.start() 前使用本方法
            2. 这些对象可以在 QML 布局中全局使用
        """
        name = name or obj.__class__.__name__
        self.root.setContextProperty(name, obj)
        # 令 self.__holder 持有该实例, 避免 Python 误将 handler 引用计数归零.
        self.__holder[name] = obj
    
    def start(self, qmlfile: str):
        """
        Args:
            qmlfile: 启动时要载入的 .qml 文件. 通常为 '{somedir}/main.qml' 或
                '{somedir}/view.qml'.
        """
        self.engine.load(qmlfile)
        self.exec_()
        #   Note: 不要用 sys.exit(self.exec_()), 这会导致 pycomm.PyHandler 先一
        #   步被释放, 导致 QML 在结束时刻误触 PyHandler.call 时会报出 'cannot
        #   call from null' 的错误.
    
    # open = run = launch = start
    #   https://ux.stackexchange.com/questions/106001/do-we-open-or-launch-or
    #   -startapps+&cd=1&hl=zh-CN&ct=clnk&gl=sg


if __name__ == '__main__':
    _app = Application('./theme')
    _app.start('../tests/Demo/LightCleanDemo.qml')
