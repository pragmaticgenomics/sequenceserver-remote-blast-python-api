# Remote BLAST api for SequenceServer Cloud

[SequenceServer Cloud](https://sequenceserver.com/cloud) provides dedicated secure servers to BLAST your data and visualize results.
This repository provides a lightweight Python API wrapper to SequenceServer Cloud users to execute BLAST queries against DBs on their SequenceServer Cloud instance.

## Usage

Sequence Server Cloud provides an API for remote BLASTing. You can [read API docs](https://sequenceserver.com/doc/api/) to familiarize yourself with it.
You can check out the example use-cases bellow to get started.

### Running an example scenario

Running examples requires to have a SequenceServer Cloud account.
[Register for yours](https://sequenceserver.com/cloud) if you don't have one.

Your instance also requires API enabled. Please contact [SequenceServer Cloud support](https://sequenceserver.com/support) to enable it and obtain an API token.

You can see the source code of the examples in the `example.py` file in this repo.

```
# Clone this repository
git clone git@github.com:pragmaticgenomics/sequenceserver-remote-blast-python-api.git

# change the working directory
cd sequenceserver-remote-blast-python-api

# install dependencies
pip install requests

# configure your environment
export SEQUENCESERVER_INSTANCE_URL="https://YOURINSTANCE.sequenceserver.com"
export SEQUENCESERVER_API_TOKEN="YOUR_SECRET_TOKEN"

# run the examples
python example.py
```

### Using from your own Python codebase

You can copy the code in `sequenceserver/sequenceserver_api.py` to the same directory in your project, or add this repo as a git submodule. Then you can import it and use it in your code:

```python
# assuming the file is in `<project_root>/sequenceserver/sequenceserver_api.py`
from sequenceserver.sequenceserver_api import SequenceServerApi
import os

base_url = os.environ.get("SEQUENCESERVER_INSTANCE_URL", "https://YOURINSTANCE.sequenceserver.com")
api_token = os.environ.get("SEQUENCESERVER_API_TOKEN", "REDACTED_OBTAIN_FROM_SUPPORT==")

sequence_server = SequenceServerApi(base_url, api_token=api_token)

# Get instance configuration
print(sequence_server.get_configuration())

# Get databases with the basic set of attributes
print(sequence_server.get_databases())

# Get databases with a full set of attributes
print(sequence_server.get_databases(full_response=True))

# Select databases to query e.g. here we're selecting all nucleotide databases
databases = [db["id"] for db in sequence_server.get_databases() if db["type"] == "nucleotide"]

blast_search_type = "tblastn"
query_seq = "QRPSEEKDRKERRRAQRCAGRRAAYRKGCEKAGKLRRKGVARASREGLKISDATAALDLR\nAQTQAQPDFGQLDHQQPQHHHQQQQPPQQQQQQPPPPQQQQQPQHPQQQHNQNPESRPHH\nHLPQQHHHQHHPGNHLHSGDSGGGIGGGGGGGGGGGGGGGGGGGGGGGGGSAGGVAVVAG"

advanced_opts = "-evalue 1.0e-8"

# Submit a BLAST job and get its ID back
job_id = sequence_server.submit_blast_job(blast_search_type, query_seq, databases, advanced_opts)

# Poll for a response, jobs can take a while depending on the DB size and query complexity
response = sequence_server.poll_job(job_id)

# Get the results of the job in selected format
# Available formats: "xml", "std_tsv", "full_tsv"
print(sequence_server.get_job_result(job_id, "xml"))
```

## Help

Open a new GitHub issue if you have any questions about using SequenceServer Cloud specifically from Python.

For any other questions, to inquire about API capabilities or if you need any help enabling API on your instance, please contact [SequenceServer Cloud support](https://sequenceserver.com/support)