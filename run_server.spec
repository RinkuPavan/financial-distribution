# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

project_root = os.path.abspath('.')          # financial-distribution/
backend_dir  = os.path.join(project_root, 'backend')  # financial-distribution/backend/

a = Analysis(
    ['backend/run_server_exe.py'],
    pathex=[
        project_root,
        backend_dir,
    ],
    binaries=[],
    datas=[
        # Include everything inside backend/ so modules are found at runtime
        ('backend/*.py', 'backend'),
    ],
    hiddenimports=[
        # Your app modules (short names — backend/ is already in pathex)
        'main',
        'services',
        'services.distribution',
        'schemas',
        'tally_schemas',
        # FastAPI + Uvicorn internals that PyInstaller misses
        'fastapi',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='run_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='backend/icon.ico' if os.path.exists('backend/icon.ico') else None,
)