# Mission Check Helper

Created to assist [WOG A3 project](https://wogames.info) missions check.


## Features

Displays:
- mission information (mission name, summart, wmt-attribute values, etc);
- sides squads: squad name, unit's inits, slot names, slot playabylity, medical and engineering abilities;
- boxes, static weapons, vehicles, it's state and inits;
- unique unit inits.

Checks:
- mission filename;
- `mission.sqm` binarization;
- mission name;
- wind and rain values;
- maximum allowed slots count;
- with supported inits:
    - personal and long range radio presence;
    - long radio drop if init gives some backpack;
    - vanilla equipment;
- if mission pbo has `description.ext` in it.


## Installation

Dependencies: debian/ubuntu linux, git, tar, bash, python2, extractpbo (depbo-tools). Deployment dependencies (from `deploy.sh`) will be installed automatically. 

0. `extractpbo` must be available for current user.

1. Download this release, `cd` in it.

2. Replace `deploy_folder` path in code below to full path to directory **without trailing slash**. Copypaste code into terminal emulator with bash and run:

```
deploy_folder=/home/some/mission_check_helper && mkdir -p $deploy_folder &&
. compile_repos.sh $deploy_folder &&
cd $deploy_folder && . deploy.sh $deploy_folder && cat $deploy_folder/run_n_update_commands
```


## Usage

All instructions will be available in `$deploy_folder/run_n_update_commands` after deployment.
