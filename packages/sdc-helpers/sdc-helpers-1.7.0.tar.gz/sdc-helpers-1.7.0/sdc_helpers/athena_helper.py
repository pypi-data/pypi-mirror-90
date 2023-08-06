"""
   SDC Athena helper module
"""
import time
import boto3
from sdc_helpers import utils


def query(
        *,
        query_source: str,
        query_string: str,
        query_bucket: str = 'sdc-athena-queries',
        poll_count: int = 60,
        interval: float = 0.5
) -> list :
    """
        Run an Athena query and transform response into list of dictionaries
        Each dictionary is essentially a row of data

        args:
            query_source (str): Source folder in S3 bucket to store response data
            query_string (str): Athena Presto SQL query string
            query_bucket (str): S3 bucket results will be stored in
                                (Default - sdc-athena-queries)
            poll_count (int): The amount of times the function should check for query completion
                              (Default - 60)
            interval (float): The interval in seconds between polls (Default - 0.5)

        return:
            data (list) : A list of dictionary objects (rows of data)
    """
    client = boto3.client('athena')
    # pylint: disable=invalid-name,too-many-nested-blocks
    s3_location = "s3://{query_bucket}/{query_source}/".format(
        query_bucket=query_bucket,
        query_source=query_source
    )

    response = client.start_query_execution(
        QueryString=query_string,
        ResultConfiguration={
            'OutputLocation': s3_location,
        },
    )

    query_execution_id = response['QueryExecutionId']

    # we need to now poll the api for when the query has completed
    while poll_count > 0:
        response = client.get_query_execution(
            QueryExecutionId=query_execution_id
        )

        if response['QueryExecution']['Status']['State'] == 'FAILED':
            raise Exception(
                'Athena query failed with error: {error}'.format(
                    error=response['QueryExecution']['Status']
                )
            )

        if response['QueryExecution']['Status']['State'] \
                not in ['QUEUED', 'RUNNING']:
            next_token = None
            data = []

            while True:
                if next_token is not None:
                    response = client.get_query_results(
                        QueryExecutionId=query_execution_id,
                        NextToken=next_token
                    )
                else:
                    response = client.get_query_results(
                        QueryExecutionId=query_execution_id
                    )

                rows = utils.dict_query(dictionary=response, path='ResultSet.Rows')

                columns = [column.get('VarCharValue') for column in rows[0].get('Data')]

                count = 0
                for row in rows:
                    if count > 0:
                        item = {}
                        value_index = 0
                        for value in row.get('Data'):
                            item[columns[value_index]] = value.get('VarCharValue')
                            value_index += 1

                        data.append(item)

                    count += 1

                next_token = response.get('NextToken')
                if next_token is None:
                    break

            return data

        poll_count -= 1
        time.sleep(interval)

    raise Exception('Athena query took too long')
