"""MQTT Binary sensor entity module."""
import json

from mqtt_hass_base.entity.sensor import MqttSensor


class MqttBinarysensor(MqttSensor):
    """MQTT Binary sensor entity class."""

    _component = "binary_sensor"

    def __init__(
        self,
        name,
        mqtt_root_topic: str,
        logger,
        device_payload,
        subscriptions,
        device_class=None,
        expire_after=0,
        force_update=False,
        off_delay=None,
    ):
        """Create a new MQTT binary sensor entity object."""
        # MqttEntity.__init__(self, name, mqtt_root_topic, logger, device_payload)
        MqttSensor.__init__(
            self,
            name,
            mqtt_root_topic,
            logger,
            device_payload,
            subscriptions,
            device_class,
            expire_after,
            off_delay,
        )
        self._device_class = device_class
        # if device_class not in BINARY_SENSOR_DEVICE_CLASSES:
        #    raise
        self._expire_after = expire_after
        self._force_update = force_update
        self._off_delay = off_delay

    def register(self):
        """Register the current entity to Hass.

        Using the MQTT discovery feature of Home Assistant.
        """
        config_payload = {
            "availability": {
                "payload_available": "online",
                "payload_not_available": "offline",
                "topic": self.availability_topic,
            },
            "device": self.device_payload,
            "expire_after": self._expire_after,
            "force_update": self._force_update,
            "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            "payload_available": "online",
            "payload_not_available": "offline",
            "payload_off": "OFF",
            "payload_on": "ON",
            "qos": 0,
            "state_topic": self.state_topic,
        }
        if self._device_class:
            config_payload["device_class"] = self._device_class
        if self._off_delay:
            config_payload["off_delay"] = self._off_delay
        if self._unique_id:
            config_payload["unique_id"] = self._unique_id

        self.logger.debug("%s: %s", self.config_topic, json.dumps(config_payload))
        self._mqtt_client.publish(
            topic=self.config_topic, retain=True, payload=json.dumps(config_payload)
        )

    def send_on(self, attributes=None):
        """Send the ON state of the sensor to Home Assistant."""
        self.send_state("ON", attributes=attributes)

    def send_off(self, attributes=None):
        """Send the OFF state of the sensor to Home Assistant."""
        self.send_state("OFF", attributes=attributes)
