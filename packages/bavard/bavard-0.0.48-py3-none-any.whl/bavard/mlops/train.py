"""Script to be called by the pipeline training docker container. Trains a pipeline instance.
"""
import argparse
import logging

import tensorflow as tf
from bavard.mlops.pipeline import ChatbotPipeline
from bavard.mlops.pub_sub import PubSub
from bavard.mlops.gcs import download_agent_data
from bavard.dialogue_policy.data.agent import Agent

logging.getLogger().setLevel(logging.DEBUG)


def get_args():
    """Argument parser.

    Returns:
      Dictionary of arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--gcp-project-id',
        type=str,
        required=True)
    parser.add_argument(
        '--agent-uname',
        type=str,
        required=True)
    parser.add_argument(
        '--job-dir',
        type=str,
        required=True,
        help='local or GCS location for writing checkpoints and exporting models')
    parser.add_argument(
        '--bucket-name',
        type=str,
        required=True)
    parser.add_argument(
        '--export-key',
        type=str,
        required=True)
    parser.add_argument(
        '--publish-id',
        type=int,
        required=False)
    parser.add_argument(
        '--verbosity',
        choices=['DEBUG', 'ERROR', 'FATAL', 'INFO', 'WARN'],
        default='INFO')
    parser.add_argument(
        '--auto',
        choices=['True', 'False'],
        default='True',
        help='whether to automatically determine the training set up for the ML model')
    args, _ = parser.parse_known_args()
    return args


def train_and_evaluate(args):
    """Trains and evaluates the Keras model.

    Trains and serializes an `MLModel` instance to the path defined in part
    by the --job-dir argument.

    Args:
      args: dictionary of arguments - see get_args() for details
    """

    agent_filename = download_agent_data(
        bucket_name=args.bucket_name, export_file_key=args.export_key)

    agent = Agent.parse_file(agent_filename)

    model = ChatbotPipeline(
        {"nlu": {"auto": args.auto == 'True'}}
    )
    model.fit(agent)
    model.to_dir(args.job_dir)

    # publish job complete message
    pubsub_msg = {
        'EVENT_TYPE': 'ML_TRAINING_JOB_COMPLETE',
        'SAVED_MODEL_DIR': args.job_dir,
        'AGENT_UNAME': args.agent_uname
    }
    if args.publish_id is not None:
        pubsub_msg['PUBLISH_ID'] = args.publish_id

    print('Publishing message to topic chatbot-service-training-jobs:', str(pubsub_msg))
    PubSub(args.gcp_project_id).publish('chatbot-service-training-jobs', pubsub_msg)
    print('Published JOB_COMPLETE message')


if __name__ == '__main__':
    args = get_args()

    try:
        tf.compat.v1.logging.set_verbosity(args.verbosity)
        train_and_evaluate(args)
    except Exception as e:
        # publish job failed message
        data = {
            'EVENT_TYPE': 'ML_TRAINING_JOB_FAILED',
            'AGENT_UNAME': args.agent_uname
        }
        if args.publish_id is not None:
            data['PUBLISH_ID'] = args.publish_id

        print('Publishing message to topic chatbot-service-training-jobs:', str(data))
        PubSub(args.gcp_project_id).publish('chatbot-service-training-jobs', data)
        print('Published ML_TRAINING_JOB_FAILED message')
        raise e
