![app_catalogue_Diagram](https://github.com/kaust-rccl/ksl-apps-catalogue/assets/141279506/9d8d966f-cea7-4321-adef-e11f5fe7a3b0)

# Application JSON File Generation Workflow

There are two main scripts to generate JSON files for the installed applications:

- **populate_json_all**: A script that is used only once to populate JSON files for pre-installed applications. The downside of using this script is that you have to insert the category of each application manually.
- **populate_json**: A script that is used inside the application directory to generate its JSON file. You have to pick its category while executing the script.

Each JSON file has the following properties:
- System name/build
- Application name/version
- Compiler version
- Classification
- Description (optional)

## Workflow Steps

The workflow for generating and updating the application JSON files is as follows:

1. On Ibex/Shaheen/Neser:
   - The user runs the "populate_json" script inside the installation directory of the newly installed application (if any).
   - A nightly cron-job runs daily on the login node of Ibex/Shaheen to copy all the JSON files to the host machine of the HPC wiki.

2. On the host machine of HPC wiki:
   - A pipeline executes the "ingest_db.py" script to feed a database from the JSON files that were copied from the clusters, pushing the new database to
     the "ksl-apps-catalogue" repository.
   - Reviewers are notified when a new push is committed to the "dev" branch. One of them has to pull it for review.

3. Review Process:
   - After reviewing the new database, the reviewer has to make a PR to merge it with the "main" branch.

4. Final Steps:
   - After the merge, a pipeline is triggered, running the "populate_apps_table.py" script to populate the catalog tables.
   - The tables are then pushed to the "ksl-docs" repository.

This workflow ensures the generation and maintenance of up-to-date application JSON files.

