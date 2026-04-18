financial-distribution/
├── run_server.spec          ← spec file goes here
├── backend/
│   ├── main.py
│   ├── run_server.py
│   ├── run_server_exe.py    ← new entry point goes here
│   ├── services/
│   │   └── distribution.py
│   ├── schemas.py
│   └── tally_schemas.py
└── tally-plugin/
    └── financial_distribution.tdl