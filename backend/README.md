This is the backend of the application.

This will be implemented using Python (Fastapi).

## Folder Structure
- `models/`: Store trained ML models here.
- `scripts/`: Store scripts for data processing and training.
- `main.py`:
    Basically the entry point for the server.
    It loads the model, connects to the database, and handles the requests.
    Performs prediction on the input data and stores the result in the database.
    Gives response to frontend.

We train the model using tensorflow and then convert it to TFLite for mobile use.

These 3 folders/files are all we need for the backend.