This component provides integration to the JLR InControl functionality to homeassistant.

Due to changes in Home Assistant, this integration requires a minimum of HA `v2022.11`.

## Functionality

**Currently, this loads a series of sensors for**

- Vehicle Info
- Status
- Alarm
- Doors
- Windows
- Tyres
- Range
- Location
- EV Battery Sensor (EVs only - deprecated!)
- Battery Sensor (EVs Only)
- Service Info
- Last Trip
- All Vehicle Data (see Note 3)

**And has services for**

- Update Health Status (forces update from vehicle)
- Honk/Flash
- Lock/Unlock
- Start Engine/Stop Engine
- Start Charging/Stop Charging
- Reset Alarm
- Start Preconditioning/Stop Preconditioning
- Set Max Charge (Always and One Off)

**Note:** Not all services are available on all models and the error log will show this if not available on your vehicle.

**Note 2**: When calling a service, HA will monitor the status of the service call and report in the error log if it failed. Debug log will show this checking and the success/failure reason.

**Note 3**: This sensor shows all returned data for attributes, statuses and position as device attribute data. See [recipes](https://github.com/msp1974/homeassistant-jlrincontrol/blob/master/Recipes.md) for how to use this in your automations or template sensors. By default it is not enabled and can be enabled in config options.

## Sample Images

![](https://raw.githubusercontent.com/msp1974/homeassistant-jlrincontrol/master/docs/panel1.png)

## Configuration

Add via Configuration -> Integrations in the UI

**Required Parameters**

```
  email: <your InControl email address>
  password: <your InControl password>
```

**Config Options**

1. scan_interval - in minutes. Default update interval is 5 minutes. Use this to change that. Minimum is 1 minute.
2. pin - set this to be able to use the lock/unlock on the lock sensor.
3. distance_unit - set this to 'mi' or 'km' to override the HA default metric for mileages (mainly for funny UK system of miles and litres!).
4. pressure_unit - set this to 'bar' or 'psi' to override the HA default unit for pressure (mainly for UK also).
5. health_update_interval - see health update section.
6. debug_data: - see debugging below.

### Migrating From Previous Versions

The new config flow will import your settings from configuration.yaml. It is recommended to remove them after this has happened, otherwise changes via the UI can be reverted by the entries in configuration.yaml.

## Vehicle Health Status Update

This integration has the ability to perform a scheduled health status update request from your vehicle. By default this is disabled. Setting the interval and your pin in the config options will enable this.

I do not know the impact on either vehicle battery or JLRs view on running this often, so please use at your own risk. I would certainly not set it to too low an interval. Recommended 120 mins.

Alternatively, you can make a more intelligent health update request automation using the service call available in this integration and the output of some sensors.

I.e. on EV vehicles you could only call it if the vehicle is charging, or on all vehicles, only call it during the day and it was more than x period since the last update.

## Debugging

1. To enable debug logging for this component, add the following to your configuration.yaml

```
    logger:
      default: critical
      logs:
        custom_components.jlrincontrol: debug
```

2. To enable logging of the attributes and status data in the debug log, set the debug data option in config options with debugging turned on as above.

### Known Issues

- Distance to service only shows in KMs.
- Service Info sensor shows ok even if car is needing service or adblue top up.

## More Information

For more information please see the [Readme.md](https://github.com/msp1974/homeassistant-jlrincontrol/blob/master/README.md)
