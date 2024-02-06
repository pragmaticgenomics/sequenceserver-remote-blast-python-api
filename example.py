from sequenceserver.sequenceserver_api import SequenceServerApi
import os

# Example usage
if __name__ == "__main__":
    # To get your own instance, register at https://sequenceserver.com/cloud/
    base_url = os.environ.get("SEQUENCESERVER_INSTANCE_URL", "https://YOURINSTANCE.sequenceserver.com")
    api_token = os.environ.get("SEQUENCESERVER_API_TOKEN", "REDACTED_OBTAIN_FROM_SUPPORT==")

    sequence_server = SequenceServerApi(base_url, api_token=api_token)

    print(f"****************************************")
    print(f"Getting configuration for {base_url}")
    print(f"****************************************")
    print(sequence_server.get_configuration())

    print(f"****************************************")
    print(f"Getting a list of databases available to {base_url}")
    print(f"****************************************")
    print(sequence_server.get_databases())

    print(f"****************************************")
    print(f"Getting a list of databases with all attributes available to {base_url}")
    print(f"****************************************")
    print(sequence_server.get_databases(full_response=True))

    # Selecting all nucleotide databases
    databases = [db["id"] for db in sequence_server.get_databases() if db["type"] == "nucleotide"]

    blast_search_type = "tblastn"
    query_seq = "QRPSEEKDRKERRRAQRCAGRRAAYRKGCEKAGKLRRKGVARASREGLKISDATAALDLR\nAQTQAQPDFGQLDHQQPQHHHQQQQPPQQQQQQPPPPQQQQQPQHPQQQHNQNPESRPHH\nHLPQQHHHQHHPGNHLHSGDSGGGIGGGGGGGGGGGGGGGGGGGGGGGGGSAGGVAVVAG"

    advanced_opts = "-evalue 1.0e-8"

    job_id = sequence_server.submit_blast_job(blast_search_type, query_seq, databases, advanced_opts)
    print(f"Job id: {job_id}")

    response = sequence_server.poll_job(job_id)
    print(f"Job: {response}")

    # Available formats: "xml", "std_tsv", "full_tsv"
    print(sequence_server.get_job_result(job_id, "xml"))
else:
    print("This module is not meant to be imported. Run it directly instead '>python example.py'")