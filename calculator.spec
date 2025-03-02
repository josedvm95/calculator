import shutil
from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['calculator.py'],
    pathex=['C:\\Users\\Jose\\PycharmProjects\\calculator'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

a.datas += [('calculator.kv', 'C:\\Users\\Jose\\PycharmProjects\\calculator\\calculator.kv', 'DATA')]
a.datas += [('config.ini', 'C:\\Users\\Jose\\PycharmProjects\\calculator\\config.ini', 'DATA')]

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    Tree('C:\\Users\\Jose\\PycharmProjects\\calculator\\'),
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='calculator',
)

shutil.copyfile('config.ini', '{0}/calculator/config.ini'.format(DISTPATH))
shutil.copyfile('calculator.kv', '{0}/calculator/calculator.kv'.format(DISTPATH))
shutil.copyfile('calculator.png', '{0}/calculator/calculator.png'.format(DISTPATH))
