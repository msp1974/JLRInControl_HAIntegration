[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

[![GitHub license](https://img.shields.io/github/license/msp1974/homeassistant-jlrincontrol)](https://github.com/msp1974/homeassistant-jlrincontrol/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/msp1974/homeassistant-jlrincontrol)](https://GitHub.com/msp1974/homeassistant-jlrincontrol/releases/)

# JLR Home Assistant Integration (v3.0.0beta3)

**NOTE: This is currently a beta version.  Please use with this knowledge.**

This repository contains a Home Assistant integration for the Jaguar Landrover InControl system, allowing visibility of key vehicle information and control of enabled services.

Due to changes in Home Assistant, this integration requires a minimum of HA v2023.10.

## Functionality

Currently this loads a series of sensors for

- Vehicle Info
- Status
- Alarm
- Doors
- Windows
- Tyres
- Range
- Location
- Battery Sensor (EV & PHEV Only)
- Service Info
- Last Trip
- All Vehicle Data (see Note 3)

Has buttons for

- Honk Blink
- Reset Alarm
- Update from Vehicle

Has switches for

- Climate (ICE only)
- Preconditioning (EV & PHEV only)
- Guardian Mode
- Service Mode
- Transport Mode
- Journey Recording

And has services for

- Update Health Status (forces update from vehicle)
- Honk/Flash
- Lock/Unlock
- Start Engine/Stop Engine
- Start Charging/Stop Charging
- Reset Alarm
- Start Preconditioning/Stop Preconditioning
- Set Max Charge (Always and One Off)

**Note:** Not all functions are available on all models and therefore the buttons/switches may not be created.  If you call services that are not supported you will get an error in the error log.

**Note 2**: When calling a service, HA will monitor the status of the service call and report in the error log if it failed.

**Note 3**: This sensor shows all returned data for attributes, statuses and position as device attribute data. See recipes for how to use this in your automations or template sensors. By default it is not enabled and can be enabled in config options.

Also, due to lack of a fleet of Jaguars and LandRovers/RangeRovers (donations welcome!), there maybe issues with some models not supporting some functions. Please raise an issue for these and say what vehicle you have and post the log.

## Sample Images

![](https://raw.githubusercontent.com/msp1974/homeassistant-jlrincontrol/master/docs/panel1.png)

## Configuration

Add via Configuration -> Integrations in the UI

### Required Parameters

- email: [your InControl email address]
- password: [your InControl password]

### Config Options

1. **Pin**: set this to be able to use the lock/unlock on the lock sensor.
2. **Scan interval**: in minutes. Default update interval is 5 minutes. Use this to change that. Minimum is 1 minute.
3. health update interval - see health update section.
4. **Pressure Unit:** set this to 'bar' or 'psi' to override the HA default unit for pressure (mainly for UK also).
5. Default climate temp:
6. Default service duration:

## Health Status Update

This integration has the ability to perform a scheduled health status update request from your vehicle. By default this is disabled. Setting the interval and your pin in the config options will enable this.

I do not know the impact on either vehicle battery or JLRs view on running this often, so please use at your own risk. I would certainly not set it to too low an interval. Recommended 120 mins.

Alternatively, you can make a more intelligent health update request automation using the service call available in this integration and the output of some sensors.

I.e. on EV vehicles you could only call it if the vehicle is charging, or on all vehicles, only call it during the day and it was more than x period since the last update.

## Creating Custom Sensors

As all use cases cannot be covered and to allow the best benefit to all of this integration, version 2.1.0 introduced and 'All Info' sensor. This sensor displays the attribute, status and position information being received from the JLR servers and allows the creation of custom sensors and use of any of this data in scripts and automations.

The [recipes](https://github.com/msp1974/homeassistant-jlrincontrol/blob/master/Recipes.md) document gives an example of a template sensor that uses this data and shows how to extract the values from the all info sensor.

**NOTE**: By default this sensor is not created and must be enabled in the config options. Configuration -> Integrations -> Select Options on the JLR Incontrol integration. You do not need to restart HA to enable or disable this sensor, but you may need to add it into your Lovelace UI after enabling it.

## Installation

**Installing via HACS and configuring via the UI is the recommended method.**

### Manual Code Installation

1. On your server clone the github repository into a suitable directory using the git clone command.<br>
   `git clone https://github.com/msp1974/homeassistant-jlrincontrol.git`
2. Copy the jlrincontrol folder to the custom_components directory of your Home Assistant installation.
3. Configure via the integrations page in the UI.

### Branch Versions

As of v1.0.0, the dev branch is now where the very latest version is held. Please note that there maybe issues with new functions or fixes that have not been fully tested. It will also be updated regularly as new fixes/functions are developed, so please check you have the latest update before raising an issue. The master branch is the current release.

## Community Recipes

The [recipes](https://github.com/msp1974/homeassistant-jlrincontrol/blob/master/Recipes.md) page is a collection of ideas contributed by the community to help you get the most out of using this integration.

## Suggestions

I am looking for suggestions to improve this integration and make it useful for many people. Please raise an issue for any functionality you would like to see.

## Contributors

This integration uses the jlrpy api written by [ardevd](https://github.com/ardevd/jlrpy). A big thanks for all the work you have done on this.

## Debugging

1. To enable debug logging for this component, add the following to your configuration.yaml

```yaml
    logger:
      default: critical
      logs:
        custom_components.jlrincontrol: debug
```

2. To enable logging of the attributes and status data in the debug log, set the debug data option in config options with debugging turned on as above.

## Change Log

### v3.0.0beta3

- Fixed error if target climate temp not available - issue [#116](https://github.com/msp1974/homeassistant-jlrincontrol/issues/116)
- Fixed error with identification of engine type - issue [#118](https://github.com/msp1974/homeassistant-jlrincontrol/issues/118)
- Fixed error with invalid attribute volume - issue [#113](https://github.com/msp1974/homeassistant-jlrincontrol/issues/113)
- Fixed error with no default pressure units - issue [#117](https://github.com/msp1974/homeassistant-jlrincontrol/issues/117)
- Fixed issue with registration & serial no showing REDACTED after diagnostics download - issue [#119](https://github.com/msp1974/homeassistant-jlrincontrol/issues/119)

### v3.0.0beta2

- Fixed error in creating service sensor - issue [#113](https://github.com/msp1974/homeassistant-jlrincontrol/issues/113)
- Fixed Unknown error when saving config options caused by missing key in older configs - issue [#115](https://github.com/msp1974/homeassistant-jlrincontrol/issues/115)
- Fixed incorrect identification of PHEV vehicles - issue [#115](https://github.com/msp1974/homeassistant-jlrincontrol/issues/115)


### v3.0.0beta1

- Added switches and buttons for key services
- Added support for guardian, service and tansport modes
- Added diagnostics download
- UOMs now come from JLR app settings
- Major rewrites of the integration code


### v2.2.5

- Fixed: migrate deprecated HA constants with enums #106 introduced in HA v2022.11 and deprecation warnings in HA v2024.1. This integration requires from now minium version v2022.11 of HA.

### v2.2.4

- Bump jlrpy to v1.5.2 to fix lock/unlock #102

### v2.2.3

- Fix usage of deprecated device class constant [#84](https://github.com/msp1974/homeassistant-jlrincontrol/issues/84)

### v2.2.2

- Fix deprecation issue of async_get_registry [#74](https://github.com/msp1974/homeassistant-jlrincontrol/issues/74)
- Fix distance and pressure deprecated to use unit_conversion
- Add config option for China region

### v2.2.1 (includes v2.1.4 Pre Release changes)

- Bump jlrpy to v1.4.1
- Added support for PHEV vehicles
- Debug data outputs all received data

### v2.1.4 - Pre Release

- Updated device_state_attributes to extra_state_attributes
- Fixed spelling mistakes in services.yaml - PR #58.  Thanks @seanauff
- Fixed: Service returned as a failure if status returned a status of 'running'
- Updated: Updated to support jlrpy 1.4.0
- Updated: All Info sensor now shows status information as 'core status' and 'ev status' to align to update from JLR on api, which will break templated automations/scripts/sensors using this data
- Updated: Set service call errors to error instead of debug to better show in logs
- Removed: Battery_EV sensor as replaced by better Battery sensor for EVs

### v2.1.3
- Added version to manifest

### v2.1.2
- Fixed: Change to constant UNIT_PERCENTAGE to PERCENTAGE in HA core

### v2.1.1

- Fixed: Lock/Unlock errors if all info sensor enabled

### v2.1

- Added: All data sensor to show returned info from vehicle

### v2.0.2

- Fixed: error when locking/unlocking via lock device sensor. Issue #39
- Fixed: not updating from server after lock/unlock call from device sensor
- Updated: improved handling of service call returns
- Updated: get status update from server when service call fails

### v2.0.1

- Fixed: errors on non unique id when changing config options

### v2.0.0beta

- Deprecated: EV_Battery sensor - this will be removed in future version
- Added: Setup and options via config flow
- Added: New Battery Sensor for EVs
- Fixed: Deprecation warnings in HA0.110.x
- Fixed: Service temp settings now in local temp units (C/F)

### v1.3.1

- Added: Does not load trip sensor if privacy mode enabled
- Fixed: Integration errors if no position or trip data

### v1.3.0

- Added: New status sensor to show engine running status
- Added: Tyre pressure unit override to cope with UK units system
- Added: New recipes
- Updated: Icon for vehicle info sensor
- Updated: Now available as HACS integration
- Fixed: Error in service descriptions
- Fixed: Tyre pressure units should now show correctly - feedback wanted for your vehicle
- Fixed: Tidy up of attribute values in service sensor

### v1.2.0

- Updated: Improved debug logging messages
- Updated: Handled errors from service calls are now debug instead of warning
- Fixed: Errors in HA v109.0 due to new IO monitoring in event loop
- Fixed: Better handling of multiple concurrent service calls
- Fixed: Scheduled health update now calls 30s after HA start

### v1.1.0

- Added: Last trip sensor
- Fixed: Multiple vehicles on account only showed first one.

### v1.0.0

- First official release - yeah!

### v0.5alpha

- Added: Alarm sensor.
- Added: jlrincontrol services as listed in functionality to control vehicle.
- Added: Ability to schedule health status update - see health status section.
- Added: Ability to set the update interval fro the JLR servers.
- Updated: Use HA units to display data instead of relying on InControl user prefs as not reliable.
- Fixed: **BREAKING CHANGE** Issue with unique ID could cause duplicates.
- Fixed: Renamed last updated to last contact and displayed in local time.
- Fixed: Unlock/Lock on door sensor did not work. Need to add pin to configuration.yaml. See additional parameters.
- Fixed: Device tracker not updating state.

### v0.4alpha

- Added: Improved debugging info to aid diagnosing differences in models

### v0.3alpha

- Fixed: Range sensor now handles EVs
- Added: New EV Charge sensor to show charge information (not fully tested)

### v0.2alpha

- Updated to use jlrpy 1.3.3
- Added a bunch of new sensor information
- Better handles vehicles that do not present some sensor info

### v0.1alpha

Initial build of the component to read basic sensors

## Known Issues

- Service Info sensor shows ok even if car is needing service or adblue top up.
- Sometimes the JLR servers do not provide user units preference info, in which case the integration defaults to HA units.  Look to save this if provided.
