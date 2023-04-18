<h1 align="center">
  <br>
    <img src="https://raw.githubusercontent.com/cybersecsi/robodroid/main/logo.png" alt= "robodroid" width="200px">
</h1>
<p align="center">
    <b>RoboDroid</b>
<p>

<p align="center">
    <img src="https://github.com/cybersecsi/robodroid/actions/workflows/release.yaml/badge.svg"/>
    <img src="https://github.com/cybersecsi/robodroid/actions/workflows/publish.yaml/badge.svg"/>
  <a href="https://github.com/cybersecsi/robodroid/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>
  <a href="https://github.com/cybersecsi/robodroid/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPL3-blue.svg"></a>
</p>

RoboDroid is a cutting-edge software tool designed to simplify the process of managing (and **very soon** also deploying) Android machines for usage in Cyber Range environments. With RoboDroid, users can easily set up and customize pre-defined behaviors for their Android machines, allowing them to create complex cyber attack scenarios and test their defenses against a wide range of threats.

<!-- omit in toc -->
## 📋 Table of Contents

- [📱 Context](#-context)
- [⚡ Overview](#-overview)
- [📚 How It Works](#-how-it-works)
  - [Interaction with the Frida Agent](#interaction-with-the-frida-agent)
- [🔌 Install](#-install)
  - [RoboDroid Library](#robodroid-library)
- [ℹ️ Usage](#ℹ️-usage)
- [🚀 Demo](#-demo)
- [🚧 Roadmap](#-roadmap)
- [📚 Credits](#-credits)
- [🪪 License](#-license)

## 📱 Context
Mobile devices have become ubiquitous in today's world. People use smartphones for almost every aspect of their lives, including banking, shopping, and communication. As a result, mobile devices are now a primary target for cybercriminals.

However, the security of mobile devices is often overlooked in cybersecurity training and testing environments. This can leave organizations vulnerable to attacks that exploit the weaknesses of mobile devices. Therefore, it is important to introduce mobile components in next-generation cyber-ranges to adapt to the current world that is more and more smartphone-addicted.

**RoboDroid** is designed to help fill this gap by providing a set of tools that can simulate human-like smartphone behavior. The pre-defined behaviors are created using [Frida](https://frida.re) and are managed in the [RoboDroid Library](https://github.com/cybersecsi/robodroid-library) repository.

## ⚡ Overview


The goal of **RoboDroid** is to provide a simple way to introduce mobile components in Cyber Range environments. Its main objective is to provide users with an easy-to-use platform that allows them to simulate human-like behaviors and actions on mobile devices.

RoboDroid leverages [Frida](https://frida.re) technology to run behaviors that are specific to applications, while using ``ADB`` for all other operations. This powerful combination enables users to create workflows of preset behaviors that can simulate a mobile user's actions.

One example of a workflow that can be used in a cyber range environment involves simulating a mobile user receiving a phishing email, clicking on the link contained in the email, and subsequently downloading a malware.

The following picture summarizes it:

![Kill Chain Example](https://raw.githubusercontent.com/cybersecsi/robodroid/main/docs/kill-chain-example.png#gh-light-mode-only)
![Kill Chain Example](https://raw.githubusercontent.com/cybersecsi/robodroid/main/docs/kill-chain-example-dark.png#gh-dark-mode-only)

The workflow can be broken down into the following steps:

1. The user receives a phishing email containing a link that appears legitimate.
2. The user clicks on the link, which redirects them to a malicious website.
3. The website prompts the user to download an app, which they do.
4. The app is installed on the user's device and begins executing malicious code.
5. The malware gains access to sensitive data on the device, such as passwords, credit card information, and other personal details.

By creating and running workflows like this, users can simulate realistic cyber attack scenarios and test their defenses against a wide range of threats. This helps to ensure that systems and networks are well-protected against potential vulnerabilities, and that users are prepared to respond effectively in the event of an attack.

## 📚 How It Works
![How RoboDroid Works](https://raw.githubusercontent.com/cybersecsi/robodroid/main/docs/how-it-works.png#gh-light-mode-only)
![How RoboDroid Works](https://raw.githubusercontent.com/cybersecsi/robodroid/main/docs/how-it-works-dark.png#gh-dark-mode-only)

### Interaction with the Frida Agent

RoboDroid ommunicates with the Frida Agent provided by the RoboDroid Library via messages, providing efficient interaction.
When the RoboDroid begins a specific behavior, it awaits a message from the Frida Agent. The message could be of either ``FAILURE`` or ``COMPLETED`` type.

If the message type is ``FAILURE`` RoboDroid restarts the current behavior to ensure successful completion. If the message type is ``COMPLETED`` the current step is marked as finished, and RoboDroid moves to the next step.

Furthermore, a message of type ``COMPLETED`` can also contain **outputs** that can be used in subsequent steps. This ensures that the tool can optimize its behavior to achieve accurate simulation of human-like actions on mobile devices.

By providing this robust communication process, RoboDroid ensures the seamless integration of the Frida Agent into its toolset, and facilitates the creation of complex workflows for the simulation of mobile devices in a Cyber Range environment.

## 🔌 Install
You can easily install it by running:
```
pipx install robodroid
```

We suggest you to use ``pipx`` instead of ``pip`` because in future Python versions package installation with ``pip`` will be removed outside virtual environments.

### RoboDroid Library
**RoboDroid** has built-in support for automatic behaviors download (and **soon** auto-update) from the [RoboDroid Library](https://github.com/cybersecsi/robodroid-library) repository. If you want to add a new Frida behavior we suggest you to head over to the specific repository and make a Pull Request.

## ℹ️ Usage
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

Before actually running it you need to provide at least one valid config file that **must** be placed under ``$HOME/.RoboDroid/config`` in ``yaml`` format.
This config file defines all the steps of the workflow that will be executed, you can take a look at the ``examples`` folder for some valid configurations. The following table provides a description of the fields used in the config file:

| **Key**   | **Required** | **Description**                                      |
|-----------|--------------|------------------------------------------------------|
| id        | True         | The ID of the workflow                               |
| init      | False        | The init section, contains the initial setup actions |
| behaviors | True         | The list of behaviors to execute                     |

In the ``init`` section you may set the APKs that must be installed and the packages that must be cleaned up (storage and cache) before running the actual workflow. The structure of this section is the following:

| **Key** | **Required** | **Description**                                  |
|---------|--------------|--------------------------------------------------|
| install | True         | List of paths of APKs to install                 |
| clear   | False        | List of packages to clean up (storage and cache) |

In the ``behaviors`` section there is the actual workflow. It is a **list** of elements that are called **steps** which are meant to be executed **sequentially**. Every *step* has the following structure:

| **Key** | **Required** | **Description**                                                             |
|---------|--------------|-----------------------------------------------------------------------------|
| id      | True         | ID of the step                                                              |
| name    | True         | The name of the behavior (in the RoboDroid Library or in the commands list) |
| type    | True         | The type of the behavior ("frida-behavior", "adb")                          |
| inputs  | False        | The list of inputs                                                          |

Finally every input has the following structure:

| **Key** | **Required** | **Description**                   |
|---------|--------------|-----------------------------------|
| id      | True         | ID of the input                   |
| value   | True         | The value to assign to this input |

The last thing to say is that you can **also use outputs from previous steps as input to the next ones**. To do that you can set the value of an input by using the **reserved** prefix ``robodroid.outputs`` followed by the ID of the step and the ID of the output, for example:
```
...
  - id: get-link
    name: k9-mail-refresh-and-get-link
    type: frida
  - id: open-and-download
    name: firefox-android-open-link-and-download
    type: frida
    inputs:
      - id: link
        value: robodroid.outputs.get-link.link
...
```

## 🚀 Demo

We made a brief demo video that shows RoboDroid in action with a template that does the following:
1. Sets up and email account on the K9 Mail app
2. Waits indefinitely for a new email and returns the first link inside it
3. Opens the link with the Firefox Android (Fenix) application, downloads the linked file and installs it

This workflow simulates a common phishing attack (although simplified) that can be used in a next-generation Cyber Range involving Android Mobile Devices.

[![RoboDroid Introduction](https://img.youtube.com/vi/jn8OQZyNLD4/maxresdefault.jpg)](http://www.youtube.com/watch?v=jn8OQZyNLD4 "RoboDroid Introduction")


## 🚧 Roadmap
*RoboDroid* is a newborn tool and still needs to grow up! Currently these are the features we plan to add very soon:
- [ ] Automatic deploy of AVD
- [ ] Automatic deploy of ReDroid instance
- [ ] Automatic deploy of Genymotion instance
- [ ] Multi-device support
- [ ] Interactive mode (without workflow config file)
- [ ] Continuous workflow mode (restart the whole workflow indefinitely until manually stopped)

Of course we plan to add more and more behaviors in the [RoboDroid Library](https://github.com/cybersecsi/robodroid-library) and more and more ``adb`` commands in this repo. We also encourage every user to contribute to this projet and make it better!

## 📚 Credits

Developed by Angelo Delicato [@SecSI](https://secsi.io)

## 🪪 License

_RoboDroid_ is released under the [GPL-3.0 LICENSE](https://github.com/cybersecsi/robodroid/blob/main/LICENSE)
