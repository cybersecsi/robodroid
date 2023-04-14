<h1 align="center">
  <br>
    <img src="https://raw.githubusercontent.com/cybersecsi/robodroid/main/logo.png" alt= "robodroid" width="200px">
</h1>
<p align="center">
    <b>RoboDroid</b>
<p>

<p align="center">
  <a href="https://github.com/cybersecsi/robodroid/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-incomplete-orange.svg?style=flat"></a>
  <a href="https://github.com/cybersecsi/robodroid/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPL3-blue.svg"></a>
</p>

RoboDroid is a cutting-edge software tool designed to simplify the process of managing (and **very soon** also deploying) Android machines for usage in Cyber Range environments. With RoboDroid, users can easily set up and customize pre-defined behaviors for their Android machines, allowing them to create complex cyber attack scenarios and test their defenses against a wide range of threats.

<!-- omit in toc -->
## Table of Contents

- [Context](#context)
- [Overview](#overview)
- [Install](#install)
- [Usage](#usage)
- [Demo](#demo)
- [Credits](#credits)
- [License](#license)

## Context
Mobile devices have become ubiquitous in today's world. People use smartphones for almost every aspect of their lives, including banking, shopping, and communication. As a result, mobile devices are now a primary target for cybercriminals.

However, the security of mobile devices is often overlooked in cybersecurity training and testing environments. This can leave organizations vulnerable to attacks that exploit the weaknesses of mobile devices. Therefore, it is important to introduce mobile components in next-generation cyber-ranges to adapt to the current world that is more and more smartphone-addicted.

**RoboDroid** is designed to help fill this gap by providing a set of tools that can simulate human-like smartphone behavior. The pre-defined behaviors are created using Frida and are managed in the [RoboDroid Library](https://github.com/cybersecsi/robodroid-library) repository.

## Overview

TODO

## Install
You can easily install it by running:
```
pipx install robodroid
```

We suggest you to use ``pipx`` instead of ``pip`` because in future Python versions package installation with ``pip`` will be removed outside virtual environments.

## Usage
```
robodroid --help
```

This will display the help for the tool:

```
    ███████╗███████╗ ██████╗███████╗██╗
    ██╔════╝██╔════╝██╔════╝██╔════╝██║
    ███████╗█████╗  ██║     ███████╗██║
    ╚════██║██╔══╝  ██║     ╚════██║██║
    ███████║███████╗╚██████╗███████║██║
    ╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝
    RoboDroid v0.0.1


 Usage: robodroid [OPTIONS]

 Manage and deploy Android machines with pre-defined behaviors for Cyber Range environments

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --log-mode          [silent|normal|debug]  Set logging mode [default: normal]                                                   │
│ --help      -h                             Show this message and exit.                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Demo

TODO
## Credits

Developed by Angelo Delicato [@SecSI](https://secsi.io)

## License

_robodroid_ is released under the [GPL-3.0 LICENSE](https://github.com/cybersecsi/robodroid/blob/main/LICENSE)
