import requests
import json
import time

# Sequence Server Cloud API wrapper.
# This class provides a simple interface to interact with a Sequence Server instance.
# For private instances, an API token is required. This token can be obtained by contacting Sequence Server Cloud team.
class SequenceServerApi:
    def __init__(self, base_url, api_token=None):
        self.base_url = base_url
        self.api_token = api_token

    # Get your instance configuration
    def get_configuration(self):
        api_url = f"{self.base_url}/searchdata.json"
        # Send GET request to the API with HTTP_ACCEPT header set to application/json
        response = requests.get(
            api_url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.api_token}" if self.api_token else None
                }
            )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching search data. Status code: {response.status_code}")

    # Get a list of databases available to your instance
    # Returns a minimalistic list of database attributes by default. This should be sufficient
    # for submitting BLAST jobs. If you need more information about the databases, set full_response to True.
    def get_databases(self, full_response=False):
        search_data = self.get_configuration()

        if full_response:
            return search_data["database"]
        else:
          keys_to_keep = ["title", "type", "id"]

          # Output array with subset of data
          lean_databases = [{key: item[key] for key in keys_to_keep} for item in search_data["database"]]

          return lean_databases


    # Submit a BLAST job to your instance. Returns the job id.
    # For a full list of available blast_algorithms and default advanced_options for each algorithm, check the
    # get_configuration response.
    def submit_blast_job(self, blast_algorithm, query_sequence, blast_databases, advanced_options=None):
        api_url = f"{self.base_url}"
        payload = {
            "method": blast_algorithm,
            "sequence": query_sequence,
            "advanced": advanced_options if advanced_options else None,
        }

        for db in blast_databases:
          payload[f"databases[]"] = db

        response = requests.post(
            api_url,
            data=payload,
            allow_redirects=False,
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.api_token}" if self.api_token else None
                }
        )

        if response.status_code == 303:
            return response.headers["Location"].split("/")[-1]

        else:
            print(f"Error submitting BLAST job. Status code: {response.status_code}. {response.text}")
            print(f"Error submitting BLAST job. Status code: {response.status_code}. {response.json()['more_info']}")

    # Poll a job by its id until it's finished
    def poll_job(self, job_id):
        job_url = f"{self.base_url}/{job_id}.json"
        response = requests.get(
            job_url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.api_token}" if self.api_token else None
                }
            )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 202:
            print(f"Job still running. Polling again in 5 seconds.")
            time.sleep(5)
            return self.poll_job(job_id)
        else:
            print(f"Error polling job. Status code: {response.status_code}. {response.text}")

    # Get the result of a job by its id. Requires the job to be completed first
    def get_job_result(self, job_id, format):
        available_formats = ["xml", "std_tsv", "full_tsv"]
        if format not in available_formats:
            raise ValueError(f"Invalid format. Available formats: {available_formats}")

        job_url = f"{self.base_url}/download/{job_id}.{format}"
        response = requests.get(
            job_url,
            headers={
                "Authorization": f"Basic {self.api_token}" if self.api_token else None
                }
            )
        return response.text


# Example usage
if __name__ == "__main__":
    # To get your own instance, register at https://sequenceserver.com/cloud/
    base_url = "https://YOURINSTANCE.sequenceserver.com"
    sequence_server = SequenceServerApi(base_url, api_token="REDACTED_OBTAIN_FROM_SUPPORT==")

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
