# Project Structure

Here is the basic skeleton for Empatia app repo:

```bash
├── commands                        # contains bash files to run automated processes
├── core                            # main app directory
│   ├── cli                         # contains modules to execute Python commands
│   ├── etl                         # contains modules to define an ETL
│   ├── models                      # contains modules to implement models
│   └── settings                    # contains modules to define all necessary settings
├── data                            # contains data files used in the project
├── notebooks                       # contains experimental files
├── PROJECT_STRUCTURE.md            # overview of the project structure
├── README.md                       # overview of the project
└── .gitignore                      # specifies intentionally untracked files that Git should ignore
```
