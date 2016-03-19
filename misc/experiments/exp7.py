from kafka import KafkaConsumer

# To consume messages
consumer = KafkaConsumer('allCronusMetrics',
                         group_id='test',
                         bootstrap_servers=['slc5b01c-d341.stratus.slc.ebay.com:9092'])
for message in consumer:
    # message value is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))