#!/usr/bin/env python
## utility to write / read messages with pubsub

import argparse
import os

from google.cloud import pubsub_v1 as pubsub


class PubSubClient:
    def __init__(self, gcp_project_id):
        self.gcp_project_id = gcp_project_id
        self.reader = pubsub.SubscriberClient()
        self.writer = pubsub.PublisherClient()

    def write(self, topic, data, time_out=None):
        """ Publishes data to a Pub/Sub topic. """
        topic_path = self.writer.topic_path(self.gcp_project_id, topic)

        payload = data
        if os.path.exists(data):
            with open(data, mode='rb') as inf:
                payload = inf.read()

        try:
            future = self.writer.publish(topic_path, payload)
            message_id = future.result(timeout=time_out)
            print(f"Published data to {topic}: {message_id}")
        except Exception as e:
            print(str(e))


    def _process_message(self, message):
        print(f"Received {message}.")
        message.ack()
        print(f"Acknowledged {message.message_id}.")

    def _check_subscription(self, topic_path, reader_path):
        """Create a new pull subscription on the given topic."""
        response = self.writer.list_topic_subscriptions(request={"topic": topic_path})
        for rdrpath in response:
            if rdrpath == reader_path:
                return

        subscription = self.reader.create_subscription(request={"name": reader_path, "topic": topic_path})
        print('Subscription created: {}'.format(subscription))

    def read(self, topic, subscription_id=None, time_out=None):
        if not subscription_id:
            subscription_id = topic + "-sub"

        topic_path = self.reader.topic_path(self.gcp_project_id, topic)
        reader_path = self.reader.subscription_path(self.gcp_project_id, subscription_id)
        try:
            self._check_subscription(topic_path, reader_path)
            future = self.reader.subscribe(reader_path, callback=self._process_message)
            future.result(timeout=time_out)
        except Exception as e:
            print(str(e))
            future.cancel()
            future.result()  # Block until the shutdown is complete.
        self.reader.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="s|sub|read, or w|write|pub")
    parser.add_argument("--topic", help="Pub/Sub topic ID")
    parser.add_argument("--data", default="data.json", help="Pub data file or payload string")
    parser.add_argument("--timeout", default=None, help="read or write timeout")
    parser.add_argument("--subscription_id", help="Pub/Sub subscription ID. Default to {topic}-sub")
    parser.add_argument("--project_id", help="Google Cloud project ID")

    args = parser.parse_args()
    if not args.project_id:
        args.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("PROJECT"))
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None):
        print("Error! GOOGLE_APPLICATION_CREDENTIALS is expected")
        exit(1)

    client = PubSubClient(args.project_id)
    if args.action in ["s", "sub", "r", "read"]:
        client.read(args.topic, args.subscription_id, int(args.timeout) if args.timeout else None)
    elif args.action in ["w", "write", "p", "pub"]:
        client.write(args.topic, args.data)
